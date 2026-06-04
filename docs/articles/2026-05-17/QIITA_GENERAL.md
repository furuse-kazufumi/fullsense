---
title: "AI を『使うだけ』から『AI に秘書を付ける』へ — 自宅 PC で動くおせっかい AI フレームワーク llive 開発日記"
tags: AI 業務効率化 セキュリティ ローカル環境 認知科学
id: cda72a85bf20524eb8f5
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

![AI に秘書を付ける — llive 開発日記 4コマ](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/general_4koma.svg)
# AI を『使うだけ』から『AI に秘書を付ける』へ — 自宅 PC で動くおせっかい AI フレームワーク llive 開発日記

著者: **古瀬 和文（ぷるやん）**

## はじめに — 「AI に任せる」って実は怖い

最近、ChatGPT や Claude、Gemini など、便利な AI が次々と出てきました。仕事の文章を書かせたり、コードを書かせたり、子どもの宿題のヒントを聞いたり、ちょっとした調べ物に使ったり。

でも、こんなふうに思ったことはありませんか?

- 「会社の機密情報を AI に投げて大丈夫?」
- 「家族との会話の文字起こしを Google に送って平気?」
- 「医療記録を AI に分析させたら個人情報はどこへ行く?」
- 「電気代も気になる。クラウドで動かすと月いくら?」
- 「ネットが切れたら何もできなくなる?」
- 「AI が間違ったことを言っても誰が責任を取るの?」

実は、これらの懸念にきちんと答えてくれる AI ツールは、まだ世の中にあまりありません。**便利な AI は基本的にクラウド頼み**で、データはどこかの大きな会社のサーバに送られて処理されます。

私が今作っている **llive (リブ)** という研究開発フレームワークは、この問題に正面から取り組んでいます。一言で言うと:

> **「AI 本体」ではなく、「AI を使いこなす秘書」を作る研究**

今日 (2026 年 5 月 17 日) 1 日で、要件 32 件追加 + プログラム約 2200 行 + テスト 78 件追加 + ベンチマーク 4 種類実施 + 記事 11 本公開、という結構な分量を進めたので、その内容を **非エンジニアの方にも分かるよう** に整理しました。

## llive を例えるなら — 「AI に秘書を付ける」感じ

AI を「優秀だけど忘れっぽくて、計算が苦手で、嘘もつく、責任感の薄い新入社員」 と想像してください。

```
[従来]               [llive がやろうとしていること]
新入社員 (AI) に  →  上司 (=人間) は新入社員に
直接仕事を依頼      指示書 (=Brief) を渡し、
                    秘書 (=llive) が以下を担当:
                    - 過去のやり取りを記録 (記憶)
                    - 危ない発言を止める (監査)
                    - 計算は電卓を使わせる (補完)
                    - 段取りを管理 (思考プロセス)
                    - 責任所在を残す (台帳)
```

つまり llive は「**AI 本体を作り替える**」のではなく、「**AI の周りに被せて、苦手な部分を補い、危ない部分を止める仕組み**」です。

中で動かす AI 本体は、Qwen (アリババの OSS LLM) や Llama (Meta の OSS LLM) を選べます。これらは大手企業が無料で公開しているもので、自宅 PC でも動かせます。

## 今日やったこと、5 つに絞って

### 1. AI に「タスク指示書 (Brief)」を渡せるようにした

これまでの llive は「ぽつん」と一言投げると一言返してくる感じだったのを、

```yaml
brief_id: portal-refresh-2026-05-17
goal: |
  ホームページのトップ画像を新製品に差し替えてほしい。
constraints:
  - 既存のリンクを壊さない
  - 画像サイズは 1MB 以内
success_criteria:
  - 画像が表示される
  - リンクテストが全部通る
approval_required: true   # 危ない作業は人間の承認を必須に
```

のような「**構造化された依頼書**」で渡せるようにしました。会社で言うところの**業務指示書のテンプレ**みたいなものです。

これにより:
- AI が「何をやればいいか」を最初から正確に把握できる
- 「やってはいけないこと」を最初に伝えられる
- 「完了条件」が明確なので、AI が勝手な解釈をしにくい
- 全部の作業記録が後から見返せる (議事録のように)

### 2. AI の「思考の癖」を 10 個に整理した

YouTube チャンネル「心理の深層」を見ていて、面白いことに気付きました。**人間の思考って 10 種類の癖の組み合わせ** で成り立っているらしいんです:

1. 構造化 — 問題を分解する
2. 再構成 — アイデアを組み替える
3. 閉ループ — 確認しながら進める
4. 自己拡張 — 道具や記憶を使う
5. 不確実性 — 「分からない」を持ちこたえる
6. 探索 — 試しにやってみる
7. 整合 — 全体の辻褄を合わせる
8. 来歴 — 経緯を覚えておく
9. 多視点 — 別の角度から見直す
10. 現実接続 — 実際の物に当てはめる

これを llive に組み込むと:
- 5 つはもう実装済み
- 3 つは既存の機能で対応済み
- 1 つは今日新しく作った
- 1 つだけが「これから」

つまり llive は **「人間の思考の癖を AI に持たせる」研究** とも言えます。

### 3. AI に「計算をさせない」仕組みを入れた

ChatGPT に「2.5 × 7.8 ÷ 0.3 はいくつ?」と聞くと、それっぽい数字を返してきますが、**結構な確率で間違えます**。AI は言葉が得意だけど、計算は得意じゃないんです。

そこで、llive は **AI に計算させない設計** にしました。AI が「ここで計算が必要だ」と判断したら、**電卓に渡す感じで決定論的に正確な答えを取得し、それを AI に「事実」として与える**。

例えば:
- AI: 「速度 5 m/s で 3 秒移動したら何メートルですか?」
- llive (内蔵): 「距離 = 速度 × 時間 = 5 × 3 = 15 m」 (数式エンジンで計算)
- AI: 「15 m です。これは…」 (llive の計算結果を引用するだけ)

さらに **「単位の次元チェック」** も入れたので、AI が「5 m/s + 3 s = 8」みたいな**単位が合わない式**を出したら必ずエラーを返して止めるようになっています (5 m/s と 3 s は足せない量です。中学物理の話)。

### 4. ベンチマークの「変な勝ち方」を自分で見破った

AI 同士の性能比較 (ベンチマーク) を取ってみたら、最初の結果で **llive が他の AI より圧倒的に速い** という数字が出ました。

| AI | 応答時間 |
|---|---|
| llive | 約 0.15 秒 |
| クラウド AI (Perplexity) | 約 4 秒 |
| ローカル AI (ollama) | 約 18 秒 |

「やった、圧勝!」と言いたいところですが、ユーザーから「**変に高速ですね、何かおかしくないですか?**」と指摘を受けて、よく調べたら:

