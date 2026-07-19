# 用語集 — musculo/evis 決定版記事 翻訳リファレンス (ja / en / zh)

> `QIITA_musculo_evis_definitive_ja.md` の英語版・中国語版(feedback_articles_per_language_separate: 言語別に別記事)を作る際の
> **一貫した訳語**を固定するための coordination 用ファイル。翻訳エージェント/自分が全セクションで同じ訳語を使うために参照する。
> zh = 簡体字。専門用語は初出で「訳語(English)」を併記する方針(feedback_term_format_jp_en の多言語版)。

## 1. 中核ドメイン用語

| ja | en | zh(简体) | 備考 |
|---|---|---|---|
| 筋骨格モデル | musculoskeletal model | 肌肉骨骼模型 | 骨・関節+筋・腱まで持つ人体シミュ |
| 筋アクチュエータ | muscle actuator | 肌肉致动器 | 縮む(引く)力のみ・活性0〜1・Hill型 |
| Hill 型筋モデル | Hill-type muscle model | Hill 型肌肉模型 | 力‐長さ‐速度依存の非線形 |
| 自由度(DoF) | degrees of freedom (DoF) | 自由度(DoF) | 独立に動ける関節軸の数 |
| 冗長(な) | redundant | 冗余 | 自由度より筋が多い |
| 筋シナジー | muscle synergy | 肌肉协同 (muscle synergy) | 少数Kの「まとめて動くパターン」 |
| 閉ループ制御 | closed-loop control | 闭环控制 | 状態を見ながら調整。開ループ=open-loop=开环 |
| 倒立振子 | inverted pendulum | 倒立摆 | 二足立ちの本質 |
| CMA-ES(進化戦略) | CMA-ES (evolution strategy) | CMA-ES(进化策略) | 数百〜千個の数値を進化最適化 |
| ベースライン | baseline | 基线 | 無学習・無制御の対照 |
| RTF(実時間比) | RTF (real-time factor) | RTF(实时因子) | シミュが実時間より何倍速いか |
| `qpos` | `qpos` | `qpos` | 全関節位置を一列に並べた配列(訳さない) |
| keyframe(キーフレーム) | keyframe | 关键帧 (keyframe) | 開始姿勢を qpos の並び順で書いた初期化データ |
| warm-start(温かい初期化) | warm-start | 温启动 (warm-start) | 既にできる方策から学習開始 |
| モーションキャプチャ(mocap) | motion capture (mocap) | 动作捕捉 (mocap) | |
| リターゲット | retargeting | 动作重定向 (retargeting) | 別骨格へ動きを移し替え |
| 逆運動学(IK) | inverse kinematics (IK) | 逆运动学 (IK) | 手先位置→関節角を逆算 |
| 差分 IK | differential IK | 微分 IK | Levenberg-Marquardt |
| キネマティック再生 | kinematic replay | 运动学回放 | 物理を回さず関節角を直接セット |
| 等式拘束 | equality constraint | 等式约束 | 関節が別関節の関数で決まる連動 |
| 浮遊基底 | floating base | 浮动基座 | 骨盤が地面固定でない |

## 2. タスク・動作

| ja | en | zh(简体) |
|---|---|---|
| 立位 / 立たせる | standing / balance | 站立 / 平衡 |
| 把持(する) | grasp / grasping | 抓握 |
| force-closure(力学的把持) | force-closure | 力封闭 |
| 運搬 / 運ぶ(制御可能な操作) | place / carry (controllable manipulation) | 搬运 / 放置(可控操作) |
| 飲む動作 | drinking motion | 喝水动作 |
| 顎(下顎) / 開閉 | mandible (jaw) / open-close | 下颌 / 开合 |
| リーチ | reach | 触及 / 伸手 |
| 猫背 / のけぞり / 背屈 | stooped (hunched) posture / arching back | 驼背 / 后仰 |
| 接地 | ground contact | 触地 |

## 3. honest disclosure 系(語調を保つ・弱めない)

| ja | en | zh(简体) |
|---|---|---|
| 正直な負け | an honest loss / candidly a loss | 诚实地承认失败 |
| 内訳を疑う | question the breakdown | 质疑(结果的)内幕/构成 |
| 誇張せず | without exaggeration | 不夸大 |
| 報酬ハッキング | reward hacking | 奖励作弊 (reward hacking) |
| 演出(キャラクター層) | cosmetic / presentation layer | 演出层(角色层) |
| 本物(研究層・筋駆動) | genuine (research layer, muscle-driven) | 真实层(研究层·肌肉驱动) |
| 台本(で動かす) | scripted (kinematically) | 脚本驱动 |
| 剛体プロップ | rigid prop | 刚体道具 |
| 速さの proxy | a proxy for speed | 速度的替代量 (proxy) |
| Human-in-the-Loop(人間をループに残す) | Human-in-the-Loop | 人在回路 (Human-in-the-Loop) |
| 「飲む」生理でなく所作 | a drinking *gesture*, not the *physiology* | 喝水的“姿态”而非“生理过程” |
| 測る前に推測しない/推測する前に測れ | measure before you guess | 猜测之前先测量 |

## 4. 固有名詞・データセット(訳さない/定訳)

| ja | en | zh(简体) |
|---|---|---|
| MS-Human-700 | MS-Human-700 | MS-Human-700 |
| MuJoCo / Menagerie | MuJoCo / Menagerie | MuJoCo / Menagerie |
| onocollo(自作研究基盤) | onocollo (our research runtime) | onocollo(自研研究运行时) |
| evis(マスコット名) | evis | evis |
| 恵比寿 | Ebisu (a Japanese god of fortune) | 惠比寿(日本七福神之一) |
| eviscerate | eviscerate (to remove viscera) | eviscerate(剖除内脏) |
| CMU MoCap (cgspeed BVH) | CMU Graphics Lab Motion Capture Database | CMU 动作捕捉数据库 |
| AMASS / AIST++ / Mixamo / SMPL | (原綴のまま) | (原文保留) |
| ICRA 2024 / Apache-2.0 | ICRA 2024 / Apache-2.0 | ICRA 2024 / Apache-2.0 |

## 5. タイトル訳(案・初期値)

- **ja**: 骨と筋だけの人体を、自宅の CPU で立たせ・掴ませ・飲ませ・踊らせた全記録 — 700本の筋肉とマスコット「evis」、正直な負けと勝ち
- **en(案)**: Standing, Grasping, Drinking, Dancing a Bones-and-Muscles Human on a Home CPU — 700 Muscles, a Mascot Named "evis", and the Honest Wins and Losses
- **zh 案(简体)**: 用家用 CPU 让一具只有骨与肌的人体站立、抓握、喝水、跳舞的全记录 —— 700 条肌肉、吉祥物“evis”,以及诚实的输与赢

> タイトルは翻訳確定時に再検討。en/zh は SEO と自然さで微調整可。
