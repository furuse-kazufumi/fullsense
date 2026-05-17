# 中国生成式 AI 規制と社内利用パターン (运用 documentation, draft v0.1)

> **本ドキュメントは法的助言 (法律建议) を構成するものではありません.
> Not legal advice / 不构成法律建议.**
> 各企業の法務部門による確認、必要に応じて専門弁護士への相談を強く推奨します.
> ドラフト版 (2026-05-17 作成). 内容は規制改正により変更される可能性があります.

## 1. 対象とする規制

本ドキュメントは、以下の中国法規における「公衆向けサービスでない社内利用」の
扱いについて整理し、FullSense (llmesh / llive / llove) の典型的な利用パターンと
照らし合わせるための運用 documentation です.

| 法規 (中) | 法規 (英) | 施行日 | 関連 |
|---|---|---|---|
| 《生成式人工智能服务管理暂行办法》 | Interim Measures for the Administration of Generative Artificial Intelligence Services | 2023-08-15 | 主要 |
| 《互联网信息服务算法推荐管理规定》 | Provisions on Administration of Algorithm Recommendation of Internet Information Services | 2022-03-01 | 主要 |
| 《互联网信息服务深度合成管理规定》 | Provisions on Administration of Deep Synthesis of Internet Information Services | 2023-01-10 | 関連 |
| 《中华人民共和国网络安全法》(修正) | Amended Cybersecurity Law (AI 専用条項追加) | 2026-01-01 | 関連 |
| 《人工智能拟人化互动服务管理暂行办法》 | Interim Measures for AI Anthropomorphic Interaction Services | 2026-07-15 予定 | 関連 |

## 2. 「公衆向けサービス」と「社内利用」の境界

### 2.1 規制対象 — 公衆向けサービス

《生成式 AI 服务管理暂行办法》第二条は、規制対象を「**境内に向けて公衆に
生成式 AI サービスを提供する**」事業者と規定しています.

「公共輿論属性 / 社会動員能力」(public opinion attributes or social mobilization
capacity) を持つサービスが filing 対象とされ、具体的には以下が例示されています:

- 论坛 (forum)
- 博客 (blog)
- 微博 (microblog)
- 聊天室 (chat room)
- 通讯群组 (communication groups)
- 公众账号 (public accounts)
- 短视频 (short video)
- 直播 (live streaming)
- 信息分享 (information sharing)
- 小程序 (mini-programs)
- その他、公衆に意見表明の channel を提供 / 公衆活動を動員する能力を持つ
  インターネットサービス

### 2.2 規制対象外 — 社内利用 (filing 免除)

同弁法第二条第三項により、以下は規制の適用範囲外です:

> 「**业内单位、企业、教育和科研机构、公共文化机构、有关专业机构等研发、应用
> 生成式人工智能技术，未向境内公众提供生成式人工智能服务的，不适用本办法的规定**.」

英訳 (参考):
> "**Industry units, enterprises, educational and research institutions, public
> cultural institutions, and relevant professional organizations that develop or
> apply generative AI technology without providing generative AI services to the
> domestic public are not subject to these Measures**."

つまり、**企業 / 教育機関 / 研究機関が生成式 AI 技術を開発・適用するが境内公衆
向けにサービスを提供しない場合**、本弁法は適用されません. これには algorithm
filing (算法备案), security assessment (安全评估) の義務も含みません.

### 2.3 境界判定の指針 (本ドキュメントの解釈)

以下に該当する利用は、社内利用 (filing 免除) の典型例と考えられます:

- AI が **従業員のみ** がアクセスし、生成内容も **社内のみ** で利用
- 社内文書 / コード / 業務メモ / 設計仕様等の作成補助
- 内部研究 / 実験 / プロトタイピング
- 部署間 / 社内拠点間の業務効率化用
- ※ ただし、社内利用といえど **後で公衆にサービス提供を始める場合**、その時点で
  filing 義務が発生します.

逆に、以下は公衆向けサービスに該当する可能性が高く、filing 対象です:

- 一般消費者向け chatbot / answer engine の提供
- 公衆 access 可能な web サービスでの AI 機能提供
- 社外パートナー / 顧客企業の従業員等が access する AI サービス
- API 形式で社外提供する AI サービス
- 「社内専用」と称しても、実態として広く公衆が access できる場合

判定が難しい例 (各企業で要確認):

- B2B SaaS で顧客企業の従業員のみがアクセス: グレー、契約条件次第
- 子会社 / 関連会社の従業員がアクセス: グレー、グループ会社の範囲次第
- 業務提携先の従業員がアクセス: グレー、契約と access 管理次第

## 3. FullSense の利用パターンと filing 該当性

### 3.1 典型的な FullSense 利用パターン (社内利用、filing 免除に該当)

- **llmesh**: 企業内 on-prem 配備、社内 LLM hub として従業員業務に利用
- **llive**: 社内文書生成 / コード生成 / 業務 Brief 作成、出力は社内のみ
- **llove**: 個別開発者の dashboard / 観測 IDE として社内利用

これらは典型的に「社内利用」に該当し、生成式 AI 弁法の filing 義務外と考えられ
ます (※ 各企業の実装と利用形態による).

### 3.2 公衆向けサービスへの転用例 (filing 対象になる)

- llmesh を経由した LLM サービスを社外顧客 / 公衆に提供
- llive Brief 生成サービスを公衆向け web で提供
- llove TUI / 拡張をプリインストールしたサービスを公衆向けに提供

