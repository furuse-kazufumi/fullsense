---
title: >-
  #43 In 2026, the Industry Named the AI's "Reins" and "Wheel" — How I Started
  Assembling a Prototype harness/loop engineering Stack Locally
tags:
  - AI
  - Agent
  - LLM
  - ClaudeCode
private: true
updated_at: '2026-06-16T06:48:26+09:00'
id: 2622da17495d61480fa2
organization_url_name: null
slide: false
ignorePublish: true
---
# #43 In 2026, the Industry Named the AI's "Reins" and "Wheel" — How I Started Assembling a Prototype harness/loop engineering Stack Locally

## Introduction: Starting with the Story of a Number I Decided to Stop Using

While preparing to write this article, I ran into a number I was dying to use.

> "A certain 2026 paper showed up to a 10x performance improvement by changing only the 'surrounding apparatus' while keeping the AI model fixed."

It's a perfect hook. In one stroke, it demonstrates the power of the "harness (apparatus)" I'm about to discuss. But when I went to the primary source, that number turned out to have **no basis**. The paper genuinely exists, yet neither the cited author's name nor the "10x" figure **appeared anywhere** in it. So I **threw that number away**.

Why begin with such a negative story? Because this very discipline of "throwing it away" is the single most important thing I want to convey in this article.

> **When you see an unusually catchy number, doubt the breakdown before you let yourself feel victorious. Drop anchor in the primary source.**

A smart AI will fluently hold forth even on things it doesn't know. Ask it sloppily, and precisely because it's smart, it will fill in the gaps on its own and sprint at full speed toward somewhere misaligned with your intent. That's exactly why the human side needs an eye that draws the line: "this part is unverified." This article is the story of a human equipped with that eye, examining 2026's "next name" for AI engineering with both feet on the ground.

(The detailed verification of the number I discarded is fully disclosed in a standalone section after Chapter 2. I wanted to promise the discipline first, so I placed only the conclusion at the very top.)

---

## Chapter 0: A Map of Terminology — The Staircase from prompt to loop

Before getting to the main topic, let me unfold a map.

In 2025, the AI industry's watchword was **prompt engineering** — the craft of "how to ask the LLM." That eventually expanded into **context engineering** — the craft of designing "what you keep in the LLM's view."

And in 2026, the industry coined two more names.

- **harness engineering** … the craft of designing the "deterministic runtime layer" that wraps the LLM.
- **loop engineering** … the craft of designing an agent as an "autonomously circulating loop."

Let me note upfront that **these were invented not by the AI, but by humans (the industry)**. The anthropomorphism that tempts you to write "the AI invented it" in the title distorts the facts. The ones who named them are the human engineers I'm about to introduce.

The concept of this article is this:

> **I keep both of these industry-named things on hand (locally) at the proof-of-concept level. But my blueprint has one more axis that rarely appears in the industry's model-centric explanatory diagrams.**

That axis is **the human who keeps holding the reins** and **the AI that can be raised like a subordinate**. In this article, I examine three themes — (A) the harness, (B) the loop, and (C) the knowledge foundation that supports them — through implementations I actually run: `RAPTOR` (a security agent), `llloop` (my homemade loop harness, alpha), and the `RAD` corpus + `LLM Wiki` (my own research knowledge).

This is a long article (about 20,000 Japanese characters, a 20-minute read). At key points I insert **plain-language explanations** (gentle definitions of terms), **interludes** (palate cleansers), and **honest disclosure** (frank breakdowns of the internals). If you get tired, take a breath at a chapter break.

### The Flow of prompt → context → harness → loop

The "maturity" of AI engineering is, as of 2026, generally described along the following staircase.

1. **prompt engineering** … polishing a single instruction.
2. **context engineering** … designing what to load into the LLM's field of view (the context window).
3. **harness engineering** … designing the LLM's "outer apparatus": the layer responsible for tool invocation, permissions, execution, and feeding results back.
4. **loop engineering** … designing that apparatus as an "autonomously circulating loop."

