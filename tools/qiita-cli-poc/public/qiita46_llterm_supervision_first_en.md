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

### 1-3. One bug led to three more structural holes

This incident did not end with a one-line fix.
Once I started tracing injection starvation, at least three structural problems came into view in a chain:

1. the collapse of occupancy measurement into `ctx 2549%`
2. over-review that fired on every rotate
3. flaky tests exposed the moment I moved an observation point

So "the progress summary never came back" was only the entrance.
The real subject was the **structure of an unsupervisable self-driving loop** that became visible through that entrance.

In the next chapter, I will look at why human intervention naturally sticks to turn boundaries, and why things break when "stop" and "emergency interruption" are treated as the same mechanism.

---

## 2. Turn boundaries and emergency interrupts must be designed as different things from the start

The first thing this injection-starvation incident made clear was that, in a loop built around headless CLIs, the place where human intervention naturally takes effect is **the turn boundary**.

Once launched, tools like `claude -p --resume` and `codex exec` do not accept fresh input from the outside until that turn ends. You may want to jump in midway and say, "stop that topic for now and prioritize this instead," but in the default setup that message cannot get through. It reaches the system only at the moment the process returns once and begins the next turn.

Looked at from the other side, that means ordinary injections naturally belong in **a queue read at turn boundaries**:

- let the current turn run to completion
- read the queue at the next boundary
- make that injected request the highest-priority context of the following turn

That model itself is not bad. The problem begins when you stuff **cases that truly must stop right now** into that same box.

### 2-1. If you implement "stop" and "emergency interrupt" as the same thing, the loop dies

The first tempting move is to reuse `cancel` directly in order to stop the currently running turn. But there is a trap here.

There are two different meanings of "stop":

1. **Permanent stop**
   You want to stop the loop itself. No further `run_turn` should launch.
2. **One-shot interruption**
   You want to cut only the current turn and make the next turn prioritize another injected task.

If you drive both with the same flag, you usually end up with **sticky cancel**. In other words, the flag you raised intending only "stop now" remains alive afterward as well, and **future `run_turn`s stop launching at all**. Reusing that for emergency interrupts is the worst shape: you only wanted to cut the current turn, but you silently killed the whole loop.

That is why `llterm` had to split the two:

- `cancel()`: permanent stop; no later `run_turn` launches
- `interrupt()`: one-shot interruption; kill the current process, but still allow the next `run_turn`

This distinction is not an implementation quirk. It is a loop-engineering principle.

> **A turn-boundary queue and an immediate interrupt must be designed as different things.**

Ordinary injections say: "respect the current turn, then pick this up at the next boundary."
Emergency injections say: "cut the current turn if necessary, because the next thing must become top priority now."

Both are "human intervention," but they do not mean the same thing. If you do not separate them, the human's intervention right becomes too coarse and ends up being useless for both purposes.

### 2-2. Emergency injection is powerful. That is exactly why it should not be the default

Another important point is that emergency interrupt is a strong tool.

It is convenient. But convenience is exactly why it must not mean the same thing as an ordinary Send. To interrupt is to discard work and thought that are currently in progress.

For example:

- a turn that is just about to finish applying a patch
- a turn that is consolidating a long review
- a turn in the middle of final sign-off

If interrupt is the default in those contexts, a single short human message can destroy an AI-side piece of work that was just reaching coherence. That is not "easy to intervene in." It is "easy to break carelessly."

So in `llterm`, ordinary Send is routed to the turn-boundary queue, while only the urgent path is exposed as an explicit separate action.
That design is not a cosmetic UX trick. It means **making the cost of intervention visible in the UI**.

> Being able to intervene is not the same as being free to intervene lightly.

If you want self-driving AI to become something you can genuinely entrust work to, then the human side's intervention rights also need to be tiered.

### 2-3. The takeaway from this chapter

The chapter reduces to two points:

- ordinary injection into a headless CLI naturally attaches to the turn boundary first
- emergency interrupt must be designed as a separate path, or it gets entangled with stop and breaks

In other words, the first thing to design in a self-driving AI loop is not only what the AI should think about. It is **at what granularity the human can intervene**.

### ☕ Break point

The one-line takeaway is enough:

> **Ordinary injection goes to the turn boundary. Emergency injection goes to interrupt. Split those two rails first.**

