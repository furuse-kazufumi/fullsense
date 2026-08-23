# EN Translation Style Guide — "Home Humanoid Games" article

## Mission
Translate the Japanese Qiita article into natural, engaging English for a global engineering audience (Qiita EN article). NOT a literal translation — an English edition by the same author.

## Tone
- Wry, warm, self-deprecating, but technically precise. The JA original is light-hearted (comedy-adjacent) yet rigorous; aim for the voice of a good conference dinner talk.
- Never boastful. Honest disclosure is sacred: translate hedges, caveats, and failure admissions EXACTLY — never strengthen a claim, never soften a failure.
- No condescension ("even beginners can...") — the JA original forbids this too.

## Hard rules
1. **Image URLs unchanged.** Keep every `![alt](https://raw.githubusercontent.com/...)` URL byte-identical. Translate the alt text and the *caption* line below it (keep the `*...*` italic format, keep "(measured in simulation)" style honesty tags).
2. **Code blocks unchanged** (``` fences, contents verbatim). Table STRUCTURE unchanged (same column counts); translate cell text but keep op names, file names, commands, numbers, units.
3. **Numbers, units, dates unchanged.** Keep the M-notation explainer (M = million training steps, not meters).
4. **Footnotes**: keep `[^id]` ids as-is; translate footnote body text; keep citation titles/URLs verbatim.
5. **Headings**: translate, keep the numbering (e.g., `## 6.5.1`).
6. **Credits/licenses verbatim in spirit**: NASA/JPL-Caltech/Univ. of Arizona, EHT Collaboration (CC BY 4.0), Pexels (Barbara Olsen), CMU mocap NSF EIA-0196217 sentence stays in English as-is, LAFAN1 CC BY-NC-ND (non-commercial), MVTec HALCON trademark note.
7. **GIF baked-in labels are Japanese** — that's fine; the intro chunk adds one note: "Figure overlays are in Japanese (the originals); captions carry the meaning."
8. Do not translate proper nouns: Fullseye, Studio, evis, hillco, MuJoCo, MJX, brax, LAFAN1, Menagerie, walk13d, ChopMimic, etc.

## Glossary (use consistently)
- 事前宣言ゲート = pre-declared gate
- 停滞打ち切り = stall termination
- 打ち切り = early termination / cutoff (context)
- 残差制御/残差 = residual control / residual
- お手本/参照モーション = reference motion (mocap "teacher" where the JA says 教師/お手本 colloquially)
- ズル = cheating (reward hacking when technical)
- 審判団 = the referee crew; 審判の審判 = auditing the referee
- かみ砕きコーナー = Plain-Language Corner (keep the 🍙 emoji)
- 凍結局所解 = the freeze local optimum
- 飛行局面 = flight phase
- 蹴上げ = riser (stairs); 踏面 = tread
- 掴めるのに運べない = "can grasp but can't carry"
- 正直な注記 = honest note; 正直な開示 = honest disclosure
- 器用さ競技 = dexterity event; 跳躍の部 = jumping event; 走りの部 = running event; 階段の部 = stairs event
- 自宅ヒューマノイド運動会 = the Home Humanoid Games
- 中間レビュー = interim review

## Output format
Write ONLY the translated markdown (no preamble/commentary). Preserve blank-line structure and blockquotes (`>`).
