import re, sys, io, pathlib
src = pathlib.Path("public/qiita_games_personal_humanoid.md").read_text(encoding="utf-8")
# frontmatter を分離
m = re.match(r"^---\n.*?\n---\n", src, re.S)
assert m, "frontmatter not found"
fm = m.group(0)
body = src[m.end():]
pathlib.Path("ml_work/frontmatter_ja.txt").write_text(fm, encoding="utf-8")
# コードフェンス外の見出し行で分割点を作る
lines = body.split("\n")
in_fence = False
sections = []  # list of list-of-lines
cur = []
for ln in lines:
    stripped = ln.lstrip()
    if stripped.startswith("```"):
        in_fence = not in_fence
    if (not in_fence) and re.match(r"^#{1,4} ", ln) and cur:
        sections.append(cur); cur = [ln]
    else:
        cur.append(ln)
if cur: sections.append(cur)
# ~34k 字で束ねる
TARGET = 34000
chunks = []
buf = []
size = 0
for sec in sections:
    s = "\n".join(sec)
    if buf and size + len(s) > TARGET:
        chunks.append("\n".join(buf)); buf = []; size = 0
    buf.append(s); size += len(s) + 1
if buf: chunks.append("\n".join(buf))
# roundtrip 検証
joined = "\n".join(chunks)
assert joined == body, f"roundtrip mismatch: {len(joined)} vs {len(body)}"
for i, c in enumerate(chunks):
    pathlib.Path(f"ml_work/chunk_{i:02d}_ja.md").write_text(c, encoding="utf-8")
print(f"OK: {len(chunks)} chunks, body={len(body)} chars")
for i, c in enumerate(chunks):
    print(f"  chunk_{i:02d}: {len(c)} chars")
