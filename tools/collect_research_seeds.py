"""FullSense research→article feedback bridge.

各 FullSense 系プロジェクトの docs/ARTICLE_SEEDS.md(生産者=研究側 llterm 等が deposit)を集約し、
記事側(FullSense/ccr)が一望できる INBOX にまとめる。研究成果 → 記事化 の情報フィードバック経路。

- 生産者(研究側): 作業中の気付きを各 project の docs/ARTICLE_SEEDS.md に append
  (## YYYY-MM-DD セッション / ### N. タイトル / - 気付き / - 根拠 / - 側面)。
- 消費者(記事側): 本スクリプトで INBOX を再生成 → 未記事化(☐)を拾って記事化 → 元エントリに
  「→ 記事化: #NN」を書くと次回 INBOX で ☑ になる(消費トラッキングは元ファイルが単一の真実)。

出力: docs/articles/INBOX_research_seeds.md (newest-first・provenance付き)
使い方: py -3.11 tools/collect_research_seeds.py
"""
import os
import re

SOURCES = {
    "llcore": r"D:/projects/llcore/docs/ARTICLE_SEEDS.md",
    "llive":  r"D:/projects/llive/docs/ARTICLE_SEEDS.md",
    "llmesh": r"D:/projects/llmesh/docs/ARTICLE_SEEDS.md",
    "llove":  r"D:/projects/llove/docs/ARTICLE_SEEDS.md",
    "llloop": r"D:/projects/llloop/docs/ARTICLE_SEEDS.md",
    "llterm": r"D:/projects/llterm/docs/ARTICLE_SEEDS.md",
}
OUT = r"D:/projects/fullsense/docs/articles/INBOX_research_seeds.md"

DATE_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})")
ENTRY_RE = re.compile(r"^###\s+(.*)")
CONSUMED_RE = re.compile(r"記事化|→\s*#|→\s*記事|published")


def first_value(body, key):
    """- **key**: ... の値1行を返す(無ければ空)."""
    m = re.search(rf"\*\*{key}\*\*[：:]\s*(.+)", body)
    return m.group(1).strip() if m else ""


def parse(path, proj):
    if not os.path.exists(path):
        return []
    lines = open(path, encoding="utf-8").read().split("\n")
    entries, cur_date, buf, title = [], "?", None, None

    def flush():
        if title is not None:
            body = "\n".join(buf)
            entries.append({
                "proj": proj, "date": cur_date, "title": title.strip(),
                "aspect": first_value(body, "側面"),
                "gist": first_value(body, "気付き")[:140],
                "consumed": bool(CONSUMED_RE.search(body)),
            })

    for ln in lines:
        dm = DATE_RE.match(ln)
        if dm:
            flush(); title, buf = None, []
            cur_date = dm.group(1)
            continue
        em = ENTRY_RE.match(ln)
        if em:
            flush()
            title, buf = em.group(1), []
            continue
        if title is not None:
            buf.append(ln)
    flush()
    return entries


def build():
    all_entries = []
    for proj, path in SOURCES.items():
        all_entries.extend(parse(path, proj))
    # newest first by date, then project
    all_entries.sort(key=lambda e: (e["date"], e["proj"]), reverse=True)

    open_n = sum(1 for e in all_entries if not e["consumed"])
    out = []
    out.append("# 研究→記事 INBOX (research feedback) — 自動集約・再生成可")
    out.append("")
    out.append("> `tools/collect_research_seeds.py` が各 FullSense 系 project の `docs/ARTICLE_SEEDS.md` を集約。")
    out.append("> ☐=未記事化 / ☑=記事化済(元エントリに「→ 記事化: #NN」を書くと ☑ になる)。")
    out.append(f"> 計 {len(all_entries)} 件 / 未記事化 **{open_n}** 件。")
    out.append("")
    cur = None
    for e in all_entries:
        if e["date"] != cur:
            cur = e["date"]
            out.append(f"\n## {cur}\n")
        box = "☑" if e["consumed"] else "☐"
        out.append(f"- {box} **[{e['proj']}]** {e['title']}")
        if e["aspect"]:
            out.append(f"  - 側面: {e['aspect']}")
        if e["gist"]:
            out.append(f"  - 気付き: {e['gist']}")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote: {OUT}  ({len(all_entries)} entries, {open_n} unwritten)")
    for proj, path in SOURCES.items():
        mark = "ok" if os.path.exists(path) else "(no ARTICLE_SEEDS.md)"
        print(f"  {proj}: {mark}")


if __name__ == "__main__":
    build()
