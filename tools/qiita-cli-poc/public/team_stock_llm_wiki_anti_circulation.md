---
title: 'LLM Wiki の本当の難所は「知識を集めること」ではなく「思考の循環を止めること」'
tags:
  - AI
  - LLM
  - KnowledgeGraph
  - Agent
  - ClaudeCode
private: false
public_private: false
slide: false
ignorePublish: true
id: b35b429dc6dc1fde207a
---
# LLM Wiki の本当の難所は「知識を集めること」ではなく「思考の循環を止めること」

> **この草稿の位置づけ**
> #43 の `3-2. LLM Wiki — 「育つ知識」のパターン` から切り出した Team stock 用の source draft です。2026-06-18 に Qiita Team `fullsense` へ POST 済みで、item id は `b35b429dc6dc1fde207a`、2026-06-19 12:41:22 +09:00 の再確認では Team API GET が `private:false` と `group.url_name: general` / `group.private: false` を返し、未認証 HTML GET は `302 /login?redirect_to=...` でした。poster payload では `group_url_name` を明示していなかったため、implicit General sharing が起きた可能性を current 仮説として追います。ただしこれは root-cause 仮説であって、team-only の証明でも否定でもありません。local source は観測値を再宣言しないよう `group_url_name` を固定せず、accidental な `qiita publish` を避けるため `ignorePublish: true` を残しています。

> **前提**
> RAG より一段先の「育つ知識基盤」を考えていて、要約・概念ページ・相互リンクを自前で持ちたい文脈を前提にします。
>
> **流れ**
> まず RAG と LLM Wiki の差を整理し、その後で `thought circulation` と anti-circulation の危険源に絞ります。
>
> **ゴール**
> `LLM Wiki` の難しさが「検索の賢さ」ではなく「自己循環をどう止めるか」にあると掴める状態を目指します。

> **この記事で話さないこと**
> ここでは全文検索の細かな評価や、Wiki UI 実装の比較までは扱いません。焦点は `thought circulation` と anti-circulation の境界設計に置きます。

LLM Wiki というと、つい「RAG より賢い知識ベース」くらいのイメージで受け取られがちです。  
ですが、実際に設計を始めると難しいのは検索精度よりも、**一度まとめた知識が自己循環し始めること**でした。

原典に近い生ソースを概念ページへ編み、相互リンクで育てていく。  
この発想自体は強力です。けれど、うまく回り始めた瞬間に別の危険が生まれます。

- 要約が要約を参照し始める
- 人間が書いた一次ソースと、AI が整形した二次ソースの区別が薄れる
- 「よくまとまっている」ページほど、誤りを自己強化しやすくなる

ここで必要になるのが、#43 で触れた `thought circulation` への安全装置です。

## この記事で扱う論点

1. RAG と LLM Wiki の違いを、`その場検索` と `事前コンパイル` の差として捉え直す
2. なぜ LLM Wiki の最大の落とし穴が `thought circulation` なのか
3. `Anti-Circulation Safeguards` をどの粒度で置くべきか
4. `llive` / `llove` / `llmesh` への役割対応づけを、実装済み事実と主観マッピングに分けて記述する

## source

- 完全版: `qiita43_harness_loop_stack.md` `3-2. LLM Wiki — 「育つ知識」のパターン`
- 切り出しの核:
  - 生ソース / Wiki / スキーマの 3 層
  - `thought circulation` を最大の落とし穴とする段落
  - `Anti-Circulation Safeguards` の箇条書き束
- 関連:
  - `RAD` corpus-first 運用
  - `RAPTOR` の evidence ladder
  - `corpus2skill` / `LLW-AC-01〜08` 系の設計メモ

## honest disclosure

この草稿は、`LLM Wiki` を「もう動いている仕組み」としては書きません。  
現時点で動いているのは corpus 側の蓄積と接続準備までで、Wiki 的自己成長や anti-circulation の多くは設計段階です。公開時も、その境界は本文で明示します。