One explanatory outlet calls this the "fourth paradigm," and LangChain (an agent-development library) summarizes it as **`Agent = Model + Harness`** (confirmed via augmentcode.com's commentary — a **secondary source**. I did not obtain LangChain's primary original text for this article, so I hedge it. Each time I restate this formula below, I'll mark it "secondary" too).

### Plain Language: What Is a "harness"?

**harness** originally refers in English to "tackle for a horse" or "a safety belt (the kind that safely tethers a baby or a rock climber)."

An LLM is enormously smart, but left alone it tends to thrash about, bolt in some unintended direction, and occasionally step out where there's no ground — like a powerful horse. Putting a **harness** on that horse — deciding firmly, on the harness side, where it can go, which tools it can use, and how it brings results back — is harness engineering.

The horse-tackle analogy is convenient, but I'll also say **where it breaks**. A real harness only "physically restrains movement," whereas an LLM harness not only "restrains" but also plays the role of "**reshaping the result and feeding it back in front of the horse's eyes**." Think of it as a harness that also has a function to show the horse the scenery and say, "look over here next." Once you include that, the analogy gets a bit cramped.

### Plain Language: How Do automation and loop Differ?

This is the heart of loop engineering. In the title I translated "loop" as "wheel" (rin), which comes from the image of "a wheel that keeps going around and around through the same steps." But it isn't just any wheel. One guide from June 2026 defines the difference crisply.

> "**Automation executes a sequence of steps. A loop has decision-making inside it. The agent is actively judging whether it has reached the goal.**"
> (Data Science Dojo, *Agentic Loops Explained: From ReAct to Loop Engineering (2026 Guide)*, 2026-06-09 / [link](https://datasciencedojo.com/blog/agentic-loops-explained-from-react-to-loop-engineering-2026-guide/))

In plain terms —

- **automation (a recipe)**: "crack the egg → mix → bake." The steps are fixed. Even if midway you notice "oh, the egg is rotten," the recipe itself doesn't stop.
- **loop**: at every cycle, it proceeds while **checking for itself** "where are things now?" "have I reached the goal?" "is this dangerous?" If it notices a rotten egg, it can decide on the spot, "abort this."

Here I want to defuse one logical trap upfront. **"A loop has decision points" and "a loop is safe" are two different things.** The reason automation can't stop for a rotten egg isn't so much the essence of automation as the poverty of a design that "placed no decision point." Conversely, even a loop will cause the same accident if its decision logic is full of holes. Having decision *points* and guaranteeing the *quality* of those decisions are separate problems, and the latter is handled by the **safety layer** that appears later. This distinction pays off several times throughout this article.

The same guide depicts the inside of an agent loop as a repetition of five stages — **Perceive → Reason → Plan → Act → Observe** — and holds that for a loop to be established, two things are required: a **trigger** and a **verifiable goal**.

Keep the phrase "verifiable goal" in mind. Later it pays off directly in Claude Code's `/goal` command and in the safety layer of my homemade harness.

### This Chapter's honest disclosure

The sources around loop engineering (Data Science Dojo, Medium articles, various blogs) are **practitioner blogs, not peer-reviewed papers**. Since the definitions (automation vs loop, P-R-P-A-O) are consistent across multiple sources, I treat them as "terminology that circulated in practice in 2026." I maintain the sense that this is not an "authoritative academic definition."

---

## Chapter 1 [Reins = harness] The Industry Definition, RAPTOR as the Real Thing, and "One More Axis"

### 1-1. Who Named harness engineering, and When (Confirmed via Primary Sources)

The timeline matters here, so I went to the primary sources.

**Mitchell Hashimoto** (co-founder of HashiCorp, co-developer of Terraform) presents this term in his February 5, 2026 blog post *My AI Adoption Journey*. What matters is his own phrasing.

> "**I don't know if there's a widely accepted term for this field, but I've come to call it harness engineering.**"
> ([mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey), 2026-02-05, text confirmed directly)

In other words, Hashimoto does not say "I invented it." He hedges carefully: "I don't know if there's a widely accepted term, but this is what I call it." So this article, too, treats it merely as "a designation that began to acquire a name in the industry around February 2026."

The core principle of harness engineering he expounds is as concrete as a craftsman's technique.

> "**Whenever you catch the agent making a mistake, take the time, each and every time, to engineer a solution so that the agent never makes that mistake again.**"
> (same post, original text confirmed)

Subsequently, on February 11, 2026, **OpenAI** published a piece by Ryan Lopopolo, said to formalize harness engineering based on the experience of "shipping a production app with zero lines of hand-written code." The tagline is **"Humans steer. Agents execute."**

That said — let me be honest here. When I accessed OpenAI's official article (openai.com/index/harness-engineering/) while writing this, I **got HTTP 403 and could not retrieve the text directly**. So the date, author, tagline, the "zero lines" claim, and the phrase "Humans steer. Agents execute." are all **based on secondary sources (the agreement of augmentcode / latent.space / zenml)**. Every place where I restate this tagline in this article, I'll mark it "(secondary)." As for the experiment-scale figures like "1 million lines / 1,500 PRs / 1 billion tokens per day," these are secondary-only and unconfirmed against the primary, so I won't use them as material for my argument; I'll mention them here only as "**reported to be**."

### 1-2. To Avoid Conflation with Karpathy's "vibe coding"

Let me sort out the timeline. There's the term **"vibe coding"** that **Andrej Karpathy** (OpenAI co-founder, former AI lead at Tesla) popularized in a tweet on February 2, 2025 ([original tweet](https://x.com/karpathy/status/1886192184808149383), URL and date confirmed). It's the style of "**handing things to the AI and coding by vibe.**"

This **predates** harness engineering (which became industry jargon around February 2026). The two are concepts of a different lineage. My own phrasing appears later, and I carefully distinguish its relationship to "vibe coding" throughout this article (the reason is in 1-4).

### 1-3. RAPTOR — Here Is the "Real Thing" of a harness

Enough abstraction. Let me show you the real thing.

I run a security research framework called **RAPTOR** locally. It's a fork of **gadievron/raptor** (MIT license; authors Gadi Evron, Daniel Cuthbert, Thomas Dullien [a.k.a. Halvar Flake], Michael Bargury, and John Cartwright) ([upstream repository](https://github.com/gadievron/raptor), author names confirmed in LICENSE and README L23-24).

RAPTOR's full name is **Recursive Autonomous Penetration Testing and Observation Robot**. It's an autonomous security research framework that chains into one workflow: analysis via **Semgrep** (a pattern-matching static analysis tool) and **CodeQL** (a dataflow-type static analysis tool that turns code into a database and queries it), binary analysis, LLM-based vulnerability verification, exploit generation, and patch generation.

And here is where it **maps onto the definition of harness engineering quite naturally when you overlay it afterward**. Let me note upfront: RAPTOR's two-layer structure was not written by its designers with the industry term "harness engineering" in mind. This is an interpretation I overlaid after the fact (observer effect included). Even so, the correspondence is surprisingly natural. RAPTOR's README explicitly states that it is a "two-layer architecture."

> "**RAPTOR is two layers.**"
>
> The **Python execution layer** (`raptor.py`, `packages/`, `core/`, `engine/`) handles the heavy lifting. It runs Semgrep and CodeQL, manages subprocesses, parses **SARIF** (a standard JSON format representing static analysis results), deduplicates findings, orchestrates LLM API calls, tracks costs, and writes output files. "**It does not make decisions. It executes.**"
>
> The **Claude Code decision layer** (`.claude/`, `tiers/`, `CLAUDE.md`) does the judging: which findings to prioritize, how to interpret results, what the attack scenarios are, whether that exploit is realistic. It "**makes the calls.**"
>
> ([upstream README "Architecture" section](https://github.com/gadievron/raptor), L236-250, text confirmed)

Overlaying this onto the industry definition of harness engineering, the correspondence is: **the harness (= the Python execution layer) handles schema validation, permissions, execution, and result injection, while the LLM (= the Claude Code decision layer) concentrates on judgment.**

The repository's `CLAUDE.md` stipulates the design principle even more succinctly.

> "**Python orchestrates everything.**"
> "**Never circumvent Python execution flow.**"

On top of this, it enforces discipline that **errs on the side of safety**: "Don't leak the location of the remote OLLAMA server," "Don't add anything other than `RAPTOR_DIR` to `sys.path` (if it's unset, halt immediately with KeyError = fail-fast, no fallback)," and so on.

#### Plain Language: What Is fail-closed?

**fail-closed** is the design policy of "**when in doubt, don't let it through.**" The antonym is fail-open (when in doubt, let it through).

Take a ticket gate, for example, when it breaks.
- **fail-open**: when it breaks, it stays open (people can pass, but so can the fraudulent).
- **fail-closed**: when it breaks, it stays shut (no one can pass, but neither can the fraudulent).

Let me also add where this analogy breaks. With a ticket gate, the inconvenience to "the people who can't pass" is temporary, but an AI agent's fail-closed carries the cost of "**being safe, yet sometimes stopping even legitimate operations.**" Who strikes that balance? The "human confirmation (CONFIRM)" described later serves as the buffer.

In the security world, the principle is fail-closed. RAPTOR implements this in several places.

1. **When scanning untrusted repositories**, `RaptorConfig.get_safe_env()` strips environment variables that "the shell might evaluate," like `TERMINAL` / `EDITOR` / `VISUAL` / `BROWSER` / `PAGER`, and passes file paths not as embedded shell strings but as **list arguments** (confirmed in `get_safe_env` in `core/config.py` and the "SECURITY: UNTRUSTED REPOS" section of `CLAUDE.md`).
2. The output of each stage of `/validate` (vulnerability verification) passes through **JSON schema validation**, and if it's invalid, it halts with exit 1 (`libexec/raptor-validate-schema`).

Furthermore, RAPTOR has a **governance package**, and the `@govern` decorator is implemented in real code (`packages/governance/policy.py`). `GovernancePolicy` declaratively holds "allowed tools / forbidden tools / forbidden patterns / max calls per request / whether human approval is required," and `check_tool` returns —

- **DENY** if it hits the forbidden list
- **REVIEW** (held) if human approval is required
- **DENY** if it isn't even on the allow list (= what you don't know doesn't get through)

This is unmistakably fail-closed. When composing multiple policies, it combines them with **"most-restrictive-wins,"** and on DENY/REVIEW it throws `PermissionError` to halt execution.

### 1-4. Here Comes "One More Axis" — What I Want to Add to the Model-Centric Diagram

Up to here has been about the industry's harness engineering and its real-world instance (RAPTOR). From here, I overlay **my own axis**.

The industry definition was **"Humans steer. Agents execute." (secondary)**. I agree with this wholeheartedly. If anything, this is **already a human-centric precedent**. Both Hashimoto and OpenAI explicitly state that humans take the helm. So I do not say "the industry fails to depict the human role." That would be an exaggeration without an exhaustive survey.

To put it precisely: **the industry's explanatory articles often present a model-centric diagram of "harness = the technical apparatus surrounding the model."** The direction "the human steers" is shown, but they rarely drill down to the granularity of **what that human concretely does, and how they "raise" the AI**. What I want to add is that granularity.

> **The harness is simultaneously an "apparatus," a "place where the human keeps holding the reins," and a "place where the AI is raised like a subordinate."**

I call this, within myself, **harness-style vibe coding**. It's a phrasing that emerged when I put my own working style into words in May 2026 — **an auxiliary line for the industry term**.

Here I strictly observe one discipline. **I do not say "I named it first" or "this is a world first."** Two reasons.

1. The industry term harness engineering (around February 2026, date confirmed in Hashimoto's primary post) **predates** this phrasing of mine (May 2026).
2. In the first place, Hashimoto himself says, "I don't know if there's a widely accepted term," so it's not a situation where one can assert who was "first."

Therefore, my position in this article is: **"I have a way of calling a human-centric operating style that is clearly distinguished from Karpathy's 'vibe coding' (February 2025, hand everything to the AI)."** If "vibe coding" is "leave it to the AI and go by vibe," my style is "**actively keep holding the harness, and use the AI while raising it as a subordinate.**"

From here on, I'll stop foregrounding the coined term itself and speak in terms of **function (the human holding the reins / raising a subordinate)**.

#### The Three-Way Breakdown of harness-style vibe coding

| Element | Content |
|---|---|
| **harness** | An agent-driven development environment like Claude Code / Codex / Cursor / Aider |
| **vibe** | The user's image, intuition, and overall sense (= high-dimensional direction) |
| **coding** | The implementation work where the AI fills in the details |

The user connects these three via the harness. The "vibe" (intuition) is not something to discard; it's treated as the **most valuable input**.

#### Three Abilities the User Needs

The core of this axis is the point that "it's not enough for the human to merely watch." I believe the user side needs three abilities.

| Ability | Role | Basis in My Case |
|---|---|---|
| **Ideation** | Presenting high-dimensional direction, cross-domain association, discovering new requirements | That burst of speed where the four-way association of "Kinnikuman Planet + R.O.D + Reincarnation + ROS PBT" instantly crystallized the design for derivative-population evolution |
| **Heuristics** | Shortcutting design decisions, anticipating similar failures, cutting off unnecessary exploration | 30 years of engineering experience + precision metrology + industrial IoT + DX experience |
| **Algorithmic understanding** | Validating the soundness of the AI's implementation, estimating computational complexity, identifying hot paths, honest disclosure of benchmarks | The native wit to instantly evaluate a gap like "about 0.8x for single calls, about 12.7x for batches" |

The third one, "algorithmic understanding," is especially important. **As is often said, AIs make mistakes fluently.** To see through fluent mistakes, you need an **eye that estimates computational complexity** on your side. This is not a novel insight. What I want to say is not a restatement of generalities but an operational specific — for example, the homemade measurement of "0.8x single / 12.7x batch" from a month ago. An AI tends to report only "12x faster in batches," but to avoid overlooking the inconvenient breakdown that **it's actually slower for single calls**, you need an eye for complexity. That's the point.

#### And "AI Growth Management" — The Same "Structure" as Raising a Subordinate

This is what I most want to say on my axis. **Using an AI is astonishingly similar to raising a subordinate.** Drawing up a correspondence table gives us this.

| Raising a Subordinate | Raising an AI (the receptacle in implementation) |
|---|---|
| Share the goal | Lay out intent and constraints every session via `CLAUDE.md` / memory / requirements docs |
| Decide the scope of delegation | Make it explicit with autonomy-scope rules (max-plan-autonomy / session-marathon) |
| Check progress | Update `SESSION_SUMMARY` / `NEXT_SESSION` / git log every turn |
| Allow failure | Keep chat memos, honest disclosure, and **negative examples too, without deleting them** |
| Measure growth | Benchmarks / number of passing tests / statistics-driven |
| Respect individuality | Protect distinctive evolution via persona / thinking factors / Novelty Lane |
| Retirement / generational change | Archive old commits / old memory without deleting them |
| Build trust | Hand the user **audit rights** via Approval Bus + Ed25519 audit chain (an approval log made tamper-proof with digital signatures) |

Here's one important caveat. **This correspondence table shows that "the metaphor works well"; it is not, in itself, proof that "humans are superior to AI."** The fact that a book on managing humans can be read as-is for an AI team is a sign of the metaphor's validity, not grounds for superiority. The argument for superiority is consolidated not in this chapter but in the three points at the end of Chapter 3 (parallelism / long-range / hazard anticipation). Here I claim only that "**the structure of raising can be transferred.**"

Why does the transfer work? The reasons can be organized into four.

1. **AIs lose context quickly** → the cost of waiting for confirmation exceeds the value of pressing on even if slightly off.
2. **Redoing is cheap for AIs** → even if they err autonomously, they can correct immediately. The cost of rebuilding is low.
3. **AIs don't rest** → waiting for human confirmation is the biggest bottleneck.
4. **AIs can explain** → why they judged that way can be traced later via the audit log.

This idea, by the way, has a lineage. It's a transcription onto an **AI team**, rather than humans, of the "management that makes the most of individuality" expounded in the celebrated *First, Break All the Rules* by **Marcus Buckingham & Curt Coffman** (original 1999, a management book based on Gallup's large-scale survey in the US) (the Japanese title, publication year, and the summary of the four principles are based on values noted in my memos, so reconfirmation against the relevant passages in the original is desirable, and I hedge here). Their four principles — (1) select for talent, (2) define the right outcomes, (3) focus on strengths, (4) place people in the right roles — can, I feel, be transferred almost verbatim to "human → AI team" management.

> **A book in which a human manager leads a human team reads, almost as-is, as a book in which a human leads an AI team.**

(I also have, on hand, an arrangement that applies Canon's "Spirit of the Three Selfs (self-motivation, self-management, self-awareness)" to AI, but its source is a teaching passed down within the company and I haven't obtained primary confirmation, so in this article I'll merely name it as a footnote-level reference and set *First, Break All the Rules* as the pillar of the argument.)

#### This Chapter's honest disclosure (Compressed Version)

- Whether "harness-style vibe coding" is my own coinage is my conjecture; I haven't nailed it down with external search. That's why I don't write "I named it / world first" but stay with "this is what I call it."
- Figures like "about 0.8x → about 12.7x" are point-in-time records from about a month ago; I haven't re-verified them against the latest code. Rather than the numbers themselves, please read this as the argument that "**you need an eye that sees through this kind of inconvenient breakdown.**"

#### Anti-Patterns (What Not to Do)

Just like raising a subordinate, "raising" has forbidden moves.

- Rejecting the user's intuition with "there's no data."
- Replacing heuristics with "let's look at the prior research first."
- Escaping algorithmic discussion into abstraction.
- Treating the AI as a "tool" without raising it, making it start from zero every time.
- Breaking the balance by being too strict / too lenient.
- **Arbitrarily changing the harness itself (`CLAUDE.md` / hooks / settings).**
- Hiding progress so the user can't hold the reins (opaque progress, vague commit messages).

The last two are also imposed on the AI side as behavioral discipline. **Show completed changes with their file path and content in one line, and keep the process observable.** Keep the whole picture always visible to the human holding the reins. This is a necessary condition for a "harness whose reins can be held."

> 🗨️ "Conversations don't click with someone who differs in IQ." — [Snack Bus-e / Forbidden Shibukawa (Alu)](https://alu.jp/series/スナックバス江/crop/PJm0yAGeJy9iSa487mrX)
>
> (Interlude) The "non-clicking" of conversations between humans and AI also comes down, in the end, to this. Ask a smart AI sloppily, and precisely because it's smart, it fills in the gaps on its own and sprints at full speed toward somewhere misaligned with your intent. That's why "reins" and "loop-level judgment" are needed — after this palate cleanser, we finally move on to the story of the "wheel."

---

Chapter 1 was about the "**why**" (philosophy). I placed an auxiliary line onto the model-centric diagram: the harness is, at once, a technical apparatus and a place where the human holds the reins and raises the AI as a subordinate. The next chapter, Chapter 2, moves to the "**how**" (control).

---

## Chapter 2 [Wheel = loop] Loop Engineering and llloop, My Homemade Harness

### 2-1. loop engineering, One Level Deeper

In Chapter 0 I defined "automation is steps, loop is judgment" (the egg-and-recipe story). Pushing one step further, loop engineering can be put like this:

> **The engineering of "designing a loop, running it, and swapping out strategies to compare and improve them."**

The point is that you can "**swap out strategies and compare them.**" Rather than a single fixed loop, you swap the loop's contents (the strategy) — like `react` / `reflexion` / `plan_execute_verify` — and experiment with "which strategy converges **faster and more safely** on the same task." This is the decisive difference from automation (a fixed recipe).

#### Plain Language: The Names of the Strategies

Let me roughly translate the representative strategies that constitute the loop's "contents."

- **ReAct** … alternately repeats "Reason" and "Act."
- **Reflexion** … when it fails, it **writes a self-reflection** and applies it to the next attempt.
- **Plan-and-Execute** … first makes a plan, then executes it in order.
- **Self-Refine** … proofreads and fixes its own output by itself.

These are "schools of how to circulate thought." For the same goal, the speed of arrival and the ease of stepping off course differ by school. That's why you need a "framework for comparison."

### 2-2. loop engineering Also Has a Security Face

loop engineering isn't only about productivity. It's also a **paradigm shift in security**.

Filip Verloy issues a sharp warning in his June 2026 Medium article *From Prompt Engineering to Loop Engineering: Why the Agent Era Demands a New Security Paradigm*.

> "Unleashing autonomous loops without a native agent control layer doesn't scale productivity — it **scales risk at machine speed**."
> ([Medium article](https://medium.com/@filipv_74515/from-prompt-engineering-to-loop-engineering-why-the-agent-era-demands-a-new-security-paradigm-816385040e3d), text confirmed)

The loop is fast. Precisely because of that, if you get the way of stopping it wrong, **mistakes too get mass-produced at full speed**. His prescription is that static controls like regular expressions or ACLs aren't enough; what's needed is **Semantic Governance**, which understands and controls the meaning of an agent's actions in real time (summarized in line with the original article's claims, not a paraphrase).

This single line, "scales risk at machine speed," is the very design motivation for the homemade harness that follows.

### 2-3. llloop — My Homemade Loop Harness

I've built **llloop** (a local, independent project, v0.1.0a0, Apache-2.0), an **independent harness for designing, running, and experimenting with autonomous loops**. It's a Python project launched on June 11, 2026.

Let me place an **honest disclosure** first. **llloop is at the alpha stage (v0.1.0a0, a skeleton).** I haven't published it to GitHub yet, so I can't paste a public repository URL in the text (I supplement with links to the already-published RAPTOR side). The demonstration tasks are currently centered on the green-keeper too, not production quality. I'll write this without padding.

That said, the skeleton of the design is this.

#### The Skeleton: The MAPE-K Control Loop

llloop's backbone is **MAPE-K**. This is a classic control loop from autonomic computing, consisting of **Monitor → Analyze → Plan → Execute**, plus the **Knowledge (K)** they all share. The design code cites Kephart & Chess's 2003 autonomic computing paper.

The implementation is the `MapeKRunner` class, and one cycle closes the loop in the order —

```
Monitor → Analyze → (terminate if the goal is met) → Plan → safety judgment → Execute → record → breaker/budget judgment
```

The inner loop adopts plan-execute-verify and Reflexion, and the strategy is swappable.

##### Plain Language: MAPE-K Compared to Thermoregulation

MAPE-K resembles human thermoregulation.
- **Monitor**: the thermometer notices "it's 38°C."
- **Analyze**: judges "that's higher than normal — this is a fever."
- **Plan**: decides "let's sweat to release the heat."
- **Execute**: actually sweats.
- **Knowledge**: the baseline "normal temperature is 36.5°C" is shared across all stages.

The difference from automation (a recipe) is clear. A recipe decides "sweat when summer comes" by the calendar, but MAPE-K **measures the current temperature and decides**. This is "a loop that judges from within."

### 2-4. ★ The Star Appears: The fail-closed Safety Layer (safety.py)

This is the part of llloop I most want to talk about. The loop is fast. Fast things need **a brake that can't be bypassed**. In 2-1 I wrote that "having decision points and guaranteeing the quality of decisions are separate problems." The one in charge of "guaranteeing the quality" is this safety layer.

llloop's safety layer `safety.py`, via `SafetyPolicy.classify`, judges each action in three tiers: **ALLOW / CONFIRM (human confirmation) / FORBID**. The order of judgment is —

1. **FORBID takes top priority** … `rm -rf /`, `curl | sh` (piping content fetched over the net straight into the shell), `--no-verify` (bypassing hooks), fork bombs, and the like are unconditionally forbidden.
2. **Dangerous commands are CONFIRM** … deletion, force-push, submodule modification, and DB drop require human confirmation.
3. **Unknown kinds are also CONFIRM** … an unfamiliar action kind isn't on the allow list, so it **falls to the safe side (confirmation)**.
4. **Only the rest is ALLOW** … read / scan / test / lint / typecheck / build / commit / push are autonomously permitted.

The "**fail-closed (when in doubt, don't let it through)**" from Chapter 0 is implemented in exactly this order. "Don't make what you don't know ALLOW. Fall to CONFIRM or FORBID." — this embodies "the difference between automation and loop" from the safety side. A recipe waves an unknown step through, but a judging loop behaves as "**I don't know this. So stop and ask.**"

And the three-piece set for preventing runaway behavior.

- **CircuitBreaker (like an electrical breaker)** … trips (cuts off) when it detects consecutive failures N times (default 3), or **divergence/stagnation** where the progress score doesn't improve for a certain number of cycles (default 4). Like a household breaker, it detects the spinning of wheels — "repeating the same failure," "progress not improving" — and structurally prevents the accident of burning API cost alone.
- **Budget** … a **hard cap** on number of iterations (default 20) / time (default 1800 seconds) / number of actions (default 200).
- **Authentication-request detection** … if it finds signs in the output like `/login`, `401`, or `session expired`, it **immediately stops the loop**.

### 2-5. Even Using an LLM, the Safety Layer Cannot Be Bypassed in the Current Implementation

I made the heading precise. The qualifier "**in the current implementation**" is essential (I disclose the reason at the end of this section).

"If you run it with an LLM, won't the LLM run away in the end?" — a reasonable doubt. llloop's answer is to **make bypassing structurally impossible**.

`LLMStrategy` has the LLM propose "just one next action, in JSON." However —

- The LLM's output is treated as **untrusted** and strictly parsed by `parse_action` (only the first `{…}` block is adopted, `kind` is validated against the allow list, and anything unparseable is discarded).
- The actual danger judgment of a command is made not by the LLM but by the **runner-side `SafetyPolicy`**.
- If the LLM is absent (the codex CLI isn't on PATH), it **degrades to a deterministic fallback strategy** (this too is fail-closed).

In short, the design core is —

> **The LLM can only "propose." The final gate is the SafetyPolicy. On the current path, the LLM cannot bypass the safety layer.**

In fact, the tests demonstrate that "**even if the LLM proposes a dangerous deletion action, the runner stops it with `SAFETY_BLOCKED`.**" This is exactly the same structure as Chapter 1's RAPTOR philosophy — "Python holds the front end of judgment, and the LLM concentrates on judgment."

#### honest disclosure (Why I Qualify It as "in the Current Implementation")

"The LLM cannot bypass the safety layer" is structurally guaranteed as a code path (`LLMStrategy → parse_action → runner.SafetyPolicy`). But this is a **conditional proposition** that depends on the premise that "**commands are executed only via llloop's Executor.**" `codex exec` itself is designed not to cause side effects, running in an `-s read-only` sandbox, but if a path were added in the future to let the LLM hit the shell directly outside the Executor, the guarantee would collapse. **There is no such path in the current implementation** — so I made the heading not the unconditional "cannot be bypassed" but "cannot be bypassed in the current implementation."

### 2-6. Launch and the Demonstration Task green-keeper

llloop's launch command is `lll` (a console script = a launch command that enters PATH when you install the package). Launching with no arguments brings up a ccr-style interactive menu (project selection + carry-over display of next_plan / last_outcome + automatic continuation of the active project after the default 30 seconds), and runs the first demonstration task **green-keeper**.

green-keeper is a loop in the style of **GitOps reconciliation** (reconciliation = aligning by matching "how things should be" against "how things are" and filling the gap). The image is a gardener who sets "all the plants in healthy condition" as desired, and when they find a withering one (drift), they water it.

In green-keeper's case:
- **desired** … all checks (pytest / ruff / mypy) green.
- **actual** … the execution result.
- **drift** … capturing a failing check as a "Symptom."
- **repair** … proposing **safe self-repair** like `ruff --fix`.

It can autonomously go as far as push, but **the default repairs do not include destructive operations** (fail-closed here too).

The tests depend only on stdlib, are mypy strict / ruff green, and number **90** at present (`test_safety` / `test_runner` / `test_strategies` / `test_llm` / `test_stdin_isolation` / `test_console_e2e` / `test_interactive_menu`, etc.). This is the value from "counting test functions."

#### honest disclosure (About the Tests Being Green)

"90 tests green" is backed by the number of test functions and the existence of the code; **I did not actually run pytest while writing this article to re-confirm green.** The confidence level is "it was green as of the most recent commit." I maintain the sense that asserting "green at the latest" would require a re-run.

### 2-7. A Loop with a "Verifiable Goal" — /goal as the Official Implementation

Once you have a loop harness, the next thing that bubbles up is the question "**from where do you drive it?**" In Chapter 0 I wrote that "a loop needs a **trigger** and a **verifiable goal**." I'll leave the externalization of the trigger side to another article ([How to Operate Claude Code on a Windows PC via SSH from Your Smartphone](https://qiita.com/furuse-kazufumi/items/be52eeb6455732161486) — readable as a story about the entry point that drives the harness from outside), and focus here on the "**verifiable goal**" side.

Claude Code's official `/goal` command is a textbook implementation of this. When you set a completion condition, after each turn a "small, fast model (Haiku by default)" judges whether the condition holds, automatically starting the next turn if unmet and clearing automatically when achieved (confirmed in the [official docs](https://code.claude.com/docs/en/goal): "v2.1.139 or later," "each turn, a small fast model checks whether the condition holds," "defaults to Haiku"). This is precisely "**a loop with a verifiable goal.**" The condition can even write a turn cap like "or stop after 20 turns" — a runaway-prevention cap is basic discipline here too.

(The release date of v2.1.139, "May 12, 2026," is secondary-only; the official docs state a version requirement but don't explicitly state a date, so I hedge the date.)

> 🗨️ "Thanks to the mystery graph, the sense of desperation is faint." — [Snack Bus-e / Forbidden Shibukawa (Alu)](https://alu.jp/series/スナックバス江/crop/UfjgydbJNoh5HDTItAlf)
>
> (Interlude) Benchmark numbers, too, dilute the sense of desperation if you just throw out a "mystery graph" by vibe. But this article's discipline is the opposite. **The mystery graph is exactly what you doubt the breakdown of.** In the next section, I do exactly that demonstration.

---

Chapter 2 was about the "**how**" (control). Circulate with MAPE-K, apply an unbypassable brake with a fail-closed safety layer, and swap out strategies to compare them — this is the prototype of loop engineering. Here, I place the verification of the "number I discarded," foreshadowed at the top, as a standalone section.

---

## ★ honest disclosure: The Story of a Number I "Stopped Using"

I'll disclose the true identity of the number I discarded, touched on at the top. It was an oft-cited claim like this:

> "**A certain 2026 paper (arXiv 2605.18747) showed up to a 10× improvement by changing only the tool harness while keeping the model fixed.**"

It's just the right "hook" for talking about the power of the harness. I checked this against the primary source. Conclusion — **this claim is unusable as-is.**

- arXiv 2605.18747 genuinely exists. Its title is *Code as Agent Harness*, submitted on May 18, 2026, a **survey paper by 42 authors total**, first author Xuying Ning et al. ([arXiv:2605.18747](https://arxiv.org/abs/2605.18747), text re-confirmed while writing this).
- However, the name "Bölük / Boluk" **does not appear** in its author list.
- Nor is there any concrete numerical claim like "10x" **in the abstract**.

In other words, the three-piece linkage of "**Bölük showed 10× in 2605.18747**" (author name, number, paper number) appears to be a **conflation of unknown origin**. I was tempted to use this number as the article's "hook." It's catchy. But when I went to the primary source, there was no basis. So I **discard it**.

Then does the harness really have no power? Not at all. **The fact itself — that "fixing the model and changing only the surrounding runtime (the harness) produces a large performance gap" — is backed up by other sources.** That said, for the figures below, all I could trace was a citation in a secondary source; I couldn't go back to the primary measurement source and conditions. So I treat them all as "**reports by ~ (secondary citation).**"

- A report that LangChain improved a coding agent on Terminal-Bench 2.0 from **52.8% → 66.5%** (same model, harness rebuild only) (**secondary citation, measurement conditions unconfirmed**).
- A comparison is also circulating that, in the same task, a model said to be **GPT-5.5** scored about 61% with one harness and about 87% with another, but **the model name "GPT-5.5" itself is outside my knowledge and needs verification**, and the figures are secondary-only, so I won't use the specific values as argumentative material in this article (I'll keep it to "it's spoken of as an example where things move greatly with harness differences").
- The dedicated benchmark *Harness-Bench* ([arXiv:2605.27922](https://arxiv.org/abs/2605.27922)) genuinely exists.
- The related paper *From Model Scaling to System Scaling: Scaling the Harness in Agentic AI* ([arXiv:2605.26112](https://arxiv.org/abs/2605.26112), first author Shangding Gu, 2026-05-25) also genuinely exists. But **this abstract too has no "10×" figure**, and since the authors' affiliations **are not listed on the abstract page**, I treat the often co-cited "UC Berkeley" as a **secondary source** (abstract page re-confirmed while writing this).

The lesson is the very discipline I placed at the top.

> **When you see an unusually catchy number, doubt the breakdown before you let yourself feel victorious. Check at the primary source whether the citation's three-piece set (who / in which paper / how much) actually clicks together.**

The harness is powerful. But to speak of that power, you don't need false attribution of authority. **The right source, with the right numbers**, is enough.

> 🗨️ "Knowing that one does not know." — [Snack Bus-e / Forbidden Shibukawa (Alu)](https://alu.jp/series/スナックバス江/crop/JRY5aSqHgjWRo1QnfR2l)
>
> (Interlude) "Knowing that you don't know" — this is the spirit of honest disclosure. An AI can fluently hold forth even on what it doesn't know. That's why the human side needs an eye that draws the line: "this part is unverified." Chapter 1's "algorithmic understanding," too, is in the end, I think, one form of this **knowing-that-one-does-not-know**.

---

## Chapter 3 [Knowledge = RAPTOR + RAD + LLM Wiki] Pouring "Knowledge" into the Harness and the Loop

In Chapter 1 we saw the "reins (harness)," in Chapter 2 the "wheel (loop)." The last is "knowledge." Both the harness and the loop are, **without good material for judgment, just spinning their wheels**. To circulate cleverly, you need the contents to circulate — knowledge.

My stack holds knowledge in three layers.

1. **My own research knowledge (the RAD corpus)** … research knowledge placed locally, about 65 domains and about 47,000 notes.
2. **Knowledge that grows wiki-style (the LLM Wiki pattern)** … a knowledge cache that weaves "concept pages" from raw sources and grows them via mutual links.
3. **A security agent that uses it safely (RAPTOR)** … the deterministic orchestration, fully controlled by Python, that we saw in Chapter 1.

### 3-1. The RAD Corpus — My Own Research Library

**RAD (Research Aggregation Directory)** is a collection of research knowledge placed locally. `RAD_INDEX.md` (auto-generated) explicitly states at the top "**65 RAD corpora**." This is an internal knowledge source that a skill called `rad-research` searches across with grep.

I'll write out the scale **with an accurate breakdown**. Here the numbers change depending on how you count, so I won't round.

- **Number of corpora**: 65 domains (verified by actual count).
- **Markdown notes within `_corpus_v2`**: about **47,097** (actual count of `.md` files). About 47,130 counting all files.
- In a separate directory there's **hacker_corpus** (security-specific: phrack / ghsa / capec / d3fend / oss_security / project_zero / payloads_all_the_things, etc.), about **32,503 files**.

#### honest disclosure (Handling the "About 49k Items" Number)

When putting it out publicly, I often round it to "my own research knowledge, about 49,000 items (about 49k)." The origin of this number is the tally record from the large-scale expansion on May 9, 2026 (the expansion added 16,377 docs, reaching a total of about 48,800).

That said, **I did not re-count the total number of documents on disk this time** (the number of corpora, 65, and the note counts of some corpora are verified by actual count). Also, hacker_corpus is in raw aggregate files, where one file contains many docs, so "number of files" and "number of contained docs" don't match.

So if I write it honestly —

> **About 65 domains, about 47,000 notes (actual Markdown count). Separately, hacker_corpus about 32,000 files. When I round it to 'about 49k-item scale,' I do so with the timestamp 'the tally value at the May 2026 expansion.'**

I'm calmly applying "doubt the breakdown of unusually large numbers," which I stated at the top, to my own numbers too.

#### RAD's Operating Rules — Don't Just Accumulate

RAD isn't "collect and done." There are three operational disciplines.

1. **K² sizing** … the size of a corpus isn't "fixed at 100"; the target is **about K² notes** relative to K, the number of internal subcategories of a topic (if K≈10, then about 100). If too thin (under about 40), expand toward K².
2. **Pruning by freshness × value** … `rad_prune.py` scores each note by "**freshness** (exponential decay of elapsed time since collection) × **value** (amount of body text + presence of sources)" and evacuates the bottom ones to `.pruned/`. Since deletion is irreversible, **the default is dry-run (it doesn't actually delete, only shows what would be deleted in a dress rehearsal)**, and actual deletion happens only when `--hard` is specified. This too is the fail-closed mindset.
3. **Agents write directly** … collection mobilizes arxiv / scholar-search / fetch / firecrawl / WebSearch all at once and **writes the results directly to disk**. This is a design that reflects the past lesson of "returning a huge collection result to the main context and hitting the session limit."

As a corpus directly tied to this article's three themes, `loop_engineering_corpus_v2` genuinely exists. It has a file-per-note structure of a001..a048 (48 notes) + b001..b048 (48 notes) = **96 notes total**, and SKILL.md's note_count matches at 96 (score 0.982).

The contents cover — control feedback (PID / anti-windup [a mechanism that suppresses runaway of the integral term] / state-space [the state-space representation] / Lyapunov [stability analysis] / MPC [model predictive control] / MAPE-K / OODA / cybernetics), autonomous agent loops (ReAct / Reflexion / Plan-and-Execute / Self-Refine / Tree-of-Thoughts, etc.), **the various schools of reinforcement learning** (policy-value iteration / PPO / RLHF / RLAIF / Constitutional / RLVR / AlphaZero, etc.), and operational CI (GitOps reconciliation / watchdog / chaos engineering). Example actual notes: `a001_pid_control` / `a009_ooda_loop_boyd` / `a013_mape_k_autonomic_loop` / `b001_mape_k_autonomic_reference_loop`.

In other words, Chapter 2's `llloop` — its MAPE-K, its safety, and its green-keeper (GitOps reconciliation) — are all **implemented with this corpus as their design basis**. The flow of knowledge (corpus) → loop (llloop) is connected in the real thing.

#### honest disclosure (The Discrepancy Between "50 Methods" and "96 Notes")

The original memo says `loop_engineering = 50 methods`, but the reality is **96 notes (2 shards)**. This is a temporal gap: "**50 methods were the starting point for the investigation, later expanded to 96 notes in a file-per-note form.**" So in this article I write "expanded to 96 notes starting from about 50 methods." **I don't pad it to "96 methods."**

Furthermore, the hierarchical-skill side generated by corpus2skill (described later) (`.claude/skills/corpus/loop_engineering/INDEX.md`) shows "39 documents / 12 clusters." This is **a hierarchy built from an older source version**, because I haven't re-run corpus2skill on the latest 96 notes. I note this so as **not to conflate** the raw-corpus count (96) with the hierarchical-skill count (39).

### 3-2. LLM Wiki — The Pattern of "Knowledge That Grows"

Collected knowledge, left alone, is "just a pile." You can search it, but it never **connects and grows**. That's where the **LLM Wiki** pattern comes into play.

This is **a pattern circulating as a statement by Andrej Karpathy** (per my memo, originating from a Gist in April 2026; however, **since I couldn't confirm the primary Gist URL in this article, I hedge both the proposer and the date**), and it holds knowledge in three layers.

1. **The raw source layer (raw, immutable)** … the original literature and logs. Not altered.
2. **The Wiki layer (compiled, concept pages the LLM manages)** … "concept pages" the LLM weaves by summarizing and cross-linking.
3. **The schema layer (schema)** … the blueprint for "what kind of pages, and how to update them."

#### Plain Language: The Difference Between RAG and LLM Wiki

**RAG (Retrieval-Augmented Generation)** is the "**run to the library each time a question comes in and look for relevant books**" approach. It's on-demand.

**LLM Wiki** is the compiled type, "**organize frequently-used knowledge into a Wiki in advance and reuse it.**" It's the approach of organizing first.

These two aren't in opposition but **complementary**. The ideal form is "**search an organized Wiki with RAG**" — the image of a well-tidied library (Wiki) that a librarian (RAG) guides you through quickly.

I **map** this LLM Wiki pattern to two actual entities (I make explicit that **both are at the design stage, with implementation in a subsequent phase**. The following is "my mapping (subjective)," not an already-implemented isomorphism).

- **llive** (a self-evolving modular memory LLM framework), its Phase 2-4 requirements LLW-01–08. For example, LLW-01 ConceptPage, LLW-02 Wiki Compiler, LLW-04 contradiction detection, LLW-08 RAG×Wiki two-layer operation.
- A v2 vision for extending **RAPTOR**'s **corpus2skill** into a continuously-updating ingest loop.

llive's four-layer memory design can, **in my mapping**, be structurally mapped to Karpathy's pattern (a correspondence purely as design intent; implementation is yet to come): semantic memory ≈ the Wiki layer, episodic memory ≈ the raw source layer, the Hippocampal Consolidation Scheduler ≈ the Wiki Compiler, the Contradiction Detector ≈ contradiction flagging, structural memory (the graph) ≈ inter-page links, Provenance ≈ source tracking.

#### ★ LLM Wiki's Greatest Pitfall: The Circulation of Thought

This is an important design warning, two sides of the same coin as honest disclosure. LLM Wiki's greatest pitfall is the **"circulation of thought (thought circulation)."**

> **The LLM generates a new page on the basis of a Wiki page it wrote itself. Then the small initial hallucination (a plausible error) becomes fixed as "consensus."**

It makes its own mistake true by citing it itself. It's like spreading a rumor alone and then believing the rumor because "everyone is saying it." Since the loop is fast (recall Verloy's warning from Chapter 2), this circulation, too, risks being **fixed at machine speed**.

Against this, llive designs **Anti-Circulation Safeguards (LLW-AC-01–08)** (at the design stage).

- **Treat raw events as authoritative, and existing summaries as no more than a working draft.**
- **Forbid chained consolidation within a single cycle** (don't immediately make your own output the basis for the next).
- **Run drift detection periodically** (regular inspection for misalignment).
- **diversity preservation** (protect minority evidence so the majority doesn't paint over it).
- **Make an external ground-truth anchor mandatory** (immovable external facts like CAD / DOI / a formal-verification hash).

That last one, "external anchor mandatory," is the very stance that runs through this whole article — **primary-source-ism**. The AI shouldn't complete things solely within itself; it must always drop anchor in an immovable external fact.

> 🗨️ "Half Trust × Half Doubt" — Snack Basue / Forbidden Shibukawa (Al)
>
> (Brief aside) The antidote to thought circulation is this **half-trust, half-doubt**. Even the summary you wrote yourself should be doubted as a "working draft," and anchored to immovable external facts (DOI / hash / CAD). It is the healthy doubt that keeps an AI from believing the rumor it started as "what everyone is saying."

https://alu.jp/series/スナックバス江/crop/Ud7lZLbei1F5xaFuAq3i

Incidentally, FullSense (described later) consists of **three products: llmesh / llive / llove**. If we map the LLM Wiki roles onto the products, **llive is the "Wiki editor," llove is the "Wiki's UI," and llmesh is the "Bus that carries the raw sources."** (RAG is not a product but a *method* of search, so I don't place it in the product column; I position it as a tool used on top of the three products.)

### 3-3. RAPTOR Doubles as the Entry Point for "Using Knowledge Safely"

Who uses the knowledge (RAD / LLM Wiki) safely? That's Chapter 1's **RAPTOR**. In RAPTOR, when you run `/sourcehunt` (per-file vulnerability hunting), if a corpus exists, a knowledge base is auto-loaded, and it's **injected into the analysis context with attribution** via `get_hints(tags)`.

And RAPTOR brings **stages of evidence** to the very way knowledge is used. The **evidence ladder** of `/sourcehunt` has six rungs.

```
suspicion
  → static_corroboration
    → crash_reproduced
      → root_cause_explained
        → exploit_demonstrated
          → patch_validated
```

When **ASan / UBSan** (sanitizers that detect memory anomalies and undefined behavior at runtime) reproduce a crash, the evidence is upgraded from "static corroboration" to "**crash reproduced**," and this becomes the gate for **PoC** (Proof of Concept = demonstration code that can actually trigger the vulnerability) generation. In other words, "**don't treat 'suspicion' on the same level as 'demonstration.'**" Express the weight of evidence in stages.

This is institutionalized in the output style too. RAPTOR's statuses are snake_case in JSON (`exploitable` / `confirmed` / `ruled_out` / `disproven`), Title Case in human-readable form, and **ALL_CAPS is forbidden**. Furthermore, **the red/green indicators 🔴/🟢 are forbidden**. The reason is exquisite — "**bad for the defender ≠ bad for the researcher**"; that is, good and bad depend on perspective, so don't glibly judge with red and green. Don't exaggerate findings; express them in stages by evidence level. This is a mechanism that **enforces honest disclosure at the design level**.

### 3-4. corpus-first advantage — Even Solo Development Can Become "Multi-Perspective"

Finally, why does this "knowledge stack" click with my own unique axis (Chapter 1)?

There's the realization of the **corpus-first strategy**. If you grow the RAD corpus first, then even in solo development, **perspectives the user isn't conscious of** — Six Hats, TRIZ (inventive principles), the KJ method, MindMap, cross-domain analogy — **can be complemented** into the AI's thinking flow.

I write this with the qualifier "can be." Corpus reference isn't a panacea. **If the relevance filter doesn't work, irrelevant or stale knowledge gets mixed in and, conversely, becomes noise.** In fact, the "pruning by freshness × value" I wrote about in 3-1 is precisely a device to suppress this noise contamination. So the accurate sense is "**multi-perspective can be complemented, on the premise that the relevance filter is working.**"

One concrete example. When designing Chapter 2's llloop safety layer, I drew the idea of "make fail-closed three-tiered (ALLOW/CONFIRM/FORBID)" from both the control-theory notes (anti-windup and circuit-breaker patterns) of `loop_engineering_corpus_v2` and RAPTOR's governance (DENY/REVIEW/DENY-if-not-on-allow-list). Even though I was designing alone, the corpus overlaid "the control-engineering perspective" and "the security perspective" behind the scenes — this is one example of how corpus-first works.

This corresponds to the difference between "**using an AI** (asking for an answer)" and "**building together with an AI** (referencing a corpus in the background, complementing multiple perspectives, while the human holds the design decisions)." In Chapter 1 I wrote that "the user side needs three abilities: ideation, heuristics, and algorithmic understanding." corpus-first is a contrivance that **can amplify** those three abilities with the AI side's knowledge foundation (with the caveat that noise management is a premise).

The human holds the reins (A), the loop circulates safely (B), and multi-perspective knowledge flows into that loop (C) — here, the three connect into a single line.

---

Chapter 3 was about the "**what**" (implementation and knowledge). Collect knowledge with RAD, grow it with LLM Wiki (with a safeguard against the pitfall of circulation), and have RAPTOR use it safely while preserving the stages of evidence. Now, at last, the integration.

---

## Integration Chapter: A (Why) → B (How) → C (What) Become a Single Worldview

Let me fold the three chapters so far onto a single sheet.

| | Theme | Question | Real Thing | "One More Axis" |
|---|---|---|---|---|
| **A** | harness engineering | **Why** (philosophy) | RAPTOR's two-layer separation | The human holds the reins and raises the AI as a subordinate |
| **B** | loop engineering | **How** (control) | llloop (MAPE-K + fail-closed, alpha) | The safety layer can't be bypassed on the current path; swap strategies to compare |
| **C** | RAD + LLM Wiki | **What** (knowledge) | About 47,000 notes (Markdown count: 47,097 docs) + the evidence ladder | corpus-first means multi-perspective and primary-source-ism even solo |

The industry's diagrams tend to line up A, B, and C as separate buzzwords. My claim is — **these three are three faces of a single worldview.** The core of that worldview converges to just two principles.

The first is **"bring the locus of responsibility to the architecture level."** The Approval Bus, the SafetyPolicy, and the evidence ladder are implemented not as the operational machismo of "let's be careful," but as **structures hard to bypass**. Chapter 1's `@govern`, Chapter 2's `SafetyPolicy`, and Chapter 3's evidence ladder all serve this single point.

The second is **"place honest disclosure at the core."** When an unusually good number ("Bölük 10×") appears, doubt the breakdown before you feel victorious. In each chapter of this article, I applied the same discipline to my own numbers too (49k items, 90 tests, 50 methods vs 96 notes).

And this worldview is self-contained locally. RAD, llloop, and RAPTOR all run on hand and don't let personal information, corporate secrets, or sensor data out. Note that this homemade stack (llloop / RAD / RAPTOR) is **a local research stack separate from** the product ecosystem I separately call **FullSense** (the **three products** llmesh / llive / llove + a suite installer). The two share a philosophy, but I draw a line between this and the product line (only llive straddles both, as the receptacle for the LLM Wiki touched on in Chapter 3).

#### Why I Can Say "It Is the Human Who Holds the Reins" — Three Observation-Based Points

Finally, I consolidate here the "argument for superiority" foreshadowed in Chapter 1. But let me first say honestly: the following is **not a measured conclusion based on citing primary research, but an observation based on my experience (a structural tendency)**. I do not say "it's been proven cognitive-scientifically." On that basis, I believe there are at least three points where the human structurally tends to have the advantage over the AI.

1. **Always parallel** … the LLM is basically fixed to a single session, but a human can keep running multiple things in the background.
2. **Long-range payoff of foreshadowing** … what an LLM can pay off is foreshadowing within a single session (a few hours). A human can **pay off today the foreshadowing they planted with an experience from 10 years ago**.
3. **Always-on hazard anticipation (KYT)** … the LLM's risk_alert won't run unless you explicitly write the code, but a human runs it unconsciously, always (that sense of "somehow" avoiding a near-miss).

So that "it is the human who holds the reins" is less machismo than an **observed tendency**. And my llive is trying to bring this human tendency, little by little, to the architecture level — that's the motivation running through A, B, and C.

---

## Conclusion: The Reins, the Wheel, and Knowledge

In 2026, the AI industry, after prompt engineering, named **harness engineering (the reins)** and **loop engineering (the wheel)** (the inventors were not the AI, but human engineers). I keep a prototype of that stack on hand, locally, at the proof-of-concept level.

- **The reins (A)** … implemented by RAPTOR's two-layer separation where "Python controls everything, and the LLM concentrates on judgment." Onto that, I added an auxiliary line to the model-centric diagram: "the human holds the reins and raises the AI as a subordinate." It's a different lineage from Karpathy's "vibe coding" (February 2025), and I don't say "I named it first."
- **The wheel (B)** … my homemade `llloop` (alpha, unpublished) circulates with MAPE-K and applies the brake with a **fail-closed safety layer that can't be bypassed on the current path**. The LLM can only propose; the final gate is the SafetyPolicy.
- **Knowledge (C)** … RAD of about 65 domains and about 47,000 notes (Markdown count: 47,097 docs) is grown with the LLM Wiki pattern (with an anti-circulation safeguard against the circulation of thought), and RAPTOR uses it safely while preserving the stages of evidence.

And what ran through this entire article was a single discipline.

> **When you see an unusually catchy number, doubt the breakdown before you let yourself feel victorious. Drop anchor in the primary source.**

I went to the primary source and **discarded** the tempting number "Bölük showed 10×." This isn't a disclosure of weakness but **part of the design philosophy**. Because what the human holding the reins needs is the "knowing-that-one-does-not-know" to see through fluent numbers.

### A Lingering Note, Like a Preview of What's Next

What I want to write next is the on-machine progress of the **LLM Wiki implementation** — llive Phase 2-4's LLW-01–08 and the v2-ification of RAPTOR's corpus2skill — which I hedged again and again in Chapter 3 as "at the design stage." After attaching an anti-circulation safeguard to the "circulation of thought," I hope to show, with moving visuals, knowledge **growing on its own**.

Hold the reins, circulate the wheel safely, and grow the knowledge. All of it, without letting data out to the outside, locally. — That, in my view, is the down-to-earth form of the "2026 paradigm shift."

---

## References (Sources)

**harness / loop engineering (terminology, primary and near-primary)**
- Mitchell Hashimoto, *My AI Adoption Journey* (2026-02-05, the presentation of "harness engineering." Hedge and date confirmed against the primary source): https://mitchellh.com/writing/my-ai-adoption-journey
- Andrej Karpathy, the original "vibe coding" tweet (2025-02-02, URL and date confirmed): https://x.com/karpathy/status/1886192184808149383
- Data Science Dojo, *Agentic Loops Explained: From ReAct to Loop Engineering (2026 Guide)* (2026-06-09): https://datasciencedojo.com/blog/agentic-loops-explained-from-react-to-loop-engineering-2026-guide/
- Filip Verloy, *From Prompt Engineering to Loop Engineering* (2026-06, "scaling risk at machine speed"): https://medium.com/@filipv_74515/from-prompt-engineering-to-loop-engineering-why-the-agent-era-demands-a-new-security-paradigm-816385040e3d
- Claude Code official docs, `/goal` (v2.1.139 or later, autonomous iteration with Haiku judging. Version requirement and Haiku confirmed against the primary source): https://code.claude.com/docs/en/goal
- arXiv:2605.18747 *Code as Agent Harness* (Xuying Ning et al., 42 authors total, 2026-05-18. Re-confirmed while writing this. ※ Neither "Bölük" nor "10×" **appears** in this paper): https://arxiv.org/abs/2605.18747
- arXiv:2605.26112 *From Model Scaling to System Scaling: Scaling the Harness in Agentic AI* (first author Shangding Gu, 2026-05-25. Affiliation not listed on the abstract page = "UC Berkeley" is a secondary source): https://arxiv.org/abs/2605.26112
- arXiv:2605.27922 *Harness-Bench*: https://arxiv.org/abs/2605.27922

**RAPTOR (the real-world stack)**
- upstream repository (gadievron/raptor, MIT. Authors Gadi Evron and 5 others): https://github.com/gadievron/raptor

**Related articles (my own)**
- How to Operate Claude Code on a Windows PC via SSH from Your Smartphone: https://qiita.com/furuse-kazufumi/items/be52eeb6455732161486

**Interludes (Snack Bus-e / Forbidden Shibukawa, Alu)**
- "Conversations don't click with someone who differs in IQ.": https://alu.jp/series/スナックバス江/crop/PJm0yAGeJy9iSa487mrX
- "Thanks to the mystery graph, the sense of desperation is faint.": https://alu.jp/series/スナックバス江/crop/UfjgydbJNoh5HDTItAlf
- "Knowing that one does not know.": https://alu.jp/series/スナックバス江/crop/JRY5aSqHgjWRo1QnfR2l

> ※ The main items hedged in the text as "secondary-only / primary unconfirmed" are as follows: the OpenAI article's text, tagline, and scale figures (the primary returns HTTP 403); LangChain's `Agent = Model + Harness` formula and the measurement sources and conditions of each harness benchmark (including the model name said to be GPT-5.5); the release date of Claude Code v2.1.139; the latest status of llloop's tests being green (no re-run performed); RAD's total document count (the current local recount is **47,097 docs as of June 17, 2026**, while older prose may still refer to "about 49k"); the proposer and date of Karpathy's LLM Wiki Gist; the source pages for Canon's "Spirit of the Three Selfs" and the four principles of *First, Break All the Rules*; and Chapter 3's "three points of human advantage" (observation-based, not measured). I will update them as soon as I can confirm them with primary sources.