- llive 側は **AI を実は呼んでいなかった** (テンプレートで応答していた)
- 速度を測っている部分が **AI の処理時間ではなく、プログラム起動時間** だった
- 比較対象 (chars 数) も **AI の返答ではなく JSON 全体の長さ** で測っていた

つまり「**勝った気になっていただけ**」でした。

そこで設計を直して、ちゃんと AI を呼ぶようにして再測定したら:

| AI | 応答時間 |
|---|---|
| llive (AI 内蔵) | 約 40 秒 |
| ローカル AI 直叩き | 約 15 秒 |

**llive のほうが 2-4 倍遅い**。理由は llive が AI に渡すプロンプトを丁寧に組み立てるので、AI の処理時間自体が長くなるからでした。

これを「**llive の付加価値は速度ではなく構造 (記憶・監査・段取り)**」と書いて公開しました。**「失敗した数字を消す」ではなく「失敗を honest に出す」** のが研究では大事です。

### 5. AI 用クイズで「平均値・分散値」を測った

10 問のクイズ (算数 / 論理 / 知識 / 推論 / 創造性) を AI に解かせて、平均正答率と速度のばらつきを統計的に測りました:

| モード | 正答率 (10 問中) | 平均応答時間 |
|---|---|---|
| Debug モード (詳しい記録あり) | 6 問 | 22.3 秒 |
| Release モード (記録最小限) | 7 問 | 22.8 秒 |

観察:
- **詳しい記録を残す Debug モードでも、応答時間はほぼ変わらない** (+1.8%) → 開発中ずっと記録を取っても性能は落ちない
- 正答率の差 (6 問 vs 7 問) は **サンプル数 10 では誤差の範囲** (1 問の差は確率的揺らぎ)

「次は 30 問以上で、複数の AI モデルで、ちゃんと比較しよう」 と決めました。

## なぜこれが大事か — 業界・社会への意義

### 自宅 PC で完結する AI = プライバシー革命

llive はネット接続なしで完全に自宅 PC 内で動作します。これは:

- **家族の会話の文字起こし** をクラウドに送らずに要約できる
- **医療情報・診療記録** を病院内に閉じたまま AI 分析できる
- **企業の機密文書** を社外に出さずに整理できる
- **災害時にネットが切れても** AI が引き続き使える
- **電気代だけで AI が動く** (クラウド月額不要)

### AI の責任所在を明確に

llive は AI のすべての判断を**台帳 (ledger) に記録**します。後から「いつ、誰が、何を、なぜ承認したか」が全部分かるので:

- **医療現場**: AI が出した薬剤提案を医師がなぜ承認/却下したかが記録に残る
- **法律事務所**: AI が起案した文書のどの部分が AI 由来か追跡可能
- **金融機関**: AI が出した投資判断の全プロセスを監督官庁に提出可能
- **教育現場**: AI が出した解答の引用元を全部辿れる

これは ChatGPT / Claude / Gemini の単独使用では**絶対にできない領域**です。

### 計算と単位を間違えない AI

特に **製造業 / 計測 / 物理 / 工学 / 医療** の現場では、AI が「5 m/s + 3 s = 8」のような単位を間違えた式を返してくると致命的です。llive はこれを**自動で止める**ので、安心して業務 AI として使えます。

### 「AI に置き換えられる」ではなく「AI と一緒に働く」

llive の TUI 画面 (llove) では、AI が「これでいいですか?」と聞いてきて、人間が承認/却下/修正できます。**完全自動ではなく、人間が判断ループに必ず入る**。

これは AI 失業の不安を減らす設計でもあります。

## これからの展望

### 短期 (~3 ヶ月) — 今日の続き

- 数学と単位の計算エンジンを完成
- AI 思考プロセス (KJ法 / マインドマップ / 矛盾解決) の自動化
- AI の出力を Z3 という形式検証ツールで検算

### 中期 (~1 年) — llive 専用の小型 AI を作る

- 大手 AI (Qwen 14B など) から「llive 専用に圧縮した小型 AI」を蒸留
- 自宅 PC でもサクサク動く軽量版を目指す

### 長期 (~3 年) — 全く新しい AI 構造へ

- Transformer (今の AI の基本構造) に頼らない、llive 専用のアーキテクチャ
- 「AI が記憶を直接参照する」「人間の承認を必須にする」が AI 自体に組み込まれた設計

## 「AI を使うなら Qwen で十分」と言われない設計

ユーザーから鋭い指摘も受けました:

> 「差別化されていないと研究の価値がない。普及している AI を使った方がマシってなりそう」

その通りです。**llive 単独では Qwen に勝てません** (生成品質は Qwen そのもの)。

でも、こう考えるとどうでしょう:

> 「Qwen を **自宅 PC で安全に責任を持って使う** なら llive が最短経路」

これは Qwen / Llama / Mistral が進化しても **変わらない価値** です。なぜなら:
- 記憶を保ち続けるのは llive
- 計算を間違えないのは llive
- 危ない発言を止めるのは llive
- 議事録を残すのは llive
- Local 環境で動かすのは llive

「**AI 本体 (Qwen) と AI を使いこなす秘書 (llive) は別物で、両方必要**」というポジションです。

## おわりに — 1 日の振り返り

今日 1 日で、

- 32 件の要件追加
- 約 2200 行のプログラム実装
- 78 件のテスト追加 (全 1014 件 OK、不具合ゼロ)
- 4 種類のベンチマーク実施
- 11 本の技術記事 + 本記事 1 本の公開

を達成しました。1 日でこれだけ進められるのは、**AI と一緒に開発しているから** です (実装中の私の相棒は Claude Opus 4.7 という AI で、コードを書いてもらいながら、設計や戦略は私が判断しています)。

llive はまだ研究開発段階 (v0.6 = 開発中バージョン) ですが、**プログラマー以外の方** でも、いずれは自宅 PC で安心して AI を使える未来を目指しています。

質問・感想・「こういう使い方ができたら嬉しい」というご要望は GitHub Issues や Twitter / X (@puruyan) までお気軽にお願いします。

---

> 本記事は技術者向けの詳細版 (同日 11 本 + Qiita 統合版 1 本) と並走する**一般読者向けバージョン**。専門用語を可能な限り平易な比喩に置き換えました。「自宅 PC で動く、おせっかいで、責任感のある AI 秘書」を作る研究、というのが llive のいちばん簡単な説明です。

### 関連リンク

- llive GitHub: <https://github.com/furuse-kazufumi/llive>
- FullSense umbrella (4 製品): <https://github.com/furuse-kazufumi/fullsense>
- 技術者向け詳細記事 (11 本): [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17)
- 技術者向け Qiita 統合版: [QIITA_SUMMARY.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/QIITA_SUMMARY.md)

---

# English