これらの転用は **transition の時点で filing が必要** になります.

### 3.3 FullSense が architecture-level で対応している関連機能

| 規制要件 (社内利用でも備えるべき) | FullSense 機能 | 状態 |
|---|---|---|
| 監査ログ (改正网络安全法 2026/01 で AI 条項追加) | llmesh + llive audit log + Approval Bus | 部分実装 |
| 人間判断必須業務での HITL | llive HITL Approval Bus | 実装済 |
| 内部生成内容の出典明示 (社内 governance のため) | llive OKA-FX 出典追跡 + Annotation Channel | 部分実装 |
| データ越境管理 | on-prem 完結設計 (cloud LLM 不要) | 実装済 |
| 安全評価レポート | (公衆向けに転用する場合に必要) | 未実装 (低優先) |

## 4. 推奨運用 (社内利用を維持するため)

以下の運用は、社内利用パターンを維持し、filing 不要範囲に留めるための参考
ガイドラインです.

### 4.1 アクセス制御

- 全 AI サービスを **企業内ネットワーク / VPN 配下** に配備
- 認証は社内 SSO / LDAP / Active Directory に統合
- 社外協業者にアクセスを開く場合は **明確な契約 + access log 保存**
- API 公開は社内に限定、外部公開する場合は filing を取得

### 4.2 監査ログ

- 全 AI request / response を 改正网络安全法 (2026/01) 対応として **6 ヶ月以上保存**
- llmesh audit log + llive Approval Bus log を運用に組込
- 法務 / 監査部門が定期的に sample レビュー

### 4.3 生成内容の社内利用維持

- 生成された内容を **そのまま公衆 publish しない** policy 確立
- 公開する場合は **人間の判断と編集** を経る (HITL Approval Bus 経由)
- 社内 wiki / docs / コードへの取り込みは OK、公衆 web への直接公開は審査必須

### 4.4 規制改正のフォロー

- 改正网络安全法 (2026/01) / 擬人化対話 AI 弁法 (2026/07 施行予定) などの
  改正情報を法務部門が定期 monitoring
- 規制変更時に運用 policy を update

## 5. 公衆向けサービスへ転用する場合 (参考)

社内利用から公衆向けサービスに transition する場合、以下が一般的に必要です
(2026/05 時点、変更可能性あり):

- 算法备案 (algorithm filing) — 互联网信息服务算法备案系统で 10 営業日以内
- 安全评估 (security assessment) — CAC で実施
- 大模型备案 (大型モデル filing) — 該当する場合
- 服务协议 (サービス利用規約) の整備
- 投诉举报机制 (苦情通報メカニズム) の整備
- 内容审核 (コンテンツ審査) の整備
- 用户实名认证 (実名認証) の整備
- 反深度合成標識 (deepfake であることの明示) — 深度合成弁法

参考: 2025/12/31 時点で生成式 AI サービス filing は 748 件、生成式 AI アプリ /
機能の filing は 435 件 (国家网信办公开数据).

## 6. 各企業で確認すべきこと

本ドキュメントは一般的整理に過ぎません. 各企業は以下を法務部門 / 専門弁護士と
確認してください:

- [ ] 自社の AI 利用が「境内公衆向け提供」に該当しないことの確認
- [ ] 子会社 / 関連会社 / パートナーへの提供が「公衆」に該当しないことの確認
- [ ] 改正网络安全法 (2026/01) の AI 条項への対応 (監査ログ等)
- [ ] 擬人化対話 AI 弁法 (2026/07 施行予定) の対応 (人型対話 AI を使う場合)
- [ ] 業界別の追加規制 (金融 / 医療 / 教育 / 政府等)
- [ ] データ越境規制 (個人情報 / 重要データの境外移転禁止)
- [ ] 行業協会 / 監督機関の追加 guideline

## 7. 参考文献 (公式 / 主要 commentary)

### 7.1 公式法規

- 《生成式人工智能服务管理暂行办法》(CAC 公式)
  https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm
- 《互联网信息服务算法推荐管理规定》(CAC 公式)
- 《互联网信息服务深度合成管理规定》(CAC 公式)
- 《人工智能拟人化互动服务管理暂行办法（征求意见稿）》(CAC, 2025/12)
  https://www.cac.gov.cn/2025-12/27/c_1768571207311996.htm

### 7.2 解説 (法律事務所 / 専門サイト)

- White & Case "AI Watch: Global regulatory tracker - China"
- IAPP "Global AI Governance Law and Policy: China"
- ICLG "Cybersecurity Laws and Regulations Report 2026 Generative AI and Cyber
  Risk in China"
- 上海市锦天城律师事务所「生成式 AI 企业合规及法律尽职调查要点」
- 中伦律师事务所「《生成式人工智能服务管理办法（征求意见稿）》要点解析」
- Lexology "中国 AI 监管全景：从算法备案到生成式人工智能的法治化路径"

### 7.3 英語 commentary

- China Briefing "How to Interpret China's First Effort to Regulate Generative AI"
- Securiti "Navigating China's AI Regulatory Landscape"
- Global Legal Insights "AI, Machine Learning & Big Data Laws | China"

---

## 改訂履歴

- 2026-05-17 — draft v0.1 作成 (戦略思索 PART 3 + WebSearch 確認に基づく)

## 多言語版予定

- ja (本ドキュメント) — 整備中
- en — 整備予定 (Week 4)
- zh — 整備予定 (Week 4)
