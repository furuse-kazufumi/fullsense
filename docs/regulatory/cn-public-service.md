# 中国生成 AI 弁法 — 公衆向けサービス filing 手順 (draft v0.2)

> **本ドキュメントは法的助言を構成するものではありません.
> Not legal advice / 不构成法律建议.**
> 公衆向け生成 AI サービスを中国で提供する場合、現地法律事務所 / 専門弁護士の
> 確認は必須です. 本 docs は技術担当者の理解補助のみ.
>
> v0.2 (2026-05-18): 「公衆向け」の技術的境界判定 / filing 後の更新義務 /
> audit-log との接続 (内容审核 event) / PII handling 中国特例 を追加.

## 1. 対象 — 社内利用 vs 公衆向け

→ **社内専用利用は filing 不要**. 詳細は `cn-internal-use.md` 参照.

本 docs は「公衆向けサービス (面向公众提供服务)」を提供する場合の
手続概要.

### 1.1 「公衆向け」の技術的境界判定

「公衆向け」かどうかは、登記時の自己申告だけでなく、CAC が運用実態を
監査する可能性がある. FullSense は以下フラグの組合せで「公衆向け」と
みなされる **リスク** が高い:

| 条件 | 「公衆向け」リスク |
|---|---|
| user 登録が **企業ドメイン以外** に開放 | 高 |
| 認証なし anonymous access が可能 | 非常に高 |
| 価格表 / sign-up ページが **公開 URL** で誰でも到達可 | 高 |
| 法人顧客のみだが、契約数 1,000+ かつ顧客所属社員数の合計が >10 万 | 中 (CII 隣接) |
| EU/US 等の海外顧客のみで中国本土 user が居ない | 低 (運用上の越境論点に切替) |

**技術的境界判定の参考実装**:

```python
def is_public_service(deployment_config: dict) -> bool:
    # FullSense 内部の運用判定 (法的判定ではなく technical heuristic)
    if deployment_config.get("auth_required") is False:
        return True
    if deployment_config.get("allowed_domains") is None:
        return True
    if deployment_config.get("user_count_estimate", 0) > 100_000:
        return True
    return False
```

判定結果は Annotation Channel `core:cn_public_service=true|false` として
emit し、運用者が誤って public 設定にした際の警告に使う.

## 2. 主な filing 義務

公衆向け生成 AI サービスを中国境内で提供する場合、複数の登記 / 評価が必要:

### 2.1 算法备案 (Algorithm Filing)

- 根拠法: 互联网信息服务算法推荐管理规定 (2022/03 施行)
- 登記システム: 互联网信息服务算法备案系统 (CAC オンライン)
- 期限: サービス launch 後 **10 営業日以内**
- 提出内容:
  - 提供者名称
  - サービス形態 (chatbot / 推薦 / 検索 等)
  - 適用分野 (金融 / 教育 / 医療 等)
  - アルゴリズム種別
  - アルゴリズム自己評価レポート (`安全自评估报告`)
  - 公開予定 disclosure 内容

### 2.2 大模型备案 (Large Model Filing)

- 根拠法: 生成式人工智能服务管理暂行办法 (2023/08 施行)
- 対象: 公衆向け生成 AI サービス
- 提出: 算法备案と並行
- 2025/12/31 時点で **748 件** が filing 済 (国家网信办公开数据)

### 2.3 安全评估 (Security Assessment)

- 「公共輿論属性 / 社会動員能力」を持つサービスは別途必要
- CAC で実施
- データ安全 / プライバシ / 内容審査 / 倫理リスクを評価

### 2.4 深度合成標識 (Deepfake Labeling)

- 根拠法: 互联网信息服务深度合成管理规定 (2023/01)
- 対象: AI 生成画像 / 音声 / 動画
- 義務: AI 生成であることを明示する識別

### 2.5 擬人化対話 AI 弁法 (2026/07/15 施行)

- 根拠法: 人工智能拟人化互动服务管理暂行办法 (2025/12 公開草案)
- 対象: 人型 AI 相互作用 (chatbot / agent 等)
- 義務: ユーザに対する明示 + 内容審査 + 異常検知

## 3. 文書整備 (filing 申請時)

- サービス利用規約 (用户协议)
- 投诉举报机制 (苦情通報メカニズム)
- 内容审核 (コンテンツ審査体制)
- 用户实名认证 (実名認証システム)
- 数据安全管理制度 (データセキュリティ管理規程)
- AI 出力標識 (深度合成 / 擬人化対話)

## 4. FullSense 利用時の技術的対応

公衆向けサービスとして提供する場合の FullSense 設定:

| 要件 | FullSense 機能 |
|---|---|
| 内容审核 | llive HITL Approval Bus + Annotation Channel `cn-content-review` |
| 用户实名认证 | (アプリケーション側、FullSense 範囲外) |
| AI 出力標識 | Annotation Channel `ai-generated` + `deepfake-warning` |
| 算法備案 metadata export | (Phase 2 実装、`llive algorithm-export`) |
| 監査ログ | llive Approval Bus + SqliteLedger (audit-log-format.md 準拠) |
| データ安全 | llmesh on-prem 完結 (data-sovereignty.md 参照) |

