---
title: '#46 What''s Hard About Self-Driving AI Isn''t "Running It" but "Supervising It" — 9 loop-engineering principles I pulled from an llterm incident'
tags:
  - AI
  - LLM
  - ClaudeCode
  - Codex
  - Agent
private: true
slide: false
ignorePublish: true
---
# #46 What's Hard About Self-Driving AI Isn't "Running It" but "Supervising It" — 9 loop-engineering principles I pulled from an llterm incident

> **Premise**
> This is about a self-driving AI harness that keeps headless CLIs such as `claude -p --resume` and `codex exec` running turn by turn.
>
> **Route**
> Starting from the incident where "summarize the current progress" never came back, I follow one continuous line through injection starvation, `ctx 2549%`, over-review, and flaky-test exposure.
>
> **Goal**
> Rather than "how to make a self-driving AI run smartly," I want to leave you with design principles for loop engineering from the angle of "how to make it structurally supervisable."

I asked the AI, "Please summarize the current progress." It still had not answered after nearly a full turn.
At first, it looked like simple slowness. But once I followed the logs, that task had entered a path where it would be swallowed forever by the structure itself. And the deeper I dug, the more other holes appeared: a physically impossible occupancy rate of `ctx 2549%`, over-review triggered on every rotate, and the weakness of a self-driving loop that was supposedly "delegated" but not actually supervisable.

What this incident drove home was that the hard part of self-driving AI is not writing clever prompts. It is designing **where humans are allowed to intervene**. Using an llterm incident as the material, this article organizes what tends to break in a loop that keeps headless CLIs running across turn boundaries into 9 principles of loop engineering. The theme is not reasoning quality. It is the design of **supervision, interruption, stopping, and observability**.

> **honest disclosure**
> This is not an "everything got fixed" story. The causal link by which `ctx 2549%` triggered rotate is confirmed. But **how that displayed number was calculated in the first place, and how it swelled all the way to 2549%, is still not fully explained**. The occupancy display on the Codex side is also provisional. An abnormal number is not a victory condition. First treat it as a sign that measurement itself is broken. That attitude is part of the article's main point.

---

## 0. Bottom line first

Let me place the claim in one sentence up front.

> **The core of self-driving AI is not how smart the inference is, but whether the structure remains supervisable.**

Said a bit more carefully:

> What is harder than "running" self-driving AI well is making it possible for a human to supervise, interrupt, and stop it.
> Therefore the real substance of loop engineering lies less in strategy itself than in the design of **intervention boundaries, observation, and stopping conditions**.

Here, `loop engineering` does not simply mean calling AI over and over.
It means building a structure in which the AI autonomously advances turn by turn while the human can still interrupt it when necessary, stop it, look back through the logs, and later explain what happened.

In other words:

- where the human can cut in
- where the AI advances to the next turn
- where failure is detected
- where the system decides "this is enough"

Designing those boundaries is what I mean here by loop engineering.

`llterm` is my homemade loop harness for repeatedly driving headless Claude Code and Codex sessions. The incident in this article began when a task injected into that loop — "summarize the current progress" — never came back.
So this is not an abstract essay about AI-agent architecture. It is **a story that lifts general principles out of one concrete failure**.

![An old man in extreme close-up ordering: "Go on."](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/025.jpg)
> 🗒️ *"Go on." — exactly the operational feeling of sending an autonomous loop around one more lap while continuing to observe it without losing sight of it*（© Forbidden shibukawa / SHUEISHA・Snack Basue）

---

## 1. "Summarize the current progress" never came back

The trigger was not dramatic.

I was running `llterm` in orchestra mode. That means an implementing AI writes code, multiple AIs review it, a responsible AI issues an integrated judgment, and if needed the result is revised before the next step. A single turn is not light. In wall-clock time it takes roughly 13 to 18 minutes.

In the middle of that, a human injected this request:

> Please summarize the current progress.

Ordinarily you would expect an answer after a short wait. The current turn finishes, the next boundary picks up the task, and the AI writes the summary. At least, that was what I as the designer expected.

But nothing came back.
Not after 5 minutes. Not after 10. Not after 13. Even so, all I could honestly say at that point was that there had been **a wait approaching one full turn**. That alone was not evidence of starvation.

The first thing to doubt was not "the AI ignored me." It was: **does the task I injected actually have a path that reaches the designed consumption point?**

### 1-1. It wasn't slow. It never reached the consumption point.

The logs showed that the problem was not a merely long turn.

At the time, `llterm` concentrated its injection-consumption point on the continuing-turn side — that is, in the prompt assembly path for "continue the same session again." But the real loop was not continuing cleanly there.

Why not? Because the displayed `ctx` usage had become **2549%**, a number that is physically impossible.

The moment you see 2549%, the correct takeaway is not "the AI is amazing." It is: **the measurement is broken**. Context occupancy does not have a legitimate path beyond its physical ceiling. Yet rotate was being triggered off that broken occupancy figure, and every turn was reopening a fresh session instead of taking the clean "continue" branch.

That produced the following chain:

- the human believed they had injected a task
- the loop rotated every turn
- the injection never reached the continuing-turn consumption point
- it got pushed into the resume prompt
- then rotate happened again

So the task was not merely delayed. It had entered **a structurally uncollectable path**. That is what I call starvation in this article.

### 1-2. It's not enough to enqueue it

The lesson at this point was simple:

> **Starvation is determined not by "was it enqueued?" but by "can it reach the point where it is consumed?"**

Being in the queue is not safety. In practice, what matters is:

- which branch actually pops it
- whether it survives across rotate
- whether it can resume after exception paths
- whether human emergency injections outrank ordinary injections

Only when those conditions line up can you honestly say the task will be processed.

In this incident, what broke was less the injected task itself than **the designer's expectation**. I assumed it would be picked up at the next turn boundary. In reality, there was no path that reliably reached that boundary. Once you misread that, self-driving AI is no longer "delegated." It is merely "lost from sight."
