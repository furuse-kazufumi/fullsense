#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert 2 'Snack Basue Gou' manga panels into Qiita article 932c4cfc6cfca636504a and PATCH.

Panels chosen for this TUI-observability-dashboard article:
  - 110 = AI 搭載ブラウザが即答を割込む無粋 -> 「なぜ TUI なのか」(ブラウザ UI を退ける論)節の直後
  - 032 = キャバクラとスナックの違い (製品の立ち位置) -> 「ファミリー構成」見出し直後 (llove の立ち位置)

Idempotent-ish: if a panel image URL already exists in the body, it is not inserted again.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

sys.path.insert(0, r"D:/projects/fullsense/tools")
from qiita_public_post import get_token  # noqa: E402

for s in ("stdout", "stderr"):
    try:
        getattr(sys, s).reconfigure(encoding="utf-8")
    except Exception:
        pass

ITEM_ID = "932c4cfc6cfca636504a"
API = f"https://qiita.com/api/v2/items/{ITEM_ID}"
RAW_BASE = "https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all"

# --- panel definitions ----------------------------------------------------- #
PANELS = [
    {
        "num": "110",
        "alt": "AI 搭載ブラウザが会話に即答を割り込んでくる場面",
        "caption": ("即答を割り込んでくる AI ブラウザもいいけれど、運用現場が見たいのは"
                    "「いまの状態を秒で、SSH 越しに、ラグなく」。だから TUI を選んだ。"),
        # anchor: 直後に挿入する行 (この行を含む段落の末尾) — 「なぜ TUI なのか」結び
        "anchor": "`llove` はこれを **1 枚のターミナル** で解く設計選択をしました。SSH 越しでも、現場 PC でも、開発機でも、**同じ画面が出ます**。",
        "where": "after_line",
    },
    {
        "num": "032",
        "alt": "キャバクラとスナックの違いを語る場面",
        "caption": ("キャバクラとスナックが違うように、Web ダッシュボードと TUI も役割が違う。"
                    "llove は「現場に居座れる観測層」という立ち位置を選んだ。"),
        # anchor: 「## ファミリー構成」見出しの直後
        "anchor": "## ファミリー構成",
        "where": "after_heading",
    },
]
COPYRIGHT = "（© Forbidden shibukawa / SHUEISHA・スナックバス江）"


def panel_block(p: dict) -> str:
    url = f"{RAW_BASE}/{p['num']}.jpg"
    return (
        f"\n![{p['alt']}]({url})\n"
        f"> 🗒️ *「{p['caption']}」* {COPYRIGHT}\n"
    )


def http_status(url: str) -> int:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main() -> int:
    note_parts: list[str] = []
    tok = get_token()
    if not tok:
        return _emit("fail", panels=[], http="-", note="NO TOKEN (QIITA_PUBLIC_TOKEN / qiita-cli credentials.json 不在)")

    # 1. GET current article
    try:
        req = urllib.request.Request(API, headers={"Authorization": "Bearer " + tok})
        with urllib.request.urlopen(req, timeout=30) as r:
            cur = json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return _emit("fail", panels=[], http="-", note=f"GET 失敗: {e}")

    body = cur.get("body", "")
    title = cur.get("title", "")
    private = bool(cur.get("private", False))
    tags = [{"name": t.get("name"), "versions": t.get("versions", [])} for t in (cur.get("tags") or [])]

    # 2. verify raw images are 200, then insert
    used: list[str] = []
    for p in PANELS:
        url = f"{RAW_BASE}/{p['num']}.jpg"
        code = http_status(url)
        if code != 200:
            note_parts.append(f"panel {p['num']} raw={code} -> skip")
            continue
        if url in body:
            note_parts.append(f"panel {p['num']} already present -> skip")
            continue
        anchor = p["anchor"]
        idx = body.find(anchor)
        if idx == -1:
            note_parts.append(f"panel {p['num']} anchor not found -> skip")
            continue
        # insertion point = end of the line that contains the anchor
        line_end = body.find("\n", idx)
        if line_end == -1:
            line_end = len(body)
        block = panel_block(p)
        body = body[:line_end] + "\n" + block + body[line_end:]
        used.append(p["num"])

    if not used:
        return _emit("fail", panels=[], http="-", note="挿入できたコマ無し: " + "; ".join(note_parts))

    # 3. PATCH
    payload = {"title": title, "body": body, "tags": tags, "private": private}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API, data=data, method="PATCH",
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            http_code = r.status
            res = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_err = ""
        try:
            body_err = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        return _emit("fail", panels=used, http=str(e.code),
                     note=f"PATCH HTTPError {e.code}: {body_err} | prechecks: {'; '.join(note_parts) or 'none'}")
    except Exception as e:  # noqa: BLE001
        return _emit("fail", panels=used, http="-", note=f"PATCH 失敗: {e}")

    if http_code == 200:
        note = (f"panels inserted at: " + ", ".join(used)
                + f"; url={res.get('url')}"
                + ("; " + "; ".join(note_parts) if note_parts else ""))
        return _emit("ok", panels=used, http=str(http_code), note=note)
    return _emit("fail", panels=used, http=str(http_code), note=f"unexpected code; res={str(res)[:200]}")


def _emit(status: str, panels, http, note: str) -> int:
    out = {"id": ITEM_ID, "status": status, "http": str(http),
           "panels": panels, "note": note}
    print("===RESULT_JSON===")
    print(json.dumps(out, ensure_ascii=False))
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