### 4.1 audit-log との接続

`audit-log-format.md` (3-4) に従い、公衆向けサービス専用の event を追加:

| event_type | 発生タイミング | 追加 fields |
|---|---|---|
| `content_review_requested` | 内容审核 gate 到達 | `brief_id`, `categories`, `auto_score` |
| `content_review_passed` | 自動 / 手動審査通過 | `brief_id`, `reviewer`, `policy_version` |
| `content_review_blocked` | 違反検出で block | `brief_id`, `reason_codes`, `policy_version` |
| `deepfake_label_applied` | 出力に深度合成ラベル付与 | `brief_id`, `media_type`, `label_method` |
| `realname_auth_verified` | 実名認証完了 | `actor`, `verification_method` (`mobile_carrier` / `id_card_ocr` / 等) |
| `algorithm_filing_metadata_dumped` | 算法備案用 metadata export | `output_path`, `model_id` |

これらは HMAC chain (audit-log-format 3.1) に組み込まれるため、CAC 監査時に
**「内容审核が必ず brief 出力前に通っていた」** ことを順序で証明可能.
具体的には `content_review_passed.seq < outcome_recorded.seq` が
全 brief で成立することを `verify_chain_detailed` が確認する.

### 4.2 PII handling 中国特例

中国 PIPL (个人信息保护法) は GDPR と類似しつつ、生成 AI 弁法と組合せで
以下の特例が発生する:

| 項目 | 中国特例 |
|---|---|
| 同意取得 | 「敏感个人信息」(医療/金融/位置/14 歳未満) は **separate consent** 必要 (PIPL Art.29) |
| 出力に user PII を含む可能性 | LLM の hallucination も含めて provider 責任. 出力フィルタリング義務化 |
| 越境 | 公衆向けサービス user データの海外移転は別途 **PIPL Art.38** の手続必要 (data-sovereignty.md 2.1 で 越境扱い) |
| 未成年保護 | 14 歳未満は guardian consent + 別途仕组み |
| 識別困難な aggregate データ | 匿名化 (de-identification) は PIPL Art.4 で「個人情報ではない」とみなす要件あり |

FullSense 側の対応:

- llive `pii_redacted` event (audit-log-format 3.4) で PIPL 第29条 敏感情報の
  category を `entity_type` に分けて記録 (例: `medical`, `financial`,
  `location`, `minor_age`).
- content_review_blocked event の `reason_codes` に PIPL Art.X 違反を明示.
- 越境発生時 (data-sovereignty 6.1) は PIPL Art.57 + 生成 AI 弁法 Art.18
  両方の通知義務 timeline を triggerring.

## 4.3 filing 後の更新義務

filing 後にモデル / アルゴリズム / 適用分野を **重大変更** した場合、
**変更後 10 営業日以内** に更新 filing が必要 (互联网信息服务算法备案管理规定).

「重大変更」の定義 (実務指針):

| 変更 | 重大変更か | 対応 |
|---|---|---|
| LLM backend を別 model に切替 (例: GLM-4 → Qwen-3) | 重大 | 更新 filing 必要 |
| Fine-tune を再実行 (同 model architecture, 新 training data) | 中 | 更新 filing 推奨 |
| Annotation Channel namespace 追加 | 軽微 | 更新不要 (内部 metadata) |
| 公衆向け対象を「中国本土 user → 中国本土+香港 user」に拡大 | 重大 | 更新 filing 必要 |
| 価格 / UI / 内容审核ポリシ更新 | 中 | 内部記録のみ |

FullSense 側で自動 detection:

- `algorithm_filing_metadata_dumped` event の `model_id` / `fine_tune_checksum`
  が前回 dump と異なる → 自動 alert で運用者に「更新 filing 要否確認」を
  notify.
- 推奨運用: 月次 `python -m llmesh timeline diff --since last_filing` で
  当該期間の重大変更候補を一覧化.

## 5. 推奨運用 (社内利用に留める判断も含めて)

**推奨**: ほとんどの企業は **社内利用** で要件を満たせるため、`cn-internal-use.md`
パターンを優先. 公衆向けにする場合のみ本 docs の手続を実施.

社内利用が成立する例:
- 従業員のみが access
- 出力は社内 wiki / 内部 docs のみに反映
- 顧客企業の従業員 access は契約 + access control で限定

公衆向けに切替える場合:
- 切替時点で算法備案 + 大模型備案 + 安全評価を提出
- 切替前のデータ取り扱いは適切に説明

## 6. 多言語版予定

- ja (本ドキュメント) — draft v0.1
- en / zh — Week 4 整備

## 7. 参考文献 (cn-internal-use.md と共通)

- 国家网信办公式 (cac.gov.cn) 各弁法
- 上海市锦天城律师事务所 / 中伦律师事务所 / 汉坤律师事务所 解説
- China Briefing / White & Case / IAPP 英語解説

## 改訂履歴

- 2026-05-18 — draft v0.1 作成
