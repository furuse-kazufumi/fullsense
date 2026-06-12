#!/usr/bin/env python3
"""Email inbound bridge: agent@furuse.work へのメール -> claude-loop inbox (FullSense control).

Telegram inbound (``fullsense_telegram_inbound.py``) のメール版。ユーザーがメールで作業指示
できるよう、IMAP で新着を取得し claude-loop ``inbox/`` にタスク JSON を落とす。次の raptor
セッション SESSION START の ``raptor-loop-queue ingest`` が拾う。

Safety (Telegram 版と同方針 + メール固有の追加):
- **stdlib only** (imaplib/email)。daemon でなく schedule/on-demand 実行。
- 各タスクに ``constraints: ["no-push", "needs-human-judgment"]`` = 自律ループは危険/不可逆操作を
  人間確認なしに実行しない。
- 認証は ``D:/api-keys.json`` から (agent_email / agent_email_password / agent_email_imap_host /
  agent_email_imap_port)。値は絶対に print しない。
- ★**送信元 allowlist (fail-closed)**: メールは誰でも送れる=untrusted。``agent_email_allowed_senders``
  (comma 区切り) に無い差出人は取り込まない。未設定時は保守的 default のみ許可し WARN。
  (raptor MCP 規約: 信頼境界の入力は再検証・fail-closed)
- **UID 永続** (.email_uid) で二重取込なし。**初回は baseline のみ** (履歴を一括取込しない)。
  現在の未読を取り込みたい場合のみ ``--backfill-unseen`` を明示。

Modes:
    py -3.11 tools/fullsense_email_inbound.py --dry-run          # 新着表示のみ (書込/ack なし)
    py -3.11 tools/fullsense_email_inbound.py --ack-only         # baseline 前進のみ (タスク作らない)
    py -3.11 tools/fullsense_email_inbound.py --backfill-unseen  # 現在の未読を取り込む (初回任意)
    py -3.11 tools/fullsense_email_inbound.py                    # UID>baseline の新着を取込 + 前進
"""
from __future__ import annotations

import argparse
import email
import imaplib
import json
import os
import sys
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime, parseaddr
from datetime import UTC, datetime
from pathlib import Path

API_KEYS_FILE = Path(r"D:\api-keys.json")
DEFAULT_ALLOWED = ("puruyan@live.jp", "kazufumi@furuse.work")  # 未設定時の保守的 default
MAX_BODY_CHARS = 8000
MAX_BACKFILL = 50


def _loop_root() -> Path:
    env = os.environ.get("RAPTOR_LOOP_DIR")
    if env:
        return Path(env)
    if os.name == "nt" and Path("D:/tools").exists():
        return Path("D:/tools/claude-loop")
    return Path.home() / ".claude-loop"


def _ensure_utf8_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):  # stderr も: 警告の cp932 文字化け回避
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except Exception:
            pass


def _secret(name: str, default: str = "") -> str:
    """D:/api-keys.json 優先 -> env。値は print しない。"""
    try:
        keys = json.loads(API_KEYS_FILE.read_text(encoding="utf-8"))
        if keys.get(name):
            return str(keys[name])
    except Exception:
        pass
    return os.environ.get(name, default)


def _allowed_senders() -> set[str]:
    raw = _secret("agent_email_allowed_senders")
    if raw:
        return {a.strip().lower() for a in raw.split(",") if a.strip()}
    print("[warn] agent_email_allowed_senders 未設定 -> 保守的 default のみ許可 "
          f"({', '.join(DEFAULT_ALLOWED)})", file=sys.stderr)
    return {a.lower() for a in DEFAULT_ALLOWED}


def _uid_path() -> Path:
    return _loop_root() / ".email_uid"


def _read_uid() -> int | None:
    p = _uid_path()
    if p.exists():
        try:
            return int(p.read_text(encoding="utf-8").strip())
        except ValueError:
            return None
    return None


def _write_uid(value: int) -> None:
    p = _uid_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(str(value), encoding="utf-8")


def _decode(s: str | None) -> str:
    if not s:
        return ""
    try:
        return str(make_header(decode_header(s)))
    except Exception:
        return s


def _extract_text(msg: email.message.Message) -> str:
    """text/plain を優先抽出。無ければ text/html を粗く除タグ。"""
    plain, html = "", ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if "attachment" in disp.lower():
                continue
            if ctype == "text/plain" and not plain:
                plain = _payload(part)
            elif ctype == "text/html" and not html:
                html = _payload(part)
    else:
        if msg.get_content_type() == "text/html":
            html = _payload(msg)
        else:
            plain = _payload(msg)
    text = plain or _strip_html(html)
    return text.strip()[:MAX_BODY_CHARS]


