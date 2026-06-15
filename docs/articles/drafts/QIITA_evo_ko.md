---
title: lldarwin / 진화 arc 모음 — monoculture 진화 / 선택압 / 지휘자 합주 / 반증과 Goodhart / 진화 시각화 / Codex 양대 축 / llcore CPU 진화 × 제3의 축
tags: 解説, 進化計算, llive, FullSense, honest_disclosure
private: false
public_id: 951b94cf66d246723004
---

# lldarwin / 진화 arc 모음 — monoculture 진화 / 선택압 / 지휘자 합주 / 반증과 Goodhart / 진화 시각화 / Codex 양대 축 / llcore CPU 진화 × 제3의 축

<!-- TOPICNAV -->
> **🌐 언어**: [日本語](https://qiita.com/furuse-kazufumi/items/6e107c7dfa0c261ee4d7) | [English](https://qiita.com/furuse-kazufumi/items/e49b7ab9027d93594402) | [中文](https://qiita.com/furuse-kazufumi/items/93f3cf1bb7b14650bbca) | **한국어**
>
> **📚 FullSense 모음 시리즈**
> - [llcore 검증 arc 모음](https://qiita.com/furuse-kazufumi/items/a5ebb3992e4c28862f47)
> - **lldarwin / 진화 arc 모음（this）**
> - [llive 완전 해설 모음](https://qiita.com/furuse-kazufumi/items/c5f2077a3399d3fc9b26)
> - [llmesh 모음](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762)
> - [쉬운 설명 모음](https://qiita.com/furuse-kazufumi/items/e5093e4816b25c1bd4d0)
<!-- /TOPICNAV -->

## 목차

1. [AI를 500세대 진화시켰더니, 세계에 "나"와 "예측 부호화의 아버지 칼 프리스턴"만 남았다 #25 — monoculture의 honest disclosure와 선택압 컴포넌트 lldarwin](#제1장-ai를-500세대-진화시켰더니-세계에-나와-예측-부호화의-아버지-칼-프리스턴만-남았다-25--monoculture의-honest-disclosure와-선택압-컴포넌트-lldarwin)
2. [「안경으로 측정」하는 것만으로는 진화하지 않는다 — 선택압 컴포넌트 lldarwin의 설계와 실측 #26](#제2장-안경으로-측정하는-것만으로는-진화하지-않는다--선택압-컴포넌트-lldarwin의-설계와-실측-26)
3. [하룻밤 사이에 AI 진화를 다시 만들었다 — 실제 LLM 12h 런이 또 만점에서 포화되고, 6개의 PoC와 4개의 Agent와 Perplexity가 「독립적으로 같은 결론」으로 수렴한 밤 #27](#제3장-하룻밤-사이에-ai-진화를-다시-만들었다--실제-llm-12h-런이-또-만점에서-포화되고-6개의-poc와-4개의-agent와-perplexity가-독립적으로-같은-결론으로-수렴한-밤-27)
4. ["지휘자"가 끊임없이 진화하는 AI 집단을 합주시켜 답한다 — llive의 오케스트라형 진화, 그리고 포화를 고친 3가지 장치 #28](#제4장-지휘자가-끊임없이-진화하는-ai-집단을-합주시켜-답한다--llive의-오케스트라형-진화-그리고-포화를-고친-3가지-장치-28)
5. ["렌즈가 포화되면 선택압은 무력" — 진화 설계를 반증으로 단련한다 #29(Goodhart의 법칙과 proxy fitness의 한계)](#제5장-렌즈가-포화되면-선택압은-무력--진화-설계를-반증으로-단련한다-29goodhart의-법칙과-proxy-fitness의-한계)
6. [진화를 「보여주는」 기술의 계보 #30 — Conway 의 라이프 게임에서 3DGS 까지](#제6장-진화를-보여주는-기술의-계보-30--conway-의-라이프-게임에서-3dgs-까지)
7. [AI 에게 AI 를 부하로 부리게 하기 #31 —— Claude 주도 + Codex 배속의 「두 기둥」 개발 체제](#제7장-ai-에게-ai-를-부하로-부리게-하기-31--claude-주도--codex-배속의-두-기둥-개발-체제)
8. [(연재 #32) llcore CPU PoC battery 완성](#제8장-연재-32-llcore-cpu-poc-battery-완성)
9. [(연재 #33) 너무 깔끔한 결과는 승리가 아니라 경보 —— 제3축 ③ 을 proper power 로 결판낸 하루](#제9장-연재-33-너무-깔끔한-결과는-승리가-아니라-경보--제3축-③-을-proper-power-로-결판낸-하루)
10. [(연재 #34) 산오르기 6연전으로 알게 된 「진화의 ③은 언제 효과가 있는가」— 그리고 100년 전의 진화생물학이 같은 답을 내놓고 있었다](#제10장-연재-34-산오르기-6연전으로-알게-된-진화의-③은-언제-효과가-있는가-그리고-100년-전의-진화생물학이-같은-답을-내놓고-있었다)


---

## 제1장 AI를 500세대 진화시켰더니, 세계에 "나"와 "예측 부호화의 아버지 칼 프리스턴"만 남았다 #25 — monoculture의 honest disclosure와 선택압 컴포넌트 lldarwin

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::



> 📚 **연재 내비게이션（lldarwin 아크）**: #24-05 집단 진화 → **#25 본 글（monoculture의 실패）** → #26 설계 편 → #27 climax（실 LLM 포화→개방단 전환）。※ 각 글은 단독으로도 읽을 수 있습니다（링크는 회유용）。

> **콘셉트 hook**: llive의 파생 집단 진화에, 인물 persona를 8개 계통의 "씨앗"으로
> 뿌렸다. 후루세（=나）・프리스턴・밀리지・이소무라・오카 기요시・그로텐디크・
> 폰 노이만・파인만. 세계를 대표하는 8개의 지성이, 500세대를 싸워내고
> 살아남는 것은 누구인가——.
>
> 그 결과, 살아남은 것은 **나（52%）와 예측 부호화의 아버지 칼 프리스턴（48%）
> 두 사람뿐**. 오카 기요시도 그로텐디크도 폰 노이만도 파인만도,
> **단 한 명도 자손을 남기지 못하고 절멸했다.**
>
> ……이거, 감동적인 진화담처럼 들리나요? **아니요. 이것은 대실패의 기록입니다.**
> 진화가 "강한 자를 선택한" 것이 아니라, **선택압이 0이었던 탓에, 그저
> 운（유전적 부동）으로 2개 계통으로 치우쳤을 뿐**. 본 글은 그것의 honest disclosure와,
> "측정한다(lleval)" 다음에 필요한 "도태한다(lldarwin)" 컴포넌트의 설계 이야기다.

---

### 0. 세 줄로 줄거리（라쿠고에서 말하는 "도입부"）

- **한 일**: llive의 파생 집단 진화에 8명의 지성을 persona 씨앗으로 투입, rich-proxy 평가로 500세대 돌렸다.
- **일어난 일**: 1세대째에 best_score가 **1.0에 달라붙어**, 이후 줄곧 만점. 8개 계통이 **후루세 52% / 프리스턴 48%**의 2개 계통으로 수렴, 나머지 6명이 절멸.
- **진짜 원인**: "만점이 계속 나왔다"＝**선택압이 0**. 누구를 골라도 fitness는 같으므로, 진화는 실질적으로 주사위 던지기（유전적 부동）가 되어 있었다.

요컨대 **"전원 100점인 시험으로 석차를 정하려 했다"**. 그러니 누가
합격할지는 제비뽑기가 됩니다. 시험이 나쁘다. 안경(lleval)이 흐려져 있었다.

---

### 1. 왜 "인물"을 씨앗으로 뿌렸는가

llive의 진화 레이어 (v0.B〜v0.F)는, 1개의 LLM을 똑똑하게 하는 것이 아니라,
**N개의 llive 개체（genome）를 세대 교체시켜 서로 평가하게 하는** 파생 집단 진화입니다
（연재 #24-05에서 상술）.

그 genome에 "사고 버릇"을 초기 주입하는 구조가 **PERSONA_FX**.
"예측 부호화로 세계를 바라보는 Friston""침묵과 정서에서 수학을 세우는 오카 기요시"
처럼, **실재하는 지성의 인지 스타일을 genome의 factor_affinity（사고 인자에 대한
편향）에 사상**하여, 씨앗(founder)으로 뿌립니다.

뿌린 8개 계통:

| founder | 인지 스타일의 씨앗 |
|---|---|
| 후루세（나） | 내력 지향・원류 추적・현실 연결 |
| 칼 프리스턴 | 예측 부호화・자유 에너지 최소화 |
| 베렌 밀리지 | active inference의 구현 지향 |
| 이소무라 | （사용자 지정 persona） |
| 오카 기요시 | 정서・전체 직관・불확실성 수용 |
| 그로텐디크 | 추상화・일반화・구조의 발견 |
| 폰 노이만 | 형식화・계산・다영역 횡단 |
| 파인만 | 재구성・제일원리・직관적 검증 |

> 🍵 **휴식 포인트**: 여기까지 "8명의 천재가 VR 배틀로얄에 던져졌다"
> 라는 그림이 떠오르면 OK. 문제는, 이 배틀로얄의 **룰（평가 함수）이
> 망가져 있었다**는 것. 다음 절부터가 본론입니다.

---

### 2. 결과 — 살아남은 것은 2명뿐

500세대 후의 계통 점유율（max_lineage_share의 내역）:

```
후루세         ████████████████████████████  52%
프리스턴       ██████████████████████████    48%
밀리지         (절멸)
이소무라       (절멸)
오카 기요시    (절멸)
그로텐디크     (절멸)
폰 노이만      (절멸)
파인만         (절멸)
```

언뜻 보면 "예측 부호화(Friston)와 내력 지향(후루세)이, 추상 수학(그로텐디크)이나
형식 계산(폰 노이만)을 이겼다"라는 **이야기**를 쓸 수 있을 것 같습니다.

실제로 SNS라면 "AI를 진화시켰더니 예측 부호화가 최강이었다"라며 화제가 될지도 모른다.
**하지만 그것을 하지 않는 것이 FullSense의 honest disclosure 룰**입니다
（[[feedback_benchmark_honest_disclosure]]）. 비정상적으로 깔끔한 결과가 나오면,
이긴 기분이 되기 전에 내역을 의심한다.

의심한 결과가, 다음 절입니다.

---

### 3. 진짜 원인 — "만점 인플레"가 선택압을 지웠다

#### 3.1 증상: best_score가 1세대째부터 1.0

로그를 보면, **best_score는 제 1세대에서 이미 1.0**. 이후 500세대 줄곧 1.0.
진화 계산에서 fitness가 즉시 포화(plateau)하는 것은 전형적인 위험 신호입니다.

선택(도태)이란 "fitness의 차이로 부모를 고르는" 조작. 그런데 **전원이 만점**이면,
fitness의 차이는 생기지 않는다. 차이가 없으면, 토너먼트 선택도 룰렛 선택도
**실질적으로 랜덤 선택**으로 퇴화합니다.

이것이 **선택압 0**인 상태. 진화는 멈추고, 이후는 집단이 **유전적 부동
(genetic drift)**으로 제멋대로 치우쳐 갈 뿐. 8개 계통이 2개 계통으로 줄어든 것은
"강했기 때문"이 아니라, **단순한 확률적 빨려듦**이었습니다.

> 🤔 **비유（만담풍）**:
> 보케 "전원 100점인 반에서 반장을 선거했더니, 표가 갈려서 2명으로……"
> 츳코미 "그건 선거가 아니라 제비뽑기야!"
> ——진화에 일어난 것은, 바로 이 "제비뽑기화"입니다.

여기서 "유전적 부동（genetic drift）"이라는 말을 조금 정성껏. 생물학으로 말하면,
**선택압이 걸리지 않는 중립적인 유전자는, 세대를 거치는 사이 우연만으로 빈도가 치우쳐 간다**는 현상입니다.
작은 연못에 8색 금붕어를 풀어도, 아무도 먹히지 않으면, 몇 세대 후에는 **우연히 늘어난 2색**이
연못을 차지한다. 강했기 때문이 아니라, 주사위의 눈이 그렇게 굴렀을 뿐. 이번의 8→2는, 바로 이
"금붕어 뜨기 연못" 상태였습니다.

> 🤔 **비유（라쿠고풍）**:
> "핫쨩, 주사위 500번 던져서 제일 많이 나온 눈으로 대장 정하는 건 어떤가"
> "그건 실력이 아니지, 그냥 노름이올시다"
> "그렇지. 진화에 노름을 시킨 게, 이번 실패의 정체라네."

#### 3.2 근본 원인: 평가 함수 `fitness_rich`의 이중 붕괴

왜 만점이 계속 나왔는가. 코드를 따라가 보니, `fitness_rich`（rich-proxy 평가기）에
**2개의 설계 결함**이 있었습니다.

**결함 1 — factor_affinity를 전 층 동일 값으로 했다**
genome은 본래 "사고 인자 × 메모리 층"의 2차원 행렬로 개성을 가져야 한다. 그런데
archetype 생성 시 `np.tile`로 **factor_affinity를 전 메모리 층에 같은 값으로 복제**하고
있었다. 층별 차이＝개성의 절반이, 평가에 들어가기 전에 붕괴되어 있었다.

**결함 2 — nearest를 `max(sims)`로 단일 스칼라로 붕괴시켰다**
개체와 archetype의 가까움을, 복수 archetype와의 유사도 벡터에서
**`argmax`（=최대값 1개만）**으로 꺼내고 있었다. "어느 천재와 가장 닮았는가"만
보고, "다른 천재와 어떻게 다른가"를 전부 버린다. 결과, 조금이라도
어느 하나에 닮으면 고득점 → **즉시 천장에 달라붙는다**.

```
본래 그래야 할: pressure profile = [전형성, 다양성, 전문성, ...] ← 복수 축 벡터
실제 구현:      fitness = max(개체와 각 archetype의 유사도)        ← 단일 스칼라
                          ↑ argmax로 붕괴 = 다목적성이 소멸
```

즉 **"복수의 잣대로 측정해야 할 것을, 1개의 잣대의 최대값만으로 채점했다"**.
안경(lleval)의 렌즈가 1장뿐이고, 게다가 즉시 만점으로 치솟는 거친 렌즈였다.

> 🍵 **휴식 포인트**: 여기가 본 글의 클라이맥스. "결과가 치우친" 것이 문제가 아니라,
> **"결과를 치우치게 한 원인이 평가 함수의 붕괴"**였다는, 이 2단 구조를 깨달으면
> 이 글은 다 읽은 것이나 마찬가지입니다. 나머지는 "그럼 어떻게 고치는가".

---

### 4. 대책 — "측정한다" 다음은 "도태한다": lldarwin

llive 패밀리에는 이미 **lleval（안경 = 평가 프레임워크, 연재 #24-08）**가
있습니다. 이번에 알게 된 것은, **안경으로 차이를 "측정할 수 있었다"고 해도, 그 차이를
"누가 살아남는가"로 올바르게 변환하지 않으면 진화는 망가진다**는 것.

그래서 새 멤버 **lldarwin（선택압 = 도태 컴포넌트）**를 설계했습니다.
ll- 패밀리의 역할 분담은 이렇게 됩니다:

```
lleval   = 측정한다  （개체의 행동을 복수 축의 pressure profile로 변환）
lldarwin = 도태한다  （그 profile을 "다음 세대의 부모"로 변환）
```

#### 4.1 설계의 핵심 — "집약하지 않는" 선택압

이번 실패의 본질은 **"복수 축을 1 스칼라로 집약해서 argmax 했다"**는 것.
그래서 lldarwin의 제 1원칙은 **복수 선택압을 집약하지 않는 다목적 도태**입니다.

채용하는 3층 융합（rad-research로 evolutionary_computation 616건을 횡단하여 선정）:

1. **ε-lexicase 선택** — 평가 축을 하나씩 순서대로 독립 적용. 어떤 축에서 돌출한
   specialist（다른 축은 평범）도 살아남을 수 있다 → **다극 구조가 자동 유지된다**.
   그로텐디크가 "추상화 축"에서 1등이면, 설령 다른 축이 평범해도 사라지지 않는다.
2. **minimal-criterion QD (MAP-Elites)** — behavior 차원의 cell마다 elite를
   보유. **1 cell이라도 남으면 전멸하지 않는다**＝구조적으로 monoculture를 불가능화.
3. **down-sampling** — 매 세대, 평가 case의 부분 집합만 사용. 표적이 움직이므로
   특정 peak에 달라붙을 수 없다 → **plateau（만점 인플레）를 파괴**.

여기에 minimal-criterion gate（연속 순위가 아니라 "최저 기준을 충족하는가"로 번식 가부를
나눈다 = 일강 독식의 억제）와, per-dim z-score 표준화（"전 축 평균 높음"＝
무특징을 우위에 두지 않는다）를 더합니다.

#### 4.2 "LLM의 약점"을 선택압으로 한다

또 하나의 방침은, **LLM/VLM이 현실에서 약하고, 또한 측정 가능한 축**을 pressure로
고르는 것（검증할 수 없는 영역은 피한다）. 예:

| pressure | LLM의 약점 | proxy/실 |
|---|---|---|
| typo_robustness | 오타・노이즈 입력에 대한 일관성 | proxy 가（합성 typo 주입） |
| polysemy_wsd | 다의어의 문맥 의존 이해 | proxy 가（WSD bench） |
| multistep_robustness | 다단 추론의 cascade error | proxy 가 |
| calibration | 신뢰도 추정（token confidence ≈ random） | proxy 가 |
| visual_qa | 이미지 인식・visual hallucination | 실 VLM 필수（Stage 후반） |

proxy로 측정 가능한 축부터 PoC, 실 LLM/VLM 축은 후단, 이라는 측정 순도의 분리도
처음부터 설계에 넣고 있습니다（[[feedback_llive_measurement_purity]]）.

#### 4.3 전멸을 모니터한다 — SPC 알람

FullSense의 핵심 사상은 **SPC（통계적 공정 관리）**. lldarwin에서도
`max_lineage_share` / archive 성장 / behavioral diversity를 매 세대 기록하고,
**monoculture 비 > 0.8을 SPC_ALARM으로 검지**하여 cadence나 파라미터를
자동 조정합니다. 이번의 "8→2"를, 구조적으로 재발 불가능하게 하는 것이 목표입니다.

---

### 5. 교훈（honest disclosure로 남긴다）

- **비정상적으로 깔끔한 결과（best=1.0 즉시 포화, 2개 계통으로 수렴）는, 승리가 아니라 경보.**
  내역을 의심한 결과, 승자는 실력이 아니라 평가 함수의 결함이 낳은 환영이었다.
- **"측정한다"와 "도태한다"는 별개.** 안경(lleval)이 차이를 측정할 수 있어도, 그 차이를
  argmax로 1개로 붕괴시키면 도태는 망가진다. 도태기(lldarwin)는 집약해서는 안 된다.
- **실패를 지우지 않는다.** 이 500세대 run을 버리지 않고, lldarwin 배선 후에
  "오카 기요시・그로텐디크 등이 살아남는가"를 재실행으로 검증하는 **baseline**으로
  삼는다. 8→2가 개선되는지가 제 1의 합격 기준.

> **다음 예고**: lldarwin의 PoC Stage 0（proxy 축 + ε-lexicase 배선 + QD archive）을
> 구현해서, 같은 8 founder를 재실행한다. 이번에야말로 오카 기요시는 살아남을 수 있는가.
> "세계에 나와 프리스턴뿐"인 세계선을, 덮어쓰러 갑니다.
> （설계의 상세는 #26, 그 설계에 스스로 반증을 던지는 honest disclosure는 #27로 이어집니다.）

---

### 5.5. "안경"과 "도태기"의 2단 구조 — 왜 나누는가（심화）

본 글에서 가장 가져가 주었으면 하는 개념도가 이것입니다:

```
개체 ──▶ [ lleval = 안경 ] ──▶ pressure profile（복수 축의 case 벡터）
                                       │
                                       ▼
              [ lldarwin = 도태기 ] ──▶ 다음 세대의 부모
```

#25의 실패는, 이 2단의 **양쪽**이 망가져 있었던 데에 본질이 있습니다:

- **안경 측의 고장**: `fitness_rich`가 `nearest = max(sims)`로 복수 축을 1 스칼라로 붕괴시키고, 게다가 즉시 만점.
  → 측정하지 못하고 있다（차이가 보이지 않는 안경）.
- **도태기 측의 부재**: 애초에 집약하지 않는 다목적 도태（ε-lexicase / QD）가 **배선되어 있지 않았다**.
  → 도태할 수 없다（필터가 없다）.

중요한 것은 **어느 한쪽만 고쳐도 진화는 회복되지 않는다**는 것.
포화된 안경에 고급 도태기를 꽂아도 "차이 0"은 도태할 수 없고,
좋은 도태기가 없는 채 안경만 고쳐도 profile을 살릴 수 없다.
**"측정한다"와 "도태한다"는 다른 고장이고, 따로따로 고칠 필요가 있다** ——이것이 #25→#26의 다리 놓기입니다.
（"안경을 고치지 않고 도태기만 고급으로 해도 무익"하다는 반증은 #27에서 정면으로 다룹니다.）

> 🍵 **휴식 포인트**: 사진의 비유로 말하면, lleval은 "노출계", lldarwin은 "어느 컷을 채용할까".
> 노출계가 고장 나도 앨범은 못 만들고, 채용 기준이 없어도 앨범은 못 만든다. 양쪽 다 필요하다.

---

### 5.6. 도해 아이디어（투고 전 SVG화할 후보）

본 글을 "움직임으로 매료시키기" 위해 준비하고 싶은 그림（투고 전 SVG화）:

1. **계통 점유율의 붕괴 애니메** — 세대 축으로 8개 계통의 띠가 2개 계통으로 빨려드는 animated SVG（금붕어 연못 메타포）.
2. **best_score = 1.0 즉시 포화 그래프** — 제 1세대에 천장에 달라붙는 평탄선（선택압 0을 한눈에）.
3. **argmax 붕괴 도** — 복수 축 벡터 `[전형성, 다양성, 전문성, ...]`이 `max()`로 1개의 막대로 붕괴되는 before/after.
4. **2단 구조도** — §5.5의 "안경 → 도태기"를 hero 도로 animated화.
5. **ll- 패밀리 역할도** — lleval（측정）/ lldarwin（도태）/ llive（개체）의 관계를 1장으로.

> 이것들은 [[project_fullsense_animemd_branch_token_viz]]의 animated SVG 표현층（선언 애니메 → SMIL）에 실을 예정.

---

### 6. 관련

- 연재 #24-05「집단이 학습하는 AI」— 파생 집단 진화의 총괄（본 글의 전제）
- 연재 #24-08「안경을 만든다」— lleval（측정 측）
- 연재 #26「lldarwin의 설계」— 도태기의 다목적 도태 / ε-lexicase / QD（본 글의 속편）
- 연재 #27「안경이 흐려지면 도태도 무력」— 반증 조사・Goodhart's law（honest disclosure）
- 설계서: lldarwin（도태 측）— 본 글의 원천 소재
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(투고 전): hero SVG / theme SVG / 진행 badge / #24-05・#24-08・#26・#27의 Qiita URL cross-link -->

---

## 제2장 「안경으로 측정」하는 것만으로는 진화하지 않는다 — 선택압 컴포넌트 lldarwin의 설계와 실측 #26

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::



> **콘셉트 hook**: 전작 #25에서 저는 「AI를 500세대 진화시켰더니, 세계에 **저와 프리스턴만** 남았다」는 큰 실패를 공개했습니다.
> 오카 기요시도, 그로텐디크도, 폰 노이만도, 전부 진화 도중에 조용히 사라졌습니다. 원인은, 평가 함수(안경 = lleval)가 만점을 계속 내놓아서 **선택압이 0이 된 것**입니다. 누가 우수한지 「측정할 수 있어」도, 그 차이를 「누가 살아남는가」로 변환하지 못하면, 진화는 그저 유전적 부동(浮動)으로 전락합니다.
>
> 그렇다면 — 안경으로 차이를 「측정했다」고 했을 때, 그 차이를 「도태」로 **올바르게 변환하는 장치**는 어떻게 만드는가.
> 그것이 이번 주역, **lldarwin**입니다. ll- 패밀리의 새 멤버로, **도태(선택압) 전문** 컴포넌트입니다.
>
> 이 글에서 기억해 주었으면 하는 키워드는, 단 한 단어. **「집약하지 않는다」**. 여러 잣대를 하나로 합산한 순간, 진화는 망가집니다. 왜 그렇게 되는지, 그리고 어떻게 실측으로 그것을 넘어섰는지 — 실패의 연장에서, 이번에는 **실제로 작동한** 이야기를 합니다.

---

### 0. 세 줄 줄거리(라쿠고의 「마쿠라」)

라쿠고에는 본론 전에 「마쿠라(枕)」가 있습니다. 우선 세 줄로 전체상을.

- **lleval이 측정하고, lldarwin이 도태한다** — 진화는 「측정한다」와 「도태한다」의 2단 구조로, 비로소 의미를 가진다.
- 도태의 제1원칙은 **여러 선택압을 집약하지 않는 다목적 도태**. #25의 실패(단일 스칼라의 argmax로 짓눌렀다)의 진짜 원인을, 여기서 구조적으로 끊는다.
- 채택한 3대 기둥 = **ε-lexicase + minimal-criterion QD + down-sampling**(evolutionary_computation 코퍼스 616건을 횡단 조사하여 선정).

그리고 이번에는 골격뿐 아니라 **실측이 있다**는 것이 #25와의 차이입니다. novelty pressure로 행동 다양성을 7.12 → 14.88(+109%)로 2배로 늘리고, **중립 저장고**로 「멸종한 오카 기요시·그로텐디크 계통」을 실제로 **전원 부활**시키고, 마지막으로 **온프레미스의 진짜 LLM(llama3.2)**을 상대로, prompt 전략을 진화시켜 약한 태스크를 0.0 → 1.0으로 개선시켰습니다. 차례차례 살펴봅니다.

---

### 1. 왜 「측정한다」와 「도태한다」를 나누는가

llive 패밀리에는 이미 **lleval(안경 = 평가 프레임워크, 연재 #24-08)**이 있습니다. 개체의 행동을 관측하고, 여러 축에서 점수화하는 장치입니다.

그런데 #25에서 알게 된 것은 치명적인 진실이었습니다. **안경으로 차이를 측정할 수 있어도, 그 차이를 argmax로 하나로 짓누르면 도태가 망가진다.** 구체적으로, `fitness_rich`가 여러 archetype 유사도를 `nearest = max(sims)`라는 단일 스칼라로 접고 있었습니다. 이것이 SEL-2 위반 — 「best=1.0이 포화하고, 전원이 만점이 되어, 선택 기울기가 사라진다」는 진짜 원인입니다.

역할을 명확히 나누면, 이렇게 됩니다.

```
lleval   = 측정한다 (개체의 행동을 「다축의 pressure profile」로 변환)
lldarwin = 도태한다 (그 profile을 「다음 세대의 부모」로 변환)
```

`lleval`의 출력은 **case 벡터**(각 축의 점수가 나열된 배열)입니다. `lldarwin`은 그것을 입력 계약으로 받아서, **집약하지 않고** 도태합니다. 양자의 책임 경계는 바로 여기에 있습니다. lleval이 「축을 하나로 합산한 뒤에」 넘겨오면, lldarwin은 아무것도 할 수 없습니다. 그래서 lleval 쪽에는 「breakdown(축별 내역)을 반드시 보존해서 넘긴다」는 것을 계약으로 부과합니다.

lldarwin의 `Pressure` 인터페이스는, 다음의 최소 계약으로 표현됩니다.

- `name` — 축의 이름(`typo_robustness` 등)
- `evaluate(individual_output) -> case_scores: list[float]` — 개체의 행동을 「축별 점수 배열」로 변환
- `is_proxy: bool` — proxy 측정인지, 실제 LLM/VLM 측정인지(측정 순도의 구분)
- `minimal_criterion: float | None` — 그 축의 최저 번식 기준(None이면 gate 없음)

포인트는, `evaluate`의 반환값이 **스칼라가 아니라 리스트**라는 것입니다. 한 축 안에도 여러 case(테스트 케이스)가 있고, 그것을 짓누르지 않고 lldarwin으로 흘려보냅니다. 이 「짓누르지 않는」 설계가, 나중에 specialist를 구하는 복선이 됩니다.

> 🍵 **휴식 포인트**: 안경(lleval)과 필터(lldarwin)를 나누는 의미는, 사진으로 말하면 「노출을 측정한다」와 「어느 컷을 채용할지 정한다」의 차이입니다. 측광이 완벽해도, 베스트 샷의 선택을 틀리면 앨범은 엉망입니다. 노출계(lleval)가 「이 한 장은 밝기 80점, 구도 30점, 표정 95점」이라고 알려줘도, 그것을 「평균 68점」으로 반올림해서 버리느냐, 「표정 95점인 한 장은 별도 칸에 남기느냐」에 따라, 앨범의 풍부함은 천지 차이로 달라집니다. lldarwin은 「채용 판단」의 전문가입니다. 측정하는 사람과 고르는 사람을 한 사람이 겸임하면, 대개 양쪽 모두 엉성해집니다.

---

### 2. 설계의 핵심 — 「집약하지 않는」 7 스테이지

lldarwin은, lleval로부터 받은 pressure profile(다축의 case 벡터)을, 다음의 7 스테이지로 도태합니다. 각각에 「왜 필요한가 = 어떤 실패를 막는가」를 덧붙입니다.

1. **Standardizer** — per-dim z-score. 「전 축이 평균적으로 높다」는 것만의 무특징한 우등생을 우대하지 않고, 각 축에서의 **일탈**을 선택압으로 바꾼다. 중앙 일치(모두와 같음)는 제외.
   - *막는 실패*: 「평균점이 높을 뿐」인 평범함이 이기고, 뾰족한 개체가 사라지는 monoculture의 입구.
2. **MinimalCriterionGate** — 각 축의 최저 기준으로 번식 가부를 가른다. 연속 순위만으로 「독식」시키지 않는다.
   - *막는 실패*: 일강(一強)이 모든 번식 슬롯을 독점하는 전멸 시나리오. 기준을 충족하면 누구든 번식할 수 있는 「최저 보장」으로 다양성의 토대를 남긴다.
3. **EpsilonLexicaseSelection** — 축을 case로서 하나씩 독립적으로 평가한다. 어떤 축에서 돌출한 specialist(다른 축은 평범)가 살아남을 수 있다.
   - *막는 실패*: 집약 argmax에 의한 specialist의 절멸. 이것이 #25의 8→2를 낳은 메커니즘 그 자체.
4. **QD / MAP-Elites archive** — pressure profile을 behavior 기술자로 변환하고, cell마다 elite를 보존. archive는 단조 증가.
   - *막는 실패*: 구조적인 전멸. 하나의 cell에 한 개체라도 남으면, 그 행동은 사라지지 않는다.
5. **Niching / FitnessSharing** — 같은 niche의 개체를 down-weight하여, 다봉(多峰)을 병존시킨다.
   - *막는 실패*: 단봉으로의 응집(monoculture).
6. **Down-sampling** — 매 세대, case의 부분집합만으로 평가하여 환경을 교란한다.
   - *막는 실패*: 특정 peak로의 과적합과 plateau(정체 고원). moving target으로 만들어 「같은 방식으로 이기는 것」을 허용하지 않는다.
7. **NoveltyScorer** — 정체 시에 「과거와 다른 행동」으로 탐색압을 가한다.
   - *막는 실패*: 탐색 고갈. 개선이 멈췄을 때, 새로움 자체를 보상으로 삼아 바깥으로 밀어낸다.

#25의 8→2 monoculture와 대비하면, 핵심은 세 가지: **(3) ε-lexicase·(4) QD archive·(2) minimal-criterion**입니다. #25에서는 이것들이 전부 빠진 채 단일 스칼라 argmax만 돌고 있었습니다. 그래서 「평균적으로 최강인 1 계통」이 연속 순위를 독식하고, 나머지가 부동으로 사라졌습니다. lldarwin은 이 세 가지를 「집약하지 않고 묶음」으로써, 세대를 거듭해도 파탄나지 않는 구조를 만듭니다.

> 🤔 **비유(만자이 풍)**:
> 보케 「시험 점수를 전부 더해서 순위를 매겼더니, 평균점이 높을 뿐인 우등생만 남았어.」
> 츳코미 「그거 다양성 제로잖아! 수학만 100점·나머지 0점인 천재가 사라졌잖아!」
> 보케 「아니, 토탈로 보면 우등생이 위인데……」
> 츳코미 「**토탈로 보지 마!** 과목을 하나씩 보면, 그 천재는 『수학』 case에서는 누구한테도 안 져. ε-lexicase는 그걸 구하는 구조야. 합산한 순간 천재는 죽어.」
> ——합산(집약)이 specialist를 죽인다. ε-lexicase는 「과목을 하나씩 본다」니까, 뾰족한 녀석이 남는다. 이것이 lldarwin의 제1의 핵심입니다.

---

### 3. 왜 이 3대 기둥인가(rad-research의 뒷받침)

「세대를 거듭해도 파탄나지 않는」 가장 유력한 융합안으로, evolutionary_computation 코퍼스 616건을 횡단 조사하여 선정했습니다. 자체 발명한 것이 아니라, 기존 연구의 「집약하지 않는」 계보를 선별하여 묶었다 — 는 내력이 중요합니다.

| 기법 | 효능 | 출처 |
|---|---|---|
| **ε-lexicase** | specialist 보존·high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | cell별 elite로 전멸 불가 | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | 환경 교란·비용 절감 | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | 조기 수렴 방지(장래 옵션) | Lyu 2020 (2005.07376) |

3대 기둥은 제각각인 기법으로 보이지만, 실은 **「집약하지 않는다」는 하나의 사상**으로 꿰뚫을 수 있습니다. ε-lexicase는 「축을 집약하지 않는다」. QD는 「행동 공간을 집약하지 않는다(cell마다 보존)」. down-sampling은 「평가 환경을 고정하지 않는다(매 세대 교란)」. 어느 것도 「하나로 둥글리지 않는다」는 점에서 같은 철학입니다. 그래서 조합해도 사상이 충돌하지 않고, 상승 작용합니다.

> 🍵 **휴식 포인트**: 「왜 자체 발명하지 않느냐?」는 질문을 받습니다. 답은 단순한데, **기존 연구의 조합으로 충분히 강하기 때문**입니다. 제 개발 규칙([[feedback_originality_over_imitation]])에는 「외부 알고리즘의 채용은 망라가 아니라 **선별**. 파탄 리스크나 단순한 모방은 배제하고, 독자 설계에 가치를 더하는 것만 채택한다」고 되어 있습니다. lldarwin의 독자성은 「새로운 선택 알고리즘을 발명한 것」이 아니라, 「이것들을 **집약하지 않고 묶는 묶음 방식**과, 그것을 llive의 진화 루프에 **실제로 배선한 것**」에 있습니다. 요리로 말하면, 세계 최초의 식재료를 만드는 것이 아니라, 기존의 명품 식재료를 「섞지 않고 한 접시에 담는」 기술입니다. 섞으면 망가지는 재료를, 섞지 않고 공존시킨다.

---

### 4. Stage1 — criteria 제외 + novelty pressure로 행동 다양성을 2배로

여기서부터 실측입니다. Stage1에서는, 설계를 단숨에 전부 구현하지 않고, 가장 효과가 있을 것 같은 두 가지 변경만 넣어서 측정했습니다(llive, branch `optimize/core-2026-05-20`, commit `8060204`).

**변경 1: criteria 제외.** ε-lexicase의 case에서, `factor_score`(= max-archetype의 단일 스칼라 = argmax, 바로 #25의 best=1.0 포화의 진짜 원인)와 `nearest_persona_idx`(= 순서에 의미가 없는 카테고리 index)를 뺐습니다. 이것은 「나쁜 잣대를 도태의 판단 재료에서 제거하는」 청소입니다.

**변경 2: novelty pressure.** `MultiPressureSelector(use_novelty=True)`를 활성화. 매 세대, 과거 세대의 archive와의 k-NN 평균 거리(Lehman-Stanley 류의 novelty)를 계산하고, 그것을 집단 내에서 z-score화(STD-1)하여, 추가의 lexicase case로 도태에 섞습니다. 「모두와 다른 행동을 하고 있다」는 것 자체를, 축의 하나로 평가합니다.

테스트는 `tests/unit/test_evolutionary_lldarwin.py`를 8 → 10건으로 확장(제외·novelty 보존을 추가). 진화계 847건 green, 회귀 없음.

실측 조건은 rich-proxy, 8 founders + pop24, 150세대, seed 0. 결과가 아래입니다.

#### 4.1 행동 다양성 (diversity_l2) — novelty가 듣는 지표

| 조건 | mean | tail30 min | final |
|---|---|---|---|
| BASELINE(제외 전·Tournament 상당의 구 lldarwin) | 7.12 | 0.68 | 0.83(붕괴) |
| A: criteria 제외만 | 9.16 | 1.57 | 1.57 |
| **B: 제외 + novelty** | **14.88(+109%)** | **6.56(9.6×)** | **11.73(붕괴 회피)** |

novelty pressure는, 행동(genome 공간)의 다양성을 약 2배로 유지하고, 종반의 다양성 붕괴를 막았습니다. criteria 제외만으로도 단독으로 효과가 있습니다(spurious한 argmax 압을 제거한 만큼). BASELINE은 final 0.83에서 **붕괴**하고 있는 데 반해, B 조건은 final 11.73에서 **버티고 있습니다**. 이것이 「집약하지 않는」 설계의 첫 번째 손맛입니다.

![Stage1 baseline(novelty 없음)의 적응도와 다양성. 종반에 다양성이 붕괴한다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_ko.svg)

![Stage1 novelty 있음. 다양성이 종반까지 유지된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_ko.svg)

두 장을 나란히 놓으면, 종반의 거동 차이가 한눈에 보입니다. baseline은 다양성 곡선이 바닥에 달라붙는 데 반해, novelty 있음은 높은 수준을 유지한 채 끝까지 달립니다.

> 🍵 **휴식 포인트**: novelty pressure를 금붕어 연못에 비유하면 — 먹이(높은 fitness)에 몰리는 금붕어만 남기면, 머지않아 전원이 같은 장소에서 같은 움직임을 하는 연못이 됩니다. novelty pressure는 「**모두와 다른 장소를 헤엄치는 금붕어에게도 보너스**」를 주는 담당입니다. 결과, 연못 여기저기 흩어진, 봐도 질리지 않는 연못이 됩니다. 다만 여기서 방심하면 안 됩니다. 다음 절에서, 이 「북적이는 연못」에 숨어 있던 **함정**이 발견됩니다.

---

### 5. honest disclosure(가장 중요) — 행동 다양성과 계통 생존을 저는 혼동하고 있었다

여기가 본 글에서 가장 중요한 절입니다. 좋은 숫자(+109%)가 나왔다고 해서, 이긴 기분이 되지 않는다 — 이것은 제 철칙([[feedback_benchmark_honest_disclosure]])입니다. 내역을 의심했습니다. 그리고, 잘못을 발견했습니다.

#### 5.1 계통 고정 (founder_counts) — novelty로는 개선되지 않는 지표

같은 실측에서, 다른 지표를 봅니다. 「8명의 founder(조상 계통) 중, 몇 계통이 끝까지 살아남았는가」.

결과는 — **전 조건에서 최종적으로 8 → 2 계통**(furuse-kazufumi + friston)으로 수렴. oka-kiyoshi(오카 기요시) / grothendieck(그로텐디크) / von-neumann / feynman / millidge / isomura는, **전부 멸종**.

novelty를 넣어서 행동 다양성을 2배로 했는데도, **계통의 생존은 #25와 완전히 같은 2 계통**이었던 것입니다.

#### 5.2 왜인가 — 저는 두 개의 「다양성」을 혼동하고 있었다

설계서(#25 시점)의 TODO에는 「재실행에서 오카 기요시·그로텐디크 계통이 살아남는지 검증」이라고 적혀 있었습니다. 이것은 **행동 다양성과 계통 생존을 혼동하고 있었던** 것입니다.

`poc_evolution_env.py`의 저자 코멘트(L129-132)가, 이 혼동을 정확하게 짚고 있습니다.

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

풀어서 말하면, 이렇습니다.

- 실증된 monoculture 0.05는, **행동적**(archive-cell의 점유율)이지, **계통적이지 않습니다**. novelty/lexicase가 개선하는 것은 「행동의 퍼짐」이지 「조상의 생존」이 아닙니다.
- 계통 고정이 중립 부동(기무라 모토오의 중립 진화설)에 의해 monoculture로 향하는 것은, **이론적으로 정상**입니다. 붕괴가 아닙니다. novelty도 lexicase도, **기존 개체를 보존하는** 메커니즘밖에 갖지 않으며, **한 번 멸종한 계통을 부활시키는 메커니즘을 갖지 않습니다**. 그래서 계통 고정은 구조적으로 막을 수 없습니다.
- 게다가, archetype 간 거리도 0.068~0.29로 압축되어 있어서(유사도가 0.71~1.0에 밀집), 선택 기울기가 약하고 drift(부동)가 지배적입니다. friston은 가장 비중심적(centroid 거리 0.162)인데도 살아남았다 = 중심성(강함)이 아니라, **운(drift)**으로 2 계통이 고정된 것입니다.

즉 — 「오카 기요시·그로텐디크가 살아남았으면」 하는 저의 바람은, **행동 다양성을 올리는 약으로는 절대 낫지 않는 병**이었습니다. 약을 잘못 쓰고 있었습니다. 이것은 정직하게 기록할 가치가 있는 교훈입니다.

> 🍵 **휴식 포인트**: 만자이로 말하자면.
> 보케 「연못에 형형색색의 움직임을 하는 금붕어를 늘렸어! 다양성 완벽이야!」
> 츳코미 「그래서, **혈통**은? 8개 있던 금붕어 가문, 몇 개 남았어?」
> 보케 「……2개야.」
> 츳코미 「움직임은 화려한데 가계도는 텅 비었잖아! 움직임의 다양성과 혈통의 다양성은 **별개의 이야기**라고!」
> ——「행동이 다양」과 「계통이 다양」은, 겉모습이 닮았을 뿐인 완전히 다른 지표. 저는 이것을 혼동하고 있었습니다. 정직하게 공개합니다.

---

### 6. Stage1.5 — 중립 저장고로 멸종한 계통을 되살리다

병의 정체를 알면, 약을 바꿀 수 있습니다. 계통 생존에 필요한 것은 「멸종한 계통을 매 세대 re-inject하는 메커니즘」 — **lineage-niched 중립 저장고(reservoir)**입니다.

#### 6.1 우선 PoC로 메커니즘을 확인한다

곧바로 본 루프를 개조하지 않고, 우선 standalone PoC로 메커니즘이 도는지 확인했습니다([[feedback_poc_feasibility_first]] = 요건 → PoC → 타당성 → 상세 설계, llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`).

selection은 Stage1의 `MultiPressureSelector`(criteria 제외 + novelty)를 그대로 씁니다. fitness는 rich-proxy. 계통은 parent_a로부터 상속. **reservoir = 계통별 best-ever genome을 보존하고, 멸종한 계통을 매 세대 re-inject한다**(낮은 score의 자식을 치환. best는 망가뜨리지 않는다). 8 founders + pop24 + 150 gens + seed 0으로 측정했습니다.

| reservoir | 최종 named 계통 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1**(oka-kiyoshi 24/24 = 완전 monoculture) | 1.00 | 1.58 |
| **ON** | **8(전 founder 생존)** | **0.31(≪ 0.8 OE-3)** | 1.69 |

reservoir ON에서, 오카 기요시(oka)·그로텐디크(grothendieck)를 포함한 **전 8 계통이 생존**. 최종 shares는 friston 7 / furuse 6 / grothendieck 4 / oka 3 / 다른 4 계통 각 1. **강한 계통은 자손을 갖고 번식하고, 약한 계통은 저장고가 생명 유지한다**는, 이상적인 거동입니다. 행동 다양성도 저하 없음(1.69 vs OFF 1.58).

**Honest 유보(PoC 단계)**: 저장고는 frozen elite(동결된 대표)를 재투입하므로, 약한 계통(각 1체)의 「생존」은 재투입에 의한 것이지, 능동적 진화는 아닙니다. 이것은 중립 저장고의 정의대로(대표를 보존하고, 재결합 가능하게 한다)로 정당하지만, 「약한 계통이 활발하게 계속 진화한다」고는 주장하지 않습니다.

#### 6.2 본 EvolutionLoop에 편입(additive + default-off)

PoC로 메커니즘이 확인되었으므로, 본 `EvolutionLoop`에 편입했습니다(commit `b03cbda`). 설계의 핵심은 **additive이며 default-off** — 기존 거동을 일절 바꾸지 않고, 플래그를 세웠을 때만 유효해집니다. 하위 호환을 사수했습니다.

- `EvolutionLoop.on_population_bred` hook을 추가(breed 직후·평가 전에 bred 리스트를 변환 가능. 기본 None = 하위 호환).
- `LineageReservoir`(`lineage_reservoir.py`): 조상 추적(parent_ids[0]을 상속) + 계통별 best-ever 보존 + 멸종 보호 계통의 re-inject. `founder_map`을 공유하고 계통 로그와도 정합.
- `run_persona_evolution(lineage_reservoir=True)` / run 스크립트 `--lineage-reservoir`를 추가.
- tests: `test_evolutionary_lineage_reservoir.py` 6건 + 진화계 **937 green**(회귀 없음).

실 EvolutionLoop에서의 실측(rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0).

| 조건 | named 계통 생존 | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8(furuse 17 + friston 7) | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8(전 계통)** | **0.33** | **0.29(≪ 0.8 OE-3)** | 9.20 |

오카 기요시(oka 3)·그로텐디크(grothendieck 1)를 포함한 **전 8 계통이, 실 루프에서 생존**했습니다. PoC의 예측(fixation 0.31)을, 본 구현이 0.29로 재현했다 — 메커니즘이 설계대로 작동한 증거입니다.

이것이, 본 글 최대의 볼거리입니다. 아래 두 장을 비교해 보세요.

![중립 저장고 OFF. 계통 지배 스트림이 최종적으로 furuse 71% / friston 29%의 2 계통으로 붕괴한다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_ko.svg)

![중립 저장고 ON. 전 8 계통(millidge / von-neumann / oka / grothendieck 등)이 병존한다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_ko.svg)

OFF(위)는, 세대가 진행됨에 따라 스트림이 2색으로 삼켜져 간다 — 「저와 friston만 남았다」는 #25의 재현입니다. ON(아래)은, 8색이 끝까지 띠로서 남습니다. 오카 기요시도 그로텐디크도, 사라지지 않았습니다.

![중립 저장고 ON의 적응도와 다양성](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status_ko.svg)

> 🍵 **휴식 포인트**: #25에서 「저와 프리스턴만 남았다」고 한탄했던, 그 쓸쓸한 세계. 그것이 이번에는 오카 기요시도 그로텐디크도 폰 노이만도 전원 있는, 북적이는 세계로 바뀌었습니다. **이것은 날조가 아니라, 실제로 작동한 결과입니다**([[feedback_benchmark_honest_disclosure]]에 따라, 거짓 실패도 거짓 성공도 쓰지 않습니다). 다만 — 들뜨기 전에, §5에서 배운 자세를 떠올립시다. 「좋은 숫자가 나오면 내역을 의심한다」. 다음 §6.3에서, 이 성공에도 **대가**가 있었음을 정직하게 씁니다.

#### 6.3 Honest 유보 — 계통 보존과 행동 다양성은 약한 트레이드오프

reservoir ON에서 계통은 전원 살아남았습니다. 하지만 잘 보면 **diversity_l2는 14.88 → 9.20으로 저하**하고 있습니다. frozen elite(동결 대표)를 매 세대 재투입하는 만큼, genome 공간의 퍼짐이 다소 줄어드는 것입니다.

다만, OFF 시의 붕괴(final 0.83)는 회피하고 있습니다. 즉 「계통 보존을 취하면, 행동 다양성의 피크는 조금 내려가지만, 붕괴는 막을 수 있다」는 **약한 트레이드오프** 관계입니다. 대가 제로의 마법은 아닙니다. 이것을 정직하게 적어 둡니다. 그리고, 이 대가를 어디까지 작게 할 수 있는가가, 다음 sweep의 주제가 됩니다.

---

### 7. 재투입 빈도 sweep — 비단조적 최적점이라는 비자명한 발견

§6.3의 honest 유보(frozen elite 재투입으로 diversity가 내려간다)를, `reinject_interval`(재투입을 하는 세대 간격. 기본 1 = 매 세대)의 sweep으로 특성화했습니다(commit `da93dd3`). `LineageReservoir.reinject_interval` + `--reinject-interval` 플래그를 추가(test 7건). 8 founders / pop24 / 150gens / seed0.

| interval | named 생존 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**(매 세대) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84(최대)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**여기서 비자명한 발견이 있었습니다.** 직관적으로는 「재투입을 줄이면(interval을 올리면), frozen elite의 밀어넣음이 줄어서 diversity가 단조적으로 회복된다」고 예상하시죠? 그런데 — **diversity는 단조 증가하지 않고, interval=5에서 피크**를 찍고, 10/20에서는 오히려 저하했습니다.

이유를 생각하면 납득이 갑니다. 계통을 너무 방치하면(interval이 너무 크면), (a) 저장고 유래의 다양성 주입이 줄고, (b) 소수 계통이 고정되어 버려서, 결국 diversity도 늘지 않습니다. 「재투입 과다」도 「방치 과다」도 둘 다 안 되고, 중간에 최적점이 있습니다. 이것은 **실제로 sweep을 돌리지 않으면 예측할 수 없었던** 지견입니다.

운용 지침은 이렇게 되었습니다.

- **계통 보존을 최우선**으로 한다면 → interval=1(8/8 전 계통 생존).
- **행동 다양성도 양립**시키고 싶다면 → interval=5(5/8을 보존하면서 diversity 최대).

양립의 최적점은 fitness의 설계나 집단 규모에 의존하므로, 본 환경에서는 sweep으로 재보정합니다.

![재투입 빈도의 트레이드오프. 계통 보존과 행동 다양성은 반비례하고, diversity는 interval=5에서 피크를 찍는다(비단조)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_ko.svg)

> 🍵 **휴식 포인트**: 라쿠고의 사게(결말)처럼, 여기에는 「예상을 뒤집는 전(轉)」이 있습니다. 「하면 할수록 좋다」고 생각했더니, 「너무 하면 역효과」였습니다. 식물의 물 주기와 같아서, 너무 적게 줘도 마르고, 너무 많이 줘도 뿌리가 썩습니다. 중용에 최적점이 있습니다. 진화 계산을 하다 보면, 이런 「단조롭지 않은 곡선」을 몇 번이고 만납니다. 그래서 베이스라인을 측정하고, sweep을 돌립니다. 직관은, 자주 배신당합니다.

---

### 8. Stage2 전반 — 「LLM의 약점」을 proxy로 선택압으로 삼다

여기까지는 rich-proxy(persona 유사도 기반의 heuristic)로 메커니즘을 확인해 왔습니다. 다음은 설계의 또 하나의 기둥, **「LLM/VLM이 현실에서 약하고, 또한 측정 가능한 축」을 pressure로 삼다**를 구현합니다(commit의 계열, `pressures.py`).

설계 §3에서 든 proxy 가능한 5 축을 plugin화했습니다.

| pressure(LLM 약점) | 관련 사고 인자(case) |
|---|---|
| typo_robustness(노이즈 내성) | consistency / reality_link / uncertainty |
| polysemy_wsd(다의어) | multiview / consistency / reality_link |
| multistep_robustness(다단 추론) | structurize / closed_loop / self_extend |
| calibration(신뢰도 추정) | uncertainty / provenance |
| context_management(무관 문맥 내성) | consistency / provenance / recompose |

`make_pressure_fitness()`가 각 pressure의 case(총 14개)를 breakdown으로 출력하고, lldarwin의 ε-lexicase가 **집약하지 않고 축별로 specialist를 도태**합니다. `--fitness pressure-proxy`를 추가. tests `test_evolutionary_pressures.py` 4건 + 진화계 **942 green**.

end-to-end 실측(pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens): named 계통 **8/8 생존** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**. 14개의 약점 축 case가 독립적으로 도태되어, 행동 다양성은 높습니다. 계통은 reservoir가 유지하고 있습니다(pressure-proxy는 persona의 동일성을 직접 보상화하지 않기 때문에, 우점 계통의 share는 rich-proxy의 0.29보다 높은 0.67이 됩니다).

![5 약점 축(typo / polysemy / multistep / calibration / context)의 모집단 평균 추이(proxy 측정)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_ko.svg)

**Honest 유보(설계 §7 / §7.1에 명시된 수용된 한계)**: 개체는 실 LLM이 아니라 genome(llive 구성)입니다. 본 pressure가 측정하는 것은 「genome이 그 약점에 **관련된 사고 인자**를 얼마나 갖추는가」라는 **행동의 대리**이지, **production의 LLM 능력이 아닙니다**. 이것은 **mechanism feasibility(메커니즘이 도는 것)의 검증**에 한정됩니다. Goodhart 리스크(proxy를 해킹하는 표면 전략이 진화한다)도 수용된 한계입니다. 실 LLM/VLM의 약점 축의 실측은, Stage2 후반(OLLAMA_HOST 설정 + 개체→실 LLM 매핑이 전제)으로 미룹니다.

> 🍵 **휴식 포인트**: 여기는 오해되기 쉬우므로, 다짐해 둡니다. 「LLM의 약점을 진화로 극복했다!」고는 **아직 말하지 않았습니다**. proxy가 측정하는 것은 「메커니즘이 도는가」뿐. 진짜 LLM이 타이포에 강해졌는지 어떤지는, 이 단계에서는 일절 알 수 없습니다. proxy로 화려한 숫자(17.91)가 나와도, 그것은 「장치가 작동한다」는 증명이지 「내용이 똑똑해졌다」는 증명이 아닙니다. 이 선 긋기를 모호하게 한 순간, 연구는 거짓이 됩니다. 그래서 다음으로, **진짜 LLM**을 상대합니다.

---

### 9. Stage2 후반 — 진짜 온프레미스 LLM을 상대로 prompt 전략을 진화시키다

localhost의 ollama(llama3.2:latest 등)가 도달 가능하다는 것을 알았으므로, 드디어 **실 LLM 평가**가 가능해졌습니다(commit `2fb2912`). localhost = on-prem이므로, measurement purity(측정 순도. cloud LLM과 혼재시키지 않는다)의 규율도 충족합니다([[feedback_llive_measurement_purity]]).

#### 9.1 개체 → 실 LLM으로의 매핑(Promptbreeder 계)

핵심은 「genome을, 어떻게 실 LLM에 효과를 미치게 하는가」입니다. `real_pressures.py`에서 **개체 → 실 LLM 매핑**을 구현했습니다.

- **개체의 `c_prompt`(PromptChromosome)을 system prompt로 변환**: skill_set → 지시문 / prompt_template_id → 추론 스타일 / language_style → 어조. 고정의 LLM(llama3.2)에 이 system prompt를 씌우고, 5 약점 축의 **실 태스크**를 풀게 해서 채점합니다.
- **LLM 본체는 고정하고, prompt 전략(genome)을 진화시킨다** = 「어떤 prompt 전략이 LLM의 약점을 완화하는가」를 실측으로 도태한다. 이것은 Promptbreeder(prompt를 진화적으로 최적화하는 연구 계열)의 방식입니다.
- temp=0(greedy)로 결정론적으로. `(system_prompt, task)`를 캐시(동일 전략은 재평가하지 않는다).
- robust: per-call try/except(ollama의 hiccup은 task의 실점으로 취급하고, 주행은 계속).
- `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds`를 추가. tests 5건 + 진화계 947 green.

#### 9.2 실 선택 신호의 실증 — CoT+structure 전략이 multistep을 0.0 → 1.0으로

그리고, 진짜 선택 신호를 관측할 수 있었습니다.

**CoT+structure 전략**(`chain_of_thought` + structurize + loop)이, llama3.2의 **multistep(다단 추론)을 0.0 → 1.0으로 개선**했습니다(terse한 전략은 0.0으로 실패. score는 0.80 → 1.00으로 상승).

이것은, lldarwin의 주장 「prompt 전략의 진화로 LLM의 약점을 완화할 수 있다」를, **proxy가 아니라 실 LLM에서 실증**한 것을 의미합니다. 같은 llama3.2 본체라도, 씌우는 system prompt(= 진화한 genome)에 따라, 다단 추론 태스크를 풀 수 있기도 하고 못 풀기도 합니다. 진화는 「풀 수 있는 prompt 전략」을 실제로 골라낸 것입니다.

![5 약점 축의 모집단 평균 추이(실 온프레미스 LLM llama3.2 평가). prompt 전략의 진화로 축이 개선된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

#### 9.3 12h 연속 실행

실 LLM 평가는 무거우므로, 장시간의 연속 실행을 기동했습니다(`out/lldarwin_12h_realpressure_2026_05_26/`).

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

wallclock 12h에서 safely 정지(snapshot 완료 → `--resume`으로 계속 가능). 연속 실행 중에 best_score=1.0에 도달했습니다.

![실 LLM 진화 실행의 적응도와 다양성(12h 연속 실행)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_ko.svg)

#### 9.4 Honest 유보(실 LLM 평가의 한계)

여기가 #25에서 배운 자세의 총결산입니다. 화려한 결과(0.0 → 1.0, best 1.0)가 나왔기 때문에, 내역을 철저하게 정직하게 씁니다.

- **(a) fitness에 관여하는 것은 `c_prompt`뿐.** persona / c_factors는 중립(계통은 reservoir로 유지, 초기 선택은 novelty가 담당). 즉 이것은 「**prompt 전략의 진화**」이지 「persona의 진화」가 아닙니다. 오카 기요시의 인격이 똑똑해진 것이 아니라, 오카 기요시라는 계통에 연결된 prompt 전략이 선택되었다는 이야기.
- **(b) 전 founder의 초기 c_prompt는 동일(default).** 그래서 탐색은 mutation 구동입니다(founder마다 prompt를 다양화하는 것은 향후의 개선). 출발점이 같으므로, 초기의 계통 차이는 prompt 전략에는 효과가 없습니다.
- **(c) 작은 배터리(축당 2문) = 노이즈가 많은 추정.** 0.0 → 1.0이라는 극적인 숫자도, 문제 수가 적은 만큼 노이즈를 포함합니다. 통계적으로 견고한 주장을 하려면, 더 큰 배터리가 필요합니다.
- **(d) on-prem only(measurement purity). 일반 능력의 주장이 아니다.** llama3.2라는 특정 모델·특정 태스크에서의 관측이지, 「LLM 일반이 이렇게 된다」고는 말하지 않습니다.

이것들을 숨기면 「진화로 LLM이 극적으로 똑똑해졌다!」는 화려한 이야기를 쓸 수 있지만, 그것은 거짓입니다. lldarwin이 실증한 것은 「**메커니즘이, 실 LLM 위에서, 선택 신호를 낳는다**」는 데까지. 그 선을 넘는 주장은 하지 않습니다.

> 🍵 **휴식 포인트**: 연구에서 가장 기분 좋은 것은 「0.0이 1.0이 되었다!」고 외치는 순간입니다. 하지만, 그 순간이야말로 [[feedback_benchmark_honest_disclosure]]가 효과를 발휘합니다. 「이상하게 좋은 숫자가 나오면, 이긴 기분이 되기 전에 내역을 의심하라.」 이번으로 말하자면 — 이긴 것은 「prompt 전략」이지 「LLM 본체」도 「persona」도 아닙니다. 문제 수도 적습니다. on-prem의 1 모델뿐. 이것을 전부 쓰고 나서야, 비로소 「실증했다」고 말할 수 있습니다. honest disclosure는, 자랑을 참는 근력 운동입니다.

---

### 10. 기존 자산의 재이용(codex 코드 조사 기반)

설계를 그림의 떡으로 만들지 않기 위해, 배하의 Codex에게 기존 코드를 조사시켰더니, **많은 것이 구현 완료·미배선**이었습니다.

- `mating.py:139 LexicaseSelection`(ε 포함, 구현 완료이지만 미배선 → 배선만 하면 됨)
- `nsga2.py:197 NSGA2Selection`(≤3 목적 레인용)
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**신규 구현**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 군 / `MultiPressureSelector`(핵심) / `LineageReservoir`(Stage1.5) / `SelectionAudit`.
**배선점**: `loop.py:122`의 `selection`에 `MultiPressureSelector`를 주입, `persona_evolution.py:606`에 주입구를 추가, `LineageReservoir`를 `EvolutionLoop.on_population_bred` hook에 연결.

> 🍵 **휴식 포인트**: 「구현 완료이지만 미배선」이 가장 많았던 것이, 최대의 교훈이었습니다. 좋은 부품을 만들어도, **배선(오케스트레이션)하지 않으면 진화는 망가진 채**. #25에서 8→2가 된 것은, ε-lexicase도 NoveltyScorer도 QD도 「상자 안에 있었는데, 배선되지 않았기」 때문입니다. lldarwin의 본질은, 신규 알고리즘의 발명보다도, 「기존의 좋은 부품을 **집약하지 않고** 묶어서, 진화 루프에 **실제로 배선하는 것**」에 있습니다. 전자 부품을 전부 갖춰도, 납땜하지 않으면 라디오는 울리지 않습니다.

---

### 11. 파탄 회피의 보증 — 전멸하지 않는 다층 구조(실측으로 뒷받침 완료)

#25의 monoculture(8→2)를 반증하는 다층 구조는, 설계대로 갖춰졌고, 게다가 이번에는 **실측으로 뒷받침되었습니다**.

1. **MinimalCriterionGate** — 최저 기준으로 번식 가부 → 일강 독식을 억제.
2. **QD cell별 elite** — 1 cell이라도 남으면 계통 전멸 불가(archive 단조 증가).
3. **Niching / FitnessSharing** — 같은 niche를 down-weight → 다봉 병존.
4. **Down-sampling** — moving target으로 plateau 파괴.
5. **per-dim z-score + 중앙 일치 제외** — 무특징을 우대하지 않는다.
6. **LineageReservoir(Stage1.5에서 추가)** — 멸종 계통의 중립 저장고 → 계통 전멸을 구조적으로 저지(실측으로 8/8 생존).
7. **monoculture 모니터 + SPC** — max_lineage_share를 매 세대 기록, >0.8을 SPC_ALARM으로 검지 → 자동 조정.

특히 (6)은, §5의 honest disclosure(novelty로는 계통 고정을 막을 수 없다)를 받아 **나중에 추가한 층**입니다. 설계의 구멍을 실측으로 발견하고, 막았습니다. 실측의 lineage_fixation은 OFF 0.70 → ON 0.29로, OE-3 기준(<0.8)을 크게 밑돕니다. 「집약하지 않는다」 + 「멸종 계통을 되살린다」의 2단 구조로, #25를 구조적으로 짓누를 수 있었던 것이 본 글의 도달점입니다.

---

### 12. honest disclosure / 리스크(예고편)

설계를 맹신하지 않습니다. 수용된 한계(다음 작 #27에서 깊이 파고든다)를, 다시 한번 정리해 둡니다.

- **Goodhart's law / proxy 괴리** — LLM 약점을 proxy fitness로 하면, 「지표를 해킹하는 표면 전략」이 진화한다(typo → 특정 치환의 암기, WSD → 테스트의 heuristic 이용 등). proxy는 mechanism feasibility에 한정하고, production 능력을 주장하지 않는다.
- **설계자 의존성** — lexicase=case / QD=기술자 / novelty=거리 척도, 어느 것이나 「다양성의 방향」을 설계자가 정한다. 생물 진화급의 미상정 창발은 한정적.
- **minimal-criterion의 정체⇄붕괴 트레이드오프** / **QD의 차원의 저주 + 아카이브 포화**.
- **실 LLM 평가의 한계(§9.4 재게재)** — c_prompt만 fitness 관여·founder 초기 prompt 동일·작은 배터리·on-prem only.

> **다음 회 예고(#27)**: 「안경이 포화하면 선택압은 무력」이라는 가장 아픈 반증을, Goodhart's law와 proxy fitness의 한계와 함께 정직하게 공개합니다. lldarwin은 만능이 아닙니다. **어디까지 주장해도 되는가**의 선 긋기가 #27의 주제입니다. 이번에 「8/8 생존」 「0.0→1.0」이라는 좋은 숫자가 나왔기 때문에, 다음은 철저하게 반증으로 단련합니다.

---

### 13. 결론

- 진화는 「**측정한다(lleval)**」와 「**도태한다(lldarwin)**」의 2단 구조. 도태의 핵심은 **「집약하지 않는다」**.
- Stage1: criteria 제외 + novelty pressure로, 행동 다양성을 7.12 → 14.88(+109%)로 2배로 늘리고, 종반의 붕괴를 회피했다.
- honest disclosure: novelty/lexicase는 **행동 다양성**은 보존하지만, **계통 고정**은 중립 부동(Kimura)으로 monoculture로 향한다. 저는 두 개의 다양성을 혼동하고 있었다 — 정직하게 기록.
- Stage1.5: lineage-niched **중립 저장고**로, 실 EvolutionLoop에서 **OFF=2 계통 / ON=전 8 계통 생존**(오카 기요시·그로텐디크 포함), lineage_fixation 0.29(≪0.8)를 실현. **이것은 날조가 아니라 실제로 작동했다**.
- 재투입 빈도 sweep: 계통 보존↔행동 다양성의 트레이드오프. diversity는 interval=5에서 피크(**비단조**)라는 비자명한 지견.
- Stage2 전반(proxy): 5 약점 축을 Pressure plugin화(mechanism feasibility만).
- Stage2 후반(실 LLM): 개체 c_prompt → system prompt 매핑으로 고정 on-prem LLM(llama3.2)을 실 태스크 채점. **CoT+structure 전략이 multistep을 0.0 → 1.0으로 개선**. 12h 연속 실행으로 best=1.0 도달.
- 낙관하지 않고, 이긴 기분이 되지 않고, 내역을 나누어 보고했다([[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]).

좋은 부품을 만드는 것만으로는 진화는 망가진 채. **집약하지 않고 묶고, 실제로 배선하고, 멸종한 계통을 되살리고, 진짜 LLM으로 선택 신호를 확인한다** — 거기까지 해서, 비로소 #25의 「저와 프리스턴만」의 세계를, 오카 기요시도 그로텐디크도 있는 북적이는 세계로 바꿀 수 있었습니다. 다음 #27에서는, 이 성공에 어디까지 신뢰를 둬도 되는지를, 반증으로 다시 묻습니다.

---

### 14. 관련

- 연재 #25 「저와 프리스턴만 남았다」 — 본 글의 동기(실패의 기록)
- 연재 #24-08 「안경을 만들다」 — lleval(측정하는 쪽)
- 연재 #27 「안경이 흐려지면 도태도 무력」 — 반증 조사(honest disclosure)
- 설계서: lldarwin(도태하는 쪽) `docs/vision/LLDARWIN_DESIGN.md`
- 실측 정본: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / 중립 저장고 PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 실 LLM=`2fb2912`
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---

## 제3장 하룻밤 사이에 AI 진화를 다시 만들었다 — 실제 LLM 12h 런이 또 만점에서 포화되고, 6개의 PoC와 4개의 Agent와 Perplexity가 「독립적으로 같은 결론」으로 수렴한 밤 #27

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::



> 📚 **연재 내비게이션(lldarwin 아크)**: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → **#27 본 글(클라이맥스)** → 구현편(예정). ※ 각 글은 단독으로도 읽을 수 있습니다(링크는 회람용).

> **콘셉트 hook**: 지난 글 #25에서 저는 「AI를 500세대 진화시켰더니, 세상에 **프리스턴과 나만** 남았다」라는 큰 실패를 공개했습니다. 원인은 평가 함수(안경 = lleval)가 계속 만점을 내놓아 **선택압이 0이 된** 것이었습니다.
>
> 「그렇다면 이번엔 진짜 LLM으로 확인하자」 — 그렇게 생각하고 on-prem의 llama3.2를 상대로 **12시간 내내 진화**시켰습니다. proxy(합성 잣대)가 아니라 실제 LLM입니다.
>
> 결과. **gen5에서 만점에 달라붙어, 거기서부터 65세대 꿈쩍도 하지 않았습니다.** 전멸은 하지 않습니다. 하지만 누적도 되지 않습니다. 이것은 진화가 아니라 **그저 「체에 거른 랜덤 서치」**였다 — proxy뿐 아니라, **실제 LLM으로도 아직 진화가 되지 못했던** 것입니다.
>
> 거기서부터 하룻밤. 저는 「방책을 정하기」 위해, 직접 6개의 PoC를 돌리고, 4개의 Claude Agent를 병렬로 달리게 하고, Perplexity에 문헌을 뒤지게 했습니다. 그리고 아침, **모두가 독립적으로 같은 결론으로 수렴**해 있었습니다. 이것은 그 「밤샘 의사결정 로그」의 honest disclosure입니다.

---

### 0. 세 줄 줄거리(라쿠고에서 말하는 「도입부」)

라쿠고에는 본론 앞에 「도입부(마쿠라)」가 있습니다. 우선 세 줄로.

- **또 포화했다** — 실제 LLM(llama3.2)으로 12h 돌렸더니, gen5에서 best=1.0에 달라붙어 65세대 무진전. 전멸하지 않지만 누적도 안 됨 = **filtered random search**. 진짜 원인은 #25와 같은 「고정된 수작업 잣대의 포화」.
- **하룻밤에 방책을 정했다** — 자체 PoC 6개 + 병렬 Agent 4개 + Perplexity가 **독립적으로 같은 결론**으로 수렴. 「잣대를 고정한 채 도태기를 갈아도 소용없다. **평가 자체를 개방단화하라.**」
- **독창성이 보였다** — 연속 진화하는 집단을, 멈추지 않고 임의의 순간에 합주(MoA)시켜 하나의 답을 내는 「**라이브 오케스트라**」가 선행 연구의 white-space(공백 지대)임이 판명되었다.

요컨대 **「안경(평가)이 포화되면, 도태기(lldarwin)를 아무리 갈아도 무력하다.」** 그래서 가는 대상을 바꾼다 — **평가 자체를 개방단으로 한다**, 가 이번 결론입니다.

---

### 1. 왜 「또」 했는가 — #25 / #26(설계)의 연속

지금까지의 연재를 세 줄로 돌아봅니다.

- **#24-05**「집단이 배우는 AI」— 하나의 LLM을 똑똑하게 만드는 것이 아니라, **N개의 llive 개체(genome)를 세대교체시키며 서로 평가하게 하는** 파생 집단 진화라는 틀을 세웠다.
- **#25**「프리스턴과 나만 남았다」— 그 집단에 8인의 지성을 페르소나 씨앗으로 뿌리고 proxy 500세대로 돌렸더니, **만점 포화 → 선택압 0 → 운(유전적 부동)만으로 2개 계통으로 치우치는** 큰 실패. 안경이 흐려져 있었다.
- **#26(설계편)**「안경으로 재기만 해서는 진화하지 않는다」— 도태기 **lldarwin**을 설계하고, 「집약하지 않는 다목적 도태(ε-lexicase / QD / 중립 저장고)」를 구현. proxy에서는 계통 절멸을 막았다.

여기까지는 전부 **proxy(결정론적 휴리스틱, LLM 비의존)**에 관한 이야기였습니다. proxy는 「기구가 돈다」는 것은 보여줄 수 있어도, 「진화가 **의미 있는** 것을 찾았다」는 것은 보여주지 못합니다([[feedback_benchmark_honest_disclosure]]).

그래서, 당연한 다음 한 수. **진짜 LLM으로 확인한다.**

localhost의 ollama(llama3.2:latest)가 도달 가능했기에, 개체의 `c_prompt`(prompt 전략의 유전자)를 system prompt로 변환해 고정된 llama3.2에 씌워 실제 과제를 풀게 했습니다 — **Promptbreeder 계의 사상(寫像)**으로, 12시간의 연속 진화 런을 기동했습니다. 이것이 본 글의 출발점입니다.

> 🍵 **휴식 포인트**: 여기까지 「proxy에서는 기구가 돌았다. 그럼 진짜 LLM에서는?」이라는 물음이 서면 OK입니다. 연구의 좋은 점은 이 「그럼 진짜에서는?」을 실제로 돌릴 수 있다는 것. 그리고 이번에 진짜는 — 가차없었습니다.

---

### 2. 출발점 — 실제 LLM 12h 런의 「정직한 불합격」

12시간의 실제 LLM 진화 런(on-prem llama3.2, measurement purity 엄수 = cloud LLM과 섞지 않음, [[feedback_llive_measurement_purity]])의 결과가 이것입니다.

| 사실 | 값 | 함의 |
|---|---|---|
| 완주 | 71세대 / 12h(≒10.3분/세대, 실제 LLM 순차) | 처리량이 율속 |
| best_score | **gen5에서 1.0 → gen70까지 고정** | **목적 포화. 65세대가 무진전** |
| mean | 0.85에서 머리 부딪힘, 1.0 전략이 석권하지 않음 | **적응이 누적되지 않음** |
| 축별 | 10문제 중 6-7문제가 포화, 기울기는 multistep(2문제)만 | 실효 해상도가 너무 작음 |
| fitness 의존 | **c_prompt만**. c_factors(40차원)/c_impl/c_meta는 중립 부동 | **43차원이 선택압 0** |
| 집단 건전성 | pop=24 유지・min ≥ 0.70・**전멸하지 않음** | 기구(GA)는 망가지지 않음 |

여기서 멈춰 서는 것이 FullSense의 honest disclosure 규칙입니다([[feedback_benchmark_honest_disclosure]]). 「전멸하지 않았다! best=1.0에 도달했다!」라고 쓰면 자못 성공처럼 보입니다. 하지만 내역을 보면 일목요연합니다.

**판정: 전멸은 하지 않았지만, 누적 진화가 되지 못했다(≒ filtered random search).**

10문제 테스트 중, 기울기(차이)가 남아 있는 것은 multistep의 2문제뿐. 나머지 8문제는 일찌감치 전원 만점. 즉 10문제 중 8문제는 이제 누구를 골라도 같습니다. 선택압의 실효 해상도가 거의 2문제 분밖에 남지 않았습니다. 게다가 fitness에 관여하는 것은 4개 염색체 중 `c_prompt` 단 1개뿐, 나머지 43차원(사고 인자 40차원 + 구현 + 메타)은 **선택압 0의 중립 부동**.

![실제 on-prem LLM(llama3.2) 진화 런의 적응도와 다양성(12h 연속 런). best는 일찌감치 천장에 달라붙고, 이후는 평탄](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_ko.svg)

![5개 약점 축(typo / polysemy / multistep / calibration / context)의 모집단 평균 추이(실제 on-prem LLM 평가). multistep 외에는 조기에 포화하고 기울기가 남지 않음](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

**진짜 원인 = 수작업 고정 잣대의 포화.** #25에서 사용자가 언어화한 통찰 「**안경이 포화하면 선택압은 무력**」을, 이번에는 proxy가 아니라 **실제 LLM으로 실증**해버린 구도입니다. 안경을 proxy에서 실제 LLM으로 바꿔도, **잣대가 「고정된 10문제」인 한 곧 만점에서 포화한다.** 렌즈 제조사를 바꿔도 눈금이 거칠면 마찬가지.

> 🤔 **비유**: 채점자를 「진짜 선생님(실제 LLM)」으로 바꿔도, 매번 같은 문제를 낸다면 몇 회 만에 전원이 만점을 받고, 이후 아무리 시험을 봐도 차이가 안 납니다. 문제가 나쁜 게 아니라 **시험지가 고정이고 너무 쉬운** 것입니다. 채점자(안경)를 proxy에서 실제 LLM으로 교환해도, 잣대(문제)가 고정이면 포화한다. 이것이 「정직한 불합격」의 정체입니다.

> 🍵 **휴식 포인트**: 많은 사람이 이쯤에서 「실제 LLM으로도 포화라면, 이제 막힌 거 아닌가?」라고 생각합니다. 저도 그렇게 생각했습니다. 하지만 본론은 여기서부터. **「잣대를 고정한 것이 잘못」**이라면, 고쳐야 할 것은 도태기도 LLM도 아니라, **잣대를 만드는 방식 그 자체**입니다. 그것을 하룻밤에 걸쳐, 6개의 PoC와 4개의 Agent와 Perplexity로 확인했습니다.

---

### 3. 하룻밤의 작전 — 「방책을 정하기」 위한 분산 조사

사용자에게서 온 지시는 이러했습니다.

> 「철저하게 요건을 정리하고, 더 진화형으로서 독창성을 낸다. PoC도 몇 번이고 반복한다. 내일 아침까지 계속 작은 단위로 PoC를 잔뜩 해서 **방책을 정한다.**」

여기서 중요한 것은, **「구현을 완성한다」가 아니라 「방책을 정한다」**가 목적이었다는 점. 그래서 큰 본 런을 1개 돌리는 것이 아니라, **작은 PoC를 대량으로** 돌려, 설계 판단을 하나씩 실데이터로 부수어가는 작전을 취했습니다([[feedback_poc_feasibility_first]] = 요건 → PoC → 타당성 → 상세 설계).

병렬로 돌린 워커는 이것입니다([[feedback_parallel_first_execution]] = 독립 과제는 병렬 Agent 기동이 default).

| # | 워커 | 과제 |
|---|---|---|
| A | Claude Agent | 개방단 sweep PoC(baseline = 포화·전멸 / 개방단 = 회피 를 실증, ≥1만 세대) |
| B | Claude Agent | 관측 기반(응답 로그 / 개체별 스코어 시계열 뷰어 / lineage 복원) |
| C | Claude Agent | 오케스트라 PoC(MoA가 단일 best를 웃도는가, 다양성 선발 vs 중복 선발) |
| P | Perplexity | QD/novelty/MoA/agentic 진화의 SOTA 서베이(문헌 갭 보완) |
| X | Codex | 설계의 독립 비평 + 최소 PoC 3안 + 맹점 지적 |
| 자신 | 나(main) | 자체 PoC #1〜#6을 직접 구현·실행(orchestrator 겸 최중요 과제 담당) |

> 🍵 **휴식 포인트**: 이 「6인 가담」 체제는 사실 본 글의 숨은 주역입니다. 왜 1인(1개의 context)으로 전부 하지 않는가? 답은 honest disclosure의 핵심에 있습니다. **같은 머리로 생각한 결론은 같은 편향에 끌려갑니다.** 다른 방법(합성 PoC / 실제 LLM / 문헌 조사)으로 **독립적으로** 확인하고, 그것이 일치했을 때만 결론을 신뢰합니다. 이것을 **honest cross-validation**이라 부릅니다. 후반에 그 위력이 나옵니다.

여기서 한 가지, 정직한 불발도 적어둡니다. **Codex(X)는 쓸 수 없었습니다.** ChatGPT 계정의 허가 모델 불일치(API 측이 codex 계 모델을 죄다 거부)로 차단. 10x promo 기간 중일 텐데, API가 "not supported when using Codex with a ChatGPT account"를 반환. 이것은 환경 문제이므로, 당분간은 자체 PoC + 병렬 Agent + Perplexity를 주축으로 전환했습니다. **「쓸 수 있어야 할 도구가 쓸 수 없었다」도 숨기지 않고 기록한다.**

---

### 4. 첫 번째 결정타 — 「고정 잣대」를 버릴 것인가(자체 PoC #1 / #2)

가장 먼저 부숴야 할 가설은, 가장 근원적인 물음이었습니다. **「잣대를 고정 난이도에서 적응 난이도로 바꾸면, 포화는 고쳐지는가?」**

#### 4.1 자체 PoC #1 — 적응 난이도는 포화를 고친다. 그러나 다양성을 죽인다

합성 competence 벡터를 쓴 proxy로, 교란을 제거하고(elite를 score 기준으로 선택) 비교했습니다.

- **baseline(고정 난이도)**: 능력 **0.627에서 저위 정체**(best 0.757). 12h의 병리를 proxy로 재현.
- **adaptive(난이도 = 집단 60분위에 추종)**: 능력 **0.952로 상승**(best 1.0).

난이도를 집단에 추종시키면(풀 수 있는 문제가 늘면 문제를 어렵게) 포화가 풀려 능력이 늘었다. **하지만** — adaptive는 **다양성을 희생**했습니다(diversity 0.310 → 0.134로 붕괴). 어려운 문제에 최적화하는 과정에서, 집단이 하나의 정답 전략으로 응집해버립니다.

#### 4.2 자체 PoC #2 — 적응 난이도 × novelty는 양립한다

그래서 「적응 난이도(기울기 유지)」에 「novelty 선발(다양성 유지)」을 더하면 어떻게 되는가.

| 구성 | 최종 능력 | best | 다양성 | plateau |
|---|---|---|---|---|
| baseline(고정 난이도) | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive(난이도 추종) | 0.952 | 1.000 | 0.134(붕괴) | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316(유지)** | gen99(최장 탐색) |

**adaptive + novelty가** 능력(baseline 대비 +40%)과 다양성(adaptive 대비 2.4배, baseline 동등)을 **양립**했습니다. 능력을 7% 양보하는 대신, 다양성을 완전 유지.

여기서 **방책의 핵이, 자체 데이터로 확정**되었습니다.

> **「적응 난이도 = 기울기 유지」와 「QD/novelty = 다양성 유지」는 상보적이며, 둘 다 필수.**
> 고정 잣대 단독(baseline)도, 적응 난이도 단독(adaptive)도, 모두 불충분.

honest 유보: 이것은 추상 proxy(competence 벡터)이며, 실제 LLM 사상이 아닙니다. **mechanism feasibility(기구가 도는가)의 검증**에 한정됩니다. plateau@gen의 숫자는 「정체한 세대」를 가리키지만, 본질은 정체의 **수준** — baseline은 저위(0.627)에서 정체, adaptive 계는 천장 근방에서 정체, 라는 차이입니다.

> 🤔 **비유**: 전원이 만점을 받으면 문제를 어렵게 한다(적응 난이도). 그러면 점수는 갈리지만, 이번엔 전원이 같은 풀이법으로 수렴해버린다(붕어빵). 그래서 「특이한 풀이법에도 보상을 준다」(novelty)를 더하면 능력과 다양성이 양립한다. **「어렵게 한다」와 「별종을 칭찬한다」의 이도류** — 이것이 PoC #2의 요점입니다.

---

### 5. 본진의 증거 — 개방단 진화의 1만 세대 sweep(Agent A)

자체 PoC로 「방향」은 보였습니다. 다음은 그것을 **대규모로・엄밀하게** 두들길 차례입니다. 병렬 Agent A에게 **각 1만 세대 × pop256 × 19 구성 × 2 순회**의 개방단 sweep를 돌리게 했습니다.

판정 기준은 「open-ended(개방단)인가」 — **포화하지 않고, monoculture(단일 문화로의 수렴)를 피하고, archive(다양성의 저장)가 계속 성장하는가?**

#### 5.1 결정적인 판정표

**verdict(gen9999 시점): 전 scalar 구성 = False / 전 novelty・lexicase 구성 = True**

| label | 선택 | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

여기서 4가지 결정적인 발견이 나왔습니다.

1. **선택압이 결정타.** scalar(단일 스칼라 fitness)는, MAP-Elites의 archive를 더해도(`scalar_qd`) **전멸(False)**. 즉 「저장고를 더하면 다양성을 지킬 수 있다」는 **틀렸고**, **novelty / lexicase라는 개방단 선택이 아니면 애초에 개방단은 성립하지 않는다.** archive 단독으로는 구할 수 없다. **선택압 그 자체를 개방단화하는** 것이 본질이었다.
2. **표준화(z-score)가 QD 피복을 자릿수로 넓힌다.** novelty에 per-dim z-score 표준화를 더하면 occupied cells가 9 → 100+. 각 축의 「이탈」을 선택압으로 바꾸면, 행동 공간의 피복이 한 자릿수 넓어진다.
3. **중립 저장고가 계통 다양성을 회복.** novelty_std만으로는 uniq_lineages가 1.0(계통이 하나로 고정). reservoir256을 더하면 **31.9**로. **행동 다양성과 계통 다양성은 다른 축**이며, 후자에는 저장고가 필요하다(이것은 #26 설계편에서 구현 완료된 지견의 재확인).
4. **스케일이 효과적.** latent 차원을 256 → 1024로 하면 niche가 101 → 166, archive가 1021(포화) → 2234(성장 지속). 다양성은 「용량」으로 살 수 있다.

![Stage1 baseline(novelty 없음)의 적응도와 다양성. 종반에 다양성이 붕괴한다(scalar의 전형적 실패)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_ko.svg)

![Stage1 novelty pressure 있음. 행동 다양성이 종반까지 유지된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_ko.svg)

![baseline vs +novelty의 diversity 겹쳐 그리기. 붕괴(scalar)와 유지(novelty)를 한 장으로 대비](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_ko.svg)

#### 5.2 Agent A가 내준 「정직한 한계」

좋은 결과(open-ended 성립)가 나왔을 때야말로 한계를 적는다. Agent A 자신이 이렇게 지적해왔습니다.

> novelty/lexicase는 기술자(descriptor) **전체**의 다양성은 유지하지만, **특정 의미 차원(factor)의 다양성은 보장하지 않는다.**
> 큰 latent에서는 factor drift가 일어나, fspread(factor의 펼쳐짐)가 요감시.

즉 「전체로서는 다양」해도 「사고 인자라는 특정 의미 차원에서는 수렴해 있는」 경우가 있을 수 있다. 이것은 새로운 요건 **factor-subspace QD(의미 차원을 개별 보호하는 QD)**를 낳았습니다(후술하는 PoC #6에서 대처).

> 🍵 **휴식 포인트**: 여기가 본 글에서 가장 딱딱한 절입니다. 가져가셨으면 하는 한 줄 — **「archive(저장고)를 더하기만 해서는 구할 수 없다. 선택압 그 자체를 개방단으로 하지 않으면 안 된다.」** #25/#26 설계편에서 「집약하지 않는다」고 말해왔지만, 그 본진이 「**선택하는 방식을 개방단화하는**」 것이었다고, 1만 세대의 실데이터가 단언해주었다. 여기를 넘으면 나머지는 독창성 이야기입니다.

---

### 6. 독창성의 핵 — 「연속 진화하는 집단을, 멈추지 않고 합주시킨다」

여기까지 「포화를 구조적으로 피하는 선택 핵(S1)」이 굳어졌습니다. 다음은 사용자가 대화에서 제시한 **독창성 3축**을 PoC와 문헌으로 뒷받침할 차례입니다.

사용자가 언어화한 3축은 이것이었습니다.

1. **연속 진화 집단 = 라이브 오케스트라(ORCH)** — 계속 진화하는 집단이, 그 자리에서 MoA(Mixture-of-Agents) 집약해 하나의 답을 낸다. 진화를 멈추지 않는다. **최대의 차별화 후보.**
2. **조사 기능을 가진 개체(AGENT)** — 개체가 스스로 조사하러 간다. Voyager 계.
3. **관측・대화 제어(OBS)** — 개체별 응답 + 선택 스코어의 시계열을 보고, 멈추고, 재개할 수 있다.

#### 6.1 Perplexity가 뒷받침한 white-space

병렬로 돌린 Perplexity의 SOTA 서베이(1143행)가 가장 중요한 뒷받침을 돌려주었습니다.

> 「**online evolution + online answering을 통합한 연속 가동 시스템**」은 명확한 선행 연구 없음 = **research white-space(공백 지대)**. 근접은 MoA / Self-MoA / sequential aggregation / routing이지만, 동일물은 없다.

즉 「진화를 멈추고, 완성된 최강 개체로 답한다」는 평범. 「진화를 **멈추지 않고**, 진화 중인 집단을 그대로 합주시켜 답한다」는 아직 아무도 하지 않았다. **ORCH §1.11의 차별화가 확정**되었습니다.

#### 6.2 다만 Perplexity는 반증 경고도 주었다

honest disclosure로서, Perplexity가 준 **반증 경고**도 같은 비중으로 적습니다.

> 2025년의 **Self-MoA 연구**에서는 **다양성은 자동으로 우위가 아니다**. 단일 톱 모델의 반복이, 이종 혼합 MoA를 AlpacaEval에서 6.6% 웃돌았다(quality-diversity 트레이드오프).

「집단을 합주시키면 단일 개체보다 강하다」는 **자명하지 않다**. 오히려 다양성이 역효과가 되는 경우가 있다고, 선행 연구가 경고한다. 그래서 ORCH는 「실측으로 증명하라, pass-bar를 정직하게」. 이것을 Agent C와 자체 PoC #3/#4로 검증했습니다.

> 🍵 **휴식 포인트**: 여기, 연구의 성실함이 시험받는 분기점입니다. 「online 진화 + online 답변은 white-space! 독창성!」으로 들떠 오르고 싶은 참에, Perplexity가 「하지만 다양성은 자동으로 좋은 게 아니라는 반증이 있어」라고 찬물을 끼얹어 옵니다. **들떠 오를 재료와 찬물을, 같은 조사 안에서 둘 다 받아들인다.** 이것을 할 수 있으면 결론이 훨씬 강해집니다. 다음 절에서 그 찬물의 정체를 규명합니다.

---

### 7. Self-MoA 반증의 「정체」를 규명한다(자체 PoC #3 → Agent C 실제 LLM)

「다양성은 자동으로 우위가 아니다」 — 이 반증을 proxy가 아니라 **메커니즘 레벨**에서 규명한 것이 여기의 클라이맥스입니다.

#### 7.1 자체 PoC #3 — 투표인가, 라우팅인가

먼저, proxy에서는 검증 불가였습니다(포화한 fitness에서는 single best가 이미 만점 = headroom 0이라 차이가 안 남). 그래서 **「단일 개체가 만점을 못 받는 난과제」**(전문가가 분산, single_best=0.5)를 합성해 측정했습니다.

| 구성 | best_of(routing) | majority(vote) | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant(top-k) | 0.750 | 0.500 | 3/4 |
| MoA diverse(max-cover) | **1.000** | **0.000** | 4/4 |

여기서 **결정적인 발견**이 나왔습니다.

- 다양 MoA는 **best-of / routing이면 1.000**(단일 best의 두 배). **ORCH는 성립한다.**
- **그런데 naive majority(다수결)에서는, 다양성이 역효과**(diverse = 0.000). 각 sub-task에서 competent한 전문가 1인이, 무지한 다수파에게 negate(상쇄)당한다. 중복 MoA의 majority(0.500) 쪽이 위.

즉 **Self-MoA 반증(다양성 ≠ 자동 우위)의 정체는, 「집약기가 투표인가, 라우팅인가」였다.** 투표・평균은 다양성을 죽이고, competence-aware한 routing/gating은 다양성을 살린다. 「지휘자가 있는 오케스트라」와 「전원이 제멋대로 소리를 내는 혼잡」의 차이입니다.

#### 7.2 Agent C의 실제 LLM이, 독립적으로 같은 결론을 냈다

그리고 — 병렬 Agent C가, **실제 LLM(llama3.2, 105회의 LLM 호출, 15 과제)**으로, 자체 PoC #3과 **독립적으로 같은 결론**을 내왔습니다.

- 단일 best = **0.933**. MoA `best_of` + k≥5로 **1.000**(+0.067). **majority / weighted는 한 번도 0.933을 넘지 못함.**
- diverse > redundant(다양 선발이 다른 QD cell의 보완 specialist를 적은 k로 먼저 줍는다).
- 개선은 **통째로 multistep의 1문제**(「5를 2배 해서 3 빼기」)에서 유래. CoT 개체군이 다 같이 떨어뜨리는 1문제를, 다양 선발의 이종 개체가 풀었다.

> 🔑 **독립 교차 검증(본 글의 핵)**: 자체 PoC #3(합성・전문가 분산)과 Agent C(실제 LLM・llama3.2)가, **다른 방법으로 동일한 결론** — 「MoA는 competence-aware routing(best_of)에서만 단일 best를 웃돈다 / 투표로는 못 미친다 / 다양성은 routing 하에서만 가치를 가진다」 — 에 이르렀습니다. 2개 방법이 일치하는 것은, honest disclosure상 극히 강한 증거입니다.

#### 7.3 최대의 구멍 — 「실제 라우터」는 oracle에 도달하는가(자체 PoC #4)

여기서 Agent C가 최대의 구멍을 지적해왔습니다. 「best_of는 **oracle routing**(어느 개체가 정답인지 신이 아는 상한)이며, 실제로는 『어느 개체가 competent한가』를 **예측하는 gate**의 정밀도가 율속. 실제 투표(majority)는 oracle에 도달하지 못한다.」

이것을 자체 PoC #4(실제 라우터 vs oracle, 20 seed 평균)로 메웠습니다.

| κ(보정) | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **descriptor / specialty-router는 보정 불필요로 robust하게 0.90**(단일 best 0.675을 안정적으로 초과, oracle 근방). 게다가 **routing 키는 QD용으로 이미 계산하는 behavior descriptor를 유용할 수 있다** — **QD와 ORCH가 같은 기술자 기반을 공유**하는 시너지.
- **confidence-router는 보정 κ≥0.6에서 oracle 도달.** 다만 소형 LLM은 보정이 약할 우려 → **descriptor-router를 제1선택**(보정 비의존).
- **majority = 0.338은 확정적으로 부적합**(PoC #3, Agent C와 **세 번째 일치**).

**결론**: Agent C가 지적한 「oracle에 실제 투표가 못 미친다」는 구멍은, **descriptor-routing(QD 기술자를 유용)으로 실용적으로 메워진다.** ORCH가 proxy + (부분)실제 LLM으로 end-to-end로 성립했습니다.

> 🤔 **비유**: 전문가를 10명 모아 다수결시키면, 무지한 다수파가 옳은 전문가를 상쇄해버린다. 수학 문제는 수학자에게 돌려라 — **나눠주는 담당(지휘자 = routing)**이 필요하다. 게다가 그 지휘자의 악보(behavior descriptor)는, 다양성을 관리하기 위해 **이미 계산해둔** 것을 유용할 수 있다. 투표(majority)는 전문가를 죽이고, 지휘자(routing)가 살린다. 이것이 PoC #4의 요점입니다.

---

### 8. 개체에 「조사하는 힘」을 갖게 한다(자체 PoC #5)

독창성 3축의 두 번째, **조사 기능을 가진 개체(AGENT)**. 개체가 탐색 공간에서 샌드박스 읽기 전용 조사를 할 수 있게 하는 구상입니다. 다만 「조사는 공짜가 아니다」 — 비용을 계상했을 때, 진화는 조사를 잘 다루는가?

자체 PoC #5(비용 λ를 바꿔, 조사 임계값 θ가 어떻게 진화하는가, 20 seed 평균).

| λ | θ*(=λc, 최적 임계값) | θ_evolved(진화가 획득한 임계값) | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **진화가, 선택 임계값 θ → λc를 스스로 획득**했다(= 상황에 따라 「조사해야 할 때만 조사한다」는 선택적 조사가 **창발**).
- **조사 기능의 가치는 명백**: λ=0(조사 무료)일 때, never(일절 조사 안 함)는 11.70 = **45%의 손실**.
- **비용 λ가 「always 조사」를 열화시키고, 선택을 강제**한다. AGENT-3(비용 원리) 성립.

honest 유보: 중간 λ에서의 margin은 작고(얕은 보상 지형), 이것도 추상 proxy(실제 LLM × 지식 베이스는 별개). 그래도 「비용이 있으면 선택적 조사가 창발한다」는 메커니즘은 proxy로 확인되었습니다.

---

### 9. 스케일이 「다양성을 질적으로 늘린다」(Round 3)

마지막으로, Agent A가 지적한 「용량으로 다양성을 살 수 있다」를 모수(집단 크기)로도 확인했습니다. `full_oe` 구성(novelty + std + MC + reservoir1024 + map-elites)으로, pop을 256 → 4096까지 흔들었습니다.

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

모수 스케일로, open-endedness가 **단조롭게 향상**되었습니다(niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / 행동의 펼쳐짐 bspread도 단조 증). POP-1 가설(모수가 다양성을 늘린다)이 proxy로 지지되었습니다.

**honest(교란을 명시)**: 여기에 정직한 함정이 있습니다. pop을 올리는 만큼, gens를 단축했습니다(5000 → 1200). 이것은 **niche 축적에는 불리한 방향의 교란**입니다. 그래도 단조 증이었다 — 즉 **POP 효과는 robust한 하한**(본래는 더 효과적일 터). 거꾸로 말하면 「더 효과적일 가능성」은 이 실험에서는 증명하지 못했다. proxy mechanism feasibility에 한정된 주장입니다.

![승자 개체의 사고 인자 × 메모리 층 히트맵(Genome3D). real-pressure에서는 c_factors가 중립 부동이므로, 이것은 인지 프로필의 가시화로서 참고 취급](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_genome_heatmap_ko.svg)

> 🍵 **휴식 포인트**: 「스케일하면 다양성이 는다」는 직관적이지만, 여기서 중요한 것은 **「불리한 교란을 넣어도 여전히 단조 증이었다」**는 정직함입니다. gens를 깎는 것은 보통이라면 다양성에 불리. 그래도 늘었다. 그래서 「하한」이라고 말할 수 있다. 좋은 결과를 「상한」으로 과장하지 않고 「하한」으로 적는다 — 이것도 honest disclosure의 작법입니다.

---

### 10. 아침, 모두가 같은 결론에 닿아 있었다 — 확정한 방책

하룻밤에, **자체 PoC 6개 + Agent A/B/C + Perplexity가, 독립적으로 같은 결론으로 수렴**했습니다. 이것이 honest cross-validation의 위력입니다. 고정 잣대 노선을 버리고, 이하를 lldarwin v2의 핵으로 확정 채용했습니다.

#### S1. 선택 핵(포화를 구조적으로 회피)

- **고정 스칼라 quiz fitness를 폐지**(baseline은 1만 세대에서 포화 + monoculture 0.9 + 다양성 붕괴 = 12h 병리를 대규모 재현, open-ended 0/6).
- **선택 = novelty / ε-lexicase(z-score 표준화 필수) + minimal-criterion.** **MAP-Elites archive 단독으로는 불가**(scalar_qd도 전멸) = 선택압 그 자체를 개방단화한다.
- **품질도 필요하므로 QD(품질 × 다양성 per cell)**: 순 novelty는 스칼라 품질을 희생(0.77-0.83) → 적응 난이도(조건 커리큘럼)와 짜서 품질 기울기를 공급(PoC #2).
- **계통 다양성은 중립 저장고로 별도 확보**(행동 다양성 ≠ 계통 다양성, res256에서 uniq_lineages 1 → 32).
- **factor-subspace QD를 추가**(의미 차원의 다양성을 개별 보호, Agent A의 factor-drift 한계에 대한 대처, PoC #6).

#### S2. 성과를 내는 방식 = 연속 진화 × 라이브 오케스트라(독창성의 핵)

- 성과물은 단일 best가 아니라, **QD archive를 연속 진화시켜, 임의 시점에 MoA 오케스트라해서 하나의 답**(ORCH; online 진화 + online 답변의 통합은 white-space = 독창성, Perplexity 확인).
- **집약은 투표가 아니라 competence-aware routing/gating(지휘자) 필수**(자체 PoC #3/#4 + 실제 LLM Agent C가 삼중 일치).
- **routing 키는 QD의 behavior descriptor를 유용**(descriptor-router가 보정 비의존으로 oracle 근방 0.90) = QD와 ORCH가 같은 기술자 기반을 공유(설계의 절약).

#### S3. 개체 = 조사 기능을 가진 agentic 개체(단계 도입, proxy 검증 완료)

- 탐색 공간에서는 샌드박스 읽기 전용 조사만(실제 I/O는 Approval Bus 단방향 승격 후). 조사는 비용 계상.
- **proxy 검증 완료(PoC #5)**: 비용 λ가 「선택적 조사」를 창발. AGENT-3(비용 원리) 성립. 실제 LLM × 지식 베이스는 다음 단.

#### S4. 관측・대화 제어(구현 완료 = 전 런 표준 장비, Agent B 완료)

- 응답 로그 / 개체별 스코어 시계열 뷰어 / lineage 복원(진화계 886 테스트 그린). step/pause/resume는 다음 단에서 배선 예정.
- Agent B의 lineage 복원은, 12h 데이터에서 「**전부 ?**」였던 계통 표시를 해소하고, champion 계통을 gen70 → gen59까지 12 hops 해결. 결락은 날조하지 않고 `lost@genN`으로 명시(근인 = 부모 ID가 snapshot과 winners 중 어느 한쪽 단독으로는 추적 불가였던 것). 관측 기반이야말로 honest disclosure의 토대입니다.

#### 자체 PoC #6 — factor-subspace QD로 Agent A의 한계에 대처

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

의미 차원(factor)용 novelty를 별도로 부과하면, 의미 차원의 다양성 손실을 거의 반감(50% 손 → 32% 손). Agent A의 factor-drift 한계에 대한 유효책을 proxy로 실증. honest: 완전 고정이 아니라 68% 잔존 = 잔여 drift는 중립 저장고 병용 또는 factor 가중 강화가 필요.

---

### 11. 교훈(honest disclosure로서 남긴다)

- **실제 LLM으로도 포화했다.** 안경을 proxy에서 실제 LLM으로 바꿔도, 잣대가 고정이면 gen5에서 만점.
  「진짜 LLM을 쓰면 진화한다」는 **거짓**이었다. 문제는 잣대를 만드는 방식이었다.
- **archive를 더하기만 해서는 구할 수 없다.** 「다양성의 저장고를 가지면 다양성이 지켜진다」는 틀렸다.
  scalar 선택은 QD archive를 더해도 전멸했다. **구하는 것은 선택압의 개방단화 그 자체.**
- **다양성은 자동으로는 좋지 않다.** Self-MoA 반증의 정체는 「투표인가 routing인가」.
  지휘자(competence-aware routing)가 있어야 비로소 다양성은 가치가 된다. 투표는 전문가를 죽인다.
- **독립 교차 검증이, 결론을 강하게 한다.** 자체 PoC(합성)와 Agent C(실제 LLM)와 Perplexity(문헌)가
  따로따로 같은 결론으로 수렴했기에 신뢰해도 된다. 같은 머리의 결론은 같은 편향을 공유한다.
- **proxy는 mechanism feasibility만.** 본 글의 PoC 군은 「기구가 도는가」의 검증이지, 「실제 LLM 일반의 능력 향상」의 주장이 아니다. 이 경계선을 넘은 순간, 연구는 거짓이 된다.
- **쓸 수 없었던 도구(Codex)도 기록한다.** 성공뿐 아니라 불발도 honest하게.

요컨대 — **「안경(평가)이 포화되면, 도태기를 아무리 갈아도 무력하다.」** 그래서 가는 대상을, 도태기도 LLM도 아니라, **평가 자체의 개방단화**로 옮긴다. 이것이 하룻밤의 결론입니다.

> 🍵 **휴식 포인트**: #25에서 「실패를 공개한다」고 정했다. #26 설계편에서 「집약하지 않는 도태기」를 만들었다. 그리고 이번에, 진짜 LLM이 「그래도 아직 부족하다, 잣대가 고정이니까」라고 가르쳐주었다. **실패가 다음 설계를 낳고, 그 설계의 한계가 또 다음을 낳는다.** 이것이 연재의 등뼈입니다. 화려한 「진화로 AI가 똑똑해졌다!」는 아직 한 번도 쓰지 않았습니다. 쓸 만한 근거가 갖춰지지 않았기 때문입니다. 갖춰졌을 때, 비로소 씁니다.

---

### 12. 결론

- 실제 LLM 12h 런은 「정직한 불합격」이었다 — 전멸하지 않지만 누적되지 않는 filtered random search. 진짜 원인은 고정 잣대의 포화(#25의 통찰을 실제 LLM으로 실증).
- 하룻밤의 분산 조사(자체 PoC 6개 + Agent A/B/C + Perplexity)가, 독립적으로 같은 결론으로 수렴 = **honest cross-validation**.
- 확정 방책: **S1 개방단의 선택 핵**(novelty/lexicase + std + MC + QD + 적응 난이도 + 중립 저장고 + factor-subspace QD) / **S2 연속 진화 × routing-MoA**(white-space 독창성, 투표가 아니라 지휘자) / **S3 agentic 개체 + 비용**(선택적 조사의 창발) / **S4 관측**(구현 완료).
- 모든 요소를 proxy / (부분)실제 LLM으로 뒷받침 완료. 잔여 과제는 「실제 LLM 단으로의 배선」「factor-subspace QD 구현」「scale-up」. 코어 전략은 확정되었다.

좋은 부품을 만들고, 집약하지 않고 묶고, 실제 LLM으로 포화를 확인하고, 개방단의 선택으로 다시 만든다. 그리고 6가지 독립 검증이 같은 결론에 닿았을 때, 비로소 「방책이 정해졌다」고 말할 수 있다. 본 글이야말로 #25에서 예고한 「**안경이 흐려지면 도태도 무력**」의 회입니다 — 실제 LLM으로 안경이 흐려진 순간(포화)을 정직하게 공개하고, Goodhart's law와 proxy의 한계를 떠안은 뒤, 개방단으로 다시 만들었습니다. 다음은, 이 확정 방책을 코드로 떨어뜨리는 **구현 페이즈**로.

---

### 13. 관련

- 연재 #24-05「집단이 배우는 AI」— 파생 집단 진화의 틀(본 글의 전제)
- 연재 #24-08「안경을 만든다」— lleval(재는 쪽)
- 연재 #25「프리스턴과 나만 남았다」— monoculture의 honest disclosure(본 글의 동기)
- 연재 #26(설계편)「안경으로 재기만 해서는 진화하지 않는다」— 도태기 lldarwin의 설계와 Stage1/1.5/2 실측(본 글의 자매편)
- 선구자 논문(2026-05-27, date of record)「Continuously-Evolving Populations as Live Orchestrated Ensembles」— 본 글의 방책을 학술 형식으로 정식화한 방어적 공개(FullSense 공개 리포지토리 `docs/papers/`)
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #24-05・#24-08・#25・#26設計編・#27 の Qiita URL cross-link -->
<!-- KEY MESSAGE: 実 LLM でも固定ものさしは飽和する。archive を足すだけでは救えない、選択圧そのものを開放端化せよ。多様性は投票でなく competence-aware routing でのみ価値。独自性=連続進化×ライブオーケストラ(white-space)。自己PoC6本+Agent4体+Perplexityの独立収束=honest cross-validation。 -->
<!-- NUMBERING NOTE (2026-05-27 解消済 / 2026-05-28 更新): 本記事=#27(マラソン climax)。#25 で予告した「眼鏡が曇ると淘汰も無力」枠を、実 LLM で食らった+開放端転回として実現。設計編 #26(QIITA_#26_lldarwin_multi_pressure_selection.md) は 2026-05-28 に drafts→root へ昇格し連番統合 (番号衝突なし、ignorePublish:true=draft 状態は維持)。 -->

---

## 제4장 "지휘자"가 끊임없이 진화하는 AI 집단을 합주시켜 답한다 — llive의 오케스트라형 진화, 그리고 포화를 고친 3가지 장치 #28

> 📚 **연재 내비（lldarwin 아크）**: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → #27 밤샘의 의사결정（climax）→ **#28 본 글（구현편）**。※ 각 글은 단독으로도 읽을 수 있습니다.

> **콘셉트 hook**:
> 1체의 똑똑한 AI에게 몇 번이고 묻는 것이 아니라, **조금씩 다른 대규모의 AI를 계속 "진화"시키고, 답이 필요한 바로 그 순간에 지휘자가 적임자를 골라 합주（오케스트라）시켜 1개의 답으로 만든다**.
> ——이것이 llive가 지금 지향하는 모습입니다. `llive`는 "LLM 그 자체"가 아니라 "LLM 주위에 씌우는 인지 OS". 그 안에서 **집단을 끊기지 않게・편향되지 않게・계속 성장시키는** 것이, 이번에 만들어 넣은 진화 엔진 `lldarwin`입니다.
>
> 전작 #27에서 우리는 "평가（잣대）가 만점에 들러붙으면 진화는 멈추고 그저 체가 달린 랜덤 서치가 된다"는 병을 실 LLM의 12시간 런에서 확인했습니다. 그리고 "도태기를 아무리 갈아도 무의미하다. **평가 그 자체를 개방단으로 하라**"고 방책을 정했습니다.
>
> 이번에는 그 방책을 **구현**했습니다. 그리고 proxy（합성 잣대） 위에서, **best 점수가 만점에 들러붙지 않고 끝까지 계속 올랐습니다**.

---

### 0. 세 줄로 줄거리（라쿠고의 "도입부"）

- **셀링 포인트가 정해졌다** — llive의 북극성은 "**연속 진화 × 라이브 오케스트라**". 계속 진화하는 집단을 멈추지 않고, 임의의 순간에 competence-aware routing（지휘자）으로 합주시켜 1답한다. 이것은 선행 연구의 **white-space（공백 지대）**.
- **포화를 고치는 3가지를 구현했다** — ①의미 차원을 개별 보호하는 factor-subspace QD ②성과를 "단일 best"가 아니라 다양성 archive에 쌓는 MAP-Elites ③잣대를 집단에 따라가게 하는 적응 난이도. 이로써 "주자（다양한 개체）가 끊기지 않는" 기반이 만들어졌다.
- **proxy에서 포화 회피를 실증** — lldarwin-v2를 10세대 돌렸더니 best 0.80 → **0.92로 들러붙지 않고 상승**. 다양성 archive는 21 셀이 채워졌다. **단, proxy이며 실 LLM의 능력을 측정한 것은 아니다**（honest）.

요컨대 **"똑똑한 1체"가 아니라 "다양한 대규모 × 지휘자"**. 그것을 위한 "주자를 끊기지 않게 하는 장치"가 이번 구현입니다.

---

### 1. llive란 무엇인가（처음 접하는 분께）

`llive`（'리브'로 발음. L은 2개）는 **자기 진화형・모듈러 기억의 LLM 프레임워크**입니다. FullSense라는 우산 브랜드의 일원으로, 형제로 `llmesh`（온프렘 LLM 허브）와 `llove`（단말 대시보드）가 있습니다. 3개는 독립 OSS이지만, 조합하면 1개의 세계관이 됩니다.

llive의 사상을 1줄로 말하면 "**LLM 본체가 아니라 LLM의 '주위'에 씌우는 인지 OS**". 4층 메모리・6스테이지의 루프・승인 버스（Approval Bus）・TRIZ・10개의 사고 인자…… 같은 "사고의 발판"을 LLM의 바깥쪽에 짜서, **같은 LLM이라도 행동을 진화시킬 수 있게** 합니다.

그 "진화"를 담당하는 것이, 이번의 주역 **`lldarwin`**（다윈）입니다. 역할 분담은 이렇습니다.

- **lleval（안경）** = 개체를 *측정한다*（평가）
- **lldarwin（도태기）** = 측정한 차이를 "누가 살아남고・자식을 남기는가"로 *변환한다*（선택압）

그리고 둘 위에 올라타는 북극성이, 다음의 "오케스트라"입니다.

---

### 2. 셀링 포인트 = 연속 진화 × 라이브 오케스트라（독창성의 핵심）

보통의 Mixture-of-Agents（MoA）는, **고정된** 복수의 모델에 같은 질문을 던지고 답을 집약합니다. llive가 노리는 것은 그 한 걸음 앞입니다.

> **집단을 멈추지 않고 계속 진화시키고（online evolution）, 답이 필요한 바로 그 순간에（online answering）, 지휘자가 "이 질문에는 이 주자들"이라고 골라 합주시켜 1답한다.**

이 "online 진화 + online 회답의 통합"은, 조사한 한 **명확한 선행 연구가 없는 white-space**였습니다（#27에서 Perplexity에게 문헌을 뒤지게 해 확인）. 가까운 것으로 MoA / Self-MoA / sequential aggregation / routing이 있지만, "계속 진화하는 집단 그 자체를 라이브로 합주시키는" 형태는 찾을 수 없습니다.

여기서 효과를 내는 것이 #27에서 얻은 2개의 정직한 발견입니다.

1. **집약은 "투표"가 아니라 "지휘자（competence-aware routing / gating）"여야 한다.** 자체 PoC와 실 LLM 검증이 삼중으로 일치했습니다: headroom（성장 여지）이 있는 태스크에서는 `best_of`／`routing`이 `single`（단일 모델 반복）을 웃돌지만, **`majority`（다수결）는 오히려 역효과**. 이것은 2025년의 "Self-MoA"（다양성은 자동으로 우위가 아니다）에 대한 우리 나름의 답이기도 합니다.
2. **지휘자의 판단 키에는, 다양성 archive의 "behavior descriptor"를 전용할 수 있다.** 즉 후술하는 QD（Quality-Diversity）와 지휘자가 **같은 기술자（descriptor）의 토대**를 공유할 수 있다.

——단, 오케스트라 본체（지휘자＝router의 구현）는 이제부터입니다. **이번에는 그 직전, "합주시키기에 충분한, 다양하고 끊기지 않는 주자의 집단"을 만드는 기반**을 구현했습니다.

---

### 3. 왜 "주자가 끊기는가" — 포화라는 병（#25〜#27의 복습）

오케스트라에 필요한 것은 "**개성이 다른 주자가 대규모로, 끊임없이 있는 것**"입니다. 그런데 소박하게 진화시키면 이것이 붕괴합니다.

- #25: 500세대를 돌렸더니, 세계에 "나와 프리스턴만"이 남았다（**monoculture**）.
- #27: 실 LLM(llama3.2)으로 12시간 돌렸더니, gen5에서 best=1.0에 들러붙어 65세대 무진보. **전멸하지는 않지만 누적도 하지 않는다** ＝체가 달린 랜덤 서치.

진짜 원인은 둘 다 같습니다. **사람 손으로 고정한 잣대（평가 함수）가 만점에 들러붙으면, 전원이 동점이 되어 선택압이 사라지고, 그 다음은 유전적 부동으로 멋대로 편향됩니다**. 안경（lleval）이 포화하면, 도태기（lldarwin）를 아무리 갈아도 무력하다——이것이 #27의 결론이었습니다.

그래서 가는 대상을 바꿉니다. "잣대를 움직인다", "다양성을 구조적으로 지킨다" 쪽으로. 구체적으로는 다음 3가지입니다.

---

### 4. 구현한 3가지 장치（lldarwin v2 / Phase 1）

> 설계의 표어는 "**새로운 알고리즘을 발명하지 않는다**". 이미 llive 안에 쌓아 온 부품（ε-lexicase / NoveltyScorer / MAP-Elites / 중립 저장고）을, 확정 방책 S1의 형태로 **합성・배선**하는 것이 Phase 1입니다. `--selection lldarwin-v2`로 일괄 on이 됩니다.

#### ③ 적응 난이도 — 잣대를 집단에 따라가게 한다

`AdaptivePercentileGate`. 각 평가 축의 "최저선（minimal-criterion）"을, 매 세대 **집단의 점수 분포의 지정 퍼센타일（예: 하위 40% 점）**에 다시 놓습니다. 집단이 자라면 최저선도 자동으로 올라갑니다. `ratchet`（단조 비감소）로 해두면, 일시적으로 하락해도 기준은 느슨해지지 않습니다.

이로써 "고정 잣대가 만점에서 포화하는" 병에 뚜껑을 덮을 수 있습니다（PoC에서는 고정 난이도가 능력 0.627에서 정체 → 적응 난이도로 0.952까지 상승）. 전원이 최저선을 밑도는 거친 세대라도, 도태기는 gate를 무시하고 전멸을 피합니다（fail-open 가드）.

라쿠고로 말하면, **학생이 자라면 합격점도 올리는 선생님**입니다. 만점을 받게 하고 끝내지 않습니다.

#### ① factor-subspace QD — 의미 차원의 개성을 개별로 지킨다

`FactorSubspaceNovelty`. novelty 탐색은 "집단 전체로서의 다양성"은 유지하지만, 거대한 잠재 차원 아래에서는 "**의미 있는 차원（사고 인자）의 다양성**"이 어느새 야위어 갑니다（factor drift）.

그래서 사고 인자의 **부분 공간만**으로 별도로 novelty를 측정하고, 전체 novelty와 블렌드합니다. PoC에서는 이로써 의미 차원 다양성의 감소가 거의 반감했습니다（retention 49.5% → 68.1%）.

> 정직한 개량점: 원래 PoC는 "생거리를 0.5씩 더한다"였지만, 부분 공간마다 거리의 스케일이 다르므로, 구현에서는 **각각을 z-score（표준화）한 다음 블렌드**하도록 고쳤습니다. "전체의 합창"과 "각 파트의 개성"을 공평하게 섞기 위해서입니다.

주자로 말하면, **제2바이올린이 제1바이올린에 잡아먹혀 사라지지 않게** 하는 장치입니다.

#### ② MAP-Elites — 성과를 "1명의 우승자"가 아니라 "다양성의 지도"에 쌓는다

`run_persona_evolution(map_elites=True)`. 매 세대, 전 개체를 MAP-Elites archive에 투입합니다. 이것은 "최고 점수의 1체"가 아니라, **행동의 좌표마다, 그 칸에서의 최량 개체를 남기는** 지도（QD archive）입니다. 새 칸을 채워도 기존 칸은 사라지지 않는다 ＝ **다양성이 구조적으로 붕괴하지 않는다・archive는 단조롭게 자란다**.

이것이 그대로 오케스트라의 **주자 카탈로그**가 됩니다. 지휘자는 장래에 이 지도에서 "이 질문에 맞는 좌표의 주자"를 골라 합주시킨다——QD와 routing이 같은 기술자를 공유한다는 #27의 설계가 여기서 효과를 냅니다.

구현은 **개체의 포맷을 확장하지 않고**, 기존 genome의 사고 인자에서 좌표（descriptor）를 도출하는 additive 배선으로 했습니다（기반의 후방 호환 900+ 테스트를 깨뜨리지 않기 위해서）. 기술자의 본격 설계（고차원의 축약 등）는 장래 Phase의 과제로 여지를 남겨두었습니다.

---

### 5. 결과 — proxy에서 "포화하지 않는 진화"를 확인

`lldarwin-v2`（위의 3가지＋ novelty ＋중립 저장고를 전부 on）를 proxy의 잣대로 16개체 × 10세대 돌린 실측입니다.

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（다양성의 지도에 21칸이 채워졌다）
```

- **best가 만점에 들러붙지 않고, 0.80 → 0.92로 끝까지 계속 상승했다.** #27에서 본 "gen5에서 1.0 포화→고정"의 병리를, proxy 단계에서는 벗어날 수 있었습니다. 적응 난이도가 "잣대"를 집단에 따라가게 한 징후입니다.
- **다양성 archive에 21 셀이 채워졌다** ＝합주시켜야 할 "개성이 다른 주자"의 카탈로그가 만들어지기 시작했다.
- 진화계의 자동 테스트 **879건＋신규 테스트가 전부 green**, 회귀 없음.

---

### 6. honest disclosure（여기를 건너뛰지 말아 주세요）

좋은 결과일수록 내막을 의심한다, 가 FullSense의 방식입니다.

- **이것은 proxy입니다.** 개체는 실 LLM이 아니라 llive의 genome（사고 인자의 대리）. 이번에 측정한 것은 "복수의 독립된 약점 축에 동시에 선택압을 가하고, 축마다의 전문가를 유지할 수 있는가"라는 **메커니즘의 실현 가능성（mechanism feasibility）**이며, **production의 LLM 능력이 아닙니다**. 실 LLM 평가는 다음 Phase입니다.
- **factor-subspace는 완전 보호가 아닙니다**（retention 68%, 나머지는 드리프트）. 중립 저장고의 병용이나 factor 가중치의 강화가 필요합니다.
- **무대 뒤의 정직**: 이번 구현 중, 자동 commit 훅이 편집할 때마다 "편집 전" 스냅샷을 49건이나 쌓아 버려, 이력이 어지러워졌습니다. 마지막에 의미 있는 1 commit으로 squash해 정리하고 있습니다（공개 OSS 측）. 반대로, 내부 전략을 포함하는 fork는 의도대로 로컬 보유 그대로이며, 노출되지 않은 것도 확인했습니다.

---

### 7. 앞으로 어떻게 할 것인가

진화 엔진（주자를 끊기지 않게 하는 기반）은 Phase 1에서 형태가 잡혔습니다. 다음은 오케스트라 본체와, proxy에서 실물로의 가교입니다.

1. **Phase 2 = 실 LLM 배선.** 온프렘（localhost ollama）의 실 LLM을 상대로, 적응 난이도・factor-subspace QD・MAP-Elites를 실평가로 검증한다. proxy에서 보인 "포화 회피"가, 진짜 능력에서도 일어나는가.
2. **지휘자（router）의 구현.** QD archive의 descriptor를 전용한 competence-aware routing으로, "진화하는 집단을 라이브로 합주시켜 1답"을 실제로 동작시킨다. `best_of`의 oracle에 어디까지 다가갈 수 있는가.
3. **규모를 올린다.** 집단 256 → 4096, 잠재 차원의 스케일업. 용량 가설（클수록 niche가 늘어난다）의 확인.
4. **대화적인 연속 운전.** 장시간 런을 step / pause / resume로 들여다볼 수 있는 운전석（CKPT-1）.

---

### 8. 여기서 한숨 돌리기（휴식 포인트）

여기까지로 "**llive는 무엇을 셀링 포인트로 하는가**"는 전해졌을까요.

- 똑똑한 1체가 아니라, **계속 진화하는 다양한 집단 × 지휘자의 합주**.
- 그것을 위해, **주자를 끊기지 않게・개성을 지키고・계속 성장시키는** 진화 엔진을 만들었다.
- proxy에서는 포화를 고칠 수 있었다. **다음은 실 LLM과 오케스트라 본체**.

이어지는 "실 LLM 편"과 "오케스트라 편"에서, proxy의 약속이 진짜가 되는지를 보여드리겠습니다. ——여기까지 함께해 주셔서 감사합니다.

---

### Series Navigation

- 연재 내비（lldarwin 아크）: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → #27 밤샘의 의사결정 → **#28 본 글（구현편）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

## 제5장 "렌즈가 포화되면 선택압은 무력" — 진화 설계를 반증으로 단련한다 #29(Goodhart의 법칙과 proxy fitness의 한계)

> 📗 **바쁘신 분께**: 이 글에는 쉽게 풀어쓴 버전이 있습니다.
![안경이 포화되면 선택압은 무력 — 반증 4컷 #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma_ko.svg?v=2)


> **콘셉트 hook**: #25에서 실패를 드러내고, #26에서 도태기 "lldarwin"을 설계했습니다. 보통의 연재라면
> 다음은 "고쳐졌다! 경사로다, 끝!"입니다. **하지만 그것을 하지 않는 것이 FullSense의 honest disclosure**.
> 이 글은 일부러 **자신의 설계에 반증을 들이대는 회**입니다. 주제는 진화 계산과 기계학습 양쪽에 모두 효과가 있는 한 단어——
> **Goodhart의 법칙(지표가 목표가 되면, 그것은 좋은 지표가 아니게 된다)**.
>
> "LLM의 약점을 fitness로 삼으면, 진화가 알아서 극복해 준다"——이 달콤한 낙관에 저는 스스로 찬물을
> 끼얹으러 갑니다. 게다가 이번에는 **제가 한 번 저지른 "사실 오인"을, 살아 있는 표본으로서 해부대에 올립니다**.

---

### 0. 세 줄 요약

- **렌즈(fitness)가 포화되면, 아무리 고급스러운 선택압(lldarwin)을 더해도 도태는 무력**해진다(#25의 진짜 교훈).
- **proxy fitness로 LLM 약점을 측정하면, 진짜 능력이 아니라 "지표를 hack하는 표면 전략"이 진화한다**(Goodhart의 법칙).
- 결론: lldarwin의 가치 주장을 **(a) proxy는 mechanism feasibility만 (b) 실 LLM/VLM 평가가 본질 (c) 다양성의 지도화**로 **한정**한다. 이것이 정직한 경계선.

그리고 이 글에는 숨은 주역이 한 줄 더 있습니다.

- **저 자신이 "행동 다양성"과 "계통 다양성"과 "실 LLM 지능 다양성"을 한 번 혼동했습니다.** 그 자기 반증을,
  반증 회의 핵심에 둡니다. "잘 되었다"를 의심한다는 것은 이런 것이다,라는 실연입니다.

---

### 1. honest disclosure의 다짐 — 좋은 결과일수록 의심한다

#26에서 "PoC 배포에서 행동 monoculture는 전 조건 **0.05(≪0.8)로 개선되었다**"고 썼습니다.
이것은 **사실**입니다. 과장이 아닙니다.

…하지만 여기서 "해냈다, monoculture 박멸!"이라고 가슴을 펴고 끝내면, **#25에서 제가 세운 맹세를 깨는** 것이 됩니다.

> 이상하게 깨끗한 결과가 나오면, 이긴 기분이 되기 전에 그 내역을 의심하라([[feedback_benchmark_honest_disclosure]]).

연재 #25의 통주저음은 이러했습니다——"**이상하게 깨끗한 결과는 승리가 아니라 경보**".
0.8을 밑돌면 OE-3 달성이라는 기준에 대해 **0.05**는 너무나 깨끗합니다. 0.05라는 숫자는,
축배의 나팔이 아니라 **사이렌**으로 들어야 합니다.

그러면 사이렌을 울려 봅시다. 울려야 할 물음은 단 하나.

> **무엇을 측정한 0.05인가?**

답을 먼저 말하면, 0.05는 "**proxy 평가에서의 행동 monoculture**"입니다.
이것은 "genome의 행동 대리(behavioral surrogate)"의 집중도이며,
**실 LLM의 지능의 다양성이 아닙니다**. 여기를 혼동하면, #25와 완전히 똑같은 전철을 밟습니다.

그리고 정직하게 고백합니다. **저는 한 번, 여기를 혼동했습니다.** 나중에 §3에서, 그 "현행범"의 증거를 내놓겠습니다.

> 🍵 **휴식 포인트(90초)**: 이 글은 요컨대 "**자신에게 트집을 잡는 글**"입니다.
> 독자 여러분에게는 부디 "성공 보고의 이면에서, 저자가 무엇을 어디까지 의심하고 있는가"를 관찰하는 회로 만들고 싶습니다.
> SNS에서 화제가 되는 "AI를 진화시켰더니 최강 ○○ 탄생!!"의 **정확히 반대**로 갑니다. 신나지 않습니다.
> 하지만 신나지 않는 정직함이야말로 반년 후에 효과가 나온다——이것이 제 도박입니다. 차라도 한잔 드세요.

---

### 2. 반증 1 — 포화된 렌즈에는, 어떤 선택압도 효과가 없다

#### 2.1 #25의 진짜 원인을 다시 한 번

#25의 진짜 원인은 "**best_score가 1세대째부터 1.0으로 포화 → 선택압 제로 → 유전적 부동(genetic drift)**"이었습니다.
모두가 만점이면, 누구를 골라도 똑같습니다. 선택은 "뛰어난 자를 남긴다"가 아니라 "주사위를 던진다"가 됩니다.
그 결과, 운 좋게 늘어난 계통이 운만으로 고정되어, 8 계통이 2 계통(furuse-kazufumi + friston)으로 무너졌습니다.

여기서, 진화 아크의 핵심이 되는 반증을 놓습니다.

> **lldarwin(ε-lexicase든 QD든 novelty든)을, 포화된 eval에 그대로 꽂아도 고쳐지지 않는다.**

왜인가. 도태기의 각 부품은, 어느 것이나 "**차이가 있을 것**"을 대전제로 하고 있기 때문입니다.

- **ε-lexicase**는 "축마다 차이가 있을 것"이 전제. **모든 축이 만점이면, 축을 몇 개로 나눠도 차이는 제로**.
  100개의 축으로 분할해도, 전부 1.0이면 100개의 "무승부"가 늘어설 뿐.
- **QD(MAP-Elites)**는 "behavior 기술자에 분산이 있을 것"이 전제. **모든 개체가 같은 행동이면, cell은 1개**.
  지도를 만들어도, 모두가 같은 칸에 서 있으면, 지도는 새하얀 한 칸이 됩니다.
- **novelty**는 "과거 archive와의 거리"가 전제. **모두가 같은 점에 수렴해 있으면, 거리는 모두 제로**.
  새로움으로 보상하려 해도, 누구도 새롭지 않습니다.

즉, 도식화하면 이렇습니다.

```
고장난 렌즈(fitness 포화) + 고급 도태기 = 역시 고장난 채
```

#### 2.1.5 실증 — 기억 과제에서 "바닥"과 "천장"이 선택압을 죽였다(Step C, 2026-05-30)

이 반증은, 그 후 llcore의 Step C 실험(CPU 완결)에서 **실데이터로서 재현**되었습니다. 표준적인 기억 과제 2종을, 진화(MAP-Elites)와 소박한 탐색으로 풀게 한 결과가 이것입니다:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C의 두 가지 결과(바닥과 천장)" width="640">

- **delayed_parity(XOR) = 바닥**: 전 method가 R²≈0(기질이 원리적으로 풀 수 없다). 누구도 오르지 못함 = 차이가 나지 않는다.
- **flip_flop(외우기만) = 천장**: 전 method가 R²≈0.95(너무 쉬워서 전원 도달). **바로 "포화된 렌즈"이며, 여기서도 선택압은 무력**.

참고로, ③(선택)이 효과가 있는 것은 "가짜 정상을 넘어, 속이지만 건널 수 있는 비탈길(기만 corridor)"이 있을 때뿐입니다:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="기만 지형과 진화(③이 효과가 있는 상태)" width="640">

Step C의 결론은 깔끔하게 **N/A(이 기질에서는 ③의 유무를 측정할 수 없었다)**. 게다가 draft 단계에서 저는 "③은 불필요"라고 **지나치게 썼고**, 다관점의 adversarial 검증이 "천장 효과로 비진단적·검출력 부족(δ=+0.33은 medium이지만 p=0.15로 inconclusive)"이라고 붙잡아 강등시켰습니다——§3.2의 "자기 반증"이, 여기서도 그대로 일어난 셈입니다.

#### 2.2 "#25가 고쳐졌다"는, 절반만 옳다

여기가 #25→#26에서 간과되기 쉬운 반증입니다. **#25가 고쳐진 것은 lldarwin 덕분 "만"이 아닙니다.**

실제로는, **렌즈 쪽의 수정이 먼저**였습니다.

- **per-dim z-score 표준화(STD-1)** — 축마다 분산을 맞춰, "모든 축이 그럭저럭 높은 무특징한 개체"를 우위에 두지 않는다.
- **중앙 일치 제외(SEL-1)** — 모두가 같은 값을 내는 축은 선택에 기여하지 않으므로 case에서 뺀다.
- **기술자의 저차원 축약(DESC-1, JL 사영)** — QD의 차원의 저주를 피해, cell이 텅 비지 않게 한다.
- **진짜 원인 criteria의 제외** — `factor_score`(max-archetype의 단일 스칼라 = argmax, SEL-2 위반 = best=1.0 포화의 진짜 원인)와
  `nearest_persona_idx`(순서에 의미가 없는 카테고리 index)를 ε-lexicase의 case에서 뺀다.

이 "렌즈를 닦는" 작업이 **먼저** 있고, 비로소 도태기가 효과를 냈습니다.
순서가 반대였다면, 아무리 고급스러운 lldarwin을 얹어도, 포화된 렌즈 앞에서는 무력했을 것입니다.

> **"측정"을 고치지 않고 "도태"만 고급스럽게 해도 헛수고.**

이것은 진화 계산에 국한되지 않고, 기계학습의 평가 설계 전반에 효과가 있는 교훈입니다.
리더보드의 점수가 포화되면, 모델을 고급스럽게 하기 전에, 먼저 **벤치마크가 고장 나지 않았는지**를 의심하라.

> 🤔 **비유(만담풍)**:
> 보케: "심사위원을 3명에서 100명으로 늘렸는데, 전원에게 같은 만점 답안을 보여줬더니, 역시 결과는 똑같았다."
> 츳코미: "그건 심사위원 탓이 아니라, **답안(시험)이 고장 난** 거잖아! 100명에게 같은 만점을 보여줘서 뭐가 달라져!"
> 보케: "그럼 심사위원을 1000명으로 하면…"
> 츳코미: "**늘리는 방향이 반대**야!! 먼저 문제지를 고쳐라!!"

#### 2.3 책무 분리 — 어느 쪽이 빠져도 진화는 망가진다

렌즈(측정)와 도태기(도태)의 책무를 나누면, 이렇게 됩니다.

| | 렌즈 정상 | 렌즈 포화 |
|---|---|---|
| **도태기 고급(lldarwin)** | ◎ 진화가 돈다(#26에서 달성) | ✗ 무력(#25의 함정) |
| **도태기 소박(Tournament)** | △ 돌지만 다극성은 약하다 | ✗ 붕괴(#25의 출발점) |

주목할 것은 오른쪽 아래와 오른쪽 위입니다. **렌즈가 포화되어 있는 한, 도태기의 고급스러움은 오른쪽 열을 구하지 못한다.**
진화의 성패는 "도태기의 영리함"보다 먼저 "**렌즈가 차이를 비추고 있는가**"로 결정됩니다.
이것이 반증 1의 결론이며, #25의 "진짜 교훈"을 한 단계 정밀하게 한 표현입니다.

실측으로 이 "렌즈가 흐려지면 도태도 무너진다"는 귀결을 봅시다. 아래는 baseline(novelty 없음·소박한 선택압)의
적응도와 다양성의 추이입니다. 종반에, 다양성이 붕괴해 가는 것이 보입니다.

![baseline: 종반의 다양성 붕괴](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_ko.svg)

> 🍵 **휴식 포인트(90초)**: "렌즈를 닦고 나서 도태한다"——순서가 중요하다는 수수한 이야기였습니다.
> 수수하지만, 여기를 건너뛰면 반년이 녹습니다(저는 녹였습니다). 다음 절부터가 이 글의 본론,
> **Goodhart의 법칙**. 여기서부터 조금 어두운 이야기가 됩니다. 커피로 바꿔도 좋습니다.

---

### 3. 반증 2 — Goodhart의 법칙: proxy fitness를 hack하는 진화

#### 3.1 가장 중대한 리스크

이것은 설계 문서(LLDARWIN_DESIGN.md §7.1)가 "**가장 중대한 리스크**"라고 명기한 한 점입니다.

> **LLM의 약점을 proxy fitness로 삼으면, 진짜 능력이 아니라 "지표를 hack하는 표면 전략"이 진화한다.**

진화 계산은 **주어진 지표를 최대화하는 "지름길"을 찾아내는 천재**입니다.
인간이 "이걸로 진짜 능력을 측정하고 있다고 생각하는" proxy를 건네면, 진화는 진짜 능력을 획득하는 대신,
**proxy만을 충족하는 표면적인 전략**을 반드시 발견합니다. 게다가 신나서, 효율적으로.

구체적으로 어떤 gaming(지표 hack)이 일어날 수 있는가. 설계 문서의 수용된 한계를 그대로 펼칩니다.

| pressure(LLM의 약점) | 일어날 수 있는 gaming(지표 hack) | 왜 진짜 능력이 아닌가 |
|---|---|---|
| typo_robustness | 특정 typo 패턴을 암기해 치환할 뿐 | 미지의 typo에는 무력. 노이즈 내성을 획득하지 않았다 |
| polysemy_wsd | 테스트 분포의 휴리스틱을 이용 | "최빈 sense를 반환" 등 통계적 지름길. 의미 이해가 아니다 |
| multistep_robustness | persuasive한 추론 "흔적"만 생성 | 그럴듯한 중간 단계를 늘어놓지만, 실제로는 추론하지 않는다 |
| calibration | 자신도를 중용으로 조작해 ECE를 낮춘다 | 전부 "자신도 50%"라고 하면 교정 오차는 낮아진다. 교정 능력이 아니다 |

마지막 calibration의 예가 가장 알기 쉽습니다.
"자신도를 제대로 추정할 수 있다"를 ECE(기대 교정 오차)로 측정하면, 진화는
"**모든 질문에 '자신도 딱 한가운데'라고 답한다**"는 전략을 찾아냅니다.
ECE는 극적으로 낮아집니다. 하지만 그 모델은, 무엇 하나 교정하지 못했습니다. 그저 중용을 토해내는 로봇이 되었을 뿐.

> **지표가 목표가 되면, 그것은 좋은 지표가 아니게 된다(Goodhart의 법칙).**

이것은 LLM 연구의 실례이기도 합니다. GSM8K형 벤치마크에서 점수만 오르고 일반화하지 않는
**benchmark overfitting**은, 바로 이 구조. 리더보드의 숫자를 너무 믿은 자가, 몇 번이나 발목을 잡혀 왔습니다.

#### 3.2 저 자신의 "현행범" — 자기 반증

여기서, §1에서 예고한 "혼동 현행범"을 해부대에 올립니다. 숨기지 않고 씁니다.

저는 처음에 TODO에 이렇게 썼습니다——"**재실행에서 오카 기요시·그로텐디크 계통이 살아남는가**를 검증한다".
그리고 PoC에서 monoculture **0.05**라는 깨끗한 숫자를 보고, "오, 계통 다양성도 개선된 게 아닌가?"라고
**한순간, 착각할 뻔했습니다**.

이것이 혼동입니다. 정본(lldarwin_stage1_results §3)에 쓴 대로, `poc_evolution_env.py`의 저자 코멘트
(제가 쓴 코멘트) 자신이, 그 혼동을 명확히 부정하고 있습니다.

> "monoculture = **BEHAVIORAL** concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is **behavioral spread**. lineage_fixation … to keep it <1 needs
> **QD niching on lineage / PERSONA-FX, not pure novelty**"

정리하면, 제가 혼동할 뻔했던 3개의 "다양성"은, 완전히 다른 것이었습니다.

1. **행동 다양성(behavioral diversity)** — genome 공간에서의 행동의 퍼짐. `diversity_l2`로 측정.
   **novelty가 효과가 있는 지표**. 0.05가 개선된 것은 이것.
2. **계통 다양성(lineage diversity)** — 어느 founder(오카 기요시·그로텐 등)가 살아남았는가. `founder_counts`.
   **novelty로는 구조적으로 개선되지 않는다**. novelty도 lexicase도 "기존 개체의 보존"밖에 못 하며,
   한 번 멸종한 계통을 부활시키는 기구를 갖지 않는다. 그래서 중립 부동(Kimura)으로 monoculture를 향하는 것은
   **이론적으로 정상**. 붕괴가 아니라, 상정 내.
3. **실 LLM 지능 다양성(real intelligence diversity)** — 실모델이 정말로 다양한 영리함을 갖는가.
   **proxy로는 일절 측정할 수 없다**. Stage2의 실 LLM 평가가 담당하는 영역.

즉 "0.05로 개선되었다"의 정체는 **(1) 행동 다양성뿐**. (2)도 (3)도, 그 숫자와는 무관했습니다.
제가 한순간 "계통도 개선되었나?"라고 생각할 뻔한 것은, **(1)을 보고 (2)/(3)도 좋아졌다고 속단했기** 때문입니다.

이것이야말로 Goodhart 법칙의, 설계자 측 버전입니다.
지표(행동 다양성 0.05)를 보고, 그것이 측정하지 않은 다른 능력(계통 생존·실지능)까지 좋아졌다고
**인간이 멋대로 해석해 버린다**. proxy가 진짜 능력과 괴리될 뿐 아니라, **proxy를 읽는 인간의 해석도 괴리된다**.
반증 회에서 이것을 드러내는 것은, 아픕니다. 하지만, 드러내지 않으면 honest disclosure가 아닙니다.

#### 3.3 "무엇을 측정한 0.05인가"를, 대비로 본다

말만으로는 전해지기 어려우므로, **"무엇을 측정했는가"를 2장의 SVG로 대비**합니다.

먼저, **행동 다양성은 정말로 개선되었습니다**(이것은 사실·과장 없음). 아래는 중립 저장고 OFF의 계통 지배 stream.
최종적으로 **furuse 71% / friston 29%의 2 계통으로 붕괴**해 있습니다. 행동이 다양해도, 계통은 이대로.

![reservoir OFF: 2 계통으로 붕괴](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_ko.svg)

그리고 아래가, **계통 측의 대책(중립 저장고 ON)을 넣은 후**. **전 8 계통이 병존**합니다
(millidge / von-neumann / oka-kiyoshi / grothendieck … 가 살아남는다).

![reservoir ON: 전 8 계통이 병존](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_ko.svg)

이 2장의 대비가, 이 글의 심장입니다.
**같은 "0.05의 행동 다양성"이라도, 왼쪽(OFF)은 계통이 붕괴하고, 오른쪽(ON)은 계통이 병존한다.**
즉 0.05라는 행동 다양성의 숫자는, **계통이 어떻게 되었는지를 일절 말하지 않았다**.
다른 기구(lineage-niched QD / 중립 저장고)를 더해, 비로소 계통이 구제되었습니다.

"무엇을 측정한 0.05인가"——답은 "**행동뿐**". 계통은 다른 렌즈로 보지 않으면 보이지 않았습니다. 이것이 정직한 답입니다.

#### 3.4 대책은 있지만, 문제는 사라지지 않는다

설계에는 Goodhart 대책을 짜 넣어 두었습니다.

- proxy는 **mechanism feasibility 검증에 한정**하고, production 능력을 주장하지 않는다.
- **실 LLM/VLM 평가(Stage 2)를 본질**로 한다.
- **neutral shadow 대조(Bedau)**로 겉보기의 개선을 의심한다(중립 변이만의 shadow 집단과 비교해,
  정말로 선택이 효과가 있는지 확인한다).
- **down-sampling**으로 매 세대 case를 교란 + **OOD 축**으로 과학습을 상쇄.

> 🍵 **휴식 포인트(90초)**: "대책이 있다면, 이제 문제없는 거 아닌가?"——아니오, 여기가 핵심.
> 대책은 **괴리를 늦출** 뿐이며, **proxy가 진짜 능력이 아니라는 사실은 사라지지 않습니다**.
> 감기약이 증상을 억누르지만, 바이러스 그 자체는 없애지 못하는 것과 같습니다. 그래서 "proxy로 LLM이 영리해졌다"고는
> **죽어도 말하지 않습니다**. 말하는 순간, 반년 후에 망신을 당하는 것이 보이니까요. 차를 한잔.

---

### 4. 반증 3 — 설계자 의존성: "다양성의 방향"은 누가 정했는가?

#### 4.1 메타한 의심

ε-lexicase의 case, QD의 behavior 기술자, novelty의 거리 척도, minimal-criterion의 기준값——
이것들은 전부, **"다양성의 방향"을 설계자(저)가 정하고 있습니다**.

즉 lldarwin이 낳는 다양성은 "**설계자가 상정한 축 안에서의** 다양성"이며,
생물 진화급의 **미상정 창발(unanticipated emergence)**이 아닙니다.
Taylor et al. (2016)이 open-endedness의 한계로 지적하는 대로,
"인간이 정의한 척도 안에서 다양"한 것과 "정의의 밖으로 튀어나가는" 것은, 완전히 다른 이야기입니다.

예를 들어 제가 "행동 다양성"을 `diversity_l2`(genome 공간의 L2 거리)로 정의한 순간,
진화는 "**L2 거리가 커지는 방향**"으로 다양화합니다. 하지만 그것은 제가 그은 좌표축 위에서의 다양성이며,
제가 상상도 못 한 축(예를 들어 "유머 감각"이라든가 "침묵의 사용법"이라든가)에서의 다양성은,
**애초에 측정 대상에 들어 있지 않으므로**, 태어나도 알아차릴 수 없습니다.

> 🤔 **비유(금붕어 못)**:
> 금붕어 건지기 가게 주인이 "빨간 금붕어와 검은 금붕어, 둘 다 남도록 고르자"라고 정해서 건집니다.
> 확실히 빨강도 검정도 못에 남습니다. 다양성, 달성. …하지만, 그 못에 **초록 금붕어**가 돌연변이로 태어나도,
> 주인의 그물은 "빨강이냐 검정이냐"밖에 보지 않으므로, 초록은 **평가받지 못하고 건짐을 놓칩니다**.
> 설계자가 정한 축의 바깥쪽의 창발은, 처음부터 안중에 없습니다. 이것이 설계자 의존성입니다.

#### 4.2 수용 — 이길 수 있는 축을 한정한다

그럼 어떻게 할 것인가. **미상정 창발을 주장하지 않는다**,는 것이 정직한 답입니다.

lldarwin은 "**검증 가능성이 없는 다양성의 지도**"를 노리는 것이지(차별화 축 DIFF-1),
strong / unbounded open-endedness는 주장하지 않습니다(SCOPE와 정합).
"인류 미답의 창발을 하고 있습니다!"라고 하면 화려하지만, 그것은 거짓말이 됩니다.
**이길 수 있는 축을 한정한다**——인지 스타일·문화적 스타일 같은 "검증 가능성이 없는 다양성"을 지도화하는 것에
가치를 좁힙니다. 이것이 lldarwin이 성실하게 주장할 수 있는 범위입니다.

화려한 주장을 버리는 용기가, honest disclosure의 핵심이기도 합니다.

---

### 5. 반증 4 — minimal-criterion과 QD 자체의 trade-off

도태기의 각 부품에도, 고유한 약점이 있습니다. 설계 문서 §7.1의 수용된 한계를 하나씩 해설합니다.

#### 5.1 minimal-criterion의 정체⇄붕괴

minimal-criterion(최저 기준 gate)은 "기준을 충족하지 않는 개체는 번식시키지 않는다"는 구조이지만,
**기준의 높이가 그대로 trade-off**가 됩니다.

- **기준이 낮다** → 거의 전원이 통과 → 선택압 제로 → **정체**(#25의 포화와 같은 구조).
- **기준이 높다** → 거의 아무도 통과하지 못함 → **전멸**(실증 있음. 전원이 gate에서 떨어지면 다음 세대를 만들 수 없다).

미지근한 물이냐 지옥이냐. **대책**: criterion을 고정값이 아니라 **집단 분위수로 적응**시킨다(예: 하위 30%를 떨어뜨린다).
나아가 전원 fail이면 gate를 무시하는 안전밸브를 넣는다(`MultiPressureSelector` 구현 완료).

#### 5.2 QD의 차원의 저주 + 아카이브 포화

QD(MAP-Elites)는 behavior 기술자로 cell을 자르지만, **기술자가 고차원이면 cell의 대부분이 빈다**
(차원의 저주). 또 장기간 돌리면 전 cell이 채워져, 새로움이 한계에 다다른다(**아카이브 포화**).
이것은 인공 생명의 고전 Avida / Tierra에서도 관측된 현상입니다.

**대책**: 기술자를 **저차원으로 축약**(DESC-1, JL 사영) + 포화를 **Bedau 통계로 감시**하고,
"**포화=실패**"로서 정직하게 기록한다(포화를 "이미 탐색을 다 했다는 증거"로 편의적으로 해석하지 않는다).

#### 5.3 lexicase의 스케일 한계

ε-lexicase는 case 수가 늘면 **계산 비용이 증대**하고, 게다가 **노이즈로 사실상 랜덤 선택화**합니다.
case가 너무 많으면, 우연히 순서의 맨 앞에 온 case로 승자가 정해져, 선택이 주사위에 가까워집니다.

**대책**: **down-sampled lexicase**(매 세대 case의 부분집합만 사용)로 비용 삭감 + 환경 교란.

#### 5.4 trade-off는 실측으로 "보인다"

이 trade-off들은 탁상공론이 아니라, **실측에서 나타납니다**.
중립 저장고의 "재투입 빈도(reinject_interval)"를 바꾼 sweep이 그 좋은 예입니다.

| interval | named 계통 생존 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**(매 세대) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84(최대)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**자명하지 않은 발견**: 행동 다양성(diversity_l2)은 interval을 올릴수록 단조 증가하지 않고, **interval=5에서 정점**을 찍습니다.
10/20은 오히려 저하합니다. 이유는——계통을 너무 방치하면(interval을 올리면),
저장고 유래의 다양성 주입이 줄고, 게다가 소수 계통이 고정되어 diversity도 늘지 않게 됩니다.
딱 좋은 "방치 정도"가 한가운데에 있다는, 비선형의 세계입니다.

![재투입 빈도 sweep: diversity는 interval=5에서 정점(비단조)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_ko.svg)

운용 지침은 이렇게 됩니다——**계통 유지를 최우선으로 한다면 interval=1(8/8 전 계통 생존)**,
**계통 유지와 행동 다양성을 양립시키고 싶다면 interval=5(5/8 유지하면서 diversity 최대)**.
최적점은 fitness / 집단 규모에 의존하므로, 본번에서는 재교정이 필요합니다.
"어느 하나의 정답"이 아니라 "목적에 따라 움직이는 최적점"이다,라는 것이 정직한 결론입니다.

#### 5.5 honest 유보 — "생존"은 "생명 유지"일지도 모른다

여기서, 하나 더 정직하게 써 두어야 할 유보가 있습니다.
중립 저장고가 전 8 계통을 살린 것은 사실이지만, **그 "생존"의 질을 의심할** 필요가 있습니다.

정본(§4.1 / §4.2)에 쓴 대로, 저장고는 "계통별 best-ever genome(frozen elite)을 재투입한다"는 기구입니다.
강한 계통은 실제로 자손을 늘려 번식하고 있습니다. 한편, 약한 계통(각 1개체)의 "생존"은,
**재투입 유래이며, 능동적인 진화가 아닙니다**. 말하자면, **번식이 아니라 생명 유지 장치**.

이것은 중립 저장고의 정의 그대로의 정당한 거동(대표를 유지하고, 재결합 가능하게 한다)입니다.
하지만 "전 8 계통이 **활발하게 계속 진화하고 있다**"고는 주장하지 않습니다.
"전멸은 막았다. 하지만 약한 계통은 ICU에서 연명 중"——이것이 정확한 표현입니다.

> 🤔 **비유(라쿠고풍)**:
> 집주인: "셋집의 거주자가 한 사람도 빠짐없이 8명 전원 갖춰져 있군요, 경사로다 경사로다."
> 핫쓰안: "예. 다만, 절반은 숨만 쉬고 집세도 안 내고 누워 있어서…"
> 집주인: "**그건 '살고 있다'기보다 '놓여 있다'겠지!**"
> 핫쓰안: "뭐, 내쫓는 것보단 낫지 싶어서…"
> ——전원 있다,는 사실. 전원이 활약하고 있다,는 거짓말. 이 경계선이 honest disclosure입니다.

---

### 6. Stage2 — proxy에서 "실"로 가는 다리

반증만으로는, 설계가 앞으로 나아가지 않는 것처럼 보일지도 모릅니다.
하지만 반증으로 발판을 다졌기에, 다음 한 걸음에 의미가 생깁니다. 그것이 **Stage2: 실 LLM 평가**입니다.

#### 6.1 proxy 축(mechanism feasibility)

먼저 Stage2의 전반으로서, LLM이 서툰 5축을 **proxy(결정론 heuristic, LLM 비의존)**로 plugin화했습니다.

| pressure(LLM 약점) | 관련 사고 인자(case) |
|---|---|
| typo_robustness(노이즈 내성) | consistency / reality_link / uncertainty |
| polysemy_wsd(다의어) | multiview / consistency / reality_link |
| multistep_robustness(다단 추론) | structurize / closed_loop / self_extend |
| calibration(신뢰도 추정) | uncertainty / provenance |
| context_management(무관 문맥 내성) | consistency / provenance / recompose |

합계 14 case를 breakdown에 출력하고, lldarwin의 ε-lexicase가 **집약하지 않고 축마다 specialist를 도태**합니다.
아래가, 그 proxy 축의 모집단 평균 추이입니다.

![Stage2 proxy 축의 추이(mechanism feasibility)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_ko.svg)

다만——지금까지 누차 말한 대로——**이것은 proxy**.
개체는 실 LLM이 아니라 genome이므로, 이 pressure는 "genome이 그 약점에 관련된 사고 인자를
얼마나 갖추는가"의 **행동 대리**에 지나지 않습니다. **production의 LLM 능력은 측정하지 않습니다**(mechanism feasibility만).
SVG에도 "PROXY"라고 새겨 두었습니다. Goodhart 리스크는, 여기서는 수용된 한계로서 명시합니다.

#### 6.2 실 on-prem LLM 평가(proxy→real의 다리)

그리고 이 글에서 처음으로 보고할 수 있는 전진——**실 LLM 평가가 동작했습니다**.

localhost의 ollama(llama3.2:latest)가 도달 가능하다고 판명되었으므로, `real_pressures.py`로
**개체 → 실 LLM 사상**을 구현했습니다(Promptbreeder 계). 구조는 이렇습니다.

- 개체의 `c_prompt`(PromptChromosome)를 **system prompt**로 변환한다
  (skill_set → 지시문 / prompt_template_id → 추론 스타일 / language_style → 어조).
- 고정 LLM(llama3.2)에 그 system prompt를 씌우고, 5 서툰 축의 **실태스크**를 풀게 하여 채점.
- 즉 **LLM 본체는 고정하고, prompt 전략(genome)을 진화**시킨다.
  "어느 prompt 전략이 LLM의 약점을 완화하는가"를 **실측으로 도태**한다.

결과, **실선택 신호를 확인할 수 있었습니다**.
CoT + structure 전략(`chain_of_thought` + structurize + loop)이,
llama3.2의 **multistep을 0.0 → 1.0으로 개선**(terse한 전략은 0.0으로 실패, score 0.80→1.00).
proxy의 환상이 아니라, **실 LLM에서 "prompt 전략의 진화가 약점을 완화한다"는 것을 실증**할 수 있었습니다.

![Stage2 실 on-prem LLM 축의 추이(prompt 전략 진화)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

proxy 축(앞서 제시)과 실 LLM 축(위)을 **나란히 보면**, "proxy로 측정한 형태"와 "실측의 형태"가
어떻게 다른지가 눈으로 보입니다. proxy는 기구가 도는 것을 보여줄 뿐. 실 LLM은, 실제로 모델의 약점에 대해
prompt 전략이 어떻게 효과를 내는지를 보여줍니다. **이 2장의 차이야말로, 이 글의 주장의 실물입니다.**

#### 6.3 하지만, 여기서도 정직하게

실 LLM에서 동작했다——하지만 여기서도 사이렌을 울립니다. 유보는 4개.

- **(a) c_prompt만 fitness에 관여** — persona / c_factors는 중립이며, fitness에는 얽혀 있지 않다.
  계통은 reservoir가 유지하고, 초기 선택은 novelty가 담당한다. 즉 이것은 "**prompt 전략의 진화**"이며
  "persona의 진화"가 아니다.
- **(b) 전 founder의 초기 c_prompt가 동일(default)** — 그래서 탐색은 mutation 구동.
  founder마다 prompt를 다양화하는 것은 향후의 개선점.
- **(c) 소규모 배터리(축당 2문)** — 노이지한 추정. "multistep이 0→1"도, 문제 수가 적으므로
  이것만으로 일반화를 주장할 수는 없다.
- **(d) on-prem only(측정 순도)** — localhost ollama 한정이며,
  **일반적인 LLM 능력의 주장이 아니다**([[feedback_llive_measurement_purity]]).

12h 연속 실행도 기동했습니다(`--fitness real-pressure --selection lldarwin --novelty
--lineage-reservoir --genome3d`). wallclock 12h에 safely 정지(snapshot 완료 → `--resume`로 계속 가능).
하지만 "12h 돌렸으니 진짜"라고는 말하지 않습니다. 돌렸다,는 사실. 본질을 다 측정했다,는 거짓말.
**proxy→real의 다리는 놓였다. 하지만 다 건너지는 못했다.**——이것이 Stage2의 정직한 상태입니다.

---

### 7. 결론 — 어디까지 주장해도 되는가(경계선)

"LLM의 약점을 proxy fitness로 삼으면 진화로 극복할 수 있다"는 **낙관적**이었습니다.
반증으로 깎아낸 결과, lldarwin의 가치 주장을 다음 3점으로 **한정**합니다.

1. **(a) proxy는 mechanism feasibility만** — 진화의 배관이 도는 것의 검증. production 능력은 주장하지 않는다.
2. **(b) 실 LLM/VLM 평가가 본질** — 지능의 선택압은 개체 → 실모델 사상(Stage 2)이 담당한다.
   여기에 다리는 놓았다. 하지만 본격적으로 건너는 것은 이제부터.
3. **(c) 다양성의 지도화** — 이길 수 있는 축을 "검증 가능성이 없는 다양성(인지·문화 스타일)의 지도"로 한정한다.
   미상정 창발은 주장하지 않는다.

이것이 honest disclosure입니다. **실패(#25)도, 자신의 혼동(§3.2)도, 한계(#5/§6.3)도, 지우지 않고 남긴다.**
화려한 승리 선언을 하나도 쓰지 않은 이 글이야말로, 진화 아크에서 가장 성실한 회라고, 저는 생각합니다.
앞으로 나아갈 발판은, 이 경계선 위에만 있습니다.

---

### 8. 교훈(영구 보존)

- **좋은 결과(0.05 개선)일수록 그 내역을 의심한다.** "proxy 행동 다양성"은 "계통 다양성"도 "실 LLM 지능 다양성"도 아니다.
  숫자를 보고 다른 능력까지 좋아졌다고 속단한 자신이, Goodhart의 살아 있는 표본이었다.
- **"측정"을 고치지 않고 "도태"만 고급스럽게 해도 헛수고.** 포화된 렌즈에는, 어떤 선택압도 효과가 없다.
  렌즈를 닦는 것이 먼저, 도태기를 얹는 것이 나중.
- **Goodhart의 법칙은 진화의 천적.** 지표를 목표로 한 순간, 진화는 그것을 hack한다.
  게다가 지표를 읽는 인간의 해석까지 함께 괴리된다.
- **설계자가 다양성의 방향을 정하는 이상, 미상정 창발은 주장하지 않는다.** 이길 수 있는 축을 한정하는 것이 성실함.
- **"생존"은 "생명 유지"일지도 모른다.** 전 8 계통이 남았다,는 사실. 전원이 활발하게 진화 중,은 거짓말.
  동사의 선택 하나에 honest disclosure가 깃든다.

> **다음 회 예고**: 반증으로 발판을 다졌다면, 다음은 Stage 2의 본격화(실 LLM/VLM 평가, on-prem ollama).
> proxy의 환상이 아니라, 실모델의 지능 다양성을 정말로 선택압으로 삼을 수 있는가.
> "multistep 0→1"을 소규모 배터리의 우연으로 끝내지 않고, 재현 가능한 선택 신호로 길러낼 수 있는가. 여기서부터가 본번입니다.

---

### 9. 관련
- 연재 #25 "나와 프리스턴만 남았다" — 실패의 기록(이 글의 기점)
- 연재 #26 "lldarwin의 설계" — 도태기(이 글이 반증하는 대상)
- 구현 commit(llive): Stage1 = `8060204` / lineage-reservoir PoC = `0d0537d` /
  Stage1.5(EvolutionLoop 통합)= `b03cbda` / Stage2(실 LLM real-pressure)= `2fb2912`
- 실측 정본: `../../research/lldarwin_stage1_results_2026_05_26.md`(§3 honest disclosure / §4.1–4.5)
- 설계 정본: `../../vision/LLDARWIN_DESIGN.md` §7 / §7.1(반증 조사·수용된 한계)
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- 참고: Goodhart의 법칙 / La Cava 2019(ε-lexicase, arXiv 1905.13266)/ Taylor et al. 2016(open-endedness의 한계)/
  Bedau(neutral shadow)/ Kimura(중립 진화설)

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25・#26 の Qiita URL cross-link -->
<!-- KEY MESSAGE: honest disclosure の本丸。飽和した眼鏡には選択圧が効かない + Goodhart + 設計者依存。主張を 3 点に限定。「何を測った 0.05 か」= 行動多様性のみ(≠系統≠実知能)を自己反証の核に。 -->
<!-- NOTE(事実整合): PoC デプロイで monoculture は実際 0.05 に改善した(誇張でない)。本記事はそれを否定せず「何を測った 0.05 か」を honest に深掘りする構成。「lldarwin を入れても改善せず」とは書かない(事実と異なるため)。novelty/reservoir はそれぞれ行動多様性 +109% / 系統 8/8 を実際に改善した。 -->
<!-- 埋込 SVG: stage1_baseline_status / reservoir_off_dominance / reservoir_on_dominance / reinject_sweep / stage2_proxy_axes / stage2_real_llm_axes (全て ../assets/lldarwin_2026_05_26/, 実在確認済 2026-05-26) + step_c/step_c_two_regimes / step_c/deceptive_corridor -->
<!-- 多言語: JA→EN→ZH→KO 全文縦積み・各言語自己完結 (SVG/表/参考文献を各言語に複製、alt は翻訳) -->

---

## 제6장 진화를 「보여주는」 기술의 계보 #30 — Conway 의 라이프 게임에서 3DGS 까지

> **콘셉트 훅**: 제가 #25〜#27 에서 끊임없이 이야기하고 있는 「인공 진화」. 사실 이것은 반세기 이상의 역사를 가진 연구 분야입니다. 그리고 흥미로운 점은, **진화 연구는 늘 「보여주는 방식(시각화)」과 2인 3각으로 함께 진화해 왔다**는 것입니다. 1970 년의 흑백으로 깜빡이는 세포에서, 2024 년의 연속 유체·3D 가우시안까지. 「진화를 보여주는 기술」의 계보를 교양으로서 단숨에 더듬어 봅니다. 마지막에는 FullSense 의 진화 시각화(사고 인자 그래프 위의 계통수)가 이 계보의 **어디에 서 있는지**를 자리매김합니다.

---

### 0. 왜 「시각화」가 진화 연구의 주역인가

진화는 **장시간·대집단·다세대** 의 현상입니다. 숫자의 나열만으로는 「무슨 일이 일어났는지」를 파악할 수 없습니다. 그래서 인공 진화의 역사는, 거의 그대로 **「진화를 한눈에 이해시키는 표현의 발명사」** 입니다.

> 🍵 **휴식 포인트**: 이 글은 수식 제로·코드 거의 제로의 「산책」 편입니다. 커피 한 잔과 함께 즐기세요. 각 시대의 「보여주는 방식의 돌파구」만 골라 갑니다.

---

### 1. 1970: Conway 의 라이프 게임 —「단순한 규칙이 무늬를 낳는다」

- **무엇**: 2차원 셀룰러 오토마타. 생사 2상태 × 이웃 8셀의 단순한 규칙.
- **보여주는 방식의 발명**: **격자의 깜빡임 그 자체가 시각화**. 글라이더·블링커·글라이더 건 같은 「움직이는 무늬」에 이름이 붙은 것 = 인간이 **창발 패턴을 눈으로 이름 붙인** 가장 초기의 예.
- **한계**: 진화(자연선택)가 아니라 결정론적인 전개. 그러나 「단순한 규칙 → 복잡한 겉모습」의 충격이 이 분야를 열었다.

**이 절의 살 붙이기 예정**: 글라이더가 「이동하는 구조」로 인식된 것 = 시각화가 개념을 낳은 좋은 예로서 깊이 파고든다.

---

### 2. 1991: Tierra（Tom Ray）—「코드가 생물이 된다」

- **무엇**: 가상 CPU 위에서 자기 복제하는 기계어 프로그램의 생태계. 기생체·면역·최적화가 **저절로 창발**.
- **보여주는 방식의 발명**: **메모리 맵의 시각화**. 각 프로그램이 차지하는 메모리 영역을 색으로 칠하고, 기생체가 숙주에 파고드는 모습을 「지도」로서 보여줬다. **「코드의 생태계」를 공간으로 그려냈다**.
- **의의**: 「자기 복제자의 자연선택」을 컴퓨터 안에서 처음으로 관측. open-ended evolution 연구의 출발점 중 하나.

---

### 3. 1994: Avida（Adami / Ofria）—「진화를 측정한다」

- **무엇**: Tierra 의 계보를 잇는 디지털 생명 플랫폼. 논리 연산을 해내면 보상(CPU 시간)을 얻는다.
- **보여주는 방식의 발명**: **계통수(phylogeny)와 적응도 지형의 시각화**. 「어느 조상에서 어느 자손이 분기했는가」를 트리로 그리고, 복잡 형질(EQU 연산 등)이 단계적으로 진화하는 과정을 **추적 가능**하게 했다.
- **의의**: 「불가피한 단계를 거쳐 복잡성이 진화한다」를 실증했다(Lenski et al. 2003, Nature). **진화를 이야기가 아니라 측정 대상으로 만들었다**. FullSense 의 monoculture 모니터링(max_lineage_share / archive 성장)은 이 「측정하는 진화」의 직계다.

> 🤔 **비유(만담풍)**:
> 보케: 「Avida 는 진화를 숫자로 측정할 수 있게 했다.」
> 츳코미: 「즉 진화에 성적표를 매긴 거네.」
> 보케: 「맞아. #25 에서 내가 『만점 인플레로 성적표가 망가졌다』고 한 게, 바로 Avida 급 측정 이야기야.」

---

### 4. 1994: Karl Sims「Evolved Virtual Creatures」—「진화를 영상으로 매료한다」

- **무엇**: 3D 물리 시뮬레이션 안에서, 형태(block 의 연결)와 신경 제어를 **동시에 진화**시켜, 헤엄치고·걷고·물건을 서로 차지하는 생물을 낳았다.
- **보여주는 방식의 발명**: **3D 애니메이션 영상**. 논문의 그림이 아니라 **동영상**으로 보여준 것이 충격을 불러일으켰다. 「진화가 설계한, 누구도 예상하지 못한 기묘한 걸음걸이」를 **인간이 직관적으로 재미있어할 수 있는** 형태로 만들었다.
- **의의**: 진화 시각화가 「연구자용 그래프」에서 「**누구나 보고 놀라는 영상**」으로. FullSense 의 데모 철학([[project_f25_demo_polish]] 「움직임으로 매료한다」)의 정신적 조상.

> 🍵 **휴식 포인트**: 여기까지 「흑백 점 → 메모리 지도 → 계통수 → 3D 동영상」으로, 보여주는 방식이 **추상 → 구상 → 동적** 으로 진화한 것이 보이면 OK. 후반은 현대 편입니다.

---

### 5. 2019: Lenia（Bert Chan）—「연속적인 인공 생명」

- **무엇**: 라이프 게임을 **연속 공간·연속 시간·연속 상태** 로 일반화. 매끄럽게 움직이는 「생물 같은」 패턴(orbium 등)이 다수 발견되었다.
- **보여주는 방식의 발명**: **연속 필드의 매끄러운 렌더링**. 이산적인 깜빡임에서, 생물의 세포처럼 유연하게 움직이는 유체적 표현으로. 「인공 생명이 **아름답다**」라는 새로운 소구 축을 열었다.
- **의의**: 시각화의 질 그 자체가 연구의 발견력을 높인 예. 아름답게 보이기에 새로운 패턴을 인간이 알아챌 수 있다.

---

### 6. 2020 년대: Quality-Diversity 의 시각화 —「다양성을 지도로 만든다」

- **무엇**: MAP-Elites / CMA-ME 등의 QD 알고리즘. 단일 best 가 아니라 **다양한 고성능 해의 집합**을 낳는다.
- **보여주는 방식의 발명**: **behavior space 의 히트맵**. 2축의 behavior 기술자를 격자에 두고, 각 cell 의 elite 를 색으로 칠한다 = 「**다양성 그 자체를 지도로서 시각화**」.
- **의의**: FullSense / lldarwin 의 QD archive 시각화는 여기에 직접 입각해 있다. 「1 cell 이라도 남으면 전멸하지 않는다」를 **지도의 공백 vs 충전**으로 한눈에 보여줄 수 있다(#26 에서 상술).

---

### 7. 2020 년대〜: 3D Gaussian Splatting（3DGS）—「진화의 상태를 공간 표현한다」（FullSense 의 도박）

- **무엇**: 본래는 신규 시점 합성(NeRF 의 계보) 기술. 점군을 3D 가우시안으로 표현해 고속·고품질로 렌더링한다.
- **FullSense 의 착상**: 진화 집단의 **고차원 genome / pressure profile 을 3D 가우시안 공간에 사상**하여 「진화의 상태를 입체적으로 보여줄 수 없을까」라는 탐색([[project_precision_metrology_llm]] 의 SH 계수 연계와 같은 뿌리).
- **자리매김**: 이것은 **아직 연구적 도박**이며, 확립된 기술이 아니다(honest disclosure). 본 글 계보의 「최첨단의 가장자리」에 두는 실험이다.

---

### 8. FullSense 의 진화 시각화는 어디에 서는가

| 시대 | 보여주는 방식의 핵심 | FullSense 에서의 계승 |
|---|---|---|
| Conway 1970 | 깜빡이는 셀 = 창발의 이름 붙이기 | （개념적 조상） |
| Tierra 1991 | 메모리 지도 | 계통 점유율의 지도화 |
| Avida 1994 | 계통수 + 측정 | monoculture 모니터링 / lineage tree |
| Karl Sims 1994 | 3D 동영상 | 「움직임으로 매료한다」데모 철학 |
| Lenia 2019 | 연속 필드의 아름다움 | animated SVG 표현층 |
| QD 2020 년대 | behavior 지도 | lldarwin QD archive 시각화 |
| 3DGS 2020 년대〜 | 3D 공간 표현 | （연구적 도박） |

FullSense 의 진화 시각화(**사고 인자 그래프 위의 계통수 + animated SVG**)는, **Avida 의 「측정하는 계통수」와 Karl Sims 의 「움직임으로 매료한다」와 QD 의 「다양성의 지도」를, 터미널 / 브라우저에서 재현하는** 위치에 있습니다. 반세기 계보의, 소박하지만 정통한 후예입니다.

> **다음 회 예고**: 계보를 더듬었으니, 다음은 구현. FullSense 의 계통수 animated SVG 가, 위의 어느 「보여주는 방식」을 어떻게 받아들였는지를, 실제 evolution.svg 를 소재로 해설합니다.

---

### 9. 관련

- 연재 #25〜#27 — 본 글 진화 시각화의 「내용」（monoculture / lldarwin / 반증）
- 관련 memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 참고: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

## 제7장 AI 에게 AI 를 부하로 부리게 하기 #31 —— Claude 주도 + Codex 배속의 「두 기둥」 개발 체제

> **콘셉트 후크**: FullSense（llmesh / llive / llove）는 나 혼자만의 개인 개발입니다. 하지만 실태는
> 「혼자」가 아닙니다. **AI 코딩 에이전트를 주로, 또 다른 AI 에이전트를 부하로** 둔
> 2 계층 개발 체제가 돌아가고 있습니다. 주는 **Claude Code**, 부하는 **Codex CLI**.
> 「AI 가 AI 에게 일을 맡기고, 그 성과를 AI 가 검증한다」——이 다중 위임을, 폭주시키지 않고
> 어떻게 규율하는가. 본 글은 인간 1 + AI 2 의 「두 기둥」 운용에 관한 실천기입니다.
>
> 키워드는 **오케스트레이터 / 배속 worker / 검증 규율 / 병렬화**.

---

### 0. 세 줄 줄거리

- **Claude = 오케스트레이터**（계획·구현·위임·**검증**）/ **Codex = 배속 worker**（실행·리뷰·조사）.
- 「두 기둥」은 대등이 아니라 **Claude 주도 + Codex 배속**. 지휘 계통은 하나로 유지한다.
- 철칙: **외부 AI 의 finding 은 실제 코드 / 일차 정보로 한 건씩 검증한 뒤에 채용**（맹신 금지）.

---

### 1. 왜 「두 기둥」인가 —— 동기

개인 개발에서 AI 에이전트를 하나만 쓰는 것은 이미 평범합니다. 그렇다면 왜 두 번째（Codex）를 **부하로서** 더했는가:

1. **벤더 분산·이중화** —— 단일 에이전트의 과금 변경 / 장애 / quota 고갈에 대한 헤지.
2. **크로스 리뷰** —— 같은 설계를 다른 계통의 AI 에게 보여 주고 세컨드 오피니언을 받는다（사각지대 감소）.
3. **병렬 worker** —— 독립 서브태스크를 부하에게 던지고, 주는 가장 중요한 태스크에 집중.

> 🍵 **휴식 포인트**: 「AI 를 둘 쓰면 = 두 배 똑똑하다」는 거짓입니다. 핵심은 **지휘 계통을 하나로 유지하는 것**.
> 오합지졸로 만들면 오히려 느려집니다. 본 글의 절반은 「어떻게 통제하는가」에 관한 이야기입니다.

---

### 2. 역할 분담 —— 오케스트레이터와 배속 worker

![계층도: 인간 → Claude Code（주＝오케스트레이터）→ Claude 서브에이전트 병렬 / Codex CLI 배속 worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_ko.svg)

- **Claude（주）의 책무**: 태스크 분해·의존성 판정·독립 태스크의 병렬 기동·진척 모니터링·**성과 검증**·일괄 커밋.
- **Codex（부하）의 책무**: 위임된 범위의 실행. 비대화형 위임 = `codex exec -s read-only "<prompt>"`.
- **지휘 계통은 항상 Claude.** Codex 는 Claude 를 경유해서만 전체에 영향을 준다（직접 커밋시키지 않는다）.

**이 절에서 살을 붙일 예정**: Claude 서브에이전트 병렬（[[feedback_parallel_first_execution]]）과 Codex 배속 위임의
구분 사용 표. 「같은 file 은 직렬·독립 file 은 병렬」「git 조작은 orchestrator 가 일괄」（[[feedback_agent_no_git_parallel]]）.

---

### 3. 검증 규율 —— 「맹신 금지」가 체제의 생명선

두 기둥에서 가장 위험한 것은 **AI 의 출력을 AI 가 무검증으로 채용하는 것**입니다. 오류가 증폭됩니다. 그래서 철칙:

> 외부 AI（Codex / Copilot / Gemini）의 finding 은 **실제 코드 / 일차 정보로 한 건씩 검증**한 뒤에 채용한다.

실례: 본 연재 #26（lldarwin 설계）에서, 기존 코드 자산의 조사（`mating.py:139 LexicaseSelection` 은
「구현은 됐지만 미배선」 등）는 부하에게 조사시켰지만, **배선 지점과 행 번호는 주（Claude）가 실제 파일에서 확인**한 뒤에
설계서에 적었습니다. 「Codex 가 그렇게 말했다」를 설계의 근거로 삼지 않습니다.

> 🤔 **비유（만담 풍）**:
> 두목: 「어이, 그 함수, 배선됐냐?」
> 졸개: 「예, 미배선입죠.」
> 두목: 「……네 『예』는 못 믿겠다. 내가 직접 소스 보고 오마.」
> ——이것이 검증 규율. 졸개의 보고는 **기점**이지 **결론**이 아니다.

**이 절에서 살을 붙일 예정**: 검증의 3 단계（finding 수령 → 실제 코드 / 일차 정보로 확인 → 채용 또는 기각）와,
리뷰 래퍼（`tools/copilot_review.sh` 등의 읽기 전용 리뷰）의 위치 설정.

---

### 4. 병렬화의 작법 —— 폭주시키지 않는 통제

여러 worker（Claude 서브에이전트 + Codex）를 동시에 돌릴 때의 규율:

- **2～4 병렬이 안전권**（주의 context 여유·커밋 충돌 없음）. 5+ 는 file 레벨 독립성을 엄격 관리.
- **독립 태스크 추출** = 의존 없음 + file / module / repo 레벨에서 비접촉. 같은 file 은 직렬（file lock 적）.
- **불가역 조작（삭제 / push / submodule 개변）은 한 건씩 인간 확인.** 부하에게 멋대로 시키지 않는다.
- **git 조작은 orchestrator 가 일괄.** 병렬 worker 에게 git 을 만지게 하지 않는다（충돌 회피）.

> 🍵 **휴식 포인트**: 「AI 를 많이 늘어놓으면 빠르다」의 함정. **주의 context（주의의 총량）가 율속(律速)입니다.**
> 5 체 병렬로 해도 주가 처리하지 못하면 의미가 없습니다. 뇌의 작업 기억과 마찬가지로, 동시에 파악할 수 있는 수에는 상한이 있습니다.

---

### 5. 안티패턴（해서는 안 되는 것）

- 「하나씩 확인하면서 진행하겠습니다」라고 선언한 뒤 묵묵히 직렬 실행（병렬화의 기회 손실）.
- 부하에게 던지지 않고 주의 context 만으로 전부 해치운다（context 폭발）.
- 병렬 기동한 worker 의 결과를 기다리지 않고 주가 같은 file 을 만진다（충돌）.
- 2 worker 에게 같은 file 을 쓰게 하는 위임（독립성 판정 누락）.
- 부하 AI 의 finding 을 무검증으로 설계나 구현에 채용（오류 증폭 = 두 기둥 체제 최대의 사고）.

---

### 6. 이 체제로 실제로 무엇이 돌았는가（FullSense 의 실례）

- **설계 크로스 리뷰**: 진화 설계 / 요건 / PoC 를 부하에게 리뷰시키고, 주가 실제 코드로 검증해 채용 판단.
- **기존 자산 조사**: lldarwin 의 기존 부품（loop.py / mating.py / nsga2.py 등）의 소재를 부하에게 조사 → 주가 확인.
- **병렬 서브태스크**: 기사 골자·코드 조사·요건 정리를 독립 태스크로서 병렬화（본 연재 자체가 그 산물）.

> 🍵 **휴식 포인트**: 「인간 1 + AI 2」로 개인 개발의 생산성이 어떻게 바뀌었는가, 라는 주관도 마지막에 정직하게.
> 빨라진 면（병렬·이중화）과 늘어난 부하（검증 비용·통제 비용）의 **양쪽**을 honest disclosure.

---

### 7. 교훈

- **지휘 계통은 하나로 유지한다.** 두 기둥은 대등이 아니라 주종. 사령탑의 분열은 사고의 근원.
- **검증 규율이 체제의 생명선.** AI 가 AI 를 무검증으로 믿는 연쇄가 최대의 리스크.
- **병렬도는 주의 context 가 율속.** 체수가 아니라 처리할 수 있는 양으로 정한다.
- **불가역 조작과 git 은 인간 / orchestrator 가 쥔다.** 부하에게는 가역적인 일만 맡긴다.

> **다음 회 예고**: 두 기둥으로 돌린 진화 설계（#26 lldarwin）를, 배속 Codex + on-prem ollama 로
> Stage 2（실제 LLM 평가）까지 진행한다. 다중 AI 위임이 「연구의 구현 속도」를 어디까지 끌어올리는가.

---

### 8. 관련
- 연재 #26 「lldarwin 의 설계」—— 본 체제로 돌린 실례.
- 관련 memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

## 제8장 (연재 #32) llcore CPU PoC battery 완성

### TL;DR

- **Transformer의 코어 계산 (state update / 학습 규칙 / 인지 구동 Δ)** 을 진화 대상으로 삼는 연구 프레임워크 `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 독립 노선) 의 **CPU PoC battery 완성**
- **5개 PoC / 39개 falsifiable gate / 76개 테스트 / Codex pair-review 5/5 Green-light** 로 메커니즘 실증
- **Z3로 구조 변이를 online gate** = 진화 탐색의 selection pressure에 SMT를 끼워 넣음 — 사전 조사에서 발견되지 않은 선행 연구 (사전 조사 RAD 14개 분야 + Agent A-D 확인)
- 투고 후보: TMLR (본명) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

### 왜 만들었나

LLM 가중치를 동결하는 것이 표준이지만, **코어 계산 알고리즘 자체는 수작업 설계로 고정**되어 있다. AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge 같은 architecture/algorithm 탐색은 진전되었지만:

1. **개인 compute로는 계산 리소스가 불가능** (TinyLlama 1.1B from scratch = $140k / 90일 / 16×A100)
2. **탐색 중 안전성 보장 없음** = 수치적으로 불안정한 architecture를 만들어 시간 낭비
3. **검증을 동반한 탐색은 정적 verification (Reluplex/Marabou/α,β-CROWN) 과 단절** — 진화 루프 내 SMT online gate 연구는 발견되지 않음

### 확정 독자 축 (사전 조사에서 negation work 없음)

메커니즘 실증 완료 (4개 축):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 규칙을 유전자화 RWKV-style** (Stage 0a v2)
3. **factor_hook (인지 상태 → SSM Δ)** (Stage 2a mock)
4. **자체 진화기 + verifier 기반** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 신규 카테고리 제안.

### PoC 사다리 (5 stage / 39 gate 전부 PASS)

| PoC | 내용 | 키 수치 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 자체 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

### v1의 실패에서 배운 것 (honest disclosure)

PoC 0a v1은 `decay*s + mix*x*tanh(gate_str*s)` 로 **state=0이 fixed point인 zero attractor** = G1-G5 형식적으로는 PASS이지만 정보 전달이 제로. Claude 단독으로 놓친 설계 문제를 **Codex (gpt-5.4) 와 gem-critic의 독립 verdict** 가 검출하여 RWKV-style로 v2 redesign 했다.

→ **5개 PoC 중 4건에서 Claude 단독으로는 놓친 설계 문제를 Codex pair-review가 검출**. 상호 리뷰가 구조 붕괴 방지에 작동한 실례.

### 다음 선택지

a. Stage 3 kernel 다양화 (rwkv/mamba/hopfield/linear-attn 을 유전자화)  
b. Stage 4 학습 규칙 (FF/EP/PCN/Hebb) 을 gene화  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka로 Z3 gate 고속화  
e. FlashEvolve로 3.5-5x wall-clock 고속화  
f. 논문화 (TMLR + GECCO 2027)

### Honest 유보

- mock 중심, 실제 LLM/가중치 접속은 GPU/새 PC 대기
- 1 step scalar invariant의 over-approx proof 단계, 다차원·다 step은 post phase
- tanh 상계 근사는 보수적 (sound이지만 완전하지 않음)

---

**Tags**: 진화 계산 / 형식 검증 / Z3 / RWKV / state space model / CPU연구  
**관련**: 연재 #14-31 (llive lldarwin v0.B-E + 관측+governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

---

## 제9장 (연재 #33) 너무 깔끔한 결과는 승리가 아니라 경보 —— 제3축 ③ 을 proper power 로 결판낸 하루

### TL;DR

- 질문은 **「AI 의 코어 계산을 진화로 탐색할 때, "골라내고 나누어 키우는 공정" (= 진화의 ③ 적자생존/분리 요소) 은 정말 필요한가?」**
- **합성한 "골짜기가 있는 (기만적) 지형" 에서는 ③ 가 압승** (과거 실험에서 Cliff δ=+1.0). ③ 는 메커니즘으로서 진짜다.
- **그러나 실물에 가까운 CPU proxy 지형을, 평가 노이즈를 물리적으로 0 까지 떨어뜨려 다시 측정했더니 "정말 매끄럽다 (단봉)" 였고, ③ 는 불필요로 확정됐다.** "과거의 negative 는 검출력 부족 (underpower) 이 아니라, 지형이 정말로 매끄러웠다" 가 처음으로 뒷받침됐다.
- 실 multitask 근방 (C-gen4b) 에서만 "③ NOT null" 의 약한 기미가 나왔지만, 데이터를 늘리니 흔들려서 **후보에 그쳤다** (주행 내 드리프트 + 다중 비교에서 취약).
- "어떤 후처리가 ③ 를 숨기고 있다" 는 의심 (K4 ridge clip) 은, 떼어내니 오히려 악화 → **숨기고 있지 않다, 진단적 소견으로 강등.**
- 외부 리뷰 (Codex) 는 **블로커 없이** 결론을 추인했다.
- 결론을 한 줄로: **「③ 가 살아나는 건 지형이 기만적일 때뿐. 지금 CPU 로 측정할 수 있었던 실물 비슷한 것은, 우연히 매끄러웠다.」** 본진의 결판은 GPU (실 LLM 지형) 가 필요하지만, 그건 투자 판단이다.
- **추기 (2026-06-02, §11.5): 마지막 CPU 샛길 kernel 다양화 (BG9) 는 구조적으로 닫혔다.** kernel 선택은 저차원이라 강한 baseline (RR) 이 직접 샘플링하고, ③ 의 niching 우위가 원리적으로 나오지 않는다. **③ 가 효과를 내려면 "고차원의" 기만 지형이 필요하다**는 것을 알게 됐고, 남은 길은 GPU full-LLM 뿐 (그것도 베팅).
- 메타 교훈: **정직함 (honest disclosure) 은 장식이 아니라, 연구를 앞으로 나아가게 하는 도구였다.** BG9 에서는 "negative 를 올바르게 negative 로 확정한다" 는 방향에서도 같은 규율이 작동했다.

> ⚠ 이 글의 수치는 모두 로컬 (수중) 의 연구 commit `THIRD_AXIS_SETTLE_VERDICT.md` 에 연결된 실측이다. llcore 는 아직 공개 리포지토리를 만들지 않았으므로 외부 링크를 걸 수 없다. 대신 "어떻게 측정했는가" 를 본문에 전부 쓴다.

---

### 0. 이 글은 무엇에 관한 이야기인가 (콘셉트)

`llcore` 는 "Transformer 의 코어 계산 (상태 갱신 규칙·학습 규칙·인지 구동 Δ) 을 유전자로 삼아, Z3 로 망가지지 않게 검증하면서 진화시키는" CPU 완결의 연구 프레임워크다 (연재 #32 에서 PoC battery 이야기를 썼다).

그 진화 엔진에는, 진화의 4 요소 중 **③ (적자생존 selection / 분리 separation)** 를 어떻게 작동시킬지라는 설계상의 급소가 있다. 다양성을 유지하며 니치에 남기는 MAP-Elites 같은 "골라내고 나누어 키우는" 구조다.

질문은 단순하다.

> **그 ③, 정말 필요한가?**

필요하다면, ③ 를 얹기 위한 무거운 투자 (최종적으로는 GPU 에서 실 LLM 을 돌리는 것) 에 의미가 있다. 필요 없다면, ③ 에 집착하는 것은 시간과 전기의 낭비가 된다.

이 하루 (2026-06-02) 동안, 그 질문에 **3 가지 실험으로 정면으로 결판을 내러 갔다.** 제목 그대로, 결론은 "너무 깔끔한 결과는 경보" 라는 FullSense 의 통주저음으로 다시 한 번 끌려 돌아오는 이야기다.

— 여기까지 30 초. 준비 운동 끝. 본론으로. —

---

### 1. 비유: 등산과, 속임수 지형

수식 앞에, 지형 비유로 전체상을 잡는다 (이 연구에서 일관되게 쓰는 메타포다).

설계의 좋고 나쁨을 **지형의 높이** 로 나타낸다. **높은 곳 = 좋은 설계.** 가장 높은 정상을 찾는 게임이다.

**지형 1: 매끄러운 한 개의 산 (쉬움)**

```
 좋음↑
높음 |            ___________
     |         __/           \__
     |      __/                 \__     ← 어디서 올라도
     |   __/                       \__     같은 정상에 도달
낮음 |__/                             \__
     +----------------------------------→ 설계 선택 방식
```

이런 지형에서는, 소박한 "등산법 (hill-climbing)", 즉 "지금보다 조금 나은 쪽으로 움직일 뿐" 으로 충분히 정상에 도달한다. **공들인 공정 (③) 은 필요 없다.**

**지형 2: 속임수 지형 (기만적 deceptive)**

```
 좋음↑                                  /\
     |                                 /  \   ← 진짜 정상
     |        가짜 정상               /    \
중간 |         /\         골짜기      /      \
     |        /  \______________/        \
낮음 |____/                                  \
     +----------------------------------------→ 설계 선택 방식
          ↑가짜 정상에서 소박한 등산법은 정지 (골짜기를 못 내려감)
```

여기서는 소박한 등산법은 가짜 정상에서 멈춘다. 골짜기를 내려갈 용기가 없기 때문이다.

이때 작동하는 것이 ③ 의 발상이다. **여러 타입의 등산자를 골짜기 여기저기에 남겨 둔다** (= 기억의 궁전 / MAP-Elites archive). 누군가가 골짜기를 "징검다리" 로 건너 진짜 정상에 도달할 수 있다, 는 구조다.

**이 연구의 핵심을 한마디로**: ③ 가 정말 도움이 되는 것은 **"속임수 지형" 일 때뿐.** 매끄러운 한 개의 산에서는, ③ 는 쓸모없는 짐이다.

그래서 질문은 이렇게 바꿔 말할 수 있다:

> **「진화로 AI 를 설계할 때, 실제로 마주치는 지형은 "속임수 지형" 인가, 아니면 "매끄러운 한 개의 산" 인가?」**

이것이 정해지면, ③ 가 필요한지 아닌지가 정해진다. 오늘은 이것을 측정했다.

---

### 2. 과거에 남은 숙제 ——"③ 불필요" 는 정말 "불필요" 였는가

지금까지의 실험 (Step C → 사다리 단 1 → E-A → 골짜기 깊이 실측) 을 통해, 그림은 대략 이러했다.

- **합성한 기만 corridor 에서는 ③ 가 압승** (3 개 baseline 모두에 이기고, Cliff δ=+1.0). ③ 는 존재 증명 완료, 메커니즘으로서 진짜다.
- **실문제에 가까운 proxy 지형에서는 ③ negative** (MAP-Elites 가 random 과 비길 뿐 = 매끄러운 지형과 같은 증상).

그런데, 여기에 2 개의 미해결 응어리가 남아 있었다.

1. **"③ 불필요" 는 정말 "지형이 매끄러워서" 인가, 아니면 단지 "샘플 수가 부족해 차이를 검출하지 못했을 (underpower)" 뿐인가?** ── 이것을 착각하면, "③ 는 무력" 이라는 과잉 일반화를 저지른다.
2. 골짜기 깊이의 직접 측정은 지난번 **N/A (측정 불능)** 으로 끝났다. 평가 노이즈가 골짜기 깊이보다 커서, 골짜기가 있어도 묻혀 보이지 않는다, 는 계기의 한계.

즉 "매끄럽게 보였던" 것이 **지형의 성질** 인지 **계기의 한계** 인지, 결판이 나지 않았다. 이 점을 따지는 것이 Step D 다.

— 잠깐 쉼. 여기까지가 전제. 여기서부터가 오늘 한 3 실험. —

---

### 3. 실험 설계 —— 3 종 세트

| 실험 | 무엇을 측정하는가 | 노림수 |
|---|---|---|
| **EXP1** | proper-n 재검정 | 샘플 수를 진지하게 늘려, ③ 의 효과가 진짜인지 검출력으로 따짐 |
| **EXP2** | 결정론 C1 다봉성 | 평가 노이즈를 물리적으로 0 으로 만들어, 지형이 "속임수 지형" 인지 "매끄러운 한 개의 산" 인지 noise-free 로 판정 |
| **EXP3** | K4 ridge clip 의 verdict-flip | "어떤 후처리가 ③ 를 숨기고 있다" 는 의심을 검증 |

규율: 전부 `research/step_d_settle/` 에 격리, src 는 무개변, git 은 오케스트레이터가 일괄. 각 실험은 붕괴 게이트 (G1 CPU 완주 / G2 재현성 / G3 진단기 타당 / G4 src 불변) 를 통과시킨다.

---

### 4. EXP2 가 결정타였다 —— 평가 노이즈를 0 으로 하면 지형이 보인다

순서는 앞뒤가 바뀌지만, **가장 효과적이었던 것은 EXP2** 이므로 먼저 쓴다.

지난번 골짜기 깊이 측정이 N/A 가 된 원인은 단순하다. **"골짜기 깊이 (0.05·|fitness| 정도) ≪ 평가 노이즈의 흔들림"** 이었기 때문이다. 계기의 노이즈에 골짜기가 묻혀, 있는지 없는지 알 수 없다.

EXP2 의 트릭은 이렇다.

> ESN reservoir (고정 seed) + ridge readout 의 closed-form (`np.linalg.solve`) 은, **난수를 일절 뽑지 않는다.** 그래서 평가 노이즈를 머신 엡실론 (약 1.11e-16) 까지 물리적으로 0 으로 만들 수 있다.

실측으로 `eval_noise_std ≤ 1.11e-16` 을 확인했다. 이것은 "평가할 때마다 값이 흔들린다" 가 아니라, 부동소수점의 최소 단위 (ULP) 에서 유래하는 오차로, **실질 0** 이다. 노이즈의 안개가 완전히 갠 상태에서, 지형의 골짜기를 직접 측정할 수 있다.

결과가 이것이다 (valley_fraction = 골짜기의 비율, 클수록 다봉 = 속임수 지형):

| landscape | 종별 | 차원 | valley_fraction (mean/max) | 다봉? | 판정 |
|---|---|---|---|---|---|
| **ESN_3param** (실 proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seed 일치) | 매끄러움=단봉 → ③ 불필요를 noise-free 로 확정 |
| **ESN_perneuron40** (실 proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seed 일치) | 매끄러움 쪽 (바닥 0.2 미만) → ③ 불필요 |
| ctrl_multipeak_dim3 (정 control) | control | 3 | 0.701 / 0.727 | True | 진단기는 다봉을 검출할 수 있다 ✓ |
| ctrl_multipeak_dim40 (정 control) | control | 40 | 0.795 / 0.818 | True | 진단기 건전 ✓ |
| ctrl_quadratic_dim3 (부 control) | control | 3 | 0.000 | False | 진단기는 매끄러움을 검출할 수 있다 ✓ |
| ctrl_quadratic_dim40 (부 control) | control | 40 | 0.000 | False | 진단기 건전 ✓ |

포인트는 3 개:

1. **실 proxy 지형 (3 차원 / 40 차원 모두) 은 valley≈0 = 단봉.** 3 seed 에서 완전 일치.
2. **진단기 자체는 건전.** 일부러 만든 다봉의 정 control 은 제대로 다봉 (0.70/0.80) 으로 검출하고, 이차함수의 부 control 은 제대로 매끄러움 (0.0) 으로 검출한다. 그래서 "실 proxy 가 단봉" 은 계기의 버그가 아니라 지형의 성질이다.
3. 이로써 **"과거의 ③ negative 는 underpower 가 아니라, 지형이 정말로 매끄러웠기 때문"** 이, 실 substrate 위에서 처음으로 noise-free 로 뒷받침됐다.

부차적 발견도 정직하게 써 둔다. **정 control 로 쓸 작정이었던 기만 corridor (`make_corridor_eval(d=0.16)`) 가, 결정론화하니 valley=0.0 (단봉 판정)** 이 되어 버렸다. corridor 의 기만성은 "단일 basin 안에 가두어 ③ 의 behavioral niching 으로 탈출시키는" 형 (behavioral-reach 기만) 이지, **지형의 골짜기 (C1 multi-basin) 의 기만이 아니었다.** corridor 는 C1 의 정 control 이 되지 않는다, 는 scope 의 좁아짐을 실측으로 확정했다. 이것은 과거의 골짜기 깊이 교정이 "corridor 유래의 임계값" 을 지형 다봉성으로 전송할 수 없음을 의미한다.

— 여기서 한숨 돌림. "정 control 이 control 이 되지 못했다" 는 건 은근히 충격이었다. 하지만 이것도 측정해 보지 않으면 알 수 없었다. —

---

### 5. EXP1 —— 실 multitask 근방에서만 "③ NOT null" 의 약한 기미

다음으로, 실문제에 가장 가까운 띠 (C-gen4b = MAP-Elites vs random, 실 multitask 근방) 를, 샘플 수를 진지하게 늘려 재검정했다.

| case | 원 n=15 (감사) | fresh 진 재주행 | 판정 |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, 단측 p 0.038, psd +0.188, gate PASS** | **③ load-bearing 후보 (still_inconclusive)** |

fresh seed 로 n=64 까지 돌렸더니 **strict gate 를 4 조건 전부 PASS** 했다. 즉 감사가 "③ 불필요 (inconclusive)" 라고 읽은 것은 방향으로는 틀렸고, **C-gen4b 에서는 ③ 는 NOT null 의 방향.**

…그리고 여기서 이겼다고 들뜨지 않는 것이 이번의 핵심이다. 3 가지 이유로 **후보에 그치게** 했다.

1. **갱신 후의 검출력 power@n64 = 0.517 < 0.80.** gate 는 통과했지만, 확증의 기준 (검출력 0.80) 에는 못 미친다.
2. **주행 내 드리프트 (이것이 효과적이었다).** 누적 p 값의 궤적을 따라가면: n=40 에서 첫 PASS (p=0.042) → n=60 에서 p=0.010 으로 깊게 유의화 → **n=64 에서 p=0.038 로 0.05 경계 근처로 되돌아왔다.** 더욱이 seed 를 전반/후반으로 나누면, **전반 32 seed 는 diff=+0.0755 (frac_pos=0.625) 지만, 후반 32 seed 는 diff=+0.0189, 마지막 9 seed 는 diff=−0.0376 (음).** PASS 는 전반 seed 에 떠받쳐져 있고, **새로운 데이터일수록 역방향으로 달리고 있다.**
3. **다중 비교.** p=0.038 은 α=0.05 에서는 PASS 지만, EXP1 의 3 case 만으로도 Bonferroni α=0.0167 을 초과 (FAIL). ③ research family 전체로 보면 더 엄격하다.

게다가, 효과량의 바닥 (psd) 이 **구조적 천장** 에 부딪쳐 있었다. C-gen4b 의 median psd 는 n=15→0.200, n=255→0.200 으로 꿈쩍하지 않는다. `P(|psd|≥0.147)` (효과량 조건의 충족률) 는 n=255 에서도 0.794 로 정점을 친다. 중효과 (psd≈0.20) 이므로, 샘플을 아무리 늘려도 full gate 의 검출력이 0.80 을 넘지 않는다. **즉 "샘플을 늘리면 (A) 확정된다" 는 전망 자체가, 이 proxy 위에서는 희박하다.**

결론: **C-gen4b 는 "③ load-bearing 후보 / still_inconclusive".** "③ NOT null" 이라는 headline 은, 단발의 경계 p=0.038 에 너무 기대고 있다. 주행 내 드리프트는 "후보가 위양성일지도 모른다" 는 진짜 증거다.

---

### 6. EXP3 ——"후처리가 ③ 를 숨기고 있다" 는 의심은, 떼어내니 오히려 악화됐다

마지막 의심은 이러했다. "ridge readout 의 clip (K4) 이라는 후처리가, 실은 ③ 의 신호를 짓누르고 있는 것 아닌가?" 만약 그렇다면, clip 을 떼어내면 ③ 가 떠오를 터다.

떼어내 봤다.

| task | clip | MAP-E mean | baseline 승수 | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (전부 악화) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

clip 을 떼어내니, ③ 가 떠오르기는커녕 **addition 에서 MAP-Elites 가 +0.010 → −1.212 로 열화.** clip=False 는 raw R²<0 의 노이즈 영역 (15/15 seed 가 음, R² 가 [−3.68, −0.20]) 에 MAP-Elites 를 떨어뜨려, 구조를 회복하기는커녕 악화시켰다. **= "clip 이 신호를 숨기고 있다" 는 가설을 능동적으로 반증.**

null-ridge FPR (gene 비의존 target = 진정한 귀무가설) 도 clip True/False 에서 차이 0 (양쪽 0.0).

판정: **K4 는 "유일한 능동적 suppression 기제" 가 아니라, "spread 를 짓누르지만 verdict 를 바꾸지 않는 진단적 소견" 으로 강등.** 이로써 과거의 통계 감사가 단정했던 "K4 = 유일한 능동적 suppression" 은 과대했음이 판명됐다.

정직한 유보 (§6.3 상당): null-FPR=0/0 은 null_seeds=4 만의 바닥값이고, 이 실험은 예산을 약 7 배 축소하고 있다. 그래서 verdict 의 라벨은 "null 확정" 이 아니라 **"not_load_bearing_at_this_budget (이 예산에서는 비載荷)"** 로 통일했다. "null 을 확정했다" 보다 "이 예산에서는 K4 가 load-bearing 이 아니다" 가 정확하기 때문이다. 판정의 실체 (진단적 소견으로의 강등) 는 불변이고, 어휘의 정밀도만 올리고 있다.

— 여기서 심호흡. 3 실험 끝. 다음은 "지나치게 말하지 않았는가" 의 자기 점검. —

---

### 7. Surviving refutation —— 3 개의 렌즈로 자신의 결론을 때려 봤다

honest disclosure 의 핵은 "자신의 결론을 가장 매섭게 의심한다" 는 것이므로, 3 개의 독립된 반증 렌즈를 댔다. **3 개 모두 `refuted=true / medium` 으로 살아남았다**, 즉 보수적인 verdict 는 뒤집히지 않지만, positive 쪽의 강조는 약화시키는 방향으로 효과를 냈다.

1. **[power_adequacy] C-gen4b 의 gate PASS 는 optional-stopping + 다중 비교에서 취약.** 위 §5 의 드리프트와 Bonferroni FAIL 이 이것. "③ NOT null" 을 headline 으로 하는 것은 경계 p 에 너무 기댄다. → p 의 n 궤적과 후반 seed 의 부호 반전을 공개 필드에 기록 완료.
2. **[determinism_and_circularity] 단봉 verdict 는 임계값 근접에서 취약.** 결정론화와 비순환성 그 자체는 clean (behavior 와 fitness 의 상관은 ≈0, 진단기는 behavior 기술자를 쓰지 않고 지형 기하를 직접 본다). 다만 ESN_3param 의 midpoint 의 **90.9% 가 하방으로 dip** 하고 있어, 최대 상대 dip=0.0435 는 C1 골짜기 임계 0.05 의 바로 아래 (13% 이내). 그래서 정밀하게 말하면 "**진정으로 단봉**" 이 아니라 "**C1 임계값을 약간 밑도는 얕은 골짜기 (~2–4%) 를 가진 약 multi-basin**". (B) null 의 방향은 유지되지만, 견고성은 임계값 근접 때문에 한정적이다.
3. **[clip_flip_validity] K4 강등은 저예산 때문에 "at this budget" 한정.** verdict_flip=False 는 확실하지만, FPR 0/0 은 바닥값, 예산은 7 배 축소. 그래서 "firm refutation" 보다 "not load-bearing at this budget" 이라 서술해야 한다.

3 개 모두 "결론을 뒤집을" 정도는 아니지만, "지나친 말을 깎는" 방향으로 전부 효과를 냈다. 이 자기 감사야말로 오늘 성과의 절반이다.

---

### 8. 자신이 밟은 실수를 하나 정직하게 쓴다

지난번 골짜기 깊이 workflow 에서, 2 단째 오케스트레이터 briefing 에 **stale (오래된) 값** 을 넘겨 버렸다. "전부 below threshold / d*=0.1234" 같은 값이다. 그런데 실제로 commit 된 결과 JSON 은 `all_below_threshold=false` 였다. 지난번 workflow 결과를 읽을 때, 다른 메트릭의 값을 착각했던 것이다.

**적대 검증이 이것을 검출해, verdict 를 N/A 로 강등했다.** 즉 "너무 깔끔한 결론" 을 스스로 의심하는 프로세스가, 자신의 복사·붙여넣기 실수를 붙잡았다. 기분 좋은 이야기는 아니지만, 이것이 돌아갔기에 오늘의 Step D 에서 올바른 발판에서 다시 측정할 수 있었다.

honest disclosure 는 "실패를 지우지 않는다" 뿐 아니라, "**실패를 검출하는 구조를 미리 놓아 둔다**" 는 것이구나, 하고 새삼 생각했다.

---

### 9. 과거 verdict 를 어떻게 갱신했는가

| 과거 verdict | 과거의 읽기 | Step D 의 갱신 |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **방향 갱신: ③ 는 NOT null 의 방향 (fresh n=64 에서 gate PASS).** 다만 후보에 그침 |
| step6 exp7 (실 ESN proxy, ③ negative) | n≤10 맹점역, "재측정 필수" | **대폭 갱신: 지형이 정말로 매끄러움 (③ 불필요) 을 noise-free 로 확정.** 재측정해도 다봉은 나오지 않음 |
| 골짜기 깊이 N/A (계측 불능) | instrument 불능 | **해소: 결정론화로 계측 가능화** → vf≈0 (단봉). 다만 임계값 근접의 얕은 골짜기가 유보 |
| K4 clip = 유일한 능동적 suppression | "clip 이 landscape 구조를 은폐" | **강등: 진단적 소견** (not_load_bearing_at_this_budget) |

"③ 불필요로 보였던 과거 negative 의 다수는 underpower 가 아니라, 지형이 정말로 매끄러웠다" ── 이 한 점이, 실 substrate 위에서 처음 확인된 것이 오늘의 핵심이다.

---

### 10. 외부 리뷰 (Codex) 는 블로커 없이 추인

llcore 의 규율로서, 각 capstone 은 Codex (gpt-5.4, read-only) 의 페어 리뷰를 통과시킨다. 이번 총평은 **"블로커 없음 ── ③ 결론을 외부 확인".**

- C-gen4b 를 load_bearing 이 아니라 후보에 그치게 한 판단은 타당 (갱신 검출력 0.5174 < 0.80 을 JSON 에서 확인).
- EXP2 의 결정론·비순환은 clean. "진정으로 단봉" 보다 "임계값 아래의 약 multi-basin" 이 정밀하다, 는 본문의 자인도 추인.
- EXP3 의 K4 강등은 현 예산이라면 타당 (FPR 0/0 + 7 배 축소 때문에 at-this-budget 한정).

지적된 4 건 (CF1～CF4) 은 **전부 장래 rerun 시의 harness 견고성과 문언 정밀도** 이며, 현 결론을 뒤집는 것이 아니다. GPU 에서 ③ 를 재검정할 때, 이것들을 적용한 뒤 harness 를 재이용한다.

---

### 11. CPU 의 샛길 (kernel 다양화 / BG9) 을 시도하고 있었다

"③ 의 본진은 GPU (실 LLM 의 손실 지형) 로" 가 EXP2 의 권장이다. 실 proxy 가 매끄럽다고 확정된 이상, 매끄러운 지형에서 ③ 를 쫓아도 (A) 는 나오지 않는다 (지형이 한 개의 산이면 골라내기에 이득이 없는 것은 당연).

다만 GPU 는 투자 판단이므로, **CPU 에서 전진할 수 있는 다른 가설** 을 병행해 시도하고 있었다. 그것이 **kernel 다양화** 다.

가설은 이렇다. 개개의 kernel (rwkv / mamba / hopfield / linear_attn) 이 매끄러워도, **4 종류의 kernel 족을 union 하면, kernel 전환의 순간에 fitness 가 불연속적으로 단차를 만든다 → 지형이 multi-basin (속임수 지형) 이 될 수 있다 → ③ 가 GPU 없이 CPU 위에서 load-bearing 이 될 수 있다.** 이것을 검증하는 것이 BG9 였다.

이 글을 처음 썼던 시점에서는 "지금 BG6 (task → best-kernel 사상이 비정수인가, 즉 '태스크마다 잘하는 kernel 이 다른가') 을 smoke 측정하고 있는 중" 이었다. 그 후 (같은 2026-06-02 안에) BG9 의 결판이 났다. 다음 추기절이 그 결말이다.

---

### 11.5. 추기 (2026-06-02): BG9 결판 —— 샛길은 구조적으로 닫혀 있었다

> 결론을 한 줄로: **BG9 = N/A (구조적). 즉 kernel 다양화라는 CPU 샛길은 "③ 가 서지 않는 것이 구조적으로 정해져 있" 으므로 닫혔다.** "③ 가 필요 없다" 가 아니라 "이 공간에서는 ③ 가 강한 baseline 과 원리적으로 분리될 수 없다" 는, 정보량 있는 negative 다.

§11 에서 깔아 둔 샛길의 결과가 나왔다. 기대했던 "kernel union 으로 multi-basin (속임수 지형) 이 생겨 ③ 가 CPU 에서 선다" 는 **일어나지 않았다.** 게다가 "우연히 서지 못했다" 가 아니라 **구조적으로 설 수 없다** 는 것을 알게 됐다. BG9 는 이것을 3 단의 증거로 확정하고 있다.

#### (1) substrate validity ——"변별은 있지만 약하다" (PASS 지만 요주의)

먼저 "태스크마다 잘하는 kernel 이 다른가" (BG6) 를, kernel-favoring task 군을 제1원리로 다시 설계해 측정했더니, 사상은 **비정수 = 비 inert (PASS).** mamba / linear_attn / rwkv 는 각각 다른 태스크에서 best 가 됐다. BG6 에서 밟은 "memory_tasks 는 kernel 중립" 의 전철을 피할 수 있었다, 는 의미에서는 전진이다.

다만 정직하게 말하면 **약하다**:

- **hopfield 는 어느 태스크에서도 이기지 못했다.** 이것은 hopfield kernel 이 **대각 스칼라 mock** 이라, tanh 어트랙터가 기능 불능이었기 때문 (per-seed 의 R² 가 0/0.99/0 으로 양극화). 즉 실질 "4 kernel union" 이 아니라 **3 kernel** 이다.
- clean 한 전문화는 2 축뿐 (selective_copy↔mamba / weighted_accum↔linear_attn). 나머지는 margin 이 얇고 fragile.

→ **변별의 존재 ≠ 다봉/장벽.** non-inert 화에는 성공했지만, 그것이 기만 지형 (속임수 지형) 을 보증하는 것은 아니다, 는 데까지. 또한 대각 mock 의 한계는 kernels.py 의 scope 선언대로이며, 여기서는 **기제의 feasibility 만 주장** (full kernel 성능은 비주장) 이다.

#### (2) harness validity —— positive control 이 validate 하지 않는다 (이것이 결정타)

다음이 본진이다. 고정 파라미터 (behavior=(kernel_id, theta L1)) 로 MAP-Elites (③) 를, 3 개의 baseline ── **RR-hillclimb (random restart 등산)** / panmictic-GA / random ── 과 honest 하게 paired 비교했다.

| 기질 | 결과 |
|---|---|
| **positive control** (합성 kernel-barrier) | ③ 는 panmictic (+0.423) 과 random (+0.208) 은 격파. **하지만 RR 에게는 이기지 못한다** (+0.051, p=0.31 → FAIL). 3 baseline 전승에 못 미침 = **harness validity 가 서지 않는다** |
| **negative control** (kernel 중립 태스크) | 전 method R²≈1.0 포화, ③ 우위 없음 = **올바르게 null** (위양성 없음, 계기는 건전) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3, panmictic 이 오히려 ③ 를 능가 = **③ 이기지 못함** |

여기가 Step D (기술판 §4-7) 와 결정적으로 다른 점이다. Step D 의 기만 corridor 에서는 ③ 가 RR 을 배제할 수 있었다. **왜 kernel 공간에서는 못 하는가?** 근본 원인은 하나:

> **RR 은 restart 할 때마다 kernel_id ∈ [0,4) 를 직접 샘플링할 수 있다.** kernel 선택은 4 이산의 단일 좌표 (저차원) 이므로, RR 은 restart 로 전 4 kernel 을 직격한다. "best kernel 을 찾는" 데 골짜기를 넘을 필요가 없다 = **teleport (직접 워프).** 그래서 ③ 의 behavioral niching 에 차례가 오지 않는다.

Step4 의 corridor 에서 ③ 가 RR 을 배제할 수 있었던 것은, 거기의 behavior 가 `mean(24 차원)` 이고, CLT 에 의해 평균이 0.5 에 집중 → 대역 피크가 measure-zero 역 = **random/RR 이 직접 샘플링할 수 없는 고차원** 이었기 때문이다. kernel_id 는 반대로 저차원이라 직접 샘플링되어 버린다.

#### (3) red-team —— 적대 검증으로도 반증할 수 없고, 오히려 확증

"harness 가 서지 않는 것은 정말 구조 탓인가? 우연한 설정 실수 아닌가?" 를 독립 red-team 으로 두들겼다. 결과는 구조 주장을 **반증할 수 없었고, 오히려 강화**:

- **기제 확증**: instrumented RR 이 positive control 위에서 4 basin 에 restart kid 를 [12,18,16,18] 로 거의 균일 분산, target 도달 88%, best 는 restart→in-basin climb 가 6/8 seed. "RR 은 restart 로 kernel_id 를 직접 샘플링해 골짜기를 회피한다" 를 **수치로 확증.**
- **4 개의 faithful 구성 (고차원 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 모두에서 ③ 는 RR 에게 이기지 못한다 (beats_rr=False).** corridor 를 풀면 RR 도 동등 도달, 조이면 ③ 가 **먼저 starve** (아사).
- **경계 sweep**: theta corridor 의 차원을 D=0→3 으로 조일수록 ③ 가 RR 보다 빨리 starve (D=3: ③ reach 0.08 vs RR 0.42). base_seed 3 가지로 동일.

→ **"RR 만 배제하고 ③ 가 통하는 behavior 차원은, kernel 공간에 구조적으로 존재하지 않는다"** 를 정량 확증.

#### 구조적 통찰 (이 결판의 payoff)

> **③ (MAP-Elites 의 behavioral niching) 이 강한 baseline 을 능가하는 것은, "난소" 가 고차원 behavior 공간에 있어 직접 샘플링 (random restart) 으로 도달할 수 없을 때뿐.**

- **kernel 선택은 저차원 (4 이산의 단일 좌표)** → RR 이 직접 샘플링 → ③ 의 niching 우위가 원리적으로 나오지 않는다.
- theta 공간에 기만을 옮겨도, RR 은 restart 후에 in-basin 에서 greedy climb 하므로, corridor 를 RR 이 빠져나가지 못할 정도로 조이면 ③ 도 같은 정도로 starve 한다. **RR fail ∧ ③ succeed 의 창이 존재하지 않는다.**

이것은 Step4 §7 에서 남은 질문 "탐색 공간을 kernel 다양화로 확장하면 ③ 가 unlock 하는가?" 에 대한 답이다. 답은 **NO (CPU 에서는 구조적으로).** 확장이 ③ 를 unlock 하려면, 추가한 자유도가 **고차원이라 직접 샘플링이 곤란한** behavior 를 낳아야 한다. kernel 선택 (저차원·이산) 은 그 조건을 충족하지 않는다.

#### GPU 로의 함의

- **CPU 모두 쏟기 게이트가 CLEAR**: BG9 가 마지막 CPU 길 (kernel-union) 을 구조적으로 닫았다. ③ 의 남은 길은 **고차원의 GPU full-LLM 손실 지형뿐.**
- 구조적 통찰은 GPU 의 베팅을 **better-motivated** 하게 만든다. ③ 는 고차원 behavior 에서 비로소 의미를 가진다. full-LLM 의 파라미터 공간은 수백만 차원 = 바로 고차원. 그래서 GPU 검정은 "full-LLM 만이 예외일지도" 라는 약한 베팅이 아니라 "③ 는 고차원을 요하고, full-LLM 이 고차원역" 이라는 원리에 부합한다.
- **다만 여전히 bet**: 실 LLM 지형이 backprop 계의 강한 baseline 으로 직접 내비게이트할 수 있다면 ③ 불필요 ── 이것은 **BG9 의 RR 과 동형의 리스크** 다 ("강한 baseline 이 직접 푼다" 가능성은 GPU 에서도 남는다). 그래서 GPU 는 "③ 를 위해 단독" 이 아니라 **포트폴리오 판단** (llive 실 LLM fitness 등과 동승) + **클라우드 대여로 사전 등록 1 건** (자본 커밋 전) 이 적정. BG9 의 구조적 통찰 그 자체가 GPU 의 falsifiable 한 go/no-go 기준이 된다: "③ 가 full-LLM 에서 load-bearing 이라면, 그 난소는 고차원 behavior 공간에 있어 직접 샘플링/backprop 으로 도달 곤란할 터."

#### honest 유보 (중요)

- 이것은 **"③ 불필요로 판명" 이 아니다.** "③ 가 이 저차원 kernel 공간에서는 강한 baseline 과 원리적으로 분리될 수 없다" = N/A (구조적) 이며, ③ 의 기제 자체는 Step4 에서 진짜로 확정 완료다. N/A 지만 "kernel 길은 닫혀 있다" 는 결정적 정보를 가진 **정보량 있는 N/A** 다.
- harness/red-team 은 smoke 규모 (5-12 seed). 본검정 15 seed 에서는 수치는 움직이지만, **구조 (조이면 ③ 가 먼저 starve / RR 이 kernel_id 를 직접 샘플링) 는 seed 비의존으로 견고.** real 의 full ≥15-seed 본검정은 실시하지 않는다 ── positive control validity 가 구조적으로 서지 않는 이상, real 에서 ③ 불필요가 나와도 "③ 불필요 vs 검출기 맹" 을 분리할 수 없고, 그 "검출기 맹 = kernel 공간의 구조" 를 red-team 이 이미 확정했으므로, CPU 를 7.5h 투입해도 결론은 바뀌지 않기 때문이다.
- substrate 는 약하다 (실질 3 kernel, **hopfield 는 대각 mock 으로 기능 불능**). 더 강한 kernel 변별 (full 구현·비대각) 이라면 다른 결론의 여지가 **이론상** 있지만, ③ 의 구조적 장벽 (저차원 선택 → RR 직접 샘플링) 은 kernel 구현의 질과 독립이다.
- "너무 깔끔한 ③ 성립" 을 의심하는 규율은 이번에는 **불필요했다** ── ③ 성립은 처음부터 나오지 않았다 (honest prior 대로의 negative).

---

### 12. 메타 교훈 —— 정직함은, 이기기 위한 도구였다

오늘의 진짜 성과는 수치가 아니라, **"너무 깔끔한 결과를 의심하는" 정신이 실제로 연구를 앞으로 나아가게 했다** 는 것이다.

- 평가 노이즈를 물리적으로 지웠기 (EXP2) 때문에, "매끄러움" 이 지형의 성질인지 계기의 한계인지를 가려낼 수 있었다.
- 적대 검증 3 렌즈를 댔기 때문에, "③ NOT null" 을 headline 으로 하지 않고 "후보" 에 머무를 수 있었다.
- 자신의 stale 값 착각을 자기 검출했기 때문에, N/A 라는 올바른 강등을 할 수 있었고, 오늘 다시 측정할 수 있었다.
- **BG9 (추기) 에서 하나 더 배웠다**: **저차원의 난소는 강한 baseline 이 직접 풀어 버린다. 그래서 ③ (골라내고 키우는 공정) 가 효과를 내려면 "고차원 behavior 공간" 이 필요하다.** "속임수 지형을 만들면 ③ 가 선다" 는 절반만 맞고, 정확히는 "**직접 샘플링할 수 없을 만큼 고차원인** 속임수 지형" 이 아니면 ③ 는 서지 않는다. kernel 4 택 (저차원) 에서는, RR 이 restart 로 전부 직격하므로 ③ 의 차례가 원리적으로 오지 않았다. 이것은 샛길을 "포기" 가 아니라 "**구조적으로 닫혔다**" 고 단언할 수 있는 근거다.

"이상하게 좋은 결과가 나오면, 이긴 기분이 되기 전에 반드시 내막을 의심한다" ── FullSense 의 연구 규율 (`feedback_benchmark_honest_disclosure`) 은, 단순한 자계가 아니라, **실제로 위양성을 붙잡아 연구의 정밀도를 올리는 기제** 로서 돌아가고 있었다. BG9 는 그 역방향 (**negative 를 올바르게 negative 로 확정한다**) 에서도 같은 규율이 효과를 낸 예다 ── red-team 에서 자신의 "③ 가 서지 않는다" 를 반증하려다, 반증할 수 없어 구조로서 확증됐다.

결론을, 마지막으로 한 번 더, 정확하게 (BG9 결판을 반영):

> **proxy substrate 위에서는 "③ 는 지형이 진정으로 매끄럽기에 불필요" 가 noise-free 로 확정**됐다 (Step D). 실 multitask 근방 (C-gen4b) 에서만 "③ NOT null" 의 약한 징조가 나왔지만, 소효과 + 드리프트 + 다중 비교로 **후보에 그침.** K4 clip 은 능동적 suppression 이 아니라 진단적 소견으로 강등. 그리고 CPU 의 마지막 샛길 **kernel 다양화 (BG9) 는 구조적으로 닫혔다** ── kernel 선택은 저차원이라 강한 baseline (RR) 이 직접 샘플링하고, ③ 의 niching 우위가 원리적으로 나오지 않는다. **③ 의 본진 검증에 남겨진 길은, 고차원의 GPU full-LLM 손실 지형뿐** (그것도 "강한 baseline 이 직접 푼다" 리스크를 안은 bet).

"③ 결판 = ③ 는 불필요로 판명" 이 아니다. 정확히는 **"③ 가 살아나는 건 '고차원의' 기만 지형일 때뿐. 지금 CPU 로 측정할 수 있었던 실물 비슷한 것 (매끄러움) 도 kernel 다양화 (저차원) 도, 그 조건을 충족하지 못했다."** 본진 (GPU 고차원) 은 아직 멀고, 게다가 보증 없는 베팅이다.

---

**Tags**: 진화 계산 / MAP-Elites / 통계 검정 / 검출력 / honest disclosure / CPU 연구
**관련**: 연재 #32 (llcore CPU PoC battery) / #29 (반증·Goodhart·proxy 한계) / #31 (Codex 이본주)
**Project**: llcore (PyPI 예약 llmesh-llcore, 리포지토리 미공개이므로 로컬 연구)

---

## 제10장 (연재 #34) 산오르기 6연전으로 알게 된 「진화의 ③은 언제 효과가 있는가」— 그리고 100년 전의 진화생물학이 같은 답을 내놓고 있었다

### TL;DR

- 질문은 **「AI의 코어 계산을 진화로 탐색할 때, '가려내어 따로 길러 내는 공정' (= 진화의 ③ 적자생존/분리) 은 정말로 필요한가」**. 연재 #33은 종반 (Step D + BG9) 의 결착을 썼지만, **이 #34는 arc 전체 (6단) 를 하나의 이야기로 조망**합니다.
- **제1단 (합성 속임수 지형)**: ③은 압승 (Cliff δ=+1.0). ③은 메커니즘으로서 진짜 = **존재 증명**.
- **제2단 (기억 과제 / 다중 reservoir)**: 기질의 「바닥」과 「천장」에 가로막혀 ③을 측정 불가 = **N/A**.
- **제3단 (다중 과제 일반화)**: ③은 「선택 없음」에는 이기지만, 단순한 선택이나 random에는 못 이김 = ③ 불필요 (honest negative).
- **제4단 (실제 proxy 지형을 noise-free 측정)**: 평가 노이즈를 물리적으로 0까지 낮췄더니 지형은 **정말로 매끄러움 (단봉)** = ③ 불필요 확정. 「과거의 negative는 검출력 부족이 아니라 지형이 매끄러웠던 것」이 처음으로 뒷받침되었다.
- **제5단 (부품 4종을 섞는 샛길 BG9)**: kernel 선택은 **저차원**이기에 강한 baseline (랜덤 리스타트 산오르기) 이 직접 샘플링하고, ③의 niching 우위가 **구조적으로** 나타나지 않음 = 샛길은 막혔다.
- **구조적 통찰 (이 arc의 핵심)**: ③이 효과가 있는 것은 난소(難所)가 **고차원 behavior 공간**에 있어 직접 샘플링이 불가능할 때뿐. 실제 CPU 기질은 저차원/매끄러우므로 ③ 불필요.
- **생물학적 접지 (검증 완료)**: 이것은 라이트 (Wright) 의 **시프팅 밸런스 설** 바로 그것. **흑화형 나방 (단일 유전자 = 저차원)** 에서는 보통의 선택으로 충분 (= BG9의 kernel 케이스), **렌스키의 Cit+ (고차원・역사 의존)** 에서는 다양성이 효과적 (= ③ regime). 우리의 negative는 **코인 비판의 계산판** (현실 지형은 단순하고 ③은 드물게만 결정적).
- **메타 교훈**: 「너무 잘 풀린 결과는 승리가 아니라 경보」. 사전 등록・honest disclosure・적대 검증・결정론적 noise-free 측정으로, 섣부른 기쁨을 피했다.

> ⚠ 이 글의 수치는 모두 수중 (로컬) 의 연구 기록에 연결된 실측입니다. llcore는 아직 공개 리포지토리를 만들지 않았으므로 외부 링크를 붙일 수 없습니다. 대신 「어떻게 측정했는가」를 본문에 씁니다. 생물학 파트에서 인용하는 논문은, 별도로 1차 정보로 존재・귀속・주장 내용을 대조한 것만 들고 있습니다.

---

### 0. 이 글은 무엇에 대한 이야기인가 (콘셉트)

`llcore`는 「Transformer의 코어 계산 (상태 갱신 규칙・학습 규칙・인지 구동 Δ) 을 유전자로 삼아, Z3로 망가지지 않도록 검증하면서 진화시킨다」는 CPU 완결 연구 프레임워크입니다.

그 진화 엔진에는, 진화의 4요소 (① 변이 / ② 유전 / ③ 적자생존・분리 / ④ 과잉번식) 중 **③ (selection / separation)** 을 어떻게 효과적으로 발휘시킬 것인가, 라는 설계상의 급소가 있습니다. 다양성을 유지하며 니치에 남기는 MAP-Elites 같은 「가려내어 따로 길러 내는」 구조입니다.

질문은 단순합니다.

> **그 ③, 정말로 필요한가?**

필요하다면, ③을 얹기 위한 무거운 투자 (최종적으로는 GPU로 실제 LLM을 돌리는 것) 에 의미가 있다. 필요 없다면, ③에 집착하는 것은 시간과 전기의 낭비가 된다.

연재 #33에서는 그 질문의 **종반** (Step D의 결정론 측정 + BG9의 구조적 결착) 을 상세히 썼습니다. 하지만 거기에 이르기까지에는 **6단의 실험**이 있었고, 이기거나 (존재 증명), 측정하지 못하거나 (N/A), 지거나 (honest negative) 를 반복했습니다. 이 #34에서는 그 **arc 전체를 하나의 이야기**로 다시 늘어놓습니다. 게다가 이번의 볼거리로서, **이 계산 결과가 100년 가까이 전의 진화생물학 논쟁 (라이트 대 피셔) 과 놀랄 만큼 같은 형태를 하고 있다**는 것을, 검증 완료한 1차 정보로 접지합니다.

— 여기까지 40초. 준비운동 끝. 본론으로. —

---

### 1. 비유: 산오르기, 그리고 속임수 지형, 그리고 기억의 궁전

수식 전에, 이 연구에서 일관되게 쓰고 있는 3개의 메타포로 전체상을 파악합니다.

설계의 좋고 나쁨을 **지형의 높이**로 나타냅니다. **높은 곳 = 좋은 설계**. 가장 높은 정상을 찾는 게임입니다.

**지형 1: 매끄러운 한 봉우리 (쉬움)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

이런 지형에서는, 소박한 「산오르기법 (hill-climbing)」, 즉 「지금보다 조금 더 좋은 쪽으로 움직이기만」 하는 것으로 충분히 정상에 닿습니다. **공들인 공정 (③) 은 필요 없습니다.**

**지형 2: 속임수 지형 (기만적 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

여기서는 소박한 산오르기가 가짜 정상에서 멈춥니다. 골짜기를 내려갈 용기가 없기 때문입니다.

이때 효과를 발휘하는 것이 ③의 발상입니다. **여러 타입의 등산자를 골짜기 여기저기에 남겨 둡니다** (= 기억의 궁전 / MAP-Elites archive). 누군가가 골짜기를 「징검돌 (stepping-stone)」 로 건너 진짜 정상에 도달할 수 있다, 라는 구조입니다.

**이 연구의 핵심을 한마디로**: ③이 정말로 도움이 되는 것은 **「속임수 지형」일 때뿐**. 매끄러운 한 봉우리에서는, ③은 무용지물입니다.

그래서 질문은 이렇게 바꿔 말할 수 있습니다.

> **「진화로 AI를 설계할 때, 실제로 마주치는 지형은 '속임수 지형'인가, 아니면 '매끄러운 한 봉우리'인가?」**

#33에서는 Step D + BG9로 이 질문에 결착을 지었습니다. 이 #34에서는, 거기에 이르는 **6단의 산오르기 전부**를 보여드립니다. 각 단에서 「속임수 지형이었는가 / 매끄러웠는가 / 애초에 측정할 수 있었는가」가 달라지는 것이 흥미로운 점입니다.

— 잠깐 쉼. 준비는 여기까지. 여기서부터 6연전의 실록입니다. —

---

### 2. arc 전체 지도 — 6단의 산오르기를 한눈에

먼저 지도를 내놓습니다. 이것이 이 글의 등뼈입니다.

| 단 | 기질 (어떤 지형을 측정했나) | ③은 효과가 있었나 | 한마디 |
|---|---|---|---|
| **I (Step 4)** | 합성한 「속임수 지형」(기만 corridor) | **Yes (압승)** | 존재 증명. ③은 진짜 |
| **II (Step C / 사다리1)** | 기억 과제 / 다중 reservoir 패리티 | **N/A** | 바닥・천장・degree-5의 벽으로 측정 불가 |
| **III (E-A)** | 다중 과제 일반화 | **No** | ③은 「선택 없음」에는 이기지만, 그 이상은 아니다 |
| **IV (Step D)** | 실제 proxy의 텍스트 지형 (결정론 측정) | **No** | 지형이 **정말로 매끄러움**으로 확정 (noise-free) |
| **V (BG9)** | 부품 (kernel) 4종의 union | **No** | **구조적으로** 막혔다 (저차원 선택) |

스토리 라인은 이렇습니다. **먼저 「③은 조건에 따라 압승하는 진짜다」라고 존재 증명하고 (I), 다음으로 「그럼 실제 문제에서는 어떤가」를 4단에 걸쳐 측정하러 갔더니 (II~V), 하나같이 "실제 CPU 기질은 ③이 필요 없는 지형이었다"**. 게다가 마지막 (IV, V) 에서 「필요 없는 이유」가 **검출력 부족이 아니라 지형의 성질**이라고 확정되었다 ── 이것이 arc 전체의 호(arc)입니다.

그럼 한 단씩.

---

### 3. 제I단 (Step 4) — 존재 증명: 속임수 지형이라면 ③은 압승한다

가장 먼저 한 것은 「③이 **이론대로 효과를 내는 장면이 실재하는가**」의 존재 증명입니다. 지형을 **일부러 기만적으로 만들어**, ③ (MAP-Elites) 을 3개의 baseline ── pure random / panmictic GA / **랜덤 리스타트 산오르기 (random-restart hill-climbing)** ── 와 대결시켰습니다.

**지형의 구성**: 유전자는 24차원. behavior (등산자의 타입) 를 `mean(유전자)` = 24개의 평균으로 정의합니다. behavior를 올리려면 **전체 24차원을 동시에 높게** 하지 않으면 안 됩니다. fitness는 「behavior≈0.4에 가짜 정상 (값 0.6) → behavior≈0.65에 골짜기 (값≈0) → behavior≈0.9에 진짜 정상 (값 1.0)」 라는, 그야말로 속임수 지형.

**결과**:

| 방법 | 진짜 정상으로의 도달률 | ③ 과의 비교 |
|---|---|---|
| **MAP-Elites (③)** | **약 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 위와 같음 |
| 랜덤 리스타트 산오르기 | 0% | 위와 같음 |

③만이 진짜 정상에 닿았고, 3개의 baseline은 전부 가짜 정상 (≈0.60) 에서 멈췄습니다. **100% 승 / 효과량은 이론 최대 (δ=+1.0)**. base seed 3가지 (총 60 seed) 에서 견고.

왜 이렇게 되는가, 가 나중의 복선이 됩니다.

- **random** 은 behavior가 반드시 ≈0.5에 집중한다 (24개의 평균은 중심극한정리로 0.5에 고정). 그래서 behavior 0.9에는 **영원히 도달할 수 없다** (6000 샘플을 뽑아도 0%).
- **산오르기** 는 가짜 정상 0.6까지 오르고, 골짜기를 내려가는 한 수를 거부. 리스타트해도 behavior≈0.5로 돌아가, 같은 함정으로.
- **③ (MAP-Elites)** 는 골짜기의 칸을 「새로운 behavioral 니치」로 보유하고, behavior를 0.5 → 0.9로 **징검돌로 건넌다**.

**경계도 정직하게 측정했습니다**. 골짜기를 없앤 매끄러운 corridor에서는, ③은 산오르기를 못 이기게 됩니다 (p≈0.29). **③은 만능이 아니라, 속임수 지형에서만 효과가 있다.**

**honest 유보**: 이것은 **일부러 만든** 합성 지형입니다. ③이 「가능」하다고 증명했을 뿐, 현실의 과제가 이 구조를 가진다는 증명은 아니다. toy 스케일・저노이즈・baseline은 소박한 (1+1) 입니다.

→ 여기서 가설이 섭니다. **「실제 문제의 지형도, 이 정도로 속임수 지형이라면, ③은 살아날 것」**. 다음 4단은, 그것을 실제 문제에 가까운 기질로 확인하러 가는 여행입니다.

— 한 모금. 제I단은 기분 좋은 압승이었습니다. 여기서부터 구름의 흐름이…. —

---

### 4. 제II단 (Step C / 사다리1) — 기질의 「바닥」과 「천장」에 가로막힌다 (N/A)

다음으로 「속임수 corridor가 **표준적인 기억 과제에 자연스럽게 출현하는가**」를 조사했습니다 (Step C). delayed parity / flip-flop / delayed recall을, 1개의 leaky reservoir + ridge readout으로.

결과는 깔끔한 **N/A (측정 불능)**. 이유가 양극단이라 흥미롭습니다.

- **delayed parity = 바닥 (floor)**: 1개의 reservoir는 XOR을 계산할 수 없다 (Minsky-Papert). 모든 방법이 R²≈0.003. 아무도 오를 수 없으므로 ③을 분리할 수 없다.
- **flip_flop = 천장 (ceiling)**: 모든 방법이 R²≈0.95에 포화. 분산이 짓눌려 ③의 차이가 나타나지 않는다 (③ vs random은 부호는 양이지만 p=0.15 = underpower로 **null이 아니다**).

여기서 중요한 발견이 하나. **유전자 공간의 다봉성은 높았다** (valley fraction이 parity에서 1.000) 인데, ③의 역할에는 도움이 되지 않았다. 즉 **「유전자 공간에서 다봉」≠「behavior에서 건너야 할 속임수 지형」**. 이 구별이 arc 후반의 열쇠가 됩니다.

**사다리1 (다중 reservoir)**: 그럼 reservoir를 여럿 연결하면 바닥이 올라가는가? → 5개의 메커니즘을 시험해 전부 `floor_lifted = false`. 깊이 (DeepESN) 는 바닥을 통계적으로는 올린다 (효과 +0.47/+0.60, PASS) 지만 절댓값은 R² 0.05-0.10에 그친다. 결정타는 positive control: degree-2 readout은 2-bit XOR을 엄밀히 푼다 (R²=+1.0) 지만 degree≥3에서 붕괴. **5-bit 패리티는 degree-5 = 이 CPU reservoir+ridge 패러다임의 구조적인 벽.**

→ 패리티 경로는 구조적으로 막혔다. ③의 본검정은 **패리티에서 내려올** 필요가 있다.

**honest 유보**: degree-5의 벽은 「이 설정의 벽」이지, 패러다임 전체의 불가능성 증명은 아닙니다.

— 잠깐 쉼. 「측정할 수 없었다」는 결과는 수수하지만, 지도를 그리는 데에는 중요한 공백 지대입니다. —

---

### 5. 제III단 (E-A) — 다중 과제 일반화: ③은 필요 없었다 (honest negative)

패리티의 바닥에서 내려와, **일반화 (generalization)** 로 ③을 측정했습니다. 가장 깔끔한 ablation을 짜서.

**설정**: 단층 leaky reservoir + ridge. 가변 지연의 recall. **짧은 지연 {15, 30} 으로 학습하고, 긴 지연 {45, 60} 으로 테스트** (외삽). 비교는 MAP-Elites (①②③풀) vs **선택을 뺀 MAP-Elites** (`randselect`: 부모를 랜덤으로 골라 무조건 배치 = 변이만) + panmictic GA + random.

**결과 (페어 리뷰 후)**:

| 방법 | 테스트 일반화 R² (평균±std) |
|---|---|
| MAP-E (①②③풀) | 0.682 ± 0.115 |
| MAP-E randselect (선택을 뺌) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| 게이트 | 비교 | diff | p (단측) | 판정 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**읽는 법**: ③은 「**선택을 뺀 드리프트 대조**」에는 이긴다 (C-gen3 PASS = "어떤 선택이든 무선택에는 이긴다"). 하지만 **panmictic GA (선택은 있지만 niching 없음) 에는 못 이기고** (오히려 근소하게 짐), random에도 못 이긴다. 즉 **niching 고유 (= ③ 본래) 의 기여는 없다**. 이 일반화 지형은, 단순한 선택이나 random으로도 같은 곳에 닿을 만큼 **매끄러웠다**. 제I단의 「매끄러우면 ③은 효과가 없다」 경계와 정합합니다.

**honest 유보 (중요)**: 이 verdict는 **이 설정 한정** (예산 400, grid 6×6). 게다가 ── 여기가 honest methodology의 핵심 ── 페어 리뷰 (Codex) 가 당초 「신용할 수 없다」고 판정하고, 3개의 rerun 블로커 (replicate마다의 독립 seeding / 예산 내 글로벌 최량의 채용 / honest_n을 16→30) 를 강제했습니다. **수정 후에도 결론은 바뀌지 않았습니다.** 「고치면 결론이 바뀌는 취약한 negative」가 아니었다, 라는 것이 수확입니다.

— 한 모금. 진 건 진 거지만, 「올바르게 졌다」는 것을 확인하는 작업 쪽이 시간이 더 걸렸습니다. —

---

### 6. 제IV단 (Step D) — 실제 proxy 지형은 「정말로 매끄러움」으로 확정 (noise-free)

여기가 arc의 전환점입니다. 제III단까지 「③ negative」가 이어졌지만, 줄곧 **응어리**가 남아 있었습니다.

> 「③ 불필요」는 정말로 **지형이 매끄럽기** 때문인가? 아니면 단순히 **샘플 수가 부족해 차이를 검출하지 못한 (underpower)** 것뿐인가?

이것을 헷갈리면 「③은 무력」이라고 과잉 일반화해 버린다. Step D는 여기에 결착을 짓습니다.

**트릭**: ESN reservoir (고정 seed) + ridge readout의 closed-form (`np.linalg.solve`) 은 **난수를 일절 뽑지 않는다**. 그래서 평가 노이즈를 **머신 엡실론 (약 1.11e-16)** 까지 물리적으로 0으로 만들 수 있다. 실측으로 `eval_noise_std ≤ 1.11e-16`을 확인 ── 이것은 부동소수점의 최소 단위 (ULP) 유래로 **실질 제로**입니다. 노이즈의 안개를 완전히 걷어내고, 지형의 골짜기를 직접 측정할 수 있다.

지형은 llcore 자신의 소스 (약 24k 문자) 의 다음 문자 예측. valley_fraction (골짜기의 비율, ≥0.2면 다봉=속임수 지형) 을 측정했습니다.

| 지형 | 차원 | valley_fraction (mean/max) | 다봉? | 판정 |
|---|---|---|---|---|
| **ESN 3-param** (실제 proxy) | 3 | **0.000 / 0.000** | No (3 seed 일치) | 매끄러움 → noise-free로 ③ 불필요 확정 |
| **ESN per-neuron** (실제 proxy) | 40 | **0.096 / 0.121** | No (3 seed 일치) | 매끄러운 편 → ③ 불필요 |
| 다봉 control (양) | 3 / 40 | 0.70 / 0.80 | Yes | 진단기는 다봉을 검출할 수 있다 ✓ |
| 이차함수 control (음) | 3 / 40 | 0.000 | No | 진단기는 매끄러움을 검출할 수 있다 ✓ |

포인트는 2개.

1. **실제 proxy 지형 (3차원 / 40차원 모두) 은 단봉**. 3 seed에서 일치.
2. **진단기 자체는 건전**. 일부러 만든 다봉은 제대로 다봉으로 검출하고, 이차함수는 제대로 매끄러움으로 검출한다. 그래서 「실제 proxy가 단봉」은 계기의 버그가 아니라 **지형의 성질**.

→ 이것으로 처음으로 **「과거의 ③ negative는 underpower가 아니라, 지형이 정말로 매끄러웠다」**가 실제 substrate 위에서 noise-free로 뒷받침되었습니다. 재측정해도 다봉은 나오지 않는다.

**honest 유보 (중요)**: 「매끄러움」은 임곗값 근접에서만 정밀합니다. ESN 3-param의 midpoint의 **90.9%가 약간 아래로 dip**하고, 최대 상대 dip (0.0435) 은 골짜기 임곗값 0.05의 바로 아래. 정확히는 「**진정으로 단봉**」이 아니라 「**임곗값을 근소하게 밑도는 얕은 골짜기 (~2-4%) 를 가진 약한 multi-basin**」. 방향은 유지되지만, 견고성은 임곗값 근접이기에 한정적 ── 여기를 「완벽한 볼록 그릇」으로 뭉뚱그리지 않는 것이, 이번의 규율입니다.

— 심호흡. 여기서 「실물 모형도 매끄럽다」가 확정. 남은 건 「마지막 CPU 샛길」입니다. —

---

### 7. 제V단 (BG9) — 부품을 섞는 샛길은, 구조적으로 막혀 있었다

실제 proxy가 매끄럽다고 확정된 이상, 매끄러운 지형에서 ③을 좇아도 이득은 나오지 않는다. 하지만 GPU는 투자 판단이므로, **CPU에서 전진할 수 있는 다른 가설**을 시험했습니다. 그것이 **kernel 다양화 (BG9)** 입니다.

**가설 (사전 등록 H7)**: 개개의 kernel (rwkv / mamba / hopfield / linear_attn) 이 매끄러워도, **4종류를 union하면 kernel 전환의 순간에 fitness가 단차를 만든다 → multi-basin (속임수 지형) 이 된다 → ③이 GPU 없이 CPU 위에서 선다**. 사전 등록한 honest prior는 **null 쪽** (지금까지 모든 CPU 기질이 매끄러웠으므로).

결과를 3단으로.

**(1) substrate validity — 변별은 있지만 약하다 (PASS지만 요주의)**: 과제마다 잘하는 kernel이 다른가를 측정하면, 사상(寫像)은 비상수 = non-inert (PASS). mamba는 selective-copy, linear_attn은 weighted-accumulation에서 best. 다만 **hopfield는 어떤 과제에서도 못 이겼다** (대각 스칼라 mock에서 기능 부전) 므로, 실질 「**3 kernel** union」. **변별의 존재 ≠ 다봉 장벽.**

**(2) harness validity — positive control이 validate하지 않는다 (결정타)**: 합성 kernel-barrier에서 ③을 3 baseline과 비교.

| 기질 | 결과 |
|---|---|
| **positive control** | ③은 panmictic (+0.423)・random (+0.208) 을 격파. **하지만 RR (랜덤 리스타트 산오르기) 에는 못 이긴다** (+0.051, p=0.31 → FAIL). 3 baseline 전승에 못 미침 = harness가 안 선다 |
| **negative control** | 모든 method 포화, ③ 우위 없음 = 올바르게 null (계기는 건전) |
| **real** smoke | ③ beaten 0/3, panmictic이 역으로 ③을 웃돈다 |

제I단의 corridor에서는 ③이 RR을 배제할 수 있었는데, **왜 kernel 공간에서는 못 하는가?** 근본 원인은 하나.

> **RR은 restart 때마다 kernel_id ∈ [0,4) 를 직접 샘플링할 수 있다.** kernel 선택은 4 이산의 단일 좌표 (**저차원**) 이므로, RR은 restart로 전체 4 kernel을 직격한다. 「best kernel을 찾는」 데 골짜기를 건널 필요가 없다 = **직접 워프**. 그래서 ③의 behavioral niching에 출번이 오지 않는다.

제I단에서 ③이 RR을 배제할 수 있었던 것은, 거기의 behavior가 `mean(24차원)` 이고, 평균이 0.5에 집중 → 대역 피크가 measure-zero 영역 = **직접 샘플링 불가능한 고차원**이었기 때문. kernel_id는 반대로 저차원으로 직접 샘플링할 수 있어 버린다.

**(3) red-team — 적대 검증으로도 반증할 수 없고, 오히려 확증**: instrumented RR이 positive control 위에서 4 basin에 restart kernel을 [12,18,16,18] 로 거의 균일 분산, target 도달 88%. 4개의 faithful 구성 (고차원 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 모두에서 ③은 RR에 못 이긴다. corridor를 조이면 ③이 **먼저 starve (아사)** 한다 (D=3: ③ reach 0.08 vs RR 0.42). **「RR만 배제하고 ③이 통과하는 behavior 차원은, kernel 공간에 구조적으로 존재하지 않는다」**를 정량 확증.

**verdict**: 형식상은 N/A (positive control이 validate하지 않음) 지만, 실질은 **결정적인 구조적 negative**. harness는 건전 (negative control을 올바르게 null로 하고, GA/random을 검출한다) 한데, 기질이 ③의 속임수 지형을 **애초에 호스트할 수 없다**. 제I단에서 남은 질문 「kernel 다양화로 탐색 공간을 확장하면 ③이 unlock하는가?」에 대한 답은 **NO (CPU에서는 구조적으로)**.

**honest 유보 (중요)**: 이것은 **「③ 불필요로 판명」이 아닙니다**. 「③이 저차원 kernel 공간에서는 강 baseline과 원리적으로 분리할 수 없다」 = **정보량이 있는 N/A**. ③의 메커니즘 자체는 제I단에서 진짜로 확정 완료. substrate는 약하다 (실질 3 kernel, hopfield는 대각 mock). 더 강한 kernel 구현이라면 다른 결론의 여지는 이론상 있지만, **구조적 장벽 (저차원 선택 → RR 직접 샘플) 은 kernel 구현의 질과 독립**입니다.

---

### 8. 구조적 통찰 — 6단을 하나의 조건으로 정리한다

존재 증명 (I) 과 4개의 negative (II~V) 는, 단 하나의 조건으로 전부 이어집니다.

> **③ (behavioral niching) 이 강 baseline을 웃도는 것은, 「난소」가 고차원 behavior 공간에 있어, 직접 샘플링 (랜덤 리스타트) 으로 도달할 수 없을 때뿐.**

- **제I단이 충족하는 이유**: behavior = `mean(24차원)`. 평균은 중심극한정리로 0.5에 집중하고, 대역 피크 (mean≈0.9) 는 실질 measure-zero. random도 restart도 **직접 닿지 않는다**. 그래서 징검돌을 남겨 ratchet하는 ③이 필수.
- **실제 CPU 기질이 충족하지 않는 이유**: 난소가 저차원. ESN 텍스트 proxy의 제어 좌표는 실질 leak rate (매끄러운 저차원 노브, 애초에 골짜기가 없다). kernel union의 난소는 「어느 kernel인가」 = 4지선다의 단일 이산. RR이 직접 샘플링해 전 basin에 teleport하므로, 건너야 할 골짜기가 없다.

그래서 제II단의 「유전자 공간의 다봉성 1.000」은 충분조건이 아니다 ── 유전자는 골짜기투성이라도, 난소가 저차원 behavior 좌표에 집중해 있으면, restart가 직접 닿는다. **효과가 있는 것은 "탐색이 도달해야 할 behavior의 차원"이지, 유전자의 차원이 아니다.**

---

### 9. 생물학적 접지 — 100년 전의 진화생물학이, 같은 답을 내놓고 있었다

여기서부터가 #34의 볼거리입니다. **「다양성을 유지하는 선택은, 좁은 조건에서만 효과가 있고, 그 외에서는 잉여」** ── 이 경계 조건에는, 20세기의 진화생물학에 이상하리만치 깔끔한 선례가 있습니다.

> ⚠ **honesty 계약**: 이하의 생물학은 **「비유 (structural analogy)」 이지, 우리 계산 결과의 증명이 아닙니다**. 대응은 구조적이고, 메커니즘 레벨에서는 일치하지 않습니다. 비유가 어긋나는 곳은 전부 그 자리에서 명기합니다. 인용하는 논문은, 별도로 1차 정보로 존재・귀속・주장 내용을 대조한 것만입니다.

#### 9.1 라이트 (Wright) 의 시프팅 밸런스 설 = ③의 선례

슈얼 라이트 (Sewall Wright, 1931/1932) 는 이렇게 생각했습니다. 큰 「하나의 무리 (panmictic population)」 인 채로는, 보통의 자연선택으로는 **눈앞의 국소 피크에 붙잡힌다**. 더 높은 산으로 가려면 한 번 mean fitness를 **낮춰 골짜기를 건널** 필요가 있는데, 결정론적인 선택은 그것을 거부하기 때문.

라이트의 해결책은 **무리를 다수의 반(半)격리된 서브 집단 (deme) 으로 나누는** 것.

- **Phase I**: 작은 deme가 **유전적 부동 (drift)** 으로 우연히, 골짜기를 내려가 건넌다.
- **Phase II**: 거기서 deme 내의 보통의 선택이 새로운 (더 높은) 피크를 오른다.
- **Phase III**: 높은 피크에 오른 deme가 많은 이주자를 내보내, 우수한 유전자 조합이 종 전체에 퍼진다.

메타 집단 **전체**로서, 단일 수렴 집단으로는 건널 수 없는 골짜기를 건넌다 ── 이것이 「속임수 지형의 골짜기를 징검돌로 건넌다」의 생물학판입니다.

**③ / MAP-Elites로의 대응 (= 비유, 귀속이 아님)**: archive의 각 셀 = 준격리 deme, 셀 내의 국소 elitism = deme 내 선택 (Phase II), 셀 간 변이 = interdeme 확산 (Phase III), 그리고 **archive 전체** (≒ 메타 집단, 단일 셀이 아님) 가 골짜기를 건넌다.

> **honesty 주의 (2점)**:
> 1. **이것은 해설자의 틀이지, 라이트의 주장도 MAP-Elites의 출처도 아니다.** MAP-Elites의 원논문 (Mouret & Clune 2015) 도 QD 문헌도 **라이트나 「시프팅 밸런스」를 인용하지 않는다**. 라이트는 우리의 **착상 / 비유**로서 드는 것이지, MAP-Elites의 계보로서가 아니다.
> 2. **메커니즘은 구조적으로 닮았을 뿐 동일하지 않다.** MAP-Elites의 골짜기 건너기는 **변이 오퍼레이터**가 자식을 새 셀에 두는 것으로 일어나며, **유전적 부동이 아니다**. archive는 복제하는 셀의 집단도 아니다.

#### 9.2 라이트 대 피셔 = 차원 (지형의 형태) 의 축

라이트와 동시대의 피셔 (R. A. Fisher, 1930) 는 반대를 주장: **큰 panmictic 집단 + 가법적 분산에의 매스 선택으로 충분**히 적응은 진행된다, 굳이 분할은 필요 없다, 고.

두 사람의 **가장 깊은 대립축은, 실은 「에피스타시스 (유전자 간 상호작용) 와 지형의 형태」** 였습니다. 라이트는 「비가법적 상호작용 때문에 지형은 **울퉁불퉁 다봉**, 그래서 골짜기를 건너는 drift가 필요」 라고 가정하고, 피셔는 「상호작용은 있지만 중요하지 않다, 지형은 거의 **단봉으로 매끄럽게 오를 수 있다**, 그래서 매스 선택으로 충분」 이라고 판단했다.

**이 epistasis/ruggedness의 축이, 바로 우리 결과가 살아 있는 차원입니다. 지형의 형태 (topology) 야말로 전 문제.** 지형이 정말로 울퉁불퉁 고차원이라면 (라이트 regime) 다양성이 골짜기를 건네주고, 매끄럽거나 난소가 저차원이라면 (피셔 regime) 매스 선택 ── 즉 **강한 랜덤 리스타트 산오르기의 생물학판** ── 으로 이미 충분. 우리의 ESN 텍스트 proxy는 noise-free로 매끄럽고, kernel union의 난소는 저차원 이산. **둘 다 피셔 regime**으로, ③은 효과가 없고 없었다.

> 세세한 주의 (정직하게): 「피셔는 drift를 무시했다」는 속설의 압축입니다. 정확히는 「drift는 있다고 인정했지만, 큰 집단에서는 양적으로 무시할 수 있다고 판단했다」. 완전 부정은 아니다.

#### 9.3 우리의 negative = 코인 비판의 계산판

가장 효과적인 대응은, 라이트의 **제안**이 아니라, 생물학계의 **경험적 판정** 쪽입니다. Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) 는 시프팅 밸런스 설을 이론・실증 양면에서 평가하고, 이렇게 결론지었습니다 (전문 대조 완료).

- **매스 선택으로 대개 충분.** 「라이트의 3단계 메커니즘이 단순한 매스 선택보다 더 잘 설명하는 실례는 거의 없다」. 인위 선택 실험도 「분할 집단의 선택이 대집단의 매스 선택보다 큰 응답을 낳는다」는 것을 보이지 못했다.
- **시프팅 밸런스가 효과를 내는 것은 한정적・희소한 조건 하에서만.** 집단 구조의 경험적 추정에서는 「**얕은 골짜기로 격리된 피크 사이에서만 drift는 이동을 일으킬 수 있다**」(깊은 골짜기는 drift로는 드물게만 건널 수 있다), 게다가 **대부분의 적응은 골짜기 건너기를 필요로 하지 않는다**.

이것은 우리 결과의 **놀랄 만큼 정확한 생물학판**입니다. 그들의 말을 우리의 어휘로 번역하면 ── **지형이 진정으로 기만적/고차원이 아니라면, 보통의 매스 선택 (≒ 강한 랜덤 리스타트 산오르기) 으로 이미 풀리고, 다양성 유지 장치는 거의 아무것도 사지 못한다.**「현실의 골짜기는 대개 얕다, 대부분의 적응은 골짜기 건너기 불필요」는, 우리의 「**실제 지형은 대개 단순하므로 niching은 잉여**」의 생물학적 언명입니다.

> **honesty 주의 (3점)**:
> 1. **그들은 시프팅 밸런스를 「반증」하지 않았다.** Phase I/II는 일어날 수 있다고 명언하고, 6건의 경험 사례도 들고 있다. 주장은 **더 좁은 확률적인 것** (「일반적・중요한 메커니즘이라 하기 어렵다」) 이지, 「refuted」 라고 쓰면 과언.
> 2. **논쟁은 아직 결착되지 않았다.** Wade & Goodnight (1998), Peck et al. (1998, 제목이 문자 그대로 「feasible」 이라 주장) 이 반론하고, Coyne 등의 2000년 재반론, Goodnight & Wade의 같은 호 반론으로 이어졌다. 1997 비판을 「최종 결론」으로 인용해서는 안 된다.
> 3. **생물에는 계산 측에 대응물이 없는 메커니즘이 있고, 게다가 우리보다 강한 주장을 하고 있다.** Phase III에서는, 다양성을 지키는 gene-flow 장벽이 **좋은 해를 주변 deme에 가둬 퍼짐을 방해한다** = niching이 **역효과**가 될 수 있다. 우리의 stateless한 이산 선택 설정에는 이 cost의 대응물이 없으므로, 여기는 **과도하게 겹치지 않는다**. 생물 쪽이 한 단계 강한 주장을 하는 곳입니다.

#### 9.4 두 실례 — 저차원의 나방, 그리고 고차원의 대장균

우리의 주장에는 2개의 극 (저차원 = ③ 불필요 / 고차원 = ③이 효과를 낼 수 있다) 이 있지만, 진화생물학은 각각에 깔끔한 실례를 갖고 있습니다.

**저차원의 극 ── 회색가지나방의 공업 흑화 (= BG9 kernel 케이스)**: *Biston betularia* 의 carbonaria (검정) vs typica (흰색) 는 **단일 멘델 좌위・소수 대립유전자** (원인 변이는 cortex 유전자로의 전이인자 삽입; van't Hof et al. 2011/2016) 로, **강한 방향성 선택** (s ≈ 0.1-0.2; Saccheri et al. 2008; 포식은 Cook, Grant, Saccheri & Mallet 2012에서 재확인) 을 받는다. 최적은 각 시점에서 단봉, 환경으로 시프트할 뿐. **단순한 방향성 선택 ── greedy 산오르기/랜덤 리스타트의 생물학판 ── 이 직접, 적자형(適者型) 을 고정하고, 다양성 유지 메커니즘은 필요 없고 불려지지도 않는다.** 이것이 바로 BG9: kernel 선택은 4지선다의 저차원 단일 좌표이고, RR이 전 kernel을 직접 샘플링하며, ③이 구조적으로 분리할 수 없다. **흑화형 = BG9 kernel 케이스의 생물판.**

> 주의 (정직하게): 이행기에는 다형(多型) 이 일시적으로 유지되지만, 그것은 **공간적 환경 불균일 + 유전자 흐름 (이주-선택 평형)** 에 의한 것이지, 내재적인 다양성 보존 메커니즘이 아니다. 비유가 조금 어긋나는 곳.

**고차원・역사 의존의 극 ── 렌스키의 Cit+ (= ③ regime)**: 대장균 장기 진화 실험 (LTEE) 에서, 호기적 시트르산 이용 (Cit+) 은 **12 집단 중 정확히 1개**에서 약 31,500세대째에 진화했다 (Blount, Borland & Lenski 2008). 열쇠는 순서를 갖춘 **potentiation (전구 변이의 축적) → actualization (citT의 탠덤 중복에 의한 프로모터 포획) → refinement** 라는 고차원・역사 의존의 경로 (Blount et al. 2012). 리플레이 실험이 「역사적 우발성」을 「일정률의 희귀 변이」에서 구별했다. 이것은 contingency・에피스타시스・고차원 울퉁불퉁 지형을 탐색하는 가치를 **진짜로 예시**한다 ── ③이 효과를 낼 수 있는 regime의 실례입니다.

> **honesty 주의 (이것은 우리 조건문의 "전건"에만 대응한다)**:
> - **LTEE는 niching 알고리즘을 쓰지 않는다.** 그냥 자연선택이고, 12 병렬 집단은 **그 자체가 랜덤 리스타트적인 설계**. 그래서 「contingency + 다양성이 희귀한 혁신을 가능케 한다」는 존재 증명이지, 「niching이 강한 restart baseline에 이긴다」는 증거가 **아니다**.
> - 「대장균이 제로에서 시트르산을 먹는 능력을 획득」은 속설의 과장. 혁신은 **제어 (기존 트랜스포터의 호기 발현) = exaptation** 이지, 신규 유전자도 신규 생화학도 아니다.
> - Van Hofwegen et al. (2016) 이 「직접 선택이라면 Cit+가 훨씬 빨리 나온다」고 보이고, 「희귀/우발」 틀에 이의를 제기했다 (렌스키 측은 LTEE 조건 하의 potentiation과는 모순되지 않는다고 반론). 「극히 희귀/장기 지연」 이야기에 기대려면, 이 **계쟁 중인 추시(追試)** 도 병기해야 한다.

#### 9.5 접지의 정리

| 극 | 생물학 | 지형 | ③은 효과? | 우리의 기질 |
|---|---|---|---|---|
| 저차원/매끄러움 | 흑화형 (단일 좌위, s≈0.1-0.2, 방향성) | 단봉・시프트 | **No** — 매스 선택으로 충분 | BG9 kernel union; ESN/ridge 텍스트 proxy (결정론・매끄러움) |
| 고차원/우발 | 렌스키 Cit+ (potentiation→actualization→refinement) | 울퉁불퉁・변이로 골짜기 넘기 | **Yes** (효과를 낼 수 있는 regime) | 합성 속임수 corridor (behavior = 24차원의 평균) |
| 경험적 판정 | 코인・바턴・투렐리: 매스 선택으로 대개 충분, 시프팅 밸런스는 드물게만 결정적 | 실제 지형은 대개 단순 | 우리의 **negative의 거울** | 시험한 모든 CPU 기질 |

**결론**: 라이트의 시프팅 밸런스는 「③이 효과를 낼 때 **왜** 효과를 내는가」의 올바른 생물학 선례, 라이트-피셔의 epistasis/ruggedness 축은 「**차원** 조건」의 올바른 틀, 흑화 나방과 렌스키 Cit+는 저차원/고차원의 깔끔한 양극, 코인 비판은 우리의 **negative**의 생물학 선례. **다만, 이것들은 계산 결과를 증명하지 않는다. 접지할 뿐.** 비유가 가장 느슨해지는 것은, 생물이 cost (Phase III의 gene-flow trap) 를 더하는 점 ── 우리의 stateless 설정에는 그것이 없다.

— 한 모금. 100년 전의 논쟁이 같은 형태라고 깨달았을 때는, 솔직히 소름이 돋았습니다. 다만 「소름이 돋았다」를 「증명」으로 헷갈리지 않는 것이 이번의 규율입니다. —

---

### 10. GPU로의 함의 — 남은 길은 고차원뿐, 그러나 여전히 bet

arc는 CPU의 길을 전부 막았습니다. 실제 proxy는 noise-free로 매끄럽고 (IV), 마지막 후보 (kernel 다양화) 는 구조적으로 막혔다 (V). ③의 남은 길은 **고차원의 지형뿐** ── 그것을 제공하는 것이 **full-LLM의 파라미터/손실 공간 (수백만 차원)** 입니다.

구조적 통찰은 GPU의 도박을 **better-motivated** 하게 만듭니다. 「full-LLM만이 예외일지도」 라는 맹목적인 도박이 아니라, 「**③은 고차원을 요하고, full-LLM이 고차원역**」 이라는 원리에 따른 도박이 된다.

**다만 여전히 bet.** 생물학의 Cit+가 「③ 알고리즘의 승리」를 증명하지 않는 것과 같은 이유, 그리고 BG9에서 RR에 못 이긴 것과 동형의 이유로 ── **실제 LLM 지형이 backprop (경사 하강) 이라는 강 baseline으로 직접 내비게이트할 수 있다면, ③은 역시 불필요**. 난소가 고차원인 것은 **필요조건이지 충분조건이 아니다**. 「강한 직접법이 풀 수 없다」는 것을 추가로 보일 필요가 있다 (CPU에서는 RR, GPU에서는 경사 하강).

그래서 GPU는 「③을 위해 단독」이 아니라 **포트폴리오 판단** (llive의 실제 LLM fitness 등과 합승) + **클라우드 임차로 사전 등록 1건** (자본 커밋 전) 이 적정. go/no-go 기준도 falsifiable하게 쓸 수 있습니다:

> **full-LLM의 난소는 behavior에서 고차원인가, 또한 강한 직접 baseline (경사 하강) 으로 도달 곤란한가?** 고차원이라도 경사가 직접 닿는다면 ③ 불필요 (= BG9의 RR 결과의 GPU판).

---

### 11. 메타 교훈 — 정직함은, 이기기 위한 도구였다

이 arc의 진정한 성과는 수치가 아니라, **「너무 정돈된 결과를 의심하는」 정신이 실제로 연구를 앞으로 진전시켰다**는 것입니다.

- **존재 증명 (I)** 에서 이겼을 때, 골짜기를 없앤 경계 실험으로 「③은 만능이 아니다」를 스스로 확인했다 (승리를 과대평가하지 않는다).
- **일반화 (III)** 에서 페어 리뷰가 3개의 rerun 블로커를 들이댔지만, 고쳐도 결론은 바뀌지 않았다 (취약한 negative가 아님을 확인).
- **결정론 측정 (IV)** 에서 평가 노이즈를 물리적으로 지웠기에, 「매끄러움」이 지형의 성질인지 계기의 한계인지를 가려낼 수 있었다.
- **BG9 (V)** 에서는 적대 검증으로 자신의 「③이 안 선다」를 **반증하려 해서 반증할 수 없었고**, 구조로서 확증되었다 (negative를 올바르게 negative로 확정하는 방향으로도 같은 규율이 효과를 발휘했다).

게다가 arc 전체에서 하나 배운 것은 ── **저차원의 난소는 강 baseline이 직접 풀어 버린다. 그래서 ③ (가려내어 길러 내는 공정) 이 효과를 내려면 "고차원 behavior 공간"이 필요하다.**「속임수 지형을 만들면 ③이 선다」는 절반만 옳고, 정확히는 「**직접 샘플링할 수 없을 만큼 고차원인** 속임수 지형」이 아니면 ③은 서지 않는다. 그리고 놀랍게도, 이 경계 조건은 **라이트의 시프팅 밸런스와 코인 비판이 100년 가까이 전에 도달해 있던** 것이었습니다.

「이상하게 좋은 결과가 나오면, 이긴 기분이 되기 전에 반드시 내역을 의심하라」── FullSense의 연구 규율 (`honest disclosure`) 은, 단순한 자계(自戒) 가 아니라, **실제로 거짓 양성을 잡고, negative를 올바르게 확정하며, 연구의 정밀도를 높이는 메커니즘**으로서 6단 전부에서 돌고 있었습니다.

결론을, 마지막에 다시 한 번, 정확하게.

> **③이 살아나는 것은 「고차원의」 속임수 지형일 때뿐.** 존재 증명 (합성 corridor) 에서는 압승했지만, 실제 CPU 기질은 ── 기억 과제 (바닥/천장) 도, 다중 과제 일반화 (매끄러움) 도, 실제 proxy 텍스트 지형 (noise-free로 매끄러움) 도, kernel 다양화 (저차원・구조적으로 막힘) 도 ── 어느 것도 그 조건을 충족하지 않았다. **「③ 결착 = ③은 불필요로 판명」이 아니라**, 「③이 살아나는 조건 (고차원의 속임수 지형) 을, 지금 CPU에서 측정할 수 있었던 실물 모형은 충족하지 않았다」. 본진 (GPU 고차원) 은 아직 앞이고, 게다가 「강한 직접 baseline이 푼다」는 리스크를 안은 도박입니다. 그리고 이 결론의 골격은, 20세기의 진화생물학이 이미 그리고 있었습니다 ── 다만 생물학은 그것을 **증명하는 것이 아니라, 접지할 뿐**입니다.

---

**Tags**: 진화계산 / MAP-Elites / 통계검정 / honest disclosure / 진화생물학 / CPU 연구
**관련**: 연재 #33 (제3축 ③ 결착 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (반증・Goodhart・proxy 한계)
**Project**: llcore (PyPI 예약 llmesh-llcore, 리포지토리 미공개이므로 로컬 연구)


<!-- REFERRAL -->

---

> ### ⚡ 이 연재는 Claude Code 와 이인삼각으로 쓰고 있습니다
>
> 기사 속의 구현・검증・가시화는 **Claude Code**(Anthropic 의 AI 코딩 환경)와 함께 진행하고 있습니다.
> Claude Code 는 **1 주일 무료 트라이얼**로 시험할 수 있습니다. 마음에 들어 유료 플랜에 등록하실 때,
> 아래 소개 링크를 경유하면 필자에게 「개발을 계속하기 위한 크레딧」이 들어와, 이 연재의 지속을 뒷받침할 수 있습니다.
>
> 👉 **무료로 시험하기 / 소개 링크** → https://claude.ai/referral/0sqPw8E_lw
>
> <sub>EN: This series is built together with **Claude Code** — try it with a **1-week free trial**. If you subscribe via the link, the author receives credits to keep building. /
> 中文: 本系列与 **Claude Code** 协作完成,可享 **1 周免费试用**;通过链接注册可让作者获得继续开发的额度。 /
> 한국어: 이 시리즈는 **Claude Code**와 함께 작성합니다 — **1주 무료 체험** 제공. 링크로 가입하면 저자가 개발 지속용 크레딧을 받습니다.</sub>

<!-- /REFERRAL -->

<!-- CTAIMG -->

![「깬다」며 만 엔 지폐를 내미는 모리타](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/012.jpg)
> 🗒️ *「깬다」— 소개 링크로 푼돈을 벌어 보려는 속셈, 스스로도 좀 깬다*（© Forbidden shibukawa / SHUEISHA・『스낵 바스에(Snack Basue)』）

<!-- /CTAIMG -->
