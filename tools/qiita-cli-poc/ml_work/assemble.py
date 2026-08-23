import re, sys, pathlib, collections
lang = sys.argv[1]  # zh / ko
ml = pathlib.Path("ml_work")
chunks = [ml / f"chunk_{i:02d}_{lang}.md" for i in range(11)]
for c in chunks: assert c.exists(), c
body = "\n".join(c.read_text(encoding="utf-8").rstrip("\n") if i < 10 else c.read_text(encoding="utf-8")
                 for i, c in enumerate(chunks))
# 注意: split 時は "\n".join だったので、末尾改行の扱いを JA と同一化する
ja_body_chunks = [ml / f"chunk_{i:02d}_ja.md" for i in range(11)]
ja_body = "\n".join(c.read_text(encoding="utf-8") for c in ja_body_chunks)

FM = {
 "zh": """---
title: 羡慕北京的人形机器人运动会,于是我在自家PC上也办了一届 — 选手·项目·裁判·转播·训练全部自己做的 Physical AI 开发记
tags:
  - Mujoco
  - PhysicalAI
  - 人形机器人
  - 强化学习
  - Simulation
private: true
updated_at: null
id: null
organization_url_name: null
slide: false
ignorePublish: false
---
""",
 "ko": """---
title: 베이징 휴머노이드 운동회가 부러워서, 집 PC에서 직접 열기로 했다 — 선수·종목·심판·중계·육성까지 전부 만드는 Physical AI 개발기
tags:
  - Mujoco
  - PhysicalAI
  - 휴머노이드
  - 강화학습
  - Simulation
private: true
updated_at: null
id: null
organization_url_name: null
slide: false
ignorePublish: false
---
""",
}
out_name = {"zh": "home_humanoid_games_zh.md", "ko": "home_humanoid_games_ko.md"}[lang]
body_full = "\n".join((ml / f"chunk_{i:02d}_{lang}.md").read_text(encoding="utf-8") for i in range(11))
text = FM[lang] + body_full
pathlib.Path("public", out_name).write_text(text, encoding="utf-8")

# ===== 記事単位監査 =====
url_re = re.compile(r'https?://[^)\s"\'<>]+')
ja_urls = collections.Counter(url_re.findall(ja_body))
tr_urls = collections.Counter(url_re.findall(body_full))
ok_url = ja_urls == tr_urls
fence = sum(1 for l in body_full.split("\n") if l.lstrip().startswith("```"))
ja_fence = sum(1 for l in ja_body.split("\n") if l.lstrip().startswith("```"))
fn_def_ja = sorted(re.findall(r'^\[\^([^\]]+)\]:', ja_body, re.M))
fn_def_tr = sorted(re.findall(r'^\[\^([^\]]+)\]:', body_full, re.M))
dup = [k for k, v in collections.Counter(fn_def_tr).items() if v > 1]
heads_ja = [l for l in ja_body.split("\n") if re.match(r'^#{1,4} ', l)]
heads_tr = [l for l in body_full.split("\n") if re.match(r'^#{1,4} ', l)]
print(f"[{lang}] size={len(text)} chars")
print(f"URL multiset: {'OK' if ok_url else 'NG'} (ja {sum(ja_urls.values())} / tr {sum(tr_urls.values())})")
if not ok_url:
    diff1 = ja_urls - tr_urls; diff2 = tr_urls - ja_urls
    print("  ja-only:", list(diff1.items())[:5]); print("  tr-only:", list(diff2.items())[:5])
print(f"fences: ja {ja_fence} / tr {fence} {'OK' if fence == ja_fence and fence % 2 == 0 else 'NG'}")
print(f"footnote defs: ja {len(fn_def_ja)} / tr {len(fn_def_tr)} {'OK' if fn_def_ja == fn_def_tr else 'NG'} dup={dup}")
print(f"headings: ja {len(heads_ja)} / tr {len(heads_tr)} {'OK' if len(heads_ja) == len(heads_tr) else 'NG'}")
sys.exit(0 if (ok_url and fence == ja_fence and fence % 2 == 0 and fn_def_ja == fn_def_tr and not dup and len(heads_ja) == len(heads_tr)) else 1)
