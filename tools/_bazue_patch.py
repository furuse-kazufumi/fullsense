# -*- coding: utf-8 -*-
"""スナックバス江コマ挿絵を Qiita 記事 ab3839f8b5b3ea91311e に追加して PATCH 反映する。
1 スクリプト完結: token 取得 -> GET -> body 加工 (raw 画像 200 確認済) -> PATCH。
"""
import sys, json, urllib.request, urllib.error

sys.path.insert(0, r'D:/projects/fullsense/tools')
from qiita_public_post import get_token

ITEM = "ab3839f8b5b3ea91311e"
RAW_BASE = "https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all"

result = {"id": ITEM, "status": "fail", "http": "", "panels": [], "note": ""}


def http_code_for(url: str) -> int:
    """raw 画像が 200 か事前確認 (GET, 本文は読まない)。"""
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.getcode()
    except urllib.error.HTTPError as e:
        return e.code


def panel_block(num: str, alt: str, serif: str, context_line: str) -> str:
    img = f"![{alt}]({RAW_BASE}/{num}.jpg)"
    cap = (f"> 🗒️ *「{serif}」— {context_line}*"
           f"（© Forbidden shibukawa / SHUEISHA・スナックバス江）")
    return img + "\n" + cap


def main() -> int:
    tok = get_token()
    if not tok:
        result["note"] = "get_token() returned None (no token)"
        return 1

    # --- GET ---
    req = urllib.request.Request(
        f"https://qiita.com/api/v2/items/{ITEM}",
        headers={"Authorization": "Bearer " + tok},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)

    body = data["body"]
    title = data["title"]
    private = data["private"]
    tags = [{"name": t["name"], "versions": t.get("versions", [])} for t in data["tags"]]

    if "bazue_all" in body:
        result["note"] = "記事に既に bazue 挿絵が存在。重複挿入を避けて中断。"
        result["status"] = "fail"
        return 1

    # --- 選んだコマ (多様性: 過度な一般化 093 + honest/over-claim 196) ---
    panels = [
        {
            "num": "093",
            "alt": "「主語がデカくない?」とツッコむスナックバス江のコマ",
            "serif": "主語がデカくない?",
            "context": "「第二の脳」という大きな看板。気恥ずかしさを承知で、それでも一番ぴったりな言葉として掲げている",
            # 挿入アンカー: 命名の気恥ずかしさを語る脱線パラグラフの直後
            "anchor": "**気恥ずかしさは正確さの前に折れる**。",
        },
        {
            "num": "196",
            "alt": "「嘘は良くない」と諭すスナックバス江のコマ",
            "serif": "嘘は良くない",
            "context": "1270 PASS はゴールであって過程ではない。途中で落ちたテストも数値の盛りも隠さず開示する (honest disclosure)",
            # 挿入アンカー: テストが途中で落ちた話の honest disclosure パラグラフ直後
            "anchor": "**1270 PASS / 回帰ゼロ** はゴールであって過程ではない。",
        },
    ]

    # raw 画像 200 事前確認
    for p in panels:
        url = f"{RAW_BASE}/{p['num']}.jpg"
        code = http_code_for(url)
        if code != 200:
            result["note"] = f"raw 画像 {p['num']}.jpg が {code} (200 でない) ため中断"
            return 1

    # --- body 加工: アンカー行の直後に画像ブロックを挿入 ---
    new_body = body
    used = []
    for p in panels:
        anchor = p["anchor"]
        idx = new_body.find(anchor)
        if idx == -1:
            result["note"] = f"アンカー未検出: {anchor!r} (コマ {p['num']} 挿入失敗)"
            return 1
        # アンカー行の行末位置を求める
        line_end = new_body.find("\n", idx)
        if line_end == -1:
            line_end = len(new_body)
        block = "\n\n" + panel_block(p["num"], p["alt"], p["serif"], p["context"])
        new_body = new_body[:line_end] + block + new_body[line_end:]
        used.append(p["num"])

    if new_body == body:
        result["note"] = "body 無変更 (挿入が反映されていない)"
        return 1

    # --- PATCH ---
    payload = json.dumps(
        {"body": new_body, "title": title, "tags": tags, "private": private},
        ensure_ascii=False,
    ).encode("utf-8")
    preq = urllib.request.Request(
        f"https://qiita.com/api/v2/items/{ITEM}",
        data=payload,
        method="PATCH",
        headers={
            "Authorization": "Bearer " + tok,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(preq, timeout=60) as r:
            code = r.getcode()
    except urllib.error.HTTPError as e:
        result["http"] = str(e.code)
        result["panels"] = used
        result["note"] = f"PATCH 失敗 HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
        return 1

    result["http"] = str(code)
    result["panels"] = used
    if code == 200:
        result["status"] = "ok"
        result["note"] = (
            "スナックバス江コマ 093(主語がデカくない?=第二の脳という大看板への自嘲)と "
            "196(嘘は良くない=honest disclosure)を該当パラグラフ直後に挿入し PATCH 200。"
            f" body {len(body)}->{len(new_body)} 字。"
        )
    else:
        result["status"] = "fail"
        result["note"] = f"PATCH レスポンス HTTP {code} (200 でない)"
    return 0


try:
    main()
except Exception as e:
    import traceback
    result["note"] = f"例外: {type(e).__name__}: {e} | {traceback.format_exc()[-400:]}"

print("RAPTOR_RESULT_JSON=" + json.dumps(result, ensure_ascii=False))
