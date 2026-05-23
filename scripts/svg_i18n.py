# SPDX-License-Identifier: Apache-2.0
"""SVG i18n variant generator for QIITA #24 series multilingual rollout.

A base SVG (Japanese) is turned into language variants (_en / _zh / _ko) by
**translating only visible text** — the content of ``<title>``, ``<text>`` and
the ``aria-label`` attribute. Geometry, animation, colours, attribute order and
whitespace are left byte-identical, which is exactly the transformation the
hand-made #24-02 variants applied (verified by diff).

This keeps imgix constraints satisfied for free: we never add ``<mpath>``,
never touch ``animateMotion``, and the output is validated as well-formed XML
with ``xml.dom.minidom`` before being written.

Usage:
    py -3.11 scripts/svg_i18n.py extract <base.svg>
        Print a JSON object whose keys are every unique translatable string
        (in document order). Fill in translations to build a mapping file.

    py -3.11 scripts/svg_i18n.py gen <base.svg> <map.json> <lang> [--out <dir>]
        ``map.json`` maps original-string -> {"en": ..., "zh": ..., "ko": ...}.
        Writes ``<base>_<lang>.svg`` next to the base (or under --out). Strings
        absent from the map, or whose entry for ``lang`` is empty/missing, pass
        through unchanged (technical terms like "TRIZ" stay as-is).

    py -3.11 scripts/svg_i18n.py verify <svg> [<svg> ...]
        Parse each file with minidom; exit non-zero if any is malformed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from xml.dom import minidom


def _ensure_utf8_stdout() -> None:
    """Reconfigure stdout/stderr to UTF-8 so em-dash / CJK survive cp932 consoles."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):  # pragma: no cover - stream-dependent
                pass

# <title>…</title> | <text …>…</text> | aria-label="…"
_TITLE_RE = re.compile(r"(<title>)(.*?)(</title>)", re.DOTALL)
_TEXT_RE = re.compile(r"(<text\b[^>]*>)(.*?)(</text>)", re.DOTALL)
_ARIA_RE = re.compile(r'(aria-label=")([^"]*)(")')

LANGS = ("en", "zh", "ko")


def _split_ws(content: str) -> tuple[str, str, str]:
    """Split into (leading_ws, core, trailing_ws) so maps key on the trimmed core."""
    core = content.strip()
    if not core:
        return "", content, ""
    start = content.index(core)
    return content[:start], core, content[start + len(core):]


def _iter_translatable(svg: str) -> list[str]:
    """Return trimmed translatable cores in document order (may contain duplicates)."""
    spans: list[tuple[int, str]] = []
    for m in _TITLE_RE.finditer(svg):
        spans.append((m.start(2), _split_ws(m.group(2))[1]))
    for m in _TEXT_RE.finditer(svg):
        spans.append((m.start(2), _split_ws(m.group(2))[1]))
    for m in _ARIA_RE.finditer(svg):
        spans.append((m.start(2), _split_ws(m.group(2))[1]))
    spans.sort(key=lambda t: t[0])
    return [s for _, s in spans if s]


def _unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def cmd_extract(base_path: str) -> int:
    svg = Path(base_path).read_text(encoding="utf-8")
    strings = _unique_ordered(_iter_translatable(svg))
    # Emit a skeleton mapping so the caller only fills in the values.
    skeleton = {s: {lang: "" for lang in LANGS} for s in strings}
    print(json.dumps(skeleton, ensure_ascii=False, indent=2))
    return 0


def _apply(svg: str, mapping: dict[str, dict[str, str]], lang: str) -> str:
    def translate(content: str) -> str:
        entry = mapping.get(content)
        if not entry:
            return content
        repl = entry.get(lang, "")
        return repl if repl else content

    def sub_title(m: re.Match[str]) -> str:
        return f"{m.group(1)}{translate(m.group(2))}{m.group(3)}"

    def sub_text(m: re.Match[str]) -> str:
        return f"{m.group(1)}{translate(m.group(2))}{m.group(3)}"

    def sub_aria(m: re.Match[str]) -> str:
        return f"{m.group(1)}{translate(m.group(2))}{m.group(3)}"

    svg = _TITLE_RE.sub(sub_title, svg)
    svg = _TEXT_RE.sub(sub_text, svg)
    svg = _ARIA_RE.sub(sub_aria, svg)
    return svg


def cmd_gen(base_path: str, map_path: str, lang: str, out_dir: str | None) -> int:
    if lang not in LANGS:
        print(f"error: lang must be one of {LANGS}, got {lang!r}", file=sys.stderr)
        return 2
    base = Path(base_path)
    svg = base.read_text(encoding="utf-8")
    mapping: dict[str, dict[str, str]] = json.loads(Path(map_path).read_text(encoding="utf-8"))
    out_svg = _apply(svg, mapping, lang)
    # fail-closed: refuse to write malformed XML
    minidom.parseString(out_svg.encode("utf-8"))
    out_base = Path(out_dir) if out_dir else base.parent
    out_path = out_base / f"{base.stem}_{lang}.svg"
    out_path.write_text(out_svg, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


def cmd_verify(paths: list[str]) -> int:
    rc = 0
    for p in paths:
        try:
            minidom.parseString(Path(p).read_text(encoding="utf-8").encode("utf-8"))
            print(f"ok   {p}")
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            print(f"FAIL {p}: {exc}", file=sys.stderr)
            rc = 1
    return rc


def main(argv: list[str]) -> int:
    _ensure_utf8_stdout()
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "extract" and len(argv) == 3:
        return cmd_extract(argv[2])
    if cmd == "gen" and len(argv) >= 5:
        out_dir = None
        if "--out" in argv:
            out_dir = argv[argv.index("--out") + 1]
        return cmd_gen(argv[2], argv[3], argv[4], out_dir)
    if cmd == "verify" and len(argv) >= 3:
        return cmd_verify(argv[2:])
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
