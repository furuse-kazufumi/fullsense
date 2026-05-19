#!/usr/bin/env python3
"""
docs/NEXT_SESSION.auto.md を自動生成する Stop hook 用スクリプト.

設計方針:
  - 手書き docs/NEXT_SESSION.md は人間 / agent が考えた「現在の方向性」を
    そのまま温存. これは drift 検出対象.
  - 自動生成は docs/NEXT_SESSION.auto.md という別ファイルに分離し,
    機械チェック可能な情報 (git log / verify_publication 直近結果 /
    関連プロジェクトの test 件数 / 未消化 operator action のチェックボックス
    化) を毎ターン上書きで貼る.

呼ばれ方:
  - raptor の Stop hook (.claude/settings.json) 経由
  - 直接呼び出し: `py -3.11 D:/projects/fullsense/scripts/gen_next_session_auto.py`
  - RAPTOR_CALLER_DIR が "D:/projects/fullsense" 以外なら no-op で 0 exit.

silent:
  - stdout には何も出さない (Claude UI を汚さない).
  - 例外は stderr に簡潔に出して exit 0 (hook が他処理を止めない).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

PORTAL_ROOT = Path("D:/projects/fullsense")
RELATED_PROJECTS: dict[str, Path] = {
    "llive": Path("D:/projects/llive"),
    "llove": Path("D:/projects/llove"),
    "llmesh": Path("D:/projects/llmesh"),
    "lldesign": Path("D:/projects/lldesign"),
    "lltrade": Path("D:/projects/lltrade"),
}


def _run(cmd: list[str], cwd: Path, timeout: int = 5) -> str:
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return (result.stdout or "").strip()
    except Exception as e:  # noqa: BLE001 - want any failure to fold into "(error: ...)"
        return f"(error: {e})"


def _portal_git_section(portal: Path) -> str:
    log = _run(["git", "log", "-10", "--oneline", "--no-decorate"], portal)
    status = _run(["git", "status", "--porcelain"], portal) or "(clean)"
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], portal)
    ahead_behind = _run(
        ["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"],
        portal,
    )
    return (
        f"- ブランチ: `{branch}`\n"
        f"- HEAD vs upstream (左=ahead 右=behind): `{ahead_behind or 'n/a'}`\n\n"
        f"```\n{log}\n```\n\n"
        f"### git status (porcelain)\n\n```\n{status}\n```\n"
    )


def _related_projects_section() -> str:
    rows: list[str] = []
    rows.append("| project | 最新 commit | 直近 commit msg | tests/ 直近 mtime |")
    rows.append("|---|---|---|---|")
    for name, path in RELATED_PROJECTS.items():
        if not path.is_dir():
            rows.append(f"| {name} | (missing) | — | — |")
            continue
        head = _run(["git", "log", "-1", "--format=%h %ad", "--date=short"], path)
        msg = _run(["git", "log", "-1", "--format=%s"], path)
        tests_dir = path / "tests"
        mtime_label = "—"
        if tests_dir.is_dir():
            try:
                latest = max(
                    (p.stat().st_mtime for p in tests_dir.rglob("*") if p.is_file()),
                    default=0,
                )
                if latest:
                    mtime_label = datetime.fromtimestamp(latest).strftime("%Y-%m-%d %H:%M")
            except OSError:
                pass
        msg_safe = (msg or "").replace("|", "\\|")
        rows.append(f"| {name} | `{head or 'n/a'}` | {msg_safe} | {mtime_label} |")
    return "\n".join(rows) + "\n"


_OPERATOR_HEADING = re.compile(r"^##\s*🧑\s+Operator actions queued.*$", re.IGNORECASE)
_AGENT_HEADING = re.compile(r"^##\s*🤖", re.IGNORECASE)


def _extract_operator_actions(next_session_md: Path) -> list[str]:
    """既存 NEXT_SESSION.md から 🧑 Operator actions セクションを抜き出し,
    `### N. タイトル` の見出しを `[ ]` checkbox に変換して返す."""
    if not next_session_md.is_file():
        return []
    in_section = False
    items: list[str] = []
    try:
        text = next_session_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for line in text.splitlines():
        if _OPERATOR_HEADING.match(line):
            in_section = True
            continue
        if in_section and _AGENT_HEADING.match(line):
            break
        if in_section and line.startswith("### "):
            title = line[4:].strip()
            items.append(title)
    return items


def _operator_actions_section(portal: Path) -> str:
    next_md = portal / "docs" / "NEXT_SESSION.md"
    items = _extract_operator_actions(next_md)
    if not items:
        return (
            "_(`NEXT_SESSION.md` から 🧑 セクションを抽出できませんでした.\n"
            " 見出しが `## 🧑 Operator actions queued ...` 形式か,\n"
            " 下位項目が `### N. ...` 形式か確認してください.)_\n"
        )
    lines = [f"- [ ] {it}" for it in items]
    lines.append("")
    lines.append(
        "_本セクションは `NEXT_SESSION.md` の 🧑 見出し配下を毎ターン再抽出したものです.\n"
        " 消化判定は手動で `NEXT_SESSION.md` 側を編集してください._"
    )
    return "\n".join(lines) + "\n"


def _verify_cache_section(portal: Path) -> str:
    """`scripts/verify_publication.sh` の直近実行結果が `out/verify_publication.last`
    に残っていれば snapshot する. 無ければ案内のみ.
    """
    cache = portal / "out" / "verify_publication.last"
    if cache.is_file():
        try:
            content = cache.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"_(cache read error: {e})_\n"
        ts = datetime.fromtimestamp(cache.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        tail = "\n".join(content.splitlines()[-30:])
        return (
            f"- 最終実行 (cache mtime): {ts}\n\n"
            f"<details><summary>verify_publication.sh tail (30 lines)</summary>\n\n"
            f"```\n{tail}\n```\n\n"
            f"</details>\n"
        )
    return (
        "- まだ `out/verify_publication.last` がありません.\n"
        "  `bash scripts/verify_publication.sh | tee out/verify_publication.last`\n"
        "  で snapshot を残すと次回以降ここに tail 30 行が貼られます.\n"
    )


def _front_matter() -> str:
    return (
        "---\n"
        'layout: default\n'
        'title: "Next Session (auto-generated)"\n'
        "nav_order: 94\n"
        "---\n\n"
    )


def _header(now: datetime) -> str:
    return (
        f"# Next Session — auto-generated snapshot\n\n"
        f"> このファイルは Stop hook (`scripts/gen_next_session_auto.py`) が\n"
        f"> 毎ターン自動上書きします. **手動編集は失われます**.\n"
        f"> 永続化したい内容は [`NEXT_SESSION.md`]({{ '/NEXT_SESSION' | relative_url }}) 側に書いてください.\n\n"
        f"- **生成時刻**: {now.strftime('%Y-%m-%d %H:%M:%S %Z').strip()}\n"
        f"- **生成元**: `scripts/gen_next_session_auto.py` (RAPTOR Stop hook)\n"
    )


def _recent_files_section(portal: Path, hours: int = 4, limit: int = 20) -> str:
    cutoff = datetime.now() - timedelta(hours=hours)
    skip_dirs = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        "out",
        ".next",
        "target",
        "_site",
        ".jekyll-cache",
    }
    rows: list[tuple[datetime, str]] = []
    for p in portal.rglob("*"):
        if not p.is_file():
            continue
        if any(part in skip_dirs for part in p.parts):
            continue
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
        except OSError:
            continue
        if mtime > cutoff:
            try:
                rel = p.relative_to(portal).as_posix()
            except ValueError:
                continue
            rows.append((mtime, rel))
    rows.sort(reverse=True)
    if not rows:
        return f"_(直近 {hours} 時間に変更されたファイル無し)_\n"
    lines = [f"- `{m.strftime('%H:%M')}` `{r}`" for m, r in rows[:limit]]
    return "\n".join(lines) + "\n"


def _compose(portal: Path) -> str:
    now = datetime.now()
    sections: list[str] = []
    sections.append(_front_matter() + _header(now))
    sections.append("\n## 1. portal git snapshot\n\n" + _portal_git_section(portal))
    sections.append("\n## 2. 関連プロジェクト最新状態\n\n" + _related_projects_section())
    sections.append("\n## 3. 未消化 operator action (NEXT_SESSION.md 由来)\n\n" + _operator_actions_section(portal))
    sections.append("\n## 4. verify_publication 直近結果 (cache)\n\n" + _verify_cache_section(portal))
    sections.append("\n## 5. 直近 4 時間に変更されたファイル (portal)\n\n" + _recent_files_section(portal))
    sections.append(
        "\n## Cross-references\n\n"
        "- [NEXT_SESSION (manual)]({{ '/NEXT_SESSION' | relative_url }}) — 人手で書く方向性メモ\n"
        "- [PROGRESS]({{ '/PROGRESS' | relative_url }}) — 累積セッション履歴\n"
        "- [Roadmap]({{ '/roadmap' | relative_url }}) — Phase + dependency\n"
        "- [Spec hub]({{ '/spec/' | relative_url }}) — FullSense Spec v1.1\n"
    )
    return "\n".join(sections) + "\n"


def main(argv: Iterable[str]) -> int:
    portal = PORTAL_ROOT
    caller = os.environ.get("RAPTOR_CALLER_DIR", "")
    if caller and Path(caller).resolve() != portal.resolve():
        # 別プロジェクトで作業中なら no-op.
        return 0
    if not portal.is_dir():
        print(f"[gen_next_session_auto] portal not found: {portal}", file=sys.stderr)
        return 0
    target = portal / "docs" / "NEXT_SESSION.auto.md"
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_compose(portal), encoding="utf-8")
    except OSError as e:
        print(f"[gen_next_session_auto] write failed: {e}", file=sys.stderr)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