![Giving AI a Secretary — llive Dev Diary, 4 Panels](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/general_4koma_en.svg)
# From "Just Using AI" to "Giving AI a Secretary" — Dev Diary of llive, the Caring AI Framework That Runs on Your Home PC

Author: **Kazufumi Furuse (puruyan)**

## Introduction — "Letting AI Handle It" Is Actually Scary

Lately, handy AIs like ChatGPT, Claude, and Gemini have been appearing one after another. We use them to write work documents, write code, get hints for our kids' homework, and do a bit of research.

But have you ever thought any of the following?

- "Is it really OK to throw my company's confidential information at an AI?"
- "Is it fine to send a transcript of my family conversation to Google?"
- "If I have an AI analyze medical records, where does the personal information go?"
- "I'm worried about the electricity bill too. How much per month does it cost to run in the cloud?"
- "If my internet connection drops, can I do nothing at all?"
- "If the AI says something wrong, who takes responsibility?"

In fact, there still aren't many AI tools out there that properly answer these concerns. **Convenient AI is basically cloud-dependent**, and your data gets sent to some big company's servers to be processed.

The research-and-development framework I'm currently building, called **llive**, tackles this problem head-on. In a single sentence:

> **Research to build not "the AI itself," but "a secretary that makes good use of the AI"**

Today (May 17, 2026), in a single day, I made quite a bit of progress: 32 requirements added + about 2,200 lines of program + 78 tests added + 4 kinds of benchmarks run + 11 articles published. So I've organized the content **in a way that even non-engineers can understand**.

## If I Were to Compare llive to Something — It's Like "Giving AI a Secretary"

Picture AI as "a new employee who is talented but forgetful, bad at arithmetic, sometimes lies, and has a weak sense of responsibility."

```
[Conventional]       [What llive is trying to do]
The boss (=human)  →  The boss (=human) hands the
asks the new          new employee a work order
employee (AI) for     (=Brief), and the secretary
work directly         (=llive) handles the following:
                      - Records past exchanges (memory)
                      - Stops dangerous statements (audit)
                      - Makes it use a calculator (augmentation)
                      - Manages the workflow (thinking process)
                      - Keeps a record of accountability (ledger)
```

In other words, llive is not about "**rebuilding the AI itself**," but rather "**a mechanism that wraps around the AI, makes up for its weak points, and stops its dangerous parts**."

The AI engine running inside can be chosen from Qwen (Alibaba's OSS LLM) or Llama (Meta's OSS LLM). These are released for free by major companies and can even run on a home PC.

## What I Did Today, Narrowed Down to 5 Things

### 1. Made It Possible to Hand the AI a "Task Brief"

Whereas the previous llive would give you a one-line reply when you tossed it a one-line prompt, now you can hand it a request like this:

```yaml
brief_id: portal-refresh-2026-05-17
goal: |
  ホームページのトップ画像を新製品に差し替えてほしい。
constraints:
  - 既存のリンクを壊さない
  - 画像サイズは 1MB 以内
success_criteria:
  - 画像が表示される
  - リンクテストが全部通る
approval_required: true   # 危ない作業は人間の承認を必須に
```

— a "**structured request form**." It's like a **work order template** in a company setting.

With this:
- The AI can grasp accurately, from the very start, "what it needs to do"
- You can communicate "what must not be done" up front
- Because the "completion criteria" are clear, the AI is less likely to make arbitrary interpretations
- All work records can be reviewed later (like meeting minutes)

### 2. Organized AI's "Thinking Habits" into 10 Types

While watching the YouTube channel "Shinri no Shinso" (The Depths of Psychology), I noticed something interesting. It seems that **human thinking is made up of combinations of 10 kinds of habits**:

1. Structuring — breaking down a problem
2. Restructuring — rearranging ideas
3. Closed loop — proceeding while verifying
4. Self-extension — using tools and memory
5. Uncertainty — enduring "I don't know"
6. Exploration — trying things out
7. Coherence — making the whole consistent
8. Provenance — remembering the history
9. Multiple perspectives — reviewing from another angle
10. Reality grounding — applying it to actual objects

When you build these into llive:
- 5 are already implemented
- 3 are covered by existing features
- 1 was newly built today
- Only 1 is "still to come"

In other words, llive can also be described as **research to give AI human thinking habits**.

### 3. Added a Mechanism to "Not Let the AI Do Arithmetic"

If you ask ChatGPT "What is 2.5 × 7.8 ÷ 0.3?", it returns a plausible-looking number, but **it gets it wrong fairly often**. AI is good with words, but not so good at arithmetic.

So I designed llive **not to let the AI do arithmetic**. When the AI judges that "a calculation is needed here," it **hands it off like to a calculator, obtains a deterministically accurate answer, and gives that to the AI as a "fact."**

For example:
- AI: "If you move at a speed of 5 m/s for 3 seconds, how many meters is that?"
- llive (built-in): "Distance = speed × time = 5 × 3 = 15 m" (computed by the math engine)
- AI: "It's 15 m. This is…" (just cites llive's calculation result)

Furthermore, I also added a **"dimensional check of units,"** so if the AI produces an expression where **the units don't match**, like "5 m/s + 3 s = 8," it will always return an error and stop (5 m/s and 3 s are quantities that cannot be added — that's middle-school physics).

### 4. Caught Myself with a "Weird Way of Winning" in a Benchmark

When I ran a performance comparison (benchmark) between AIs, the first result showed numbers where **llive was overwhelmingly faster than other AIs**.

| AI | Response time |
|---|---|
| llive | about 0.15 s |
| Cloud AI (Perplexity) | about 4 s |
| Local AI (ollama) | about 18 s |

I wanted to shout "Yes, a landslide victory!", but a user pointed out, "**It's suspiciously fast — isn't something off?**" When I investigated carefully, it turned out:

- The llive side **wasn't actually calling the AI** (it was responding with a template)
- The part measuring speed was **not the AI's processing time, but the program's startup time**
- The comparison metric (number of chars) was also measured as **the length of the entire JSON, not the AI's reply**

In other words, I had just been "**fooling myself into thinking I'd won**."

So I fixed the design to properly call the AI and re-measured:

| AI | Response time |
|---|---|
| llive (with built-in AI) | about 40 s |
| Local AI called directly | about 15 s |

**llive is 2–4 times slower.** The reason is that because llive carefully assembles the prompt it hands to the AI, the AI's processing time itself becomes longer.

I wrote and published this as "**llive's added value is not speed, but structure (memory, audit, workflow)**." In research, what matters is "**honestly publishing the failure**," not "**erasing the failed numbers**."

### 5. Measured "Mean and Variance" with an AI Quiz

I had the AI solve a 10-question quiz (arithmetic / logic / knowledge / reasoning / creativity) and statistically measured the average correct-answer rate and the variability of speed:

| Mode | Correct answers (out of 10) | Average response time |
|---|---|---|
| Debug mode (with detailed records) | 6 | 22.3 s |
| Release mode (minimal records) | 7 | 22.8 s |

Observations:
- **Even in Debug mode, which keeps detailed records, the response time barely changes** (+1.8%) → keeping records throughout development doesn't degrade performance
- The difference in correct-answer rate (6 vs 7) is **within the margin of error at a sample size of 10** (a 1-question difference is probabilistic fluctuation)

I decided, "Next time, let's do 30+ questions and compare properly across multiple AI models."

## Why This Matters — Significance for the Industry and Society

### AI Completed on a Home PC = a Privacy Revolution

llive operates entirely within your home PC, with no internet connection. This means:

- **Transcripts of family conversations** can be summarized without sending them to the cloud
- **Medical information and clinical records** can be analyzed by AI while staying within the hospital
- **A company's confidential documents** can be organized without leaving the company
- **Even if the internet goes down during a disaster,** the AI can continue to be used
- **The AI runs on just the electricity bill** (no monthly cloud subscription required)

### Making AI Accountability Clear

llive records every judgment the AI makes in a **ledger**. Since you can later know fully "when, who, what, and why it was approved," then:

- **Medical settings**: a record remains of why a doctor approved/rejected a drug suggestion made by the AI
- **Law firms**: it's possible to trace which parts of a document drafted by the AI came from the AI
- **Financial institutions**: the entire process of an investment decision made by the AI can be submitted to supervisory authorities
- **Educational settings**: you can fully trace the citation sources of an answer produced by the AI

These are domains that are **absolutely impossible** with standalone use of ChatGPT / Claude / Gemini.

### AI That Doesn't Get Arithmetic and Units Wrong

Especially in **manufacturing / metrology / physics / engineering / medical** settings, it's fatal if the AI returns an expression with mistaken units, like "5 m/s + 3 s = 8." Since llive **stops this automatically**, you can use it as a business AI with peace of mind.

### Not "Being Replaced by AI," but "Working Together with AI"

On llive's TUI screen (llove), the AI asks "Is this OK?", and the human can approve / reject / revise. **It's not fully automated — the human is always part of the decision loop.**

This is also a design that reduces the anxiety of AI-driven unemployment.

## The Road Ahead

### Short term (~3 months) — A continuation of today

- Complete the math and unit calculation engine
- Automate AI thinking processes (KJ method / mind maps / contradiction resolution)
- Verify the AI's output with a formal verification tool called Z3

### Mid term (~1 year) — Build a small AI dedicated to llive

- Distill a "small AI compressed for llive's exclusive use" from a major AI (such as Qwen 14B)
- Aim for a lightweight version that runs smoothly even on a home PC

### Long term (~3 years) — Toward an entirely new AI structure

- An architecture dedicated to llive that doesn't rely on Transformers (the basic structure of today's AI)
- A design where "the AI references memory directly" and "human approval is mandatory" are built into the AI itself

## A Design That Won't Be Told "If You're Going to Use AI, Qwen Is Enough"

I also received a sharp comment from a user:

> "If it's not differentiated, the research has no value. It seems like it'd be better to just use a widely adopted AI."

That's right. **llive alone can't beat Qwen** (the generation quality is Qwen itself).

But how about thinking of it this way:

> "If you want to **use Qwen safely and responsibly on your home PC**, llive is the shortest path."

This is value that **won't change** even as Qwen / Llama / Mistral evolve. Because:
- It's llive that keeps memory persistent
- It's llive that doesn't get calculations wrong
- It's llive that stops dangerous statements
- It's llive that keeps the minutes
- It's llive that runs it in a Local environment

The position is: "**The AI itself (Qwen) and the secretary that makes good use of the AI (llive) are different things, and you need both.**"

## In Closing — Looking Back on the Day

In a single day today, I achieved:

- 32 requirements added
- About 2,200 lines of program implemented
- 78 tests added (all 1,014 OK, zero defects)
- 4 kinds of benchmarks run
- 11 technical articles + this 1 article published

The reason I can make this much progress in a single day is **because I'm developing together with AI** (my partner during implementation is an AI called Claude Opus 4.7; while it writes the code, I make the judgments on design and strategy).

llive is still in the research-and-development stage (v0.6 = a version under development), but I'm aiming for a future where **even non-programmers** can someday use AI with peace of mind on their home PC.

Questions, impressions, and requests like "I'd be happy if I could use it this way" are welcome anytime via GitHub Issues or Twitter / X (@puruyan).

---

> This article is the **version for general readers**, running in parallel with the detailed version for engineers (11 articles the same day + 1 integrated Qiita edition). I replaced technical jargon with plain analogies as much as possible. The simplest explanation of llive is: research to build "a caring, responsible AI secretary that runs on your home PC."

### Related Links

- llive GitHub: <https://github.com/furuse-kazufumi/llive>
- FullSense umbrella (4 products): <https://github.com/furuse-kazufumi/fullsense>
- Detailed articles for engineers (11): [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17)
- Integrated Qiita edition for engineers: [QIITA_SUMMARY.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/QIITA_SUMMARY.md)

---

# 中文

![给 AI 配一个秘书 — llive 开发日记 四格](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/general_4koma_zh.svg)
# 从"只是使用 AI"到"给 AI 配一个秘书"——在家用 PC 上运行的爱管闲事的 AI 框架 llive 开发日记

作者：**古濑和文（puruyan）**

## 前言——"交给 AI 处理"其实很可怕

最近，ChatGPT、Claude、Gemini 等好用的 AI 接连出现。我们用它们来写工作文档、写代码、给孩子的作业找思路、做点小调查。

但你是否曾经这样想过呢？

- "把公司的机密信息抛给 AI，真的没问题吗？"
- "把家人对话的文字记录发给 Google，没关系吗？"
- "让 AI 分析医疗记录，个人信息会跑到哪里去？"
- "电费也让人在意。在云端运行一个月要多少钱？"
- "如果网断了，是不是就什么都做不了？"
- "如果 AI 说错了话，谁来负责？"

事实上，能够妥善回答这些顾虑的 AI 工具，目前世上还不太多。**好用的 AI 基本上都依赖云端**，数据会被发送到某个大公司的服务器上去处理。

我现在正在开发的、名为 **llive** 的研究开发框架，正面应对这个问题。用一句话来说就是：

> **不是打造"AI 本体"，而是打造"善用 AI 的秘书"的研究**

今天（2026 年 5 月 17 日）一天之内，我推进了相当可观的工作量：新增需求 32 项 + 程序约 2200 行 + 新增测试 78 项 + 实施 4 种基准测试 + 公开文章 11 篇。因此我把内容整理成了**连非工程师也能看懂**的形式。

## 要打个比方的话——llive 就像"给 AI 配一个秘书"

