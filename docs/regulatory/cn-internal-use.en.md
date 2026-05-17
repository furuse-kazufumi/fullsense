# China's Generative AI Regulation — Internal Use Pattern (operational docs, draft v0.1)

> **This document does NOT constitute legal advice / 法律建议 / 法的助言.**
> Each organisation must confirm with its own legal department or a
> qualified China-licensed practitioner. Draft v0.1, 2026-05-18 — content
> may change as the regulatory landscape evolves.

## 1. Regulations in scope

This document summarises how the following PRC regulations apply when an
enterprise deploys FullSense (llmesh / llive / llove) for **internal,
non-public AI use** — and explains why this pattern is typically exempt
from the headline filing requirements.

| Regulation (zh) | Regulation (en) | Effective | Relevance |
|---|---|---|---|
| 《生成式人工智能服务管理暂行办法》 | Interim Measures for the Administration of Generative AI Services | 2023-08-15 | primary |
| 《互联网信息服务算法推荐管理规定》 | Algorithm Recommendation Provisions | 2022-03-01 | primary |
| 《互联网信息服务深度合成管理规定》 | Deep Synthesis Provisions | 2023-01-10 | related |
| 中华人民共和国网络安全法 (amended) | Amended Cybersecurity Law (adds an AI compliance clause) | 2026-01-01 | related |
| 《人工智能拟人化互动服务管理暂行办法》 | Interim Measures on AI Anthropomorphic Interaction Services | 2026-07-15 (planned) | related |

## 2. Public service vs. internal use

### 2.1 Public-facing services (filing required)

The Interim Measures Article 2 defines the scope as anyone "providing
generative AI services to the public **within the territory of the PRC**."
Algorithm filing (算法备案) and security assessment requirements are
triggered for services that exhibit "public opinion attributes or social
mobilisation capacity" — typically:

- forums, blogs, microblogs, chat rooms, communication groups
- public accounts, short video, live streaming
- information sharing platforms, mini-programs
- any internet service that opens an expression channel to the general
  public or has the capacity to mobilise public activity

### 2.2 Internal use (filing exempt)

Article 2(3) explicitly **excludes** the following from the Measures:

> "Industry units, enterprises, educational and research institutions,
> public cultural institutions, and relevant professional organisations
> that develop or apply generative AI technology **without providing
> generative AI services to the domestic public** are not subject to
> these Measures."

In other words, **if your AI is used only by your employees and the
generated content stays inside your organisation**, algorithm filing and
security assessment are not required.

### 2.3 Boundary guidance

Typical internal-use patterns (likely filing-exempt):

- Generative AI accessed **only by employees**, with outputs flowing
  into internal systems (wiki, code, design docs, business memos)
- Internal R&D, prototyping, or knowledge management
- Cross-department / cross-site internal automation
- Note: if you later open the service to the public, filing obligations
  attach at that moment.

Public-service patterns (filing required):

- Consumer-facing chatbots / answer engines
- Public web AI features
- AI services that external partners or customer employees access
- API-form services exposed externally
- "Internal-only" facades that in practice allow wide public access

Grey areas (each org must verify):

- B2B SaaS used by customer-org employees only
- Subsidiary / affiliate access
- Business-partner staff access under a defined contract

## 3. FullSense usage patterns

### 3.1 Typical (internal use, exempt)

- **llmesh** deployed on-prem as the company's internal LLM hub for
  staff productivity.
- **llive** generating internal documents, code, briefs — outputs stay
  in internal systems.
- **llove** as the per-developer dashboard / observation IDE.

These map to the filing-exempt pattern provided the org's actual
access controls match the description.

### 3.2 Public-service conversions (filing required at the switch)

If you later expose any of the above to the public web, partner
customers, or general consumers, filing obligations attach at the
moment of conversion. Plan the transition with counsel.

### 3.3 FullSense architecture-level coverage