def _payload(part: email.message.Message) -> str:
    try:
        raw = part.get_payload(decode=True)
        if raw is None:
            return ""
        charset = part.get_content_charset() or "utf-8"
        return raw.decode(charset, "replace")
    except Exception:
        return ""


def _strip_html(html: str) -> str:
    import re
    if not html:
        return ""
    html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html)
    return html


def _to_task(uid: int, msg: email.message.Message, sender: str) -> dict:
    subject = _decode(msg.get("Subject")) or "(no subject)"
    body = _extract_text(msg)
    when = ""
    try:
        when = parsedate_to_datetime(msg.get("Date")).isoformat()
    except Exception:
        pass
    return {
        "title": f"[email] {subject[:80]}",
        "description": (subject + "\n\n" + body).strip(),
        "project": "fullsense",
        "priority": 4,
        "constraints": ["no-push", "needs-human-judgment"],
        "source": "email",
        "email_uid": uid,
        "email_from": sender,
        "email_message_id": msg.get("Message-ID", ""),
        "email_date": when,
        "received_at": datetime.now(UTC).isoformat(),
    }


def _connect() -> imaplib.IMAP4_SSL:
    host = _secret("agent_email_imap_host")
    port = int(_secret("agent_email_imap_port", "993") or "993")
    user = _secret("agent_email")
    pw = _secret("agent_email_password")
    if not (host and user and pw):
        raise RuntimeError("agent_email / _password / _imap_host 未設定")
    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(user, pw)
    return conn


def _search_uids(conn: imaplib.IMAP4_SSL, criterion: str) -> list[int]:
    typ, data = conn.uid("search", None, criterion)
    if typ != "OK" or not data or not data[0]:
        return []
    return sorted(int(x) for x in data[0].split())


def main() -> int:
    _ensure_utf8_stdout()
    ap = argparse.ArgumentParser(description="Email inbound -> claude-loop inbox")
    ap.add_argument("--dry-run", action="store_true", help="新着表示のみ、書込/ack なし")
    ap.add_argument("--ack-only", action="store_true", help="baseline 前進のみ、タスク作らない")
    ap.add_argument("--backfill-unseen", action="store_true", help="現在の未読を取り込む(初回任意)")
    args = ap.parse_args()

    user = _secret("agent_email")
    if not user or not _secret("agent_email_password"):
        print("[skip] agent_email / agent_email_password 未設定", file=sys.stderr)
        return 1

    allowed = _allowed_senders()
    try:
        conn = _connect()
    except Exception as e:
        print(f"[skip] IMAP 接続失敗: {type(e).__name__}", file=sys.stderr)  # 例外値に creds 含めない
        return 1

    try:
        conn.select("INBOX")
        last = _read_uid()
        all_uids = _search_uids(conn, "ALL")
        max_uid = all_uids[-1] if all_uids else 0

        # 初回 (baseline 未設定) は履歴を一括取込しない
        if last is None and not args.backfill_unseen:
            if not args.dry_run:
                _write_uid(max_uid)
            print(f"baseline set to UID {max_uid} (初回: 既存メールは取り込まない / "
                  f"現在の未読が要るなら --backfill-unseen)")
            return 0

        if args.backfill_unseen:
            uids = _search_uids(conn, "UNSEEN")[-MAX_BACKFILL:]
        else:
            uids = [u for u in _search_uids(conn, f"UID {(last or 0) + 1}:*") if u > (last or 0)]

        print(f"new emails: {len(uids)} (baseline UID={last})")
        inbox = _loop_root() / "inbox"
        wrote = 0
        for uid in uids:
            typ, data = conn.uid("fetch", str(uid), "(RFC822)")
            if typ != "OK" or not data or not data[0]:
                continue
            msg = email.message_from_bytes(data[0][1])
            sender = parseaddr(msg.get("From", ""))[1].lower()
            subj = _decode(msg.get("Subject"))[:60]
            if sender not in allowed:
                print(f"  uid={uid}  SKIP untrusted sender={sender!r}  subj={subj!r}")
                continue
            print(f"  uid={uid}  from={sender}  subj={subj!r}")
            if args.dry_run or args.ack_only:
                continue
            inbox.mkdir(parents=True, exist_ok=True)
            task = _to_task(uid, msg, sender)
            (inbox / f"email_{uid}.json").write_text(
                json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            wrote += 1

        if not args.dry_run:
            new_baseline = max(max_uid, last or 0)
            _write_uid(new_baseline)
            print(f"baseline advanced to {new_baseline}"
                  + ("" if args.ack_only else f"; wrote {wrote} inbox task(s)"))
        return 0
    finally:
        try:
            conn.logout()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