请把 AI 想象成"一个很优秀，但健忘、不擅长算术、还会说谎、责任感淡薄的新员工"。

```
[传统方式]            [llive 想要做的事]
上司（=人类）   →    上司（=人类）给新员工
直接向新员工        递交一份指示书（=Brief），
（AI）委派工作      由秘书（=llive）负责以下事项：
                    - 记录过去的往来（记忆）
                    - 制止危险的发言（审计）
                    - 让它用计算器算（补足）
                    - 管理工作流程（思考过程）
                    - 留存责任归属（台账）
```

也就是说，llive 不是要"**改造 AI 本体**"，而是"**套在 AI 外面，弥补它不擅长的部分、制止它危险的部分的一套机制**"。

在里面运行的 AI 本体，可以从 Qwen（阿里巴巴的 OSS LLM）或 Llama（Meta 的 OSS LLM）中选择。这些都是大企业免费公开的，在家用 PC 上也能运行。

## 今天做的事，精简为 5 件

### 1. 让 AI 可以接收"任务指示书（Brief）"

以前的 llive 是你"啪"地扔一句话，它就回你一句话的感觉；现在改成了可以用下面这样的形式来递交请求：

```yaml
brief_id: portal-refresh-2026-05-17
goal: |
  ホームページのトップ画像を新製品に差し替えてほしい。
constraints:
  - 既存のリンクを壊さない
  - 画像サイズは 1MB 以内
success_criteria:
  - 画像が表示される
  - リンクテストが全部通る
approval_required: true   # 危ない作業は人間の承認を必須に
```

——一份"**结构化的请求书**"。这就像公司里所说的**业务指示书模板**。

由此带来：
- AI 从一开始就能准确把握"该做什么"
- 可以一开始就告诉它"不能做什么"
- 由于"完成条件"明确，AI 不容易擅自做出解释
- 所有的工作记录事后都能回看（就像会议记录一样）

### 2. 把 AI 的"思维习惯"整理成 10 种

在看 YouTube 频道"心理的深层"时，我注意到一件有趣的事。**人类的思维似乎是由 10 种习惯的组合**构成的：

1. 结构化——分解问题
2. 重构——重新组合想法
3. 闭环——一边确认一边推进
4. 自我扩展——使用工具和记忆
5. 不确定性——撑住"不知道"的状态
6. 探索——试着做做看
7. 整合——让整体说得通
8. 来历——记住经过
9. 多视角——从别的角度重新审视
10. 现实连接——套用到实际的事物上

把这些嵌入 llive 后：
- 有 5 项已经实现
- 有 3 项靠现有功能已经覆盖
- 有 1 项是今天新做的
- 只有 1 项是"接下来要做的"

也就是说，llive 也可以说是**"让 AI 拥有人类思维习惯"的研究**。

### 3. 加入了"不让 AI 做算术"的机制

如果你问 ChatGPT"2.5 × 7.8 ÷ 0.3 是多少？"，它会返回一个看起来像那么回事的数字，但**相当大概率会算错**。AI 擅长语言，却不擅长算术。

因此，我把 llive 设计成**不让 AI 做算术**。当 AI 判断"这里需要计算"时，**就像交给计算器一样，取得一个确定性的、准确的答案，再把它作为"事实"提供给 AI**。

例如：
- AI："以 5 m/s 的速度移动 3 秒，是多少米？"
- llive（内置）："距离 = 速度 × 时间 = 5 × 3 = 15 m"（用数式引擎计算）
- AI："是 15 m。这……"（只是引用 llive 的计算结果）

此外，我还加入了**"单位的量纲检查"**，所以如果 AI 给出像"5 m/s + 3 s = 8"这种**单位对不上的式子**，它一定会返回错误并停止（5 m/s 和 3 s 是无法相加的量。这是初中物理的内容）。

### 4. 自己识破了基准测试里"奇怪的获胜方式"

我尝试测了一下 AI 之间的性能比较（基准测试），最初的结果显示出**llive 比其他 AI 压倒性地快**的数字。

| AI | 响应时间 |
|---|---|
| llive | 约 0.15 秒 |
| 云端 AI（Perplexity） | 约 4 秒 |
| 本地 AI（ollama） | 约 18 秒 |

本想喊一句"成了，完胜！"，但收到用户的指出"**快得有点奇怪吧，是不是哪里不对劲？**"，仔细一查发现：

- llive 这边**其实根本没有调用 AI**（是用模板在回应）
- 测量速度的那部分，**测的不是 AI 的处理时间，而是程序的启动时间**
- 比较对象（字符数）也是按**整个 JSON 的长度，而非 AI 的回复**来测的

也就是说，只是"**自以为赢了而已**"。

于是我修正了设计，让它好好调用 AI 后重新测量：

| AI | 响应时间 |
|---|---|
| llive（内置 AI） | 约 40 秒 |
| 直接调用本地 AI | 约 15 秒 |

**llive 反而慢了 2-4 倍。**原因在于，llive 会精心组装递交给 AI 的提示词，所以 AI 的处理时间本身就变长了。

我把这点写成"**llive 的附加价值不在速度，而在结构（记忆、审计、流程）**"并公开了。在研究中，重要的是"**诚实地把失败摆出来**"，而不是"**抹掉失败的数字**"。

### 5. 用面向 AI 的测验测了"平均值、方差值"

我让 AI 解了一套 10 道题的测验（算术 / 逻辑 / 知识 / 推理 / 创造性），并统计性地测量了平均正确率和速度的离散程度：

| 模式 | 正确率（10 题中） | 平均响应时间 |
|---|---|---|
| Debug 模式（有详细记录） | 6 题 | 22.3 秒 |
| Release 模式（记录最少） | 7 题 | 22.8 秒 |

观察：
- **即使是留存详细记录的 Debug 模式，响应时间也几乎不变**（+1.8%）→ 在开发期间一直做记录，性能也不会下降
- 正确率的差异（6 题 vs 7 题）在**样本数为 10 时属于误差范围内**（1 题的差异是概率性的波动）

我决定："下次用 30 题以上、用多个 AI 模型，好好地做比较。"

## 为什么这很重要——对行业与社会的意义

### 在家用 PC 上完成的 AI = 隐私革命

llive 无需联网，完全在家用 PC 内运行。这意味着：

- 可以不把**家人对话的文字记录**发到云端就完成摘要
- 可以让 AI 在**医疗信息、诊疗记录**封闭于医院内的状态下进行分析
- 可以在不把**企业的机密文档**带出公司外的情况下进行整理
- **即使灾害时网络中断**，AI 也能继续使用
- **AI 仅靠电费就能运行**（无需云端月费）

### 明确 AI 的责任归属

llive 会把 AI 的所有判断**记录在台账（ledger）里**。事后能完整知道"何时、是谁、做了什么、为何批准"，因此：

