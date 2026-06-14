#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent verification of llmesh en/zh/ko translations."""
import re, sys
from pathlib import Path

DRAFTS = Path(r"D:\projects\fullsense\docs\articles\drafts")
FILES = {
    "en": ("QIITA_llmesh_en.md", "Chapter"),
    "zh": ("QIITA_llmesh_zh.md", "第"),
    "ko": ("QIITA_llmesh_ko.md", "제"),
}
JA_SOURCE = DRAFTS / "QIITA_llmesh_ja.md"

def slug(heading: str) -> str:
    s = re.sub(r"[^\w\s-]", "", heading.lower(), flags=re.UNICODE)
    s = re.sub(r"\s", "-", s)
    return s

# hiragana + katakana (leftover Japanese prose indicator); exclude CJK han (shared w/ zh)
KANA = re.compile(r"[぀-ヿ]")

def analyze(path: Path, prefix: str):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    issues = []

    # front matter
    if not text.startswith("---\n"):
        issues.append("front matter missing/!start")
    fm_end = text.find("\n---\n", 4)
    fm = text[4:fm_end] if fm_end > 0 else ""
    if "public_id" in fm:
        issues.append("public_id present (should be omitted)")
    if "private: false" not in fm:
        issues.append("private: false missing")

    # chapter headings  ## <prefix>...
    ch_headings = []
    for ln in lines:
        if ln.startswith("## "):
            body = ln[3:].strip()
            if prefix == "Chapter" and body.startswith("Chapter "):
                ch_headings.append(body)
            elif prefix == "第" and re.match(r"第\d+章", body):
                ch_headings.append(body)
            elif prefix == "제" and re.match(r"제\d+장", body):
                ch_headings.append(body)

    # TOC entries: numbered list with (#anchor)
    toc = re.findall(r"^\d+\. \[.*?\]\(#(.*?)\)", text, flags=re.M)

    # markers
    def cnt(m): return text.count(m)
    markers = {
        "TOPICNAV": cnt("<!-- TOPICNAV -->"),
        "/TOPICNAV": cnt("<!-- /TOPICNAV -->"),
        "KAMI": cnt("<!-- KAMI -->"),
        "INTERLUDE": cnt("<!-- INTERLUDE -->"),
        "team-kb": cnt("<!-- fullsense-team-kb -->"),
        "REFERRAL": cnt("<!-- REFERRAL -->"),
        "/REFERRAL": cnt("<!-- /REFERRAL -->"),
    }

    # anchor match
    anchor_report = []
    expected = [slug(h) for h in ch_headings]
    ok_anchors = (len(toc) == len(expected) == 7) and all(a == e for a, e in zip(toc, expected))
    if not ok_anchors:
        for i in range(max(len(toc), len(expected))):
            e = expected[i] if i < len(expected) else "<none>"
            a = toc[i] if i < len(toc) else "<none>"
            mark = "OK" if e == a else "MISMATCH"
            anchor_report.append(f"   [{i+1}] {mark}\n        heading->{e}\n        toc    ->{a}")

    # kana scan outside code fences and outside <sub> line
    in_code = False
    kana_lines = []
    for n, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if "<sub>" in ln or "</sub>" in ln:
            continue
        if KANA.search(ln):
            kana_lines.append((n, ln.strip()[:90]))

    # ends with /REFERRAL
    ends_ok = text.rstrip().endswith("<!-- /REFERRAL -->")

    print(f"===== {path.name} =====")
    print(f"  lines: {len(lines)}   chapters: {len(ch_headings)}   toc entries: {len(toc)}")
    print(f"  ends with /REFERRAL: {ends_ok}")
    print(f"  markers: {markers}")
    print(f"  anchors 7/7 match: {ok_anchors}")
    if anchor_report:
        print("\n".join(anchor_report))
    print(f"  kana-outside-code lines: {len(kana_lines)}")
    for n, s in kana_lines[:25]:
        print(f"     L{n}: {s}")
    if issues:
        print(f"  ISSUES: {issues}")
    print()
    return ok_anchors, ends_ok, markers, len(kana_lines), issues

allok = True
for lang, (fn, pref) in FILES.items():
    p = DRAFTS / fn
    if not p.exists():
        print(f"MISSING: {fn}"); allok = False; continue
    ok_a, ends_ok, markers, kana, issues = analyze(p, pref)
    if not (ok_a and ends_ok and markers["KAMI"] == 14 and markers["team-kb"] == 7
            and markers["TOPICNAV"] == 1 and markers["REFERRAL"] == 1 and not issues):
        allok = False

# reference: source marker counts
src = JA_SOURCE.read_text(encoding="utf-8")
print("===== ja source reference =====")
print(f"  KAMI={src.count('<!-- KAMI -->')} INTERLUDE={src.count('<!-- INTERLUDE -->')} "
      f"team-kb={src.count('<!-- fullsense-team-kb -->')} "
      f"chapters={len(re.findall(r'^## 第\\d+章', src, flags=re.M))}")
print("\nALL GREEN" if allok else "\nNEEDS ATTENTION")
