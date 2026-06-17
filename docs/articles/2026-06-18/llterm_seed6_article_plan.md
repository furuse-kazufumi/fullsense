# llterm 種 #6 記事設計メモ (2026-06-18)

対象: llterm 種 #6 を Qiita 長編へ落とすための設計メモ  
参照時点: llterm commit `ff066bdf99db74263f1c6208fa8a671a080bc7fc`  
根拠スナップショット: [llterm_seed6_evidence.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_evidence.md)

## 記事の狙い

- 種 #6「ハーネス/ループエンジニアリングのノウハウ」を、Qiita 長編として書ける粒度まで落とす
- 種 #1〜#5 を分散公開せず、**1 本の through-line** に束ねる
- `llterm` 固有の incident を、**headless CLI を turn 境界で駆動する自走 AI harness** 一般へ持ち上げる

## controlling idea

> 自走 AI は「賢く回すこと」より「人間が監督・割り込み・停止できること」のほうが難しい。  
> だから loop engineering の本体は、戦略そのものより **介入境界・観測・停止条件** の設計にある。

短い言い換え:

> 自走 AI の本体は、推論の賢さではなく**監督できる構造**にある。

## 記事の約束

- 単なる llterm 開発日誌にしない
- 1 件の starvation 障害から、複数の設計原則がどう連鎖的に見つかったかを示す
- `honest disclosure` は飾りではなく、`ctx 2549%` や「直し切っていない残課題」を書くための構造にする

## 推奨タイトル

第一候補:

- 自走 AI ループの作り方と落とし穴

代替:

- 自走AIは「回すこと」より「監督すること」が難しい
- Claude Code / Codex を自走させて分かった、loop engineering の本体
- 自走 AI を止める・割り込む・観測する: llterm 障害対応から抽出した 9 原則

## hook + nut graf 叩き台

### hook

AI に「今の進捗を要約して」と頼んだ。  
13 分待っても返ってこない。遅いだけではなかった。ログを追うと、そのタスクは構造上、永久に飲み込まれる経路に入っていた。  
しかも掘るほど、別の穴まで出てきた。`ctx 2549%` という物理的にありえない占有率、rotate のたびに回る過剰レビュー、そして「任せているはずなのに監督できない」自走ループの弱さ。

根拠: [llterm_seed6_evidence.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_evidence.md) の A / B

### nut graf

この一件で痛感したのは、自走 AI の難しさは「賢いプロンプトを書くこと」ではなく、**人間がどこで介入できるかを設計すること**だという点だった。  
本稿では `llterm` の障害対応を材料に、headless CLI を turn 境界で回すループで何が壊れやすいかを 9 つの原則として整理する。テーマは推論性能ではなく、**監督・割り込み・停止・観測**の設計である。

## 6-beat through-line

### 1. anomaly

- 「進捗を要約して」が 13 分返らない
- 単なる遅延ではなく、構造上の starvation だった

### 2. setup

- llterm は Claude Code / Codex を headless に回す loop harness
- 人間はターン中に injection で割り込める、という前提だった

### 3. complication

- 消費点が継続ターン側にしかなく、rotate 連発だと injection を拾えない
- `ctx 2549%` により毎ターン rotate
- codex 側の自己圧縮と llterm 側 rotate が競合し、1 セッション=1 ターンに縮退する
- handoff ターンにもフルレビューが走り、時間とレートを食う

### 4. investigation

- production ログから starvation / ctx 過大計上 / 過剰レビューを切り分ける
- 「たまたま緑」のテストも疑い、決定論化の必要が見える

### 5. resolution

- opener 側でも injection を消費
- sticky cancel と one-shot interrupt を分離
- handoff ターンは unreviewed に落とす
- 全行タイムスタンプ + ローテログで追跡可能性を底上げ

### 6. pull-back

- 自走 AI の本体は戦略ではなく監督可能性
- 残課題: `ctx 2549%` の根本算定は未解決、codex 側占有表示はまだ痩せる

## 種 #1〜#5 の章マッピング

| 元の種 | #6 での役割 | 置き場所 |
|---|---|---|
| 種 #1 注入タスク飢餓 | 主事件 / hook / anomaly | 導入 + 第1章 |
| 種 #2 過剰レビュー削減 | 「適用範囲を設計しないレビューは高コスト」の実例 | 第4章 |
| 種 #3 緊急割り込み | 介入境界の設計原則 | 第2章 |
| 種 #4 全行タイムスタンプ + ローテログ | 監査可能性を architecture level で担保 | 第5章 |
| 種 #5 flaky test 顕在化 | 観測だけでなく検証系も決定論化が必要 | 第6章 |

注記: 第3章の `ctx 2549%` と「自己圧縮 × rotate」の衝突は、種の 1 本ではなく **原則 2 / 原則 3** から起こす章。

## 章構成案

### 0. 冒頭 3 点ボックス

- 前提: headless CLI を turn 境界で回す自走 AI harness の話
- 流れ: starvation incident → 3 つの構造バグ → 9 原則
- ゴール: 自走 AI を「回す」より「監督できる」設計の勘所を持ち帰る