Next we return to the `ctx 2549%` figure that was breaking that very intervention point. From there, the story flips from "the AI was too smart" to "the human measurement was broken."

---

## 3. `ctx 2549%` did not mean "the AI got fat." It meant the measurement was broken

If you keep tracing injection starvation, sooner or later you hit `ctx 2549%`.

What makes this number nasty is that at a glance it looks only like "something seems very bad." But once a context-occupancy gauge displays 2549%, the meaning is actually fairly clear:

> **When a metric exceeds its physical ceiling, suspect the measurement first.**

Here, `ctx` was supposed to mean "what fraction of the context window is occupied right now." If that display truly represented occupancy, it should never exceed 100%. Even 200% would already be absurd. So 2549% did not signal improvement or growth. It signaled that **the meaning of the metric itself had broken down**.

### 3-1. What was broken was not the AI. It was the definition of occupancy

At the principle level, the first break was that a **cumulative** token count intended for billing had been fed directly into occupancy control.

A cumulative billing counter is fine if you want to know "how many tokens have been spent so far." But occupancy is asking something different: **how much of the context window is occupied right now, at this moment**.

Those are similar, but not the same:

- cumulative value: total consumption so far
- occupancy: current instantaneous usage

In systems that resend context across tool round-trips and resume hops, cumulative values naturally swell.
If you read that cumulative number as occupancy, you get a principled failure mode: "the current turn still fits in the window, but the indicator alone keeps inflating by multiples."

And at the implementation level, the record suggests that **double counting during cache reread** was a strong candidate mechanism behind the observed swelling.
So there are really two layers here:

- **design-level mistake**: feeding a billing cumulative value into occupancy control
- **observed-value swelling mechanism**: cache reread double counting is a strong candidate, but the exact arithmetic path to 2549% is still unresolved

The most natural reading is that `2549%` appeared where those two layers met.

### 3-2. The rotate causality is confirmed. What remains unresolved is the breakdown of the displayed arithmetic

This is where the confidence levels must be separated.

- **confirmed**: the broken `ctx` display was being used for threshold control, so rotate fired every turn
- **unresolved**: even if cache reread double counting is the strongest candidate, what exact stack of rereads and resends inflated the number all the way to 2549%

So "the full arithmetic behind the displayed number remains unresolved" does **not** mean "the direct cause of rotate is still unknown."
The causality that triggered rotate is confirmed. What remains open is how rigorously we can decompose the way that grotesque number grew.

If you blur that line, honest disclosure itself becomes blurry.
Overstating the unresolved part is inaccurate, but so is refusing to mark the confirmed part as confirmed.

### 3-3. If you stack an outer rotate on top of a component that already self-compresses, the system degenerates

Another principle became visible here:

> **Do not double-manage a component that already manages itself.**

Systems like Codex already carry their own internal logic for session continuation and context compression on the `exec resume` side.
If an outer harness then forces rotate again from the outside based on an occupancy threshold, the management boundary becomes duplicated.

Then this happens:

- the inner side believes "this session can still continue"
- the outer side decides "this should already be cut"
- the outer side cuts every turn
- the result degenerates into one session equaling one turn

That is not a model-capability problem. It is **a conflict between management boundaries**.

Put differently, a smarter harness is not automatically better.
If the outer layer tries to take over responsibilities the inner layer already owns, it crushes the freedom of the loop as a whole.

### 3-4. The takeaway from this chapter

The chapter reduces to three points:

- 2549% was not "an impressive number"; it was "a broken number"
- if you confuse cumulative values with instantaneous occupancy, rotate control breaks
- if you add an outer rotate to a component that already self-compresses, the boundaries conflict and the system degenerates

In other words, before prompt design, the first thing to design in a self-driving AI loop is **what you measure, how you measure it, and what control authority you assign to that number**.

### ☕ Break point

The one-line summary is this:

> **2549% was not evidence of a strong AI. It was a sign that broken measurement had been wired directly into control.**

Next we move to another reversal: the way "review for quality" can, under some conditions, become nothing more than an expensive second dip.

---

## 4. Multi-AI review improves quality, but if you stack it unconditionally it only makes everything slower

What the `ctx 2549%` episode revealed was that once measurement breaks, rotate breaks with it.
But when rotate breaks, the truly painful part is not merely that "the loop spins too often." It is that **every spin drags an expensive review bundle along with it**.