- **医疗现场**：医生为何批准/驳回 AI 给出的药物建议，会留有记录
- **律师事务所**：AI 起草的文档里哪些部分源自 AI，可以追溯
- **金融机构**：AI 给出的投资判断的全过程，可以提交给监管机关
- **教育现场**：AI 给出的答案的引用来源，可以全部追溯

这些是单独使用 ChatGPT / Claude / Gemini **绝对做不到的领域**。

### 不会把计算和单位弄错的 AI

尤其在**制造业 / 计量 / 物理 / 工程 / 医疗**的现场，AI 返回像"5 m/s + 3 s = 8"这种弄错了单位的式子，会是致命的。由于 llive **会自动制止这种情况**，所以可以放心地把它当作业务 AI 来使用。

### 不是"被 AI 取代"，而是"和 AI 一起工作"

在 llive 的 TUI 画面（llove）上，AI 会来问"这样可以吗？"，人类可以批准/驳回/修改。**它不是全自动的——人类必定处于判断回路之中。**

这也是一种能减轻 AI 引发失业焦虑的设计。

## 今后的展望

### 短期（~3 个月）——今天的延续

- 完成数学与单位的计算引擎
- 自动化 AI 思考过程（KJ 法 / 思维导图 / 矛盾解决）
- 用名为 Z3 的形式化验证工具对 AI 的输出进行验算

### 中期（~1 年）——打造 llive 专用的小型 AI

- 从大型 AI（如 Qwen 14B）蒸馏出"为 llive 专用而压缩的小型 AI"
- 力求做出在家用 PC 上也能流畅运行的轻量版

### 长期（~3 年）——迈向全新的 AI 结构

- 不依赖 Transformer（当今 AI 的基本结构）、为 llive 专用的架构
- 一种把"AI 直接引用记忆""必须经过人类批准"内建进 AI 本身的设计

## 一种不会被说"要用 AI 的话 Qwen 就够了"的设计

我也收到了用户尖锐的指出：

> "如果没有差异化，研究就没有价值。感觉还不如用普及了的 AI 来得划算。"

确实如此。**llive 单独是赢不了 Qwen 的**（生成质量就是 Qwen 本身）。

但是，这样想想如何呢：

> "如果要**在家用 PC 上安全、负责任地使用 Qwen**，llive 是最短路径。"

这是即便 Qwen / Llama / Mistral 进化了也**不会改变的价值**。因为：
- 持续保有记忆的是 llive
- 不把计算弄错的是 llive
- 制止危险发言的是 llive
- 留存会议记录的是 llive
- 在 Local 环境中运行的是 llive

其定位是："**AI 本体（Qwen）和善用 AI 的秘书（llive）是两回事，两者都需要。**"

## 结语——一天的回顾

今天一天之内，我达成了：

- 新增 32 项需求
- 实现约 2200 行程序
- 新增 78 项测试（全部 1014 项 OK，零缺陷）
- 实施 4 种基准测试
- 公开 11 篇技术文章 + 本文 1 篇

之所以一天能推进这么多，是**因为我是和 AI 一起开发的**（实现过程中我的搭档是一个叫 Claude Opus 4.7 的 AI，让它来写代码，而设计和战略由我来判断）。

llive 还处于研究开发阶段（v0.6 = 开发中的版本），但我所追求的，是一个**连非程序员**也终有一天能在家用 PC 上安心使用 AI 的未来。

如有疑问、感想，或是"要是能这样用就好了"之类的需求，欢迎随时通过 GitHub Issues 或 Twitter / X（@puruyan）联系我。

---

> 本文是与面向工程师的详细版（同日 11 篇 + Qiita 统合版 1 篇）并行推进的**面向一般读者的版本**。我尽可能把专业术语替换成了平易的比喻。llive 最简单的解释就是：打造"在家用 PC 上运行的、爱管闲事的、有责任感的 AI 秘书"的研究。

### 相关链接

- llive GitHub: <https://github.com/furuse-kazufumi/llive>
- FullSense umbrella（4 个产品）: <https://github.com/furuse-kazufumi/fullsense>
- 面向工程师的详细文章（11 篇）: [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17)
- 面向工程师的 Qiita 统合版: [QIITA_SUMMARY.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/QIITA_SUMMARY.md)

---

# 한국어

![AI에게 비서를 붙이다 — llive 개발 일기 4컷](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/general_4koma_ko.svg)
# 'AI를 그냥 쓰기'에서 'AI에게 비서를 붙이기'로 — 가정용 PC에서 돌아가는 참견쟁이 AI 프레임워크 llive 개발 일기

저자: **후루세 가즈후미(puruyan)**

## 들어가며 — "AI에게 맡긴다"는 건 사실 무섭다

요즘 ChatGPT, Claude, Gemini 등 편리한 AI가 잇따라 등장하고 있습니다. 업무 문서를 쓰게 하거나, 코드를 작성하게 하거나, 아이의 숙제 힌트를 묻거나, 간단한 조사에 쓰거나 합니다.

그런데 이렇게 생각해 본 적은 없으신가요?

- "회사 기밀 정보를 AI에 던져도 괜찮을까?"
- "가족과의 대화 녹취록을 Google에 보내도 괜찮을까?"
- "의료 기록을 AI에게 분석시키면 개인정보는 어디로 가는 걸까?"
- "전기 요금도 신경 쓰인다. 클라우드에서 돌리면 한 달에 얼마지?"
- "인터넷이 끊기면 아무것도 못 하게 되나?"
- "AI가 틀린 말을 해도 누가 책임을 지지?"

사실 이런 우려에 제대로 답해 주는 AI 도구는 아직 세상에 그리 많지 않습니다. **편리한 AI는 기본적으로 클라우드에 의존**하고 있어서, 데이터는 어딘가의 거대한 회사 서버로 보내져 처리됩니다.

제가 지금 만들고 있는 **llive(리브)**라는 연구개발 프레임워크는 이 문제에 정면으로 맞서고 있습니다. 한마디로 말하면:

> **"AI 본체"가 아니라, "AI를 능숙하게 다루는 비서"를 만드는 연구**

오늘(2026년 5월 17일) 하루에, 요건 32건 추가 + 프로그램 약 2200줄 + 테스트 78건 추가 + 벤치마크 4종 실시 + 기사 11편 공개라는 꽤 많은 분량을 진행했기에, 그 내용을 **비엔지니어 분들도 이해할 수 있도록** 정리했습니다.

## llive를 비유하자면 — "AI에게 비서를 붙이는" 느낌

AI를 "유능하지만 잘 잊고, 계산이 서툴고, 거짓말도 하며, 책임감이 옅은 신입 사원"이라고 상상해 보세요.

