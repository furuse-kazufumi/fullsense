"""Qiita 公開キュー — 限定公開の在庫を貯めて、公開枠を無駄にしない。

背景(2026-08-24 に実測して分かったこと):
- Qiita には連続投稿を抑える仕組みがあり、**公開に失敗すると 502 が返る**
  (レート制限ヘッダは正常。同じ本文でも private のままなら更新は通る =
   本文サイズの問題ではなく「公開という操作」が弾かれている)
- したがって公開は **枠が空くのを待って 1 本ずつ** 通すのが正しい運用になる
- 枠が空いたときに出す物が無いと無駄になるので、**在庫を並べておく**

使い方:
  python qiita_queue.py list                 限定公開の在庫を一覧(未登録も含む)
  python qiita_queue.py queue                公開キューの順番を見る
  python qiita_queue.py add <名前> ...       キューの末尾に積む
  python qiita_queue.py top <名前>           キューの先頭へ移す
  python qiita_queue.py rm  <名前> ...       キューから外す
  python qiita_queue.py status               次にいつ出せるか
  python qiita_queue.py run [--dry-run]      枠が空いていれば先頭を 1 本公開する
  python qiita_queue.py run --loop           枠が空くまで待って公開し続ける

安全弁:
- 送信前にローカル本文の長さを確認し、**極端に短ければ送らない**
- 公開後に API から取り直して private と本文長を検証する
- 公開が 502 で弾かれたら在庫は減らさず、待ち時間を伸ばして次に回す
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
STATE = ROOT / "qiita_queue.json"
CRED = pathlib.Path.home() / ".config/qiita-cli/credentials.json"
JST = timezone(timedelta(hours=9))
DEFAULT_INTERVAL_H = 48          # 2 日空ける(2026-08-24 の方針)
MIN_BODY = 200                   # これより短い本文は送らない


# ---------- 記事の読み取り ----------
def read_article(name):
    p = PUB / f"{name}.md"
    s = p.read_text(encoding="utf-8")
    end = s.index("\n---\n", 4)
    fm, body = s[4:end], s[end + 5:]
    m = re.search(r"^title:\s*(.*)$", fm, re.M)
    title = m.group(1).strip()
    if title in (">-", ">", "|", "|-", ""):          # 折り返し形式
        seg = fm[fm.index("title:"):fm.index("tags:")].split("\n")[1:]
        title = " ".join(x.strip() for x in seg if x.strip())
    title = title.strip("'\"")
    tags = []
    if "tags:" in fm and "private:" in fm:
        tags = [t.strip() for t in re.findall(
            r"^\s+-\s+(.+)$", fm[fm.index("tags:"):fm.index("private:")], re.M)]
    mid = re.search(r"^id:\s*(\S+)$", fm, re.M)
    iid = mid.group(1) if mid else None
    if iid in ("null", "なし", "None"):
        iid = None
    priv = bool(re.search(r"^private:\s*true\s*$", fm, re.M))
    return {"name": name, "id": iid, "title": title, "tags": tags,
            "body": body, "private": priv, "chars": len(body)}


def all_private():
    out = []
    for f in sorted(PUB.glob("*.md")):
        try:
            a = read_article(f.stem)
        except Exception:
            continue
        if a["private"]:
            out.append(a)
    return out


# ---------- API ----------
def token():
    c = json.loads(CRED.read_text(encoding="utf-8"))
    return c["credentials"][0]["accessToken"]


def api_get(iid, tok):
    req = urllib.request.Request(f"https://qiita.com/api/v2/items/{iid}",
                                 headers={"Authorization": f"Bearer {tok}"})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())
    return d["private"], len(d["body"])


def api_publish(a, tok):
    """公開を試みる。成功なら None、失敗ならエラー文字列を返す。"""
    if a["chars"] < MIN_BODY:
        return f"本文が短すぎる({a['chars']} 字)ので送らない"
    payload = {"title": a["title"], "body": a["body"], "private": False,
               "tags": [{"name": t, "versions": []} for t in a["tags"]]}
    req = urllib.request.Request(
        f"https://qiita.com/api/v2/items/{a['id']}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": "application/json"}, method="PATCH")
    try:
        urllib.request.urlopen(req, timeout=300).read()
        return None
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:
        return type(e).__name__


# ---------- 状態 ----------
def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"queue": [], "history": [], "last_published": None,
            "interval_hours": DEFAULT_INTERVAL_H, "last_rejected": None}


def save_state(st):
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def next_slot(st):
    """次に公開してよい時刻。hold_until があればそれが最優先。"""
    iv = timedelta(hours=st.get("interval_hours", DEFAULT_INTERVAL_H))
    hold = (datetime.fromisoformat(st["hold_until"])
            if st.get("hold_until") else None)
    base = None
    if st.get("last_published"):
        base = datetime.fromisoformat(st["last_published"])
    if st.get("last_rejected"):
        rej = datetime.fromisoformat(st["last_rejected"]) + timedelta(hours=6)
        base = max(base, rej) if base else rej
    slot = (base + iv) if st.get("last_published") else (
        datetime.fromisoformat(st["last_rejected"]) + timedelta(hours=6)
        if st.get("last_rejected") else datetime.now(JST))
    return max(slot, hold) if hold else slot


# ---------- コマンド ----------
def cmd_list(args):
    st = load_state()
    arts = all_private()
    print(f"限定公開の在庫: {len(arts)} 本")
    print(f"{'':2s} {'名前':<44s} {'字数':>8s}  {'ID':<22s} キュー")
    for a in arts:
        pos = (st["queue"].index(a["name"]) + 1) if a["name"] in st["queue"] else None
        mark = "○" if a["id"] else "新"
        print(f"{mark:2s} {a['name'][:44]:<44s} {a['chars']:>8,d}  "
              f"{(a['id'] or '(未作成)'):<22s} {pos if pos else '-'}")
    print("\n○ = Qiita 上に既にある(公開するだけ)/ 新 = まだ作成されていない")


def cmd_queue(args):
    st = load_state()
    if not st["queue"]:
        print("キューは空。add で積んでください")
        return
    print(f"公開キュー({len(st['queue'])} 本、間隔 {st['interval_hours']} 時間)")
    for i, n in enumerate(st["queue"], 1):
        try:
            a = read_article(n)
            print(f"  {i}. {n}  {a['chars']:,} 字  {a['title'][:40]}")
        except Exception:
            print(f"  {i}. {n}  (読めない)")


def cmd_add(args):
    st = load_state()
    for n in args.names:
        if not (PUB / f"{n}.md").exists():
            print(f"  見つからない: {n}")
            continue
        if n in st["queue"]:
            print(f"  すでにキューにある: {n}")
            continue
        st["queue"].append(n)
        print(f"  積んだ: {n}")
    save_state(st)


def cmd_rm(args):
    st = load_state()
    for n in args.names:
        if n in st["queue"]:
            st["queue"].remove(n)
            print(f"  外した: {n}")
    save_state(st)


def cmd_top(args):
    st = load_state()
    for n in reversed(args.names):
        if n in st["queue"]:
            st["queue"].remove(n)
            st["queue"].insert(0, n)
            print(f"  先頭へ: {n}")
    save_state(st)


def cmd_status(args):
    st = load_state()
    now = datetime.now(JST)
    nxt = next_slot(st)
    print(f"いま        : {now:%Y-%m-%d %H:%M}")
    print(f"最終公開    : {st['last_published'] or 'なし'}")
    print(f"直近の拒否  : {st['last_rejected'] or 'なし'}")
    print(f"公開間隔    : {st['interval_hours']} 時間")
    if nxt <= now:
        print(f"次の枠      : **いま出せる**(キュー {len(st['queue'])} 本)")
    else:
        print(f"次の枠      : {nxt:%Y-%m-%d %H:%M}(あと {(nxt-now).total_seconds()/3600:.1f} 時間)")
    if st["history"]:
        print("履歴:")
        for h in st["history"][-5:]:
            print(f"  {h['at'][:16]}  {h['name']}")


def cmd_hold(args):
    """指定時間だけ公開を止める(連続投稿制限に当たった直後などに使う)。"""
    st = load_state()
    st["hold_until"] = (datetime.now(JST) + timedelta(hours=args.hours)).isoformat()
    save_state(st)
    print(f"{args.hours} 時間 保留した -> {st['hold_until'][:16]} まで公開しない")


def try_publish(st, tok, dry=False):
    """枠が空いていれば先頭を 1 本公開する。戻り値: (公開できたか, メッセージ)"""
    now = datetime.now(JST)
    nxt = next_slot(st)
    if nxt > now:
        return False, f"まだ枠が来ていない(あと {(nxt-now).total_seconds()/3600:.1f} 時間)"
    while st["queue"]:
        name = st["queue"][0]
        try:
            a = read_article(name)
        except Exception as e:
            st["queue"].pop(0)
            save_state(st)
            return False, f"{name}: 読めないので外した({e})"
        if a["id"] is None:
            st["queue"].pop(0)
            save_state(st)
            return False, f"{name}: Qiita 上に未作成。先に qiita publish で作ってください"
        priv, blen = api_get(a["id"], tok)
        if not priv:
            st["queue"].pop(0)
            save_state(st)
            return False, f"{name}: すでに公開済みだったので外した"
        if dry:
            return False, f"[dry-run] {name}({a['chars']:,} 字)を公開するところ"
        err = api_publish(a, tok)
        priv2, blen2 = api_get(a["id"], tok)
        if blen2 < max(blen, a["chars"]) * 0.9:
            return False, f"**本文が縮んだ {blen}->{blen2}。中断**"
        if not priv2:
            st["queue"].pop(0)
            st["last_published"] = now.isoformat()
            st["last_rejected"] = None
            st["history"].append({"name": name, "id": a["id"],
                                  "at": now.isoformat(), "chars": a["chars"]})
            save_state(st)
            # ローカルの private も落としておく
            p = PUB / f"{name}.md"
            p.write_text(p.read_text(encoding="utf-8")
                         .replace("private: true", "private: false", 1), encoding="utf-8")
            return True, (f"公開した: {name} "
                          f"https://qiita.com/furuse-kazufumi/items/{a['id']}")
        st["last_rejected"] = now.isoformat()
        save_state(st)
        return False, f"{name}: 枠が空いていない({err})。6 時間後に再試行"
    return False, "キューが空"


def cmd_run(args):
    st = load_state()
    if args.interval_hours:
        st["interval_hours"] = args.interval_hours
        save_state(st)
    tok = token()
    while True:
        ok, msg = try_publish(st, tok, dry=args.dry_run)
        print(f"[{datetime.now(JST):%m-%d %H:%M}] {msg}", flush=True)
        if not args.loop:
            return 0 if ok else 1
        if not st["queue"]:
            return 0
        nxt = next_slot(st)
        wait = max((nxt - datetime.now(JST)).total_seconds(), 1800)
        time.sleep(min(wait, 21600))       # 最大 6 時間ごとに目を覚ます


def main():
    ap = argparse.ArgumentParser(description="Qiita 公開キュー")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("queue").set_defaults(fn=cmd_queue)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    ph = sub.add_parser("hold")
    ph.add_argument("hours", type=float)
    ph.set_defaults(fn=cmd_hold)
    for c, fn in (("add", cmd_add), ("rm", cmd_rm), ("top", cmd_top)):
        p = sub.add_parser(c)
        p.add_argument("names", nargs="+")
        p.set_defaults(fn=fn)
    p = sub.add_parser("run")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--loop", action="store_true")
    p.add_argument("--interval-hours", type=int, default=None)
    p.set_defaults(fn=cmd_run)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