In rough outline, one orchestra-mode turn looks like this:

1. a conductor AI implements
2. multiple AIs review in parallel
3. a responsible AI issues an integrated judgment
4. the conductor AI applies revisions
5. if needed, the system requests final sign-off

As a quality pipeline, that is defensible.
The problem was that **the same review intensity was being applied to every kind of turn**.

### 4-1. We were running full review even on turns that merely recorded state

The handoff and EXIT formatting that become necessary after rotate are, in essence:

- update `SESSION_SUMMARY.md`
- update `next_plan.md`
- shape the working context for the next turn

The crucial point is that these are less "new design decisions" than tasks that **shape and preserve what already happened**.
And yet, at that time, those turns were still going through the entire orchestra review bundle.

So what actually happened was this:

- one full review on the implementation turn
- then another full review on the record-keeping turn caused by rotate

That was not a problem of review quality. It was **a problem of scope**.

### 4-2. Review should not be maximized by volume. It should be designed by scope

The lesson here is blunt:

> **Review is not designed by volume. It is designed by scope.**

It is reasonable for implementation turns to receive heavy review.
But once you apply that same intensity to record-keeping turns like handoff, time and rate-limit cost balloon before quality gains do.

This is equally true of human review:

- a patch with real design changes
- a simple log-formatting edit
- a comment fix
- a handoff update

Any organization that throws the same review body at all four usually becomes slow.
AI orchestration is no different. Simply increasing the number of reviews is not quality engineering. It becomes design only when you decide **what depth of scrutiny belongs to what kind of work**.

On the `llterm` side, that led us toward an unreviewed path for record-keeping turns.
That is better described not as "reducing review," but as **returning review responsibilities to the places where they actually belong**.

### 4-3. Double-dipping sign-off was the same class of problem

The same lens forced a rethink of the default behavior of final sign-off.

If the responsible AI has already issued an integrated judgment, but every later revision turn still receives another unconditional sign-off, the system drifts toward "reviewing the review."
Of course large changes may still require re-confirmation. But if that becomes the default, the whole flow grows heavy.

Again, the key distinction is not yes or no. It is scope:

- sign-off that is always required
- sign-off that is required only under conditions

If you fail to design that distinction and instead fall back to "check everything just in case," the AIs will happily keep working and the processing system will become heavier without the human even noticing.

### 4-4. The takeaway from this chapter

This chapter reduces to three points:

- full review is a tool for quality, but it should not be applied uniformly to every turn
- record-keeping turns such as handoff and EXIT should use a different review intensity from implementation turns
- sign-off, too, is healthier for the whole loop when it becomes conditional rather than default-stacked

In other words, the quality of self-driving AI is not determined by **how many reviewers you attached**, but by **what kind of scrutiny you assign to what kind of moment**.

### ☕ Break point

More review is not automatically more virtuous.

> **Heavy scrutiny belongs only on heavy turns.**

In the next chapter we turn to the opposite side of the problem. Even if you lighten review, that still does not count as supervision if nothing can be traced afterward.

---

## 5. If you cannot trace it afterward, it is not supervision

When people write about self-driving AI, the discussion tends to drift toward "how should we make it think?"
But in real operation, what matters just as much is **whether you can reconstruct what happened afterward**.

If human beings are going to intervene midway, stop the loop, and revise the design, then at minimum they must be able to recover:

- what was emitted, and when
- what happened in which turn
- where the system first began to go wrong

### 5-1. Per-line timestamps are mundane, but they form the foundation of supervision

That is why we added **timestamps on every output line**.

At first glance this sounds boring.
But whether those timestamps exist drastically changes how an incident can be read.

For example:

- which AI returned first
- at which turn boundary an injection was actually read
- what happened before and after rotate
- how much longer a handoff turn was than it needed to be

Without timestamps at line heads, those questions become vague very quickly.

What makes this dangerous is that vagueness still lets you feel as if you "basically understood it."
That is exactly why traceability must not be treated as a convenience feature. It is **a structure that forces guesses to move closer to observation**.

### 5-2. Rotate logs are not for blaming the past. They are for fixing the future

On top of that, `llterm` is also moving toward leaving a rotate log on an hourly cadence.

