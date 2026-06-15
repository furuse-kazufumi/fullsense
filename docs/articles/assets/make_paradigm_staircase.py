"""#43 挿絵: prompt → context → harness → loop の階段 (2025→2026).
言語ニュートラル(英語用語のみ) → ja/en/zh/ko 全版に同一 SVG を流用可. 見やすさ第一・静的完成形.
"""
import os

OUT = os.environ.get("STAIR_SVG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "paradigm_staircase.svg"))

steps = [
    ("prompt", "engineering", "craft the ask", "2025", "#6b7785"),
    ("context", "engineering", "design what it sees", "2025", "#6b7785"),
    ("harness", "engineering", "design the apparatus", "2026", "#1565c0"),
    ("loop", "engineering", "design the autonomy", "2026", "#2e7d32"),
]

W, H = 1000, 440
bw, bh = 200, 84
x0 = 40
gap = (W - 2 * x0 - bw) / 3          # 240
baseY = 332
rise = 66

X = [x0 + i * gap for i in range(4)]          # 40, 280, 520, 760
Y = [baseY - i * rise for i in range(4)]       # 332, 266, 200, 134

p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Segoe UI, Hiragino Sans, Meiryo, sans-serif">']
p.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

# era bands (behind)
p.append(f'<rect x="20" y="100" width="480" height="300" rx="10" fill="#f4f5f7"/>')
p.append(f'<rect x="510" y="100" width="470" height="300" rx="10" fill="#eef4fb"/>')
p.append(f'<text x="260" y="126" font-size="16" fill="#8a94a3" text-anchor="middle" font-weight="bold">2025 — prompt / context</text>')
p.append(f'<text x="745" y="126" font-size="16" fill="#3f7cc0" text-anchor="middle" font-weight="bold">2026 — harness / loop</text>')

# arrows between steps (diagonal up-right)
for i in range(3):
    x1 = X[i] + bw
    y1 = Y[i] + bh / 2
    x2 = X[i + 1]
    y2 = Y[i + 1] + bh / 2
    p.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2-8:.0f}" y2="{y2+6:.0f}" stroke="#b0b8c4" stroke-width="3"/>')
    # arrowhead
    p.append(f'<path d="M{x2-8:.0f},{y2+6:.0f} l-12,-3 l4,9 z" fill="#b0b8c4"/>')

# step boxes
for i, (term, sub, gloss, era, color) in enumerate(steps):
    x, y = X[i], Y[i]
    p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw}" height="{bh}" rx="10" fill="{color}"/>')
    p.append(f'<text x="{x+bw/2:.0f}" y="{y+34:.0f}" font-size="23" fill="#fff" text-anchor="middle" font-weight="bold">{term}</text>')
    p.append(f'<text x="{x+bw/2:.0f}" y="{y+57:.0f}" font-size="16" fill="#e8eef5" text-anchor="middle">{sub}</text>')
    p.append(f'<text x="{x+bw/2:.0f}" y="{y+bh+22:.0f}" font-size="14" fill="#555" text-anchor="middle">{gloss}</text>')

# baseline axis
p.append(f'<line x1="20" y1="404" x2="980" y2="404" stroke="#333" stroke-width="2"/>')
p.append(f'<text x="980" y="426" font-size="15" fill="#333" text-anchor="end">engineering maturity →</text>')
# title
p.append(f'<text x="{W/2:.0f}" y="58" font-size="25" fill="#1a1a1a" text-anchor="middle" font-weight="bold">The staircase of AI engineering: 2025 → 2026</text>')
p.append(f'<text x="{W/2:.0f}" y="84" font-size="14.5" fill="#666" text-anchor="middle">prompt → context → harness → loop （上の段ほど「LLM の外側」を設計する）</text>')
p.append('</svg>')

open(OUT, "w", encoding="utf-8").write("\n".join(p))
print("wrote:", OUT, f"({os.path.getsize(OUT)} bytes)")