```
[기존]                [llive가 하려는 것]
신입 사원(AI)에게  →  상사(=인간)는 신입 사원에게
직접 일을 의뢰       지시서(=Brief)를 건네고,
                     비서(=llive)가 다음을 담당:
                     - 과거 주고받은 내용을 기록 (기억)
                     - 위험한 발언을 멈춤 (감사)
                     - 계산은 계산기를 쓰게 함 (보완)
                     - 단계를 관리 (사고 프로세스)
                     - 책임 소재를 남김 (대장)
```

즉 llive는 "**AI 본체를 다시 만드는**" 것이 아니라, "**AI 주위에 씌워서, 서툰 부분을 보완하고, 위험한 부분을 멈추는 구조**"입니다.

안에서 돌리는 AI 본체는 Qwen(알리바바의 OSS LLM)이나 Llama(Meta의 OSS LLM)를 고를 수 있습니다. 이들은 대기업이 무료로 공개한 것으로, 가정용 PC에서도 돌릴 수 있습니다.

## 오늘 한 일, 5가지로 추려서

### 1. AI에게 "작업 지시서(Brief)"를 건넬 수 있게 했다

지금까지의 llive는 "툭" 하고 한마디 던지면 한마디 돌려주는 느낌이었던 것을, 다음과 같은 형태로 건넬 수 있게 했습니다:

```yaml
brief_id: portal-refresh-2026-05-17
goal: |
  ホームページのトップ画像を新製品に差し替えてほしい。
constraints:
  - 既存のリンクを壊さない
  - 画像サイズは 1MB 以内
success_criteria:
  - 画像が表示される
  - リンクテストが全部通る
approval_required: true   # 危ない作業は人間の承認を必須に
```

같은 "**구조화된 요청서**"입니다. 회사로 치면 **업무 지시서 템플릿** 같은 것입니다.

이로써:
- AI가 "무엇을 하면 되는지"를 처음부터 정확히 파악할 수 있다
- "해서는 안 되는 것"을 처음에 전달할 수 있다
- "완료 조건"이 명확하므로, AI가 멋대로 해석하기 어렵다
- 모든 작업 기록을 나중에 다시 볼 수 있다 (회의록처럼)

### 2. AI의 "사고 습관"을 10가지로 정리했다

유튜브 채널 "심리의 심층"을 보다가 재미있는 것을 알아챘습니다. **인간의 사고는 10가지 습관의 조합**으로 이루어져 있는 것 같습니다:

1. 구조화 — 문제를 분해한다
2. 재구성 — 아이디어를 재조합한다
3. 폐루프 — 확인하면서 진행한다
4. 자기 확장 — 도구와 기억을 사용한다
5. 불확실성 — "모르겠다"를 버텨낸다
6. 탐색 — 시험 삼아 해 본다
7. 정합 — 전체의 앞뒤를 맞춘다
8. 내력 — 경위를 기억해 둔다
9. 다시점 — 다른 각도에서 다시 본다
10. 현실 접속 — 실제 사물에 대입한다

이를 llive에 넣으면:
- 5가지는 이미 구현 완료
- 3가지는 기존 기능으로 대응 완료
- 1가지는 오늘 새로 만들었다
- 단 1가지만이 "앞으로"

즉 llive는 **"인간의 사고 습관을 AI에게 갖게 하는" 연구**라고도 할 수 있습니다.

### 3. AI에게 "계산을 시키지 않는" 구조를 넣었다

ChatGPT에게 "2.5 × 7.8 ÷ 0.3은 얼마야?"라고 물으면, 그럴싸한 숫자를 돌려주지만 **꽤 높은 확률로 틀립니다**. AI는 말은 잘하지만, 계산은 잘하지 못합니다.

그래서 llive는 **AI에게 계산을 시키지 않는 설계**로 했습니다. AI가 "여기서 계산이 필요하다"고 판단하면, **계산기에 넘기는 느낌으로 결정론적으로 정확한 답을 얻어, 그것을 AI에게 "사실"로서 줍니다**.

예를 들어:
- AI: "속도 5 m/s로 3초 이동하면 몇 미터인가요?"
- llive(내장): "거리 = 속도 × 시간 = 5 × 3 = 15 m" (수식 엔진으로 계산)
- AI: "15 m입니다. 이것은…" (llive의 계산 결과를 인용할 뿐)

게다가 **"단위의 차원 체크"**도 넣었기 때문에, AI가 "5 m/s + 3 s = 8"처럼 **단위가 맞지 않는 식**을 내놓으면 반드시 오류를 돌려주고 멈추도록 되어 있습니다 (5 m/s와 3 s는 더할 수 없는 양입니다. 중학교 물리 이야기입니다).

### 4. 벤치마크의 "이상한 승리 방식"을 스스로 간파했다

AI끼리의 성능 비교(벤치마크)를 측정해 봤더니, 첫 결과에서 **llive가 다른 AI보다 압도적으로 빠르다**는 수치가 나왔습니다.

| AI | 응답 시간 |
|---|---|
| llive | 약 0.15초 |
| 클라우드 AI (Perplexity) | 약 4초 |
| 로컬 AI (ollama) | 약 18초 |

"됐다, 압승!"이라고 말하고 싶었지만, 사용자로부터 "**이상하게 빠른데요, 뭔가 잘못된 거 아닌가요?**"라는 지적을 받고 잘 조사해 보니:

- llive 쪽은 **사실 AI를 부르지 않았다** (템플릿으로 응답하고 있었다)
- 속도를 재는 부분이 **AI의 처리 시간이 아니라, 프로그램 기동 시간**이었다
- 비교 대상(chars 수)도 **AI의 답변이 아니라 JSON 전체의 길이**로 재고 있었다

즉 "**이긴 줄로만 알고 있었던 것**"이었습니다.

그래서 설계를 고쳐서 제대로 AI를 부르도록 하고 다시 측정했더니:

| AI | 응답 시간 |
|---|---|
| llive (AI 내장) | 약 40초 |
| 로컬 AI 직접 호출 | 약 15초 |

**llive 쪽이 2~4배 느리다.** 이유는 llive가 AI에게 건네는 프롬프트를 정성껏 조립하기 때문에, AI의 처리 시간 자체가 길어지기 때문이었습니다.

이를 "**llive의 부가가치는 속도가 아니라 구조(기억·감사·단계)**"라고 써서 공개했습니다. 연구에서는 "**실패한 숫자를 지우는**" 것이 아니라 "**실패를 정직하게 내놓는**" 것이 중요합니다.

### 5. AI용 퀴즈로 "평균값·분산값"을 측정했다

10문제짜리 퀴즈(산수 / 논리 / 지식 / 추론 / 창의성)를 AI에게 풀게 해서, 평균 정답률과 속도의 편차를 통계적으로 측정했습니다:

| 모드 | 정답률 (10문제 중) | 평균 응답 시간 |
|---|---|---|
| Debug 모드 (상세 기록 있음) | 6문제 | 22.3초 |
| Release 모드 (기록 최소한) | 7문제 | 22.8초 |

관찰:
- **상세한 기록을 남기는 Debug 모드에서도, 응답 시간은 거의 변하지 않는다**(+1.8%) → 개발 중 내내 기록을 남겨도 성능은 떨어지지 않는다
- 정답률의 차이(6문제 vs 7문제)는 **샘플 수 10에서는 오차 범위 내**(1문제 차이는 확률적 흔들림)

"다음에는 30문제 이상으로, 여러 AI 모델로, 제대로 비교하자"고 정했습니다.

## 왜 이것이 중요한가 — 업계·사회에 대한 의의

### 가정용 PC에서 완결되는 AI = 프라이버시 혁명

llive는 인터넷 연결 없이 완전히 가정용 PC 안에서 동작합니다. 이것은:

- **가족 대화의 녹취록**을 클라우드에 보내지 않고 요약할 수 있다
- **의료 정보·진료 기록**을 병원 내에 닫아 둔 채로 AI 분석할 수 있다
- **기업의 기밀 문서**를 사외로 내보내지 않고 정리할 수 있다
- **재해 시에 인터넷이 끊겨도** AI를 계속 쓸 수 있다
- **전기 요금만으로 AI가 돌아간다** (클라우드 월정액 불필요)

### AI의 책임 소재를 명확하게

llive는 AI의 모든 판단을 **대장(ledger)에 기록**합니다. 나중에 "언제, 누가, 무엇을, 왜 승인했는가"를 전부 알 수 있으므로:

- **의료 현장**: AI가 내놓은 약제 제안을 의사가 왜 승인/반려했는지가 기록에 남는다
- **법률 사무소**: AI가 기안한 문서의 어느 부분이 AI에서 유래했는지 추적 가능
- **금융 기관**: AI가 내놓은 투자 판단의 전 과정을 감독 관청에 제출 가능
- **교육 현장**: AI가 내놓은 답안의 인용 출처를 전부 따라갈 수 있다

이것은 ChatGPT / Claude / Gemini의 단독 사용으로는 **절대 할 수 없는 영역**입니다.

### 계산과 단위를 틀리지 않는 AI

특히 **제조업 / 계측 / 물리 / 공학 / 의료** 현장에서는, AI가 "5 m/s + 3 s = 8" 같은 단위를 틀린 식을 돌려주면 치명적입니다. llive는 이것을 **자동으로 멈추므로**, 안심하고 업무 AI로 쓸 수 있습니다.

### "AI로 대체된다"가 아니라 "AI와 함께 일한다"

llive의 TUI 화면(llove)에서는, AI가 "이걸로 괜찮나요?"라고 물어 오고, 인간이 승인/반려/수정할 수 있습니다. **완전 자동이 아니라, 인간이 반드시 판단 루프에 들어갑니다.**

이것은 AI로 인한 실업 불안을 줄이는 설계이기도 합니다.

## 앞으로의 전망

### 단기(~3개월) — 오늘의 연속

- 수학과 단위 계산 엔진을 완성
- AI 사고 프로세스(KJ법 / 마인드맵 / 모순 해결)의 자동화
- AI의 출력을 Z3라는 형식 검증 도구로 검산

### 중기(~1년) — llive 전용 소형 AI를 만든다

- 대형 AI(Qwen 14B 등)에서 "llive 전용으로 압축한 소형 AI"를 증류
- 가정용 PC에서도 쾌적하게 돌아가는 경량판을 목표로

### 장기(~3년) — 전혀 새로운 AI 구조로

- Transformer(지금 AI의 기본 구조)에 의존하지 않는, llive 전용 아키텍처
- "AI가 기억을 직접 참조한다" "인간의 승인을 필수로 한다"가 AI 자체에 내장된 설계

## "AI를 쓸 거면 Qwen으로 충분하다"는 말을 듣지 않는 설계

사용자로부터 날카로운 지적도 받았습니다:

> "차별화되지 않으면 연구의 가치가 없다. 보급된 AI를 쓰는 편이 낫다는 식이 될 것 같다."

맞는 말입니다. **llive 단독으로는 Qwen을 이길 수 없습니다**(생성 품질은 Qwen 그 자체).

하지만, 이렇게 생각하면 어떨까요:

> "Qwen을 **가정용 PC에서 안전하게 책임지고 쓰려면** llive가 최단 경로"

이것은 Qwen / Llama / Mistral이 진화해도 **변하지 않는 가치**입니다. 왜냐하면:
- 기억을 계속 보유하는 것은 llive
- 계산을 틀리지 않는 것은 llive
- 위험한 발언을 멈추는 것은 llive
- 회의록을 남기는 것은 llive
- Local 환경에서 돌리는 것은 llive

"**AI 본체(Qwen)와 AI를 능숙하게 다루는 비서(llive)는 별개이며, 둘 다 필요하다**"는 포지션입니다.

## 마치며 — 하루의 회고

오늘 하루에,

- 32건의 요건 추가
- 약 2200줄의 프로그램 구현
- 78건의 테스트 추가 (전 1014건 OK, 결함 제로)
- 4종류의 벤치마크 실시
- 11편의 기술 기사 + 본 기사 1편 공개

를 달성했습니다. 하루에 이만큼 진행할 수 있는 것은 **AI와 함께 개발하고 있기 때문**입니다 (구현 중 저의 파트너는 Claude Opus 4.7이라는 AI로, 코드를 작성하게 하면서, 설계와 전략은 제가 판단하고 있습니다).

llive는 아직 연구개발 단계(v0.6 = 개발 중 버전)이지만, **프로그래머가 아닌 분**도 언젠가는 가정용 PC에서 안심하고 AI를 쓸 수 있는 미래를 목표로 하고 있습니다.

질문·감상·"이렇게 쓸 수 있으면 좋겠다"는 요청은 GitHub Issues나 Twitter / X(@puruyan)로 부담 없이 부탁드립니다.

---

> 본 기사는 엔지니어용 상세판(같은 날 11편 + Qiita 통합판 1편)과 병행하는 **일반 독자용 버전**입니다. 전문 용어를 가능한 한 쉬운 비유로 바꿨습니다. "가정용 PC에서 돌아가는, 참견쟁이이고, 책임감 있는 AI 비서"를 만드는 연구, 라는 것이 llive의 가장 간단한 설명입니다.

### 관련 링크

- llive GitHub: <https://github.com/furuse-kazufumi/llive>
- FullSense umbrella (4개 제품): <https://github.com/furuse-kazufumi/fullsense>
- 엔지니어용 상세 기사 (11편): [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17)
- 엔지니어용 Qiita 통합판: [QIITA_SUMMARY.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/QIITA_SUMMARY.md)