The important point here is not to turn logs into a tool for surveillance or blame.
Logs matter less for deciding "who was at fault" than for finding **what must be changed so the same failure does not recur**.

In this starvation incident, if the logs had been sloppy, it would have been easy to blur the explanation into one of these:

- maybe it was only slow this one time
- maybe the model was just capricious
- the queue was populated, so perhaps the implementation was correct

But because the record was traceable, the failure could be driven all the way down to "the consumption point did not exist."
That is the essence of supervision.

> Traceability is needed not to accuse the past, but to repair the design of the future.

### 5-3. If telemetry is not fail-safe, it becomes an obstacle in production

That said, traceability can also become too heavy.

Suppose you decide logging matters so much that:

- the GUI dies whenever the disk starts filling
- a permissions error stops the entire loop
- failure to write logs takes the main execution path down with it

At that point telemetry stops being an aid to supervision and becomes a brand-new fault source.

So telemetry needs to be designed as "mandatory, but not the protagonist."
The main path must keep running, while enough information is still preserved to reconstruct what happened afterward. That balance is the point.

### 5-4. The takeaway from this chapter

This chapter reduces to three points:

- if you claim to supervise self-driving AI, the ability to reconstruct what happened afterward is a prerequisite
- per-line timestamps and rotate logs form part of the architecture-level substrate for that reconstruction
- telemetry fails if it is either too weak or too strong; it has to be designed toward fail-safe behavior

In other words, supervisability cannot be improvised out of "smart humans will manage somehow."
You have to **embed traceability into the system as a mechanism**.

Next we move to the way that same traceability loops back into testing. In other words: was that green test really green?

---

## 6. You also have to distrust tests that are "green by accident"

While fixing the incident, one more weakness surfaced: the brittleness of the tests.

This, too, is a very loop-engineering kind of lesson.  
The races and ordering dependencies that show up in production usually cast a shadow over the tests as well. The difference is that in production they appear as failures, while in tests they can stay hidden as "green by accident."

### 6-1. The test was not really green. It only happened to look green

The problematic test drove the real loop on threads while directly asserting against the state of the injection queue.

At first glance, that type of test looks attractive because it feels close to production.  
In reality, however, the result varies with details such as:

- when the worker reads the queue
- when the main thread performs the assertion
- at what timing output-log I/O gets inserted

In other words, the test was not validating only "is the function correct?" It was also implicitly validating "does it happen to run in this order?"

Adding output-log I/O shifted the timing of the main thread just enough for that ambiguity to surface.  
So this should be read less as "the logging feature broke the test" and more as **the test had always depended on a race, and only now finally broke**.

### 6-2. Concurrent tests need block points so they become deterministic

What was needed here was not speed. It was **fixed ordering**.

Concretely:

- pause the worker briefly
- create a window in which the injection has not yet been consumed
- assert inside that window
- then stop explicitly afterward

That is, introduce a block point.

Once you do that, the test stops being "something that happens to pass by accident" and becomes "something that must pass through this point under these conditions."

What matters in concurrent systems is not only making the test resemble reality.  
It is **being able to control where the observation takes place**.

### 6-3. Honest disclosure also has to apply to tests

The most important point in this chapter is that honest disclosure does not apply only to the article's narrative.

Even when a test is green, there may still be room for doubt:

- is that green deterministic?
- did it merely slip past the race by chance?
- would it turn red if the observation point moved?

If you skip those questions and just say "everything passed, so it's fine," then the ground falls away beneath the article no matter how often it preaches honest disclosure.

> In the same way you distrust suspiciously good numbers, you should also distrust suspiciously green tests.

That mapping is probably one of the more important ones in this entire article.

### 6-4. The takeaway from this chapter

This chapter reduces to three points:

- the greenness of a concurrent test can be produced not only by functional correctness, but also by accidental ordering
- without block points that fix the observation site, tests become fundamentally prone to flakiness
- honest disclosure should be applied not only to prose, but also to how test results are interpreted

At this point, the six chapters of material extracted from the incident are in place.  
Next, we generalize them into nine principles so this incident response does not remain just an `llterm`-specific memo.

### ☕ Break point

Distrust not only the numbers, but also the greenness of the tests.  
By this point, `honest disclosure` should be visible not as a writing trick, but as an operating discipline.