### 1. 「進捗を要約して」が永久に返らなかった

- 13 分待ち
- rotate で継続ターンへ届かず、注入が opener に押し出され続ける
- 種 #1 をここで回収

### 2. ターン粒度と割り込みを分けて設計する

- turn boundary が介入の最小単位
- sticky cancel と one-shot interrupt を分ける
- 緊急注入は opt-in にする
- 種 #3 を回収

### 3. 2549% は「AI が太った」のではなく計測が壊れていた

- 物理上限を超える数字は、改善ではなく計測バグの兆候
- billing 用累積値を occupancy 制御へ流用した誤り
- codex が自前で圧縮する系に外側から rotate を重ねると、境界の二重管理で縮退する
- honest disclosure の山場 1
- 根拠: [llterm_seed6_evidence.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_evidence.md) の B / C / D

### 4. 多 AI レビューは質だが、無条件に重ねると時間を食う

- orchestra 1 ターンの実コスト
- handoff / EXIT 整形にフルレビューは不要
- 種 #2 を回収

### 5. 追えないなら監督ではない

- 全行タイムスタンプ
- 1 時間ローテログ
- fail-safe な telemetry
- 種 #4 を回収

### 6. テストも「たまたま緑」を疑う

- race に依存した緑
- 出力ログ追加で flaky が露出
- block point を作って決定論化
- 種 #5 を回収
- 根拠: [llterm_seed6_evidence.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_evidence.md) の E

### 7. 抽出した 9 原則

1. **ターン境界を制御単位として設計する**  
   headless CLI を回す系では、人間の介入はまずターン境界に吸着する。即時介入が欲しいなら interrupt を別建てにする。
2. **物理上限を超える指標は、まず計測を疑う**  
   `ctx 2549%` のような数字は勝ち筋ではなく計測破綻のサイン。占有率は瞬間値として測る。
3. **自己管理コンポーネントに外側の管理を二重掛けしない**  
   codex の自己圧縮と llterm の rotate を重ねると、境界が競合して縮退する。管理境界は 1 つに絞る。
4. **レビューは量ではなく適用範囲で設計する**  
   実装ターンと記録ターンを分けずに同じ強度でレビューすると、高コストな二度漬けになる。
5. **飢餓は「積んだ」ではなく「消費点に届くか」で決まる**  
   queue に積んだだけでは足りない。rotate や分岐をまたいでも必ず拾う消費点が必要。
6. **監督可能性は telemetry を architecture に埋め込んで作る**  
   全行タイムスタンプや時間ローテログは後付けの便利機能ではなく、HITL の土台。
7. **推測ではなく production 観測から芋づるで掘る**  
   1 観察から複数の構造バグを辿る姿勢が、solo AI judgment を避ける。
8. **並行テストは「たまたま緑」をまず疑う**  
   race 依存の緑は、観測点を少し動かしただけで崩れる。block point を作って決定論化する。
9. **honest disclosure を結果ではなく判断基準として使う**  
   異常値を盛らず、直っていない残課題まで書くことで、記事全体の信頼性を作る。

各原則の根拠: [llterm_seed6_evidence.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_evidence.md)

### 8. honest disclosure / 残課題

- `ctx 2549%` の根本算定はまだ残る
- codex 側占有率は暫定的に痩せる
- この設計は「headless CLI を turn 境界で駆動する loop」に特に効く、と適用条件を書く

## 見出し候補

- 自走 AI の最小制御単位は「ターン境界」だった
- `ctx 2549%` が教えてくれたのは、AI の賢さではなく計測の壊れ方だった
- レビューは質だが、掛け方を間違えるとただ遅い
- 追えない自走は監督ではない
- 緑のテストでも信用しすぎるな

## 図や挿絵の候補

- 今回は **単一の長編 Qiita 記事** として設計するため、バス江コマは **1 枚だけ**使う
- 採用候補は `025.jpg`。loop engineering を実地で回している感じが最も強く、記事全体の代表絵として使える
- `006.jpg` / `081.jpg` / `163.jpg` は別記事や派生かみくだき版へ回し、この長編では使わない

注意:

- `alu.jp` crop `1DLuaYTNfWIQz3tqCv1h` を使う場合、出典として支えられるのは「聖書の引用みたいになってる…!」まで。`honest disclosure` を毎回持ち出す感じ等は筆者比喩として分離する。

## honest disclosure の位置

- 第3章で「数字を疑う」
- 第6章で「テストの緑を疑う」
- 第8章で「まだ直っていないもの」を書く

これで、honest disclosure は単独節ではなく、記事全体を貫く判断基準として見せられる。

## 次の実作業

1. この章構成をベースに Qiita 草稿 `ja` を起こす
2. 冒頭 100 語と第1章だけ先に書き、through-line が立つか確認する
3. 第7章の 9 原則を各 1 段落へ肉付けし、第3章 / 第6章 / 第8章の evidence link と整合させる
