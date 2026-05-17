# LinkedIn 게시물 — 2026-05-17 엔지니어 요약 (한국어판)

🚀 **하루 만에 요구사항 32건 + 코드 2,200줄 + 테스트 78건 + 벤치마크 4종 — 자기 진화형 모듈식 메모리 LLM 프레임워크 llive 개발기**

오늘 (2026-05-17), 자기 진화형 모듈식 메모리 LLM 프레임워크 **llive** 가 다음과 같이 진행되었습니다.

✅ **Brief API end-to-end 완성** — 외부 클라이언트 (lldesign / lltrade / MCP) 가 구조화된 작업 단위를 전달할 수 있는 API. schema / loader / ledger / runner / CLI / MCP 를 한 세션 내에 구현 (5일 예상을 하루에 완주)
✅ **요구사항 32건 추가** — v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8
✅ **테스트 936 → 1,014 PASS / 0 fail / 0 regression**
✅ **벤치마크 4종 실시** — progressive matrix 15 셀 / fair 재실행 / quiz Debug + Release (평균 / 표준편차 통계 포함)
✅ **honest disclosure** — 초기 벤치에서 llive 134-184ms (4/4 OK) 라는 의심스러운 속도가 나왔으나, 조사 결과 LLMBackend 미연결로 인한 template fallback 임을 발견. 교훈을 memory 에 저장하고 fair 재실행 (32-51s) 결과를 공개

💡 **중요한 발견**: "llive 의 부가가치는 속도가 아니라 구조 (ledger / approval / governance / grounding / 6 stage trace)". 포지셔닝: "Qwen / Llama / Mistral 을 Local PC 에서 안전하고 책임감 있게 사용".

📊 **Progressive matrix 주요 결과** (xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b}, on-prem only):
- Brief API 오버헤드 < 1 %
- 전 15 셀 decision=note (loop 가 token 압력에 완전히 안정적)

🔗 상세 기사 (11 편 + 통합 2 편) 및 raw data:
<https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17>

#LLM #Agent #OnPrem #Ollama #Python

저자: 후루세 카즈후미 (puruyan)