| Requirement (also useful for internal use) | FullSense feature | Status |
|---|---|---|
| Audit log (Amended Cybersecurity Law 2026-01) | llmesh + llive audit log + Approval Bus | partial |
| Human oversight | llive HITL Approval Bus | shipped |
| Output provenance tracking | llive OKA-FX + Annotation Channel | partial |
| Cross-border data control | on-prem-only architecture | shipped |
| Public-service safety assessment report | (only needed if you go public) | not implemented (low priority) |

## 4. Recommended operating practices

These guidelines help an organisation **stay within the filing-exempt
internal-use pattern**.

### 4.1 Access control

- Deploy AI services behind the **corporate network / VPN**.
- Authenticate via internal SSO / LDAP / Active Directory.
- If partner access is required, gate it through an explicit contract +
  access log.
- Do not expose APIs externally without filing in place.

### 4.2 Audit logging

- Retain every AI request / response for **at least 6 months** (Amended
  Cybersecurity Law); 6 years if you also operate under EU AI Act.
- Wire llmesh audit log + llive Approval Bus log into the production loop.
- Sample-review logs through legal / audit functions periodically.

### 4.3 Keeping outputs internal

- Establish a policy that **generated content is not published publicly
  without human review**.
- Use the HITL Approval Bus as the chokepoint between "generated" and
  "published."
- Internal wiki / docs / code ingestion is fine; direct push to public
  web requires review.

### 4.4 Regulation watch

- Track amendments to the Cybersecurity Law (2026-01) and the upcoming
  AI Anthropomorphic Interaction rule (2026-07-15) through legal.
- Update operating policies as the regulatory text evolves.

## 5. When you DO go public (reference, not how-to)

If a public-service transition is planned, prepare for:

- Algorithm filing (算法备案) within 10 business days via CAC's online
  registration system.
- Security assessment (安全评估) for "public opinion / social
  mobilisation" services.
- Large-model filing (大模型备案) if applicable.
- Terms of service, complaint mechanism, content review pipeline,
  real-name authentication.
- Deep-synthesis labels (深度合成标识) for AI-generated media.

As of 2025-12-31, the CAC public records show **748** registered
generative AI services and **435** registered apps / features.

## 6. Checklist for each organisation

- [ ] Confirm AI usage is **not** "providing to the domestic public."
- [ ] Confirm subsidiary / affiliate / partner access does **not**
      constitute "public."
- [ ] Comply with the AI clause in the Amended Cybersecurity Law (audit
      logs etc.).
- [ ] Prepare for the AI Anthropomorphic Interaction rule (2026-07-15)
      if you ship human-like dialogue agents.
- [ ] Check sector-specific overlays (finance, healthcare, education,
      government).
- [ ] Cross-border data export controls (personal information,
      important data).
- [ ] Industry association / regulator guidance.

## 7. References (official + secondary)

### 7.1 Official

- 《生成式人工智能服务管理暂行办法》(CAC):
  https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm
- 《互联网信息服务算法推荐管理规定》(CAC)
- 《互联网信息服务深度合成管理规定》(CAC)
- 《人工智能拟人化互动服务管理暂行办法（征求意见稿）》(CAC, 2025-12):
  https://www.cac.gov.cn/2025-12/27/c_1768571207311996.htm

### 7.2 Secondary (commentary)

- White & Case "AI Watch: Global regulatory tracker — China"
- IAPP "Global AI Governance Law and Policy: China"
- ICLG 2026 Cybersecurity Laws — Generative AI in China
- China Briefing "Interpreting China's Generative AI Measures"
- Securiti "Navigating China's AI Regulatory Landscape"

## 8. Revision history

- 2026-05-18 — draft v0.1 (en) authored alongside the Japanese version
  (cn-internal-use.md).

## 9. Localisation roadmap

- ja: `cn-internal-use.md` (draft v0.1)
- en: this document (draft v0.1)
- zh: planned (Week 4 of v3.2 roadmap)
