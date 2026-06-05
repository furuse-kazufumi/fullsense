# English

# The "evolving AI's checkpoint is too heavy and breaks down" problem

## A parable: a checkpoint, and a gatekeeper who walks around every corner

An evolving AI has a **checkpoint** before entering the castle town. It is a gatekeeper who verifies "won't this individual run away out of control?" (we call this the inspector). It is a diligent gatekeeper who never overlooks a runaway individual.

But this gatekeeper has an absurdly meticulous way of checking. If the castle (= the AI's state) has n "rooms," he walks **all 2ⁿ ways through the corners of the rooms** to check. If there are 8 rooms it takes 256 ways, but with 16 rooms it is 60,000-some ways, and with 32 rooms it is **4.3 billion ways**. The moment you try to grow it to the scale of an insect's brain, the gatekeeper collapses from overwork first. This was the true identity of the "ceiling on evolution."

## What we did: don't walk every corner — take in the rooms "at a glance"

So we tried an approximation that "stops walking every corner and estimates the whole room at a glance."

- The first naive estimate (B1): safe, but **too cautious** — it turned away even individuals that were actually harmless. It let only 30% of the contracting individuals into the castle. That is putting the cart before the horse — stricter than the cheapest gatekeeper — and for a moment we got discouraged, thinking "the cheap glance is no good."
- The version that changed how the estimate is built (B2 = pressing down from above with absolute values): this hit the mark. **It let through nearly 80% (77.6%) of the people the diligent gatekeeper passes, with a single glance.** Paired with the cheap gatekeeper, 87%. The speed at 16 rooms was **12,000×**. Oversights (false positives) were zero.

Lesson: the "cheap glance" itself was not the problem — **the way the first estimate was built was just clumsy**. Before starting to build the heavy full-scale apparatus (SDP), we checked cheaply with a small experiment, and figured it out in seconds.

## Another idea: model it on "creatures that declutter"

Living things sometimes keep discarding what they don't need and become simpler. Cave fish discard their eyes, parasites discard their genes, deep-sea bacteria trim their genomes to travel light. **If "maintenance cost > usefulness," the simpler one survives.**

We want to bring this into AI evolution too. If we add not just "good performance" but "**a simple body that is cheap to verify**" to the score, the AI will steer on its own toward a lighter structure.

But there is a pitfall. "Simple" comes in two kinds:

- **Good simplicity** = the body's build is simple (truly light). This is welcome.
- **Bad simplicity ①** = the gatekeeper is so strict that you get a pseudo-honor-student who learns nothing (= the trap of the cheapest ∞ gatekeeper).
- **Bad simplicity ②** = an individual that has degenerated into "saying nothing" (= sticking to a unigram). Safe and cheap, but incompetent. A parasite that trimmed so much it can no longer fend for itself.

llcore has an eye (a soundness oracle) that sees through "whether it is truly stable," so it can **tell good simplicity apart from degenerate simplicity**. This is the FullSense worldview —— "evolve not merely to be clever, but in a direction where one can prove it is cheap and safe."

## The honest breakdown: "the inspector makes it smart" was an overstatement

Finally, the story I cut the most today. We had a result that "the stronger the gatekeeper, the smarter the AI gets." The numbers are real. But when you doubt the breakdown ——

Even when we shuffled the text into a mess so that there was "zero substance to learn," **the difference between gatekeepers did not vanish**. In other words, this difference was not because it "learned the language," but a phenomenon unrelated to substance: "**ease of evolving (ease of moving)**." Furthermore, when we trained hard with gradients instead of evolution, the result was the same for every gatekeeper — the benefit of a strong gatekeeper was "limited to evolution (random mutation)."

It is not a defeat. **Doubt the breakdown before you feel like you've won** —— this is the core of FullSense research ([feedback_benchmark_honest_disclosure]). The real finding was the more accurate description: "the inspector's payoff is not learning but evolvability."

---

The point in 3 lines:
- An evolving AI's checkpoint (the inspector) **explodes as 2ⁿ** and breaks down as the rooms increase.
- With a **sound estimate that takes the whole thing in at a glance (B2)** instead of looking at every corner, we passed nearly 80% at 10,000× speed with zero oversights.
- "Turning cost into evolutionary selection pressure" + "honest disclosure that doubts the breakdown" —— toward an AI that travels light and does not pretend to be clever.

(The main article has the exact numbers, tables, and figures. The preceding installment = #35: the ladder of inspectors.)
