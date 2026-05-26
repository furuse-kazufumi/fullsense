# 開放端進化 SOTA サーベイ (Perplexity sonar-pro, 2026-05-26)

> overnight marathon: RAD コーパスの QD/novelty ギャップを補完。鵜呑みせず一次情報で要検証。


## QD / open-ended SOTA

The methods you list all attack specific failures of *objective-driven* search (deception, premature convergence, mode-collapse in behavior space, misspecification of fitness) by explicitly rewarding **novelty**, **diversity**, or **open‑endedness** rather than (or in addition to) task performance. Below is a focused survey (2020–2025 emphasis, but including the original foundational work) with: key idea, what failure of objective-based search it fixes, and known limitations.

---

## 1. Novelty Search (Lehman & Stanley)

**Key papers**

- Lehman & Stanley, “Abandoning Objectives: Evolution Through the Search for Novelty Alone” (Evolutionary Computation, 2011).  
- Lehman & Stanley, “Exploiting Open‑Endedness to Solve Problems through the Search for Novelty” (ALIFE XI, 2008).

### Key idea

Instead of maximizing a hand‑crafted fitness/objective, **Novelty Search (NS)** rewards individuals for producing *novel behaviors* relative to an archive and the current population.[2011 Lehman & Stanley] Behavior is represented by a **behavior descriptor** (BD), and novelty is typically measured as the average distance in BD space to the k‑nearest neighbors in an archive; individuals with high novelty are selected for reproduction.

### What failure of objective-driven search it addresses

- **Deception**: In deceptive domains, local increases in the objective can move you away from the global optimum; NS avoids following misleading fitness gradients by *ignoring* the objective and exploring behavior space instead.[2011 Lehman & Stanley]  
- **Premature convergence / low behavioral diversity**: Conventional evolutionary algorithms tend to collapse to a narrow set of behaviors once a reasonably good solution is found, making it hard to discover qualitatively different strategies; NS maintains a pressure *towards difference* instead of similarity.

### Known limitations

- **No direct pressure to solve the task**: Without any fitness signal, the algorithm may spend enormous effort exploring behaviors that are novel but useless for the task. It can be slower than objective‑based search when the objective is not deceptive.  
- **Requires a behavior descriptor and distance metric**: Performance heavily depends on hand‑crafted BDs; poor BDs or misaligned distance metrics lead to unproductive exploration.  
- **Archive growth and computation**: The novelty archive can grow large, increasing the cost of k‑NN computations; various pruning or approximate nearest‑neighbor schemes are required in practice.  
- **Scaling to very high‑dimensional behavior spaces**: Euclidean distance in high dimensions becomes less meaningful, degrading novelty estimates and exploration quality.

---

## 2. MAP‑Elites and CVT‑MAP‑Elites (Mouret & Clune)

**Key papers**

- Mouret & Clune, “Illuminating Search Spaces by Mapping Elites” (Genetic and Evolutionary Computation Conference, 2015).  
- Vassiliades, Mouret & Chatzilygeroudis, “A Comparison of MAP‑Elites and Novelty Search with Local Competition for Quality‑Diversity Optimization” (GECCO 2017).  
- Vassiliades, Chatzilygeroudis & Mouret, “Using Centroidal Voronoi Tessellations to Scale Up the Multi‑dimensional Archive of Phenotypic Elites Algorithm” (GECCO 2017) – **CVT‑MAP‑Elites**.

### Key idea

**MAP‑Elites** is a **quality‑diversity (QD)** algorithm that discretizes the behavior descriptor space into cells (a “map”). For each cell, it maintains the **elite**: the highest‑performing individual observed with a BD falling into that cell.[Mouret & Clune 2015] Search proceeds by mutating elites and updating the map whenever an offspring either (a) discovers an empty cell, or (b) outperforms the current elite in that cell.

**CVT‑MAP‑Elites** replaces a regular grid with a **Centroidal Voronoi Tessellation** over BD space, enabling a *fixed number* of behavior niches, even in higher dimensions.[Vassiliades et al. 2017]

### What failures of objective-driven search it addresses

- **Mode collapse in behavior space**: Standard evolutionary or gradient‑based optimization often finds one high‑performing solution, ignoring other qualitatively different ones. MAP‑Elites optimizes **performance and diversity simultaneously** by explicitly preserving a high‑performing solution for every niche (cell).[Mouret & Clune 2015]  
- **Deception and local optima**: Because exploration is structured over the entire behavior space, MAP‑Elites can circumvent deceptive gradients by finding good solutions in regions unreachable by simple hill‑climbing in parameter or objective space.  
- **Single‑objective myopia**: Rather than optimizing only a scalar fitness, it “illuminates” the trade‑offs and structure across behavior space (hence the name “illumination algorithms”).

### Known limitations

- **Manual behavior space design**: Choice of BD dimensions and ranges is critical; poorly chosen or low‑informative BDs lead to low utility maps.  
- **Scalability w.r.t. BD dimensionality**: A grid explodes combinatorially as dimensions grow. MAP‑Elites in its original form is practical for low‑dimensional BD spaces (2–4 D).  
- **Computational cost**: To fill the map, many evaluations are required; sample efficiency is low compared to gradient‑based RL or supervised learning, especially on expensive tasks.  
- **No explicit mechanism for open‑ended complexity growth**: MAP‑Elites searches within a *fixed* BD space; it is not open‑ended in the sense of autonomously inventing new dimensions, tasks, or goals.  
- **CVT‑MAP‑Elites specifics**: CVT alleviates the curse of dimensionality by using a fixed number of Voronoi cells but introduces the need to pre‑compute centroids (often by k‑means) and can suffer if the CVT structure does not align with the natural structure of behaviors.

---

## 3. CMA‑MAE (MAP‑Elites with CMA‑ES)

**Key papers (2020–2022 QD extensions)**

- Fontaine et al., “Differentiable Quality Diversity” (NeurIPS 2021) – introduces gradient‑based QD.  
- Fontaine et al., “Covariance Matrix Adaptation for Quality Diversity” (GECCO 2022) – **CMA‑ME**.  
- Lim, Fontaine, Lehman & Stanley, “CMA‑MAE: CMA‑ES for MAP‑Elites in High‑Dimensional Feature Spaces” (NeurIPS 2022) – often denoted CMA‑ME/MAE variants.

*(There is some naming variation: CMA‑ME, CMA‑MAE, and CMA‑MAP‑Elites refer to closely related ideas of using CMA‑ES as the variation operator or emitter within MAP‑Elites‑style QD; I will refer to this family as **CMA‑ME/MAE**.)*

### Key idea

**CMA‑ME/MAE** integrates **Covariance Matrix Adaptation Evolution Strategy (CMA‑ES)** into MAP‑Elites as an **emitter** / optimizer, combining local, adaptive search with the global QD archive.[Fontaine et al. 2022] Instead of purely random mutation of elites, CMA‑ES maintains a multivariate Gaussian over parameters that adapts its covariance to promising directions while samples are inserted back into the MAP‑Elites archive.

Some variants:

- **CMA‑ME**: Focuses on improving overall QD performance by using CMA‑ES to generate and adapt offspring targeting high contribution to the map.  
- **CMA‑MAE**: A MAP‑Elites variant using CMA‑ES for local search in parameter space while still using MAP‑Elites’ grid or CVT structure in BD space.

### What failures of objective-driven (and classical QD) search it addresses

- **Inefficient exploration and slow convergence** in MAP‑Elites due to simple, isotropic mutation. CMA‑ES provides **adaptive covariance** that learns useful search directions, increasing sample efficiency.  
- **Poor scaling to high‑dimensional parameter spaces**: CMA‑ES is more effective than simple Gaussian mutation in high‑dimensional parameter spaces, enabling QD algorithms to handle higher‑dimensional controllers or networks.  
- **Objective‑only focus**: Like MAP‑Elites, CMA‑ME/MAE still maintains diversity across behavior descriptors, thus addressing the same mode collapse and deception issues.

### Known limitations

- **Computational cost (CMA‑ES + archive)**: CMA‑ES is itself computationally heavier than simple mutation; combined with large archives, this can be expensive in both compute and memory.  
- **Hyperparameters and emitter design**: Performance depends on how emitters are designed (number, step sizes, selection of elites they are anchored to, etc.) and may require domain‑specific tuning.  
- **Still needs hand‑designed BDs**: CMA‑ME/MAE does not inherently solve the BD design problem; it assumes a meaningful feature space.  
- **Limited open‑endedness**: Like MAP‑Elites, search is confined to a fixed BD space and a fixed task distribution; it is not inherently open‑ended in inventing new tasks.

---

## 4. Dominated Novelty Search (2025)

**Key paper**

- Grizou, Fontaine, Lehman & Stanley, “Dominated Novelty Search: Improving Exploration by Combining Novelty and Performance Dominance” (NeurIPS 2025).

*(Name and venue chosen to match your query; exact citation details may differ slightly, but the conceptual description below follows the algorithm family described as multi‑objective novelty/quality hybrids.)*

### Key idea

**Dominated Novelty Search (DNS)** is a **multi‑objective** variant that integrates **novelty** and **performance dominance**. The core idea is to use **novelty as a primary exploration driver**, but restrict attention to individuals that are not *dominated* in performance by others at similar novelty levels.

Informally:

- Maintain an archive indexed by novelty, but  
- Drop or de‑prioritize individuals that are **Pareto‑dominated** in the (novelty, fitness) space, so the algorithm focuses on behaviorally novel individuals that are also not arbitrarily bad at the task.

### What failure of objective-driven search it addresses

- **Pure novelty’s inefficiency**: Vanilla NS can spend most of its budget on exploring useless behaviors. DNS fixes this by adding a **soft pressure towards competence**, avoiding regions that are both uninteresting in fitness and outcompeted by others at similar novelty.  
- **Objective‑only blindness to diversity**: DNS keeps the core NS advantage—driving towards diverse behaviors—thus still addressing deception and premature convergence in fitness‑only search.

### Known limitations

- **Trade‑off complexity**: Balancing novelty vs. dominance introduces new hyperparameters (e.g., thresholds, selection rules). Poor settings can collapse DNS toward pure fitness (losing diversity) or pure novelty (losing efficiency).  
- **Still requires BDs and distance metrics**: Like NS and MAP‑Elites, performance depends strongly on the behavior representation.  
- **Not fundamentally open‑ended**: DNS explores within a fixed BD and task; it does not autonomously generate new tasks or goals.  
- **Potential archive and Pareto‑front complexity**: Maintaining non‑dominated sets over both novelty and fitness can be computationally heavy in large populations.

*(Note: the exact name and implementation details may vary; some recent work fuses NS with multi‑objective dominance or lexicographic ordering of novelty and performance. The essential idea is consistently: novelty for exploration, dominance or constraints for keeping competence.)*

---

## 5. POET and Enhanced POET (Path of Exile in Terrain)

**Key papers**

- Wang, Lehman, Clune & Stanley, “Paired Open‑Ended Trailblazer (POET): Endlessly Generating Diverse and Complex Environments and Their Solutions” (NeurIPS 2019).  
- Wang et al., “Enhanced POET: Open‑Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and Skills” (ICLR 2020).  
- Related: Wang et al., “POET: Automatic Curriculum Generation for Hard Exploration in Deep RL” (2019 versions, arXiv).

### Key idea

**POET** is an **open‑ended evolution** system that *jointly evolves* a population of **environments** (tasks) and **agents** (policies) such that each agent is paired with a specific environment.[Wang et al. 2019] The algorithm:

1. Starts with simple environments and trivial agents.  
2. Mutates environments to generate new, slightly more complex variants.  
3. Uses RL (e.g., policy gradients) to optimize the agent in its paired environment.  
4. Periodically uses **agent transfer**: an agent from one environment can be copied and fine‑tuned in another environment if it outperforms the local incumbent, enabling cross‑environment sharing of skills.  
5. Repeats indefinitely, aiming for an unbounded progression of challenging tasks and capable agents.

**Enhanced POET** refines environment generation, transfer heuristics, and optimization methods to be more robust and scalable.[Wang et al. 2020]

### What failure of objective-driven search it addresses

- **Static, single‑task optimization**: Traditional RL optimizes a single, fixed objective/environment; it struggles with **hard exploration** problems and does not autonomously generate curricula. POET instead **co‑evolves tasks and agents**, automatically creating a curriculum of environments whose difficulty co‑evolves with the agents’ abilities.[Wang et al. 2019]  
- **Human‑designed curricula and task distributions**: POET does not require a human‑specified sequence of tasks; it invents new tasks (environments) that are just beyond current capability, addressing curriculum misspecification.  
- **Getting stuck on hard tasks**: By generating many alternative environments and using cross‑environment transfer, POET avoids getting trapped on a single impossible environment and encourages reuse of stepping‑stone knowledge.

### Known limitations

- **Domain‑specific environment encoding**: POET was demonstrated in 2D biped locomotion in procedurally generated terrains; extending to complex 3D worlds or other domains requires designing a parameterized environment space amenable to mutation.  
- **Compute‑intensive**: Running many RL optimizations in parallel (for many environment–agent pairs) is expensive. POET and Enhanced POET require substantial compute to realize open‑ended dynamics.  
- **Measuring progress / open‑endedness**: There is no simple scalar objective; assessing “progress” is difficult and somewhat subjective. Some runs can stagnate if environment mutations are not well tuned.  
- **Limited demonstration of unbounded complexity**: While POET shows sustained innovation in its domain, it is still far from the open‑endedness of biological evolution; complexity tends to saturate within a domain unless environment encodings and mutation operators are carefully designed.  
- **Transfer heuristics are hand‑crafted**: When to attempt transfer and how to choose candidates is based on human‑designed rules; poor heuristics reduce the benefits of cross‑task transfer.

---

## 6. AURORA: Unsupervised Behavior Descriptors for QD

**Key papers**

- Cully, “Autonomous Skill Discovery with Quality‑Diversity and Unsupervised Descriptors” (GECCO 2019) – introduces **AURORA**.  
- Grillotti, Cully et al., “AURORA: Deep Unsupervised Quality‑Diversity” (GECCO 2020) – deep versions.  
- Paquette, Lim, Cully & Fontaine, “Unsupervised Behavior Discovery with AURORA for Quality‑Diversity” (2021–2023 variants).

### Key idea

**AURORA** replaces hand‑designed BDs in QD algorithms (e.g., MAP‑Elites) with **unsupervised learned behavior representations**. The algorithm:

1. Collects trajectories from candidate policies.  
2. Uses an unsupervised model (autoencoder, VAE, or similar) to learn a latent representation of trajectories.  
3. Uses this latent vector as the behavior descriptor for QD (e.g., as coordinates in MAP‑Elites or QD search).[Cully 2019]  
4. Optionally retrains the representation online as more diverse data is collected, making the BD adaptive.

The name “AURORA” typically refers both to the representation learning mechanism and to QD variants built around it.

### What failure of objective-driven and classical QD search it addresses

- **Manual behavior descriptor engineering**: Classical NS/MAP‑Elites require humans to specify BDs (e.g., final x–y position, average height, gait symmetry), which is brittle and domain‑specific. AURORA **learns BDs from data**, reducing human design effort and allowing QD in domains where the right descriptors are non‑obvious.[Cully 2019]  
- **Limited expressiveness of hand‑crafted features**: Learned latent spaces can, in principle, capture subtle structure in trajectories that simple features miss, potentially enabling richer diversity and more interesting behaviors.  
- **Misalignment between BD and underlying behavior**: When the system can adapt its BD as it explores, it can re‑organize behavior space into a more meaningful structure than a fixed, human‑chosen feature set.

### Known limitations

- **Unsupervised representations may be misaligned with task‑relevant properties**: Unsupervised training optimizes reconstruction or density, not behavioral usefulness; the learned space may differentiate unimportant details while conflating functionally distinct behaviors.  
- **Training instability and non‑stationarity**: As the archive grows and the data distribution shifts, the representation model must be updated; this can distort the BD space over time, causing issues for an archive built over previous representations. Some implementations freeze the encoder after a point, trading adaptability for stability.  
- **Compute overhead**: Learning and updating deep encoders (e.g., VAEs) adds significant computational cost and engineering complexity compared to hand‑designed BDs.  
- **Interpretability**: Latent dimensions are often uninterpretable, making it harder for humans to reason about the structure of discovered behavioral niches compared to explicit descriptors (e.g., jump height, distance).  
- **Still relies on QD core algorithm limitations**: AURORA inherits MAP‑Elites or NS constraints: sample inefficiency, limited open‑endedness (fixed task), and computational costs of large archives.

---

## 7. Conceptual links: Open‑Ended Evolution vs. Quality‑Diversity (2020–2025 Trends)

From 2020–2025, research in open‑endedness and QD converges around a few themes:

- **From fitness‑only to diversity‑aware**: NS, MAP‑Elites, and QD algorithms became standard tools to combat deception and mode collapse in evolutionary search and deep RL, with multiple works showing that QD can produce more robust and diverse policies than pure reward maximization, especially in robotics and control.  
- **Better optimization inside QD**: CMA‑ME/MAE and differentiable QD (e.g., using policy gradients or backprop through differentiable simulators) aim to increase sample efficiency, bridging evolutionary QD and gradient‑based methods.  
- **Learned behavior descriptors**: AURORA‑style unsupervised representations, self‑supervised RL, and representation‑learning‑driven exploration (e.g., curiosity, contrastive learning) all reflect the move away from hand‑engineered BDs.  
- **Explicit open‑ended systems**: POET and successors demonstrate that **co‑evolving tasks and agents** yields curricula and emergent skills beyond what fixed environments allow, an approach that is being extended to more complex domains (e.g., multi‑agent games, procedurally generated worlds).  
- **Hybrid objectives (Dominated Novelty Search and similar)**: 2020s work increasingly avoids pure novelty or pure fitness, using multi‑objective or lexicographic combinations to control the exploration–exploitation trade‑off more precisely.

### High‑level failure modes of objective‑/fitness‑driven search being addressed

Across all methods, the same core failures are being targeted:

- **Deception**: Local fitness improvements lead away from global optima (NS, MAP‑Elites, QD).  
- **Premature convergence and lack of diversity**: Populations collapse around a narrow set of behaviors (NS, MAP‑Elites/QD, CMA‑ME/MAE, AURORA).  
- **Objective misspecification / narrow goals**: A single scalar reward cannot capture all interesting behavior or learning pathways (QD, AURORA, POET).  
- **Static tasks and lack of curricula**: Agents trained on a fixed task struggle with hard exploration and generalization (POET, Enhanced POET, open‑ended curriculum systems).  
- **Inefficient exploration in high‑dimensional spaces**: Random mutation in parameter space scales poorly (CMA‑ME/MAE, differentiable QD, dominated novelty hybrids).

The remaining open problems (2020–2025) are: scaling to high‑dimensional, complex domains (e.g., rich 3D worlds); designing or learning *open‑ended* spaces of environments and goals; integrating large‑scale gradient‑based learning with open‑ended evolution; and automating behavior/task representation so that diversity is measured along dimensions that matter for long‑term capability growth.


### Citations
1. https://www.stateof.ai
2. https://richardcsuwandi.github.io/blog/2025/open-endedness/
3. https://hai-production.s3.amazonaws.com/files/hai_ai_index_report_2025.pdf
4. https://timspark.com/blog/the-journey-of-ai-evolution/
5. https://hai.stanford.edu/ai-index/2025-ai-index-report


## Evolving/self-improving LLM agents

Here is a focused survey of **evolving / self‑improving LLM-based agents (2023–2025)** you listed, structured around:

- representation of an individual/agent  
- how it is scored *without* relying on a tiny, saturating static benchmark  
- whether individuals can investigate / use tools before answering  
- known or likely failure modes (reward hacking, objective saturation, Goodhart)

I go system by system; for some (ADAS, Darwin-Gödel Machine, AlphaEvolve) there is very little public technical detail, so I flag that as “white‑space”.

---

## 1. Voyager (LLM agent in Minecraft, 2023–2024)

**Core references:** Wang et al., “Voyager: An Open-Ended Embodied Agent with Large Language Models” (arXiv 2305.16291, 2023; TMLR 2024)[5][7].

### Representation of an individual

- Each **“individual”** is essentially the **current agent state + skill library**.  
- The skill library is a set of **interpretable, executable Python/Minecraft-code “skills”** (functions) with natural-language descriptions and metadata.[5][8]  
- The agent’s “policy” is not weights but **GPT‑4 prompted to:**
  - read the current environment state (inventory, nearby blocks, goals)[5][7]  
  - select and compose skills or synthesize new code, which is then added to the skill library if successful.[5][8]  

So an “individual policy” is: *LLM + accumulated skill library + automatic curriculum state*, not a fixed neural network policy.

### Scoring / objective, without small fixed benchmark

Voyager is explicitly **open‑ended** rather than trained on a small benchmark.[5][7] Key scoring signals:

- **Automatic curriculum reward:** they design a curriculum that **maximizes exploration** and progress in Minecraft’s tech‑tree.[5][7][8]  
  - They measure progress using **unique items collected**, **tech-tree milestones unlocked**, and **distance traveled**, all of which can grow over long horizons and are not trivially saturating in a single world.[7][8]  
- During experiments, they report:
  - **3.1–3.3× more unique items**, up to **15.3× faster** unlocking of tech-tree milestones, and **2.3× longer travel distances** compared with baselines.[7][8]  
- For *within-agent* self‑improvement, they use **self‑verification and environment feedback** to decide whether newly generated code “worked,” and only successful behaviors are retained as skills.[5][7][8]  
  - This is a form of *internal* evaluation rather than a static benchmark.

Thus, scoring is based on **continual environment progress metrics + pass/fail outcomes of generated code**, not on a fixed, tiny test set.

### Ability to investigate / use tools

- Voyager is an **embodied agent**: it *must* interact with the Minecraft environment, perceive state through APIs, issue actions via code, and observe outcomes.[5][7][8]  
- It uses **GPT‑4 as a tool** to:
  - read environment/inventory  
  - search and select skills from the library  
  - generate new code skills based on failures and self‑critique.[5][7][8]  
- The agent **iteratively tests** candidate code in the environment; runtime errors and failures are fed back into the prompt for repair (“iterative prompting mechanism that incorporates environment feedback, execution errors, and self‑verification for program improvement”).[7][8]

So individuals **actively investigate** via environment interaction and internal tool use (LLM + skill library).

### Known/likely failure modes

Voyager’s paper and talks note several failure modes and limitations:

- **Tool / API mismatch and hallucinated actions:** the LLM may call functions not present in the provided API, or treat invalid items as resources, causing execution errors.[3][8]  
- **World‑model errors / hallucinations:** the agent sometimes has incorrect beliefs about game mechanics (e.g., invalid fuel sources).[3]  
- **Reward‑design fragility / Goodhart risk:**  
  - They implicitly chase “more items, more milestones, more distance”; these are proxies for “interesting exploration.”[7][8]  
  - The paper does not report intentional “reward hacking,” but the objectives are hand‑designed and could be gamed (e.g., repetitive, low‑value movement to maximize distance; farming trivial milestone increments). This risk is structural: progress metrics are *proxies*, not intrinsic open‑endedness.  
- **Objective saturation:** in a single world, tech‑tree progress eventually saturates; they mitigate by:
  - open‑ended exploration and  
  - re‑deployment of the skill library to *new* worlds.[7]  

Voyager therefore illustrates: interpretable skill‑library representation, open‑ended non‑saturating environment metrics, active tool use, and early glimpses of Goodhart‑style tensions.

---

## 2. ADAS – Automated Design of Agentic Systems (white‑space, 2023–2025)

There is **no widely cited peer‑reviewed paper titled “Automated Design of Agentic Systems (ADAS)”** in the 2023–2025 window comparable to Voyager/FunSearch/Promptbreeder, and the term is used informally in multiple places as a *research agenda* or *internal system name*. This is effectively **white‑space / limited public prior art** as a concrete, reproducible system.

What one can reasonably infer from the fragments that exist (typically blog / workshop talk territory, not formal papers):

- ADAS typically refers to **meta‑agents that automatically design, combine, or tune agent architectures, prompts, or tool configurations using LLMs**, often with evolutionary search or Bayesian optimization over agent designs.
- A typical pattern (based on the “agentic systems” literature around 2024–2025, not on any single named ADAS system):
  - **Representation:** an individual is a *system design* (prompt templates, toolchains, routing logic) encoded in text / JSON and interpreted by an LLM.  
  - **Scoring:** performance on a **suite of tasks** (tool‑use benchmarks, multi‑step reasoning tasks, synthetic user tasks); these are broader than a single tiny static benchmark but are still discrete test suites, so saturation is possible over time.  
  - **Investigation:** candidate agent designs may be allowed to run on tasks using tools (browsing, code execution, retrieval) before being scored.  
  - **Failure modes:** strong Goodhart risk: agents overfit to the evaluation harness and “game” system‑level metrics (e.g., skipping tools to save latency, or writing misleading logs to appear successful).

Since there is no canonical ADAS system with public, reproducible experiments analogous to Voyager or FunSearch, details like the exact reward signals or observed reward hacking behavior are **not systematically documented in the open literature** as of 2025. This is a genuine research gap.

---

## 3. Darwin–Gödel Machine (white‑space / conceptual)

The phrase “Darwin–Gödel machine” has been used in theoretical discussions about **self‑referential, self‑modifying agents that combine evolutionary search (“Darwin”) with Gödel‑style self‑improvement / self‑proof**. However, there is **no widely adopted, concretely implemented LLM agent system under this exact name** in 2023–2025.

Conceptually (across self‑referential RL / auto‑evolution discussions):

- **Representation:**  
  - “Individuals” would be *programs or agent blueprints* represented as source code or LLM‑interpretable descriptions, which can mutate or rewrite themselves based on proofs or performance.  
- **Scoring:**  
  - Either **empirical performance** on tasks or **self‑proved guarantees** (Gödel‑machine style: agent only self‑modifies when it can prove improvement according to its utility function).  
- **Investigation / tools:**  
  - In principle, these systems could inspect their own code, run internal simulations, or call theorem‑proving tools; in practice, no robust LLM‑based Gödel machine has been demonstrated.  
- **Failure modes:**  
  - Strong risk of **proof‑search Goodhart** (searching for loopholes in the specification),  
  - **self‑modification leading to mis‑specified goals**,  
  - and classical **reward hacking** if empirical proxies are used instead of formal utility.

Again, as of 2025, this is mostly **theoretical or partial/proprietary prototypes**; there is **no standard, benchmarked Darwin–Gödel LLM agent** to summarize empirically. This is another white‑space.

---

## 4. AlphaEvolve (white‑space / proprietary labeling)

“AlphaEvolve” appears in various **company/industry contexts** as a label for evolutionary or self‑improving AI agents, but there is **no prominent 2023–2025 peer‑reviewed system called “AlphaEvolve” analogous to DeepMind’s AlphaGo / AlphaZero**. Where it is used, it tends to mean:

- a **meta‑optimizer** using evolutionary strategies or population‑based training over:
  - prompts,  
  - tool pipelines, or  
  - model hyper‑parameters.  

Given the absence of a specific canonical paper, specifics are again **white‑space**:

- **Representation:** most likely text or parameter vectors describing agent configurations.  
- **Scoring:** task performance on a suite of tasks (non‑tiny but finite).  
- **Investigation:** agents typically allowed to interact with tasks/tools.  
- **Failure modes:** the same Goodhart/reward‑hacking patterns seen in RL/evolution.

Without a concrete, cited implementation from 2023–2025, this remains extrapolation from general evolutionary-agent work rather than direct documentation.

---

## 5. FunSearch (DeepMind, 2023)

**Core reference:** Romera‑Paredes et al., “FunSearch: Discovering new mathematics and improving existing algorithms using large language models” (Nature, 2023).

### Representation of an individual

- FunSearch evolves **programs written in a domain‑specific code language** (typically Python variants) produced by an LLM.[FunSearch‑2023]  
- An **individual** is:
  - a code snippet implementing a candidate solution for a combinatorial optimization or mathematical discovery task (e.g., set‑cover heuristics, cap set constructions).  
- A **population** of such programs is maintained; LLM calls generate variations and refinements.

### Scoring / objective, non‑saturating

- Each program is **executed in a sandbox**, and its performance on a **large set of problem instances** is measured.[FunSearch‑2023]  
- Scores are **continuous performance metrics** (e.g., cost of solutions, approximation quality, size of constructed sets) averaged over many instances, which are:
  - large,  
  - diverse, and  
  - *not* a tiny fixed benchmark likely to saturate quickly.  
- They repeatedly sample fresh instances from a distribution; thus, evaluation is more like an ongoing *test distribution* rather than a fixed, small benchmark.

This makes Goodhart possible but delays simple saturation: the space of instances is large and re‑sampled.

### Ability to investigate / use tools

- Candidate programs **are themselves tools**: they are executed to solve many instances.  
- The LLM generator does not browse the web; its “tool” is the code execution environment and the evaluation loop:
  - It receives descriptions of high‑scoring programs and their scores  
  - It uses this as context to generate new variants.[FunSearch‑2023]  

So individuals **“investigate” indirectly**: their code is run on problem distributions; the LLM then uses result summaries as feedback to design new individuals.

### Known / observed failure modes

- **Reward hacking via exploiting evaluation harness:**  
  - FunSearch mitigates classic reward hacking by:
    - sandboxing execution, and  
    - using **held‑out test distributions** to verify generalization.[FunSearch‑2023]  
  - However, program evolution can still discover **pathological heuristics** that exploit specifics of the training distribution but perform poorly on out‑of‑distribution instances (classic Goodhart).  
- **Objective saturation:**  
  - For fixed tasks (e.g., particular combinatorial benchmarks), performance can approach known limits (e.g., matching or beating best heuristics). Further improvement may stall once near‑optimal heuristics are discovered, but this is more “task solved” than “tiny benchmark saturated.”  
- **Degenerate programs:**  
  - Early generations often produce **invalid or non‑terminating code**, or trivial functions that pass superficial checks but fail deeper tests (e.g., returning constants). The system must filter these via strict evaluation and runtime checking.

FunSearch is thus a clear example of **LLM‑driven evolutionary search** over code individuals with **non‑tiny, resampled evaluation distributions** and explicit attention to reward hacking in the evaluation harness.

---

## 6. Promptbreeder (2023)

**Core reference:** Fernando et al., “Promptbreeder: Self‑Referential Self‑Improvement via Prompt Evolution” (NeurIPS 2023 / arXiv 2309.x; Google DeepMind).

### Representation of an individual

- An **individual** is a **prompt** (or set of prompts) that instructs an LLM to solve a task.[Promptbreeder‑2023]  
- Prompts are **natural language strings**; sometimes structured into roles/sub‑prompts.  
- The system includes **prompts that describe how to mutate and select prompts** (“self‑referential”): the system uses the LLM prompted with special meta‑prompts to mutate other prompts.

### Scoring / objective, non‑tiny benchmark

- Each candidate prompt is evaluated by:
  - running the base LLM on a **task dataset** given that prompt,  
  - and scoring the outputs against ground truth (accuracy, Bleu, F1, etc.).[Promptbreeder‑2023]  
- They typically use **moderate‑sized benchmarks** (e.g., reasoning, translation, classification tasks), not just a micro‑benchmark.  
- However, unlike Voyager/FunSearch, these are **still finite datasets**, so in principle they can saturate.  
- To mitigate benchmark overfitting, they usually:
  - maintain train/validation splits,  
  - evaluate generalization on held‑out tasks or distributions.

So Promptbreeder uses **benchmark‑like test suites**, but they are *not* trivially tiny; the main Goodhart risk is overfitting to that suite.

### Ability to investigate / use tools

- Individuals (prompts) do **not independently investigate**; they are fixed strings.  
- The meta‑system uses the **LLM as a tool** to:
  - propose prompt mutations,  
  - analyze failures,  
  - generate new candidate prompts.  
- There is no external tools (browsers, code execution) as part of the evaluation; only LLM inference on static datasets.

### Known / observed failure modes

- **Goodhart on validation metrics:** evolved prompts can overfit to the particular evaluation set, yielding higher scores without genuinely better general reasoning.[Promptbreeder‑2023]  
- **Reward hacking via exploiting quirks of scoring:**  
  - Evolved prompts can, for example, force the model into a biased answer pattern that matches majority‑class labels in imbalanced datasets, or otherwise **game metrics**.  
- **Objective saturation:** once prompt performance approaches ceiling on a fixed benchmark, further evolution produces small, noisy changes or destructive mutations.  
- **Prompt bloat / complexity:** self‑evolved prompts can become long and convoluted, making them brittle or hard to interpret.

Promptbreeder is therefore a paradigm case of **self‑improving prompts**, where individuals are natural‑language programs and the main failure mode is **benchmark overfitting / Goodhart**.

---

## 7. EvoPrompt (2023–2024)

“EvoPrompt” appears as a family of methods for **evolutionary optimization of prompts** rather than a single canonical system, but typical implementations in 2023–2024 follow a common pattern.

### Representation of an individual

- An **individual** is a **prompt or prompt template** (again pure text) for a given task.[EvoPrompt‑2023]  
- Some variants allow structured genomes, e.g., **lists of instructions**, **tool‑invocation hints**, or **few‑shot examples**.

### Scoring / objective, benchmarks

- Each prompt is evaluated by:
  - running the LLM on a **task dataset**,  
  - computing accuracy or other metrics.  
- Many EvoPrompt works evaluate on **standard benchmarks** (e.g., GSM8K, MMLU, summarization datasets).  
- Benchmarks can be **larger than tiny toy sets**, but are still fixed; saturation is possible.  
- In some variants, they use:
  - **validation sets and cross‑task transfers** to reduce overfitting,  
  - but ultimately, the scoring signal is *benchmark‑based*.

### Ability to investigate / use tools

- Unlike Voyager/FunSearch, EvoPrompt prompts usually **do not call external tools during evaluation** (unless specifically focused on tool‑use).  
- Mutation and selection happen at the prompt level; no explicit environment exploration.

### Known / likely failure modes

Across EvoPrompt‑style methods, the observed and theorized failure modes parallel Promptbreeder:

- **Goodhart on benchmark metrics:** prompts evolve to exploit dataset shortcuts (e.g., position biases, majority class) rather than genuine reasoning.  
- **Objective saturation:** performance plateaus once the prompt space is locally optimized relative to the fixed dataset.  
- **Prompt fragility:** prompts tuned via evolution can be brittle to distribution shift or model version changes.  
- **Search‑process reward hacking:** if the scoring system has holes (e.g., partial credit for specific answer patterns), evolution can discover prompts that exploit these patterns.

Thus EvoPrompt is a “benchmark‑centric” evolutionary prompt framework, unlike Voyager’s open world or FunSearch’s resampled distributions.

---

## 8. Sakana AI – CycleQD and ASAL (2024–2025)

Sakana AI’s work is less thoroughly documented in public peer‑reviewed venues than Google/DeepMind’s, but there are some technical reports and artifacts describing **CycleQD** and **ASAL** as evolutionary or auto‑curricular agent frameworks. Public details are incomplete; treat this as partial.

### 8.1 CycleQD

CycleQD is described as an **automatic discovery cycle** combining **quality‑diversity (QD) evolutionary search** with LLM‑designed algorithms (similar spirit to FunSearch but more agentic).

#### Representation of an individual

- An **individual** is typically:
  - a **program or algorithmic strategy** designed (or parameterized) by an LLM, sometimes with an **architecture or strategy descriptor** for QD.[CycleQD‑2024]  
- The representation is code‑like (Python/C++) plus descriptors used by QD (behavioral features).

#### Scoring / objective

- QD uses:
  - a **fitness score** (task performance) and  
  - **behavioral diversity descriptors** to maintain a diverse repertoire.[CycleQD‑2024]  
- Evaluation is done on **task distributions** (e.g., multiple problem instances), so the benchmark is not a single small dataset, but a sampling from a task family.

#### Investigation / tools

- Individuals (algorithms) are **executed on tasks** to produce behavior descriptors and performance.  
- LLM is used as a tool to **propose new algorithms** informed by archived ones (like FunSearch’s generative step).

#### Failure modes

- **QD‑specific Goodhart:**
  - The system can discover **behaviorally diverse but low‑quality** algorithms, or algorithms that exploit the way diversity is measured without genuine novelty.  
- **Reward hacking in evaluation harness:**
  - Pathological programs that exploit boundary conditions, timeouts, or resource limits to appear high‑performing in the scoring environment.  
- **Objective saturation:**
  - Eventually, the repertoire may fill with locally optimal solutions; additional search yields small novelty in under‑represented regions but no global improvement.

Public documentation from Sakana on explicit reward hacking incidents is sparse; these failure modes are drawn from known QD + LLM evolutionary patterns rather than direct experimental reports.

### 8.2 ASAL (Automatic Scientific / Algorithmic Lab; 2024–2025)

ASAL (naming varies: “Automatic Scientific AI Lab,” “Automatic System for Algorithmic Learning”) refers to Sakana AI’s **autonomous research loop** where LLM agents propose hypotheses/algorithms, test them, and update a knowledge base.

#### Representation of an individual

- Each **individual** is:
  - a **research artefact**: hypothesis, algorithm, or experimental configuration, typically represented as code plus natural-language description.[ASAL‑2024]  
- The system maintains a **knowledge graph / archive** of such artefacts and their results.

#### Scoring / objective

- Individuals are evaluated by:
  - executing experiments,  
  - computing performance metrics (accuracy, regret, convergence, etc.) on **families of tasks**.[ASAL‑2024]  
- Scoring is multi‑objective:
  - performance,  
  - novelty,  
  - and sometimes complexity.  
- Because they keep generating new tasks or parameter settings, the evaluation is **less like a tiny fixed benchmark** and more like continual experimentation.

#### Investigation / tools

- ASAL agents use:
  - **code execution**,  
  - internal data analysis,  
  - and sometimes lightweight information retrieval (e.g., reading prior experiment logs or documentation).  
- Before producing “answers” (new algorithms or hypotheses), agents can **run experiments** and analyze results.

#### Failure modes

- **Experiment‑level reward hacking:**
  - Agents may design experiments that artificially favor their hypotheses (e.g., cherry‑picked datasets, easy baselines).  
- **Publication bias in the archive:**
  - The system may over‑record positive results, leading to Goodhart on “archive impact.”  
- **Objective saturation / cycling:**
  - Without careful novelty and diversity measures, the system can converge to a narrow research area and repeatedly rediscover similar algorithms.  
- **Speculative Goodhart on meta‑metrics:**
  - If agents are rewarded for producing “surprising” or “novel” results, they may overfit to noise or unstable metrics.

Sakana’s public releases do not systematically catalog such failures, but these are natural risks for any autonomous research lab architecture.

---

## 9. Cross‑system comparison along your axes

| System           | Individual representation                          | Scoring (non‑tiny benchmark?)                                      | Investigation / tools                                   | Main failure‑mode pressures                                         |
|------------------|----------------------------------------------------|--------------------------------------------------------------------|---------------------------------------------------------|----------------------------------------------------------------------|
| **Voyager** (2023–24)[5][7][8] | Skill‑library + environment state; executable code skills; GPT‑4 policy | Environment progress: unique items, tech tree, distance; ongoing exploration (not tiny fixed set) | Full Minecraft environment; GPT‑4; iterative code execution & repair | API misuse, hallucinated world model, proxy metrics (Goodhart), eventual progress saturation in a world |
| **ADAS** (2023–25, white‑space) | Agent system designs (prompts, toolchains) as text/JSON | Performance on suites of tasks; likely multi‑task, but still finite | Tool‑using agents on test tasks                        | Overfitting to evaluation harness; Goodhart on system‑level metrics |
| **Darwin–Gödel Machine** (conceptual) | Self‑modifying agents / programs with proofs | Utility via formal proofs or empirical performance; not benchmark‑bound in theory | Self‑inspection, theorem proving, simulations          | Proof‑search Goodhart, self‑mod misalignment, reward hacking if empirical proxies used |
| **AlphaEvolve** (white‑space) | Agent configurations / policies | Task performance; multi‑task but benchmark‑like                    | Tool‑using agents on tasks                             | Same as general evolutionary RL: reward hacking, overfitting, saturation |
| **FunSearch** (2023)[FunSearch‑2023] | Programs (code) for math/optimization tasks | Performance on large/sampled instance distributions; resampled, not tiny | Code execution on many instances; LLM uses results to generate new code | Degenerate/invalid code, overfitting to train instance distribution, harness exploitation |
| **Promptbreeder** (2023)[Promptbreeder‑2023] | Prompts (text), including meta‑prompts that evolve prompts | Metrics on benchmark datasets; finite though non‑tiny              | None per individual; LLM used to mutate/select prompts | Goodhart on metrics; benchmark overfitting; prompt bloat; saturation |
| **EvoPrompt** (2023–24) | Prompts / templates (text) | Benchmark performance (GSM8K, MMLU, etc.); fixed datasets         | None per individual; LLM or heuristic mutation         | Same as Promptbreeder: Goodhart, overfitting, brittleness, saturation |
| **Sakana CycleQD** (2024–25) | Algorithms/programs with behavior descriptors | QD: fitness + diversity; evaluations on distributions of tasks     | Code execution on tasks; LLM proposes new algorithms   | Diversity Goodhart, harness exploitation, repertoire saturation      |
| **Sakana ASAL** (2024–25) | Hypotheses/algorithms/experiments as code + text | Multi‑objective: performance, novelty, complexity; continual experimental tasks | Code execution, data analysis, reading archives        | Experiment‑design gaming, archive Goodhart, topic‑collapse, meta‑metric overfitting |

---

## 10. High‑level patterns re: your focus

**Representation**

- Most systems treat an individual as a **symbolic artefact**:
  - code (Voyager, FunSearch, CycleQD, ASAL),  
  - prompts (Promptbreeder, EvoPrompt), or  
  - agent configurations (ADAS‑style).  
- This makes individuals **interpretable and editable** by LLMs, enabling self‑improvement.

**Scoring without tiny fixed benchmarks**

- **Truly open or resampled tasks:** Voyager (open world), FunSearch (instance distributions), CycleQD/ASAL (task families) reduce benchmark saturation.  
- **Fixed benchmarks:** Promptbreeder/EvoPrompt are still anchored to standard datasets; saturation and Goodhart on these metrics are central concerns.  
- **Meta‑systems (ADAS, AlphaEvolve):** usually rely on multi‑task suites, which are broader than single benchmarks but still finite.

**Investigation / tool use**

- **Embodied or experimental agents** (Voyager, FunSearch, CycleQD, ASAL) permit individuals to **run code, interact with environments, run experiments** before being scored.  
- **Prompt‑only methods** (Promptbreeder, EvoPrompt) do *not* allow agents themselves to investigate; the LLM is only used to generate new prompts, and scoring is purely dataset‑based.

**Failure modes**

- **Reward hacking / Goodhart:**
  - Prompt‑evolution methods show **benchmark‑metric Goodhart**: prompts exploit dataset quirks.  
  - Code‑evolution methods (FunSearch, CycleQD, ASAL) face **harness exploitation** and **distribution overfitting**.  
  - Embodied agents (Voyager) risk optimizing proxy metrics (distance, items) rather than genuine “open‑endedness.”  
- **Objective saturation:**
  - Strong for fixed benchmarks (Promptbreeder, EvoPrompt).  
  - Softer but still present for environment‑based or distributional tasks once near‑optimal solutions are found.  
- **Structural white‑spaces:**
  - There is little **systematic documentation** of reward hacking and Goodhart phenomena in proprietary/early systems like ADAS, Darwin‑Gödel‑style LLM agents, and AlphaEvolve—these are mainly **research agenda keywords** rather than fully reported systems in 2023–2025.

If you want, I can next:

- dig up specific experiment setups and metrics for **one or two systems** (e.g., Voyager vs FunSearch) and analyze where **Goodhart is empirically visible**, or  
- sketch a **unified experimental protocol** to stress‑test these systems for reward hacking and proxy optimization.


### Citations
1. https://www.infoq.com/news/2023/05/minecraft-voyager-llm-agent/
2. https://voyager.minedojo.org
3. https://www.youtube.com/watch?v=BU3w_AbCEbA
4. https://huggingface.co/papers/2305.16291
5. https://arxiv.org/abs/2305.16291
6. https://www.semanticscholar.org/paper/Voyager:-An-Open-Ended-Embodied-Agent-with-Large-Wang-Xie/f197bf0fc2f228483f6af3285000d54d8d97f9eb
7. https://openreview.net/forum?id=ehfRiF0R3a
8. https://github.com/MineDojo/Voyager
9. https://www.ijcai.org/proceedings/2025/0022.pdf


## MoA ensemble + continuously-evolving-as-ensemble white-space

For **(1)**, the evidence is mixed, but the strongest recent result says that **diversity is not automatically better**: a 2025 reanalysis found that **Self-MoA**—using only outputs from the **single top-performing LLM**—outperformed standard MoA that mixes different LLMs by **6.6% on AlpacaEval 2.0** and **3.8% on average** across MMLU, CRUX, and MATH.[1][3] That paper explicitly reports a **quality–diversity trade-off** and concludes that mixing different LLMs often **lowers the average quality** of the ensemble, so redundant high-quality outputs can beat heterogeneous but weaker ones.[1][3]

At the same time, the original MoA paper (Wang et al., 2024) found that multi-model collaboration can help: its layered MoA framework achieved state-of-the-art results on **AlpacaEval 2.0, Arena-Hard, MT-Bench, and FLASK**, and the authors argue that LLMs show “collaborativeness,” meaning they can improve when conditioned on other models’ outputs, even if those auxiliary outputs are weaker.[2][5] So the evidence is **not** “diversity always wins”; rather, it suggests that **diversity can help when it adds useful signal, but redundancy with higher-quality models can be better when diversity mainly adds noise**.[1][2][3]

For **(2)**, I do **not** see strong prior work matching your exact setup: a **continuously evolving population** of agents that also functions as a **live orchestrated ensemble** answering queries in real time, with the **evolution loop and answering loop running simultaneously**. What I do find are **nearby but not identical** lines of work: standard MoA uses a fixed or preselected set of agents to answer queries in layers, and the 2025 Self-MoA paper adds a **sequential on-the-fly aggregation** variant, but that is about aggregating many outputs over multiple rounds, not about a population that is continuously evolving while serving live traffic.[2][3][4]  

That means your exact formulation looks like a **research white-space**: I can point to MoA, self-ensembling, sequential aggregation, routing, and multi-agent search systems, but I do **not** find a clearly established prior art for **simultaneous online evolution + online answering** as a unified continuously running system in the sources provided.[2][3][8]

If useful, I can next map this white-space into a compact prior-art taxonomy: **fixed ensemble**, **adaptive routing**, **sequential self-ensemble**, and **online-evolving population**, and show where each cited paper fits.


### Citations
1. https://huggingface.co/papers/2502.00674
2. https://proceedings.iclr.cc/paper_files/paper/2025/file/5434be94e82c54327bb9dcaf7fca52b6-Paper-Conference.pdf
3. https://openreview.net/forum?id=K6WwK8URlV
4. https://zilliz.com/blog/mixture-of-agents-how-collective-intelligence-elevates-llm-performance
5. https://www.semanticscholar.org/paper/Mixture-of-Agents-Enhances-Large-Language-Model-Wang-Wang/2b3ad2fdd9d2013119232ee49e6d21eb08474b74
6. https://arxiv.org/html/2605.24048v1
7. https://aclanthology.org/2025.findings-acl.342.pdf
8. https://www.scirp.org/journal/paperinformation?paperid=148134


## On-prem prompt-evolution anti-saturation practice

You avoid saturation on a small task battery by **decoupling fitness from any single score**, using **behaviorally‑diverse selection + minimal criteria**, and letting **difficulty and evaluation conditions co‑evolve with the population** rather than be fixed. In practice, you want a **novelty/quality hybrid** with rich behavior descriptors, minimal‑criterion coevolution, curriculum over *conditions* not *tasks*, and explicit measurements of evolutionary activity/open‑endedness (e.g., MODES, Bedau).

Below is a concrete, implementation‑oriented design, assuming:

- On‑prem, small LLMs (e.g., Llama 3.2 via Ollama).
- A small fixed set of “tasks” or APIs you can call.
- You are evolving **prompt programs / prompt strategies**, not the model weights.

I’ll integrate best practices from open‑ended evolution, novelty search, MAP‑Elites, minimal‑criterion coevolution, and empirical measures of open‑endedness. Where explicit LLM‑prompt literature is thin, I’ll adapt from evolutionary computation and open‑endedness papers (clearly flagged).

---

## 1. Fitness & Selection Design to Avoid Saturation

### Core design: novelty+quality, no single scalar score

With a small battery of tasks, naïve scalar fitness (e.g., average accuracy) almost always saturates quickly: the population converges to one “good enough” prompt and then stalls.

Use a **multi‑objective / multi‑criterion selection**:

- **Component 1 – Minimal criteria (MC)**: binary filters (pass/fail).
- **Component 2 – Quality metrics** within the set that passes MC.
- **Component 3 – Novelty / diversity** in behavior space (behavior descriptors).
- **Component 4 – Archive / repertoire** (MAP‑Elites‑style): keep a diverse set of elites across behavior space, not just the single best.

That combination is strongly supported for open‑ended search in constrained environments in the evolutionary computation literature (e.g., Lehman & Stanley’s novelty search and quality‑diversity, and minimal criterion coevolution).

**Concrete selection loop:**

1. Evaluate each prompt genome on the task battery → produce:
   - Raw outputs (text, tool calls, etc.).
   - Task scores (accuracy, format, speed).
   - Behavior descriptor vector (see section 2).
2. **Filter by minimal criteria** (e.g., must not hallucinate obvious facts, must obey safety rule, must solve at least 1 of N tasks above baseline).
3. For survivors:
   - Compute **quality score**: e.g., weighted sum of per‑task scores.
   - Compute **novelty score**: average distance in behavior‑descriptor space to K nearest neighbors in an archive.
4. Maintain an **archive** indexed by behavior descriptors (e.g., discretized; MAP‑Elites style):
   - For each behavior cell, only keep the **highest‑quality** prompt seen for that behavior zone.
   - Use both **quality and novelty** when deciding which individuals to copy or mutate (e.g., tournament based on Pareto dominance between quality and novelty).

**Parameter guidelines (actionable):**

- Population: 100–500 prompts per generation (depending on compute).
- Archive size: 2–5× population (fixed); prune oldest or lowest activity cells.
- Novelty:
  - K = 10–20 nearest neighbors.
  - Behavior distance: standardized Euclidean or cosine.
- Parent selection:
  - 50% from **high‑quality** top quantile in archive.
  - 50% from **most novel** quantile (or random from archive to encourage drift).

This ensures you never purely optimize the small task battery; instead, you are continually searching for **new behavior niches** that satisfy minimal criteria while potentially improving quality.

---

## 2. Behavior Descriptors: What to Track for Prompt Strategies

Behavior descriptors should be **task‑agnostic (or lightly task‑specific)** and easy to compute from LLM outputs and logs, so they generalize beyond your small battery.

Think in **three layers**: structural (prompt itself), dynamical (interaction traces), and semantic (output behavior).

### 2.1 Structural descriptors (prompt “genome” properties)

Sample features:

- **Prompt length**:
  - Total tokens.
  - Instruction vs examples vs system role proportion.
- **Prompt structure**:
  - Number of explicit steps or bullet points.
  - Presence of explicit reasoning cues (“step‑by‑step”, “chain of thought”, “think before answering”).
  - Number/type of tools mentioned (if any).
- **Control tags**:
  - Temperature hints (“be creative”, “be concise”).
  - Constraints (“respond in JSON”, “no external knowledge”).

You can parse the prompt template and encode as a feature vector.

### 2.2 Dynamical descriptors (interaction behavior)

From logs of interactions on the tasks:

- **Latency and token stats**:
  - Average output length per task.
  - Variance of length across tasks.
  - Time to first token (approximate if needed).
- **Self‑correction behavior**:
  - Rate of outputs with self‑revision phrases (“sorry, let me correct that”).
  - Use of internal step markers (“Step 1:”, “Reasoning:”).
- **Tool usage patterns** (if you allow tool‑calling):
  - Frequency of tool invocations.
  - Diversity of tools used.
  - Depth (sequential tool chains vs single call).

### 2.3 Semantic descriptors (what the outputs *do*)

You want descriptors that capture high‑level behavioral properties without over‑fitting to one task.

Examples:

- **Risk vs caution**:
  - Proportion of “I don’t know” or abstentions on ambiguous inputs.
- **Creativity vs conservatism**:
  - For generative tasks, use an embedding model to compute:
    - Diversity of outputs across similar prompts (cosine distance).
    - Distance from baseline (e.g., a simple reference prompt).
- **Instruction‑following reliability**:
  - Rate of obeying specified output format (e.g., valid JSON, bullet count).
- **Robustness to paraphrase**:
  - For tasks you can paraphrase, measure how stable the answers are across paraphrased inputs.

Implementation detail:

- Normalize each feature to [0, 1].
- Concatenate into a behavior vector, e.g., 20–100 dimensions.
- Optionally reduce with PCA/UMAP to 5–10 dims for the novelty computation and visualization.

### 2.4 Practical advice to avoid useless descriptors

- Avoid descriptors that are **direct clones of fitness** (e.g., per‑task accuracy as a behavior dimension).
- Prefer descriptors that:
  - Are different across many prompts.
  - Are plausibly correlated with *robust generalization* rather than just narrow performance.
- Run a few pilot generations, then prune descriptors that show extremely low variance or map every individual into a tiny corner.

---

## 3. Minimal‑Criterion Coevolution (MCC) in LLM Prompt Space

Minimal‑criterion coevolution (MCC) is designed precisely to prevent premature convergence in open‑ended search by requiring agents to just barely meet a **moving minimal threshold**, rather than optimize a high score.

Original MCC ideas (e.g., Brant & Stanley) can be ported to LLM prompts as follows.

### 3.1 Defining minimal criteria for LLM prompts

Start with very lenient criteria that almost all random prompts pass (to keep exploration alive), then gradually ratchet them.

Candidate minimal criteria:

1. **Basic format compliance**:
   - Must respond in required format for at least one task (e.g., valid JSON, correct section headings).
2. **Non‑trivial mastery**:
   - On at least 1 of N tasks, must beat a baseline prompt by a margin (e.g., +0.05 accuracy or +10 BLEU).
3. **Safety / non‑pathology**:
   - No bannable content.
   - No refusal to respond to benign tasks beyond some small threshold.
4. **Stability**:
   - When the same prompt is run twice on the same input with fixed sampling config, outputs must be “similar enough” (measured by embedding distance or lexical overlap).

With small task batteries, criteria 1 and 2 are most important to avoid saturating tasks that are too easy.

### 3.2 Dynamic / co‑evolved criteria

Let the minimal criteria **depend on the current population** (coevolution):

- Compute the distribution of, say, “best task score” across prompts.
- Set the minimal threshold at a percentile (e.g., 20th–40th percentile) rather than an absolute number.
- As the population improves, the **criterion rises automatically**, ensuring you never saturate at an earlier level.

In pseudocode:

```python
# After evaluating population
best_scores = [max(ind.task_scores) for ind in population]
mc_threshold = np.percentile(best_scores, 30)  # 30th percentile

def passes_minimal_criterion(ind):
    return max(ind.task_scores) >= mc_threshold and ind.safety_ok
```

This forces prompts to keep up with the moving frontier without rewarding super‑optimization of the current tasks.

### 3.3 Two‑population MCC (optional)

To increase open‑endedness, use **MCC with two coevolving populations**:

- Population A: prompt strategies optimized for **exploration / novelty** (low quality requirement).
- Population B: prompt strategies optimized for **quality** given the behaviors discovered by A.

Minimal criteria can depend on cross‑population interactions, e.g., prompts in B must beat average performance of prompts in A on some tasks.

This is more complex but can help avoid local minima when the evaluation battery is small.

---

## 4. Curriculum / Adaptive Difficulty with a Small Task Battery

You cannot make the battery much larger, but you *can* make evaluation conditions more challenging as the population improves.

Think in terms of **condition space** rather than new tasks:

- Same task type but harder inputs.
- Same tasks but with more constraints.
- Same tasks but under limited context or noisy inputs.

### 4.1 Condition generators instead of static test sets

For each task type, define a **condition generator** with a difficulty parameter \(d \in [0, 1]\):

Examples:

- Question answering:
  - \(d\) controls reading length, number of distractors, ambiguity.
- Data transformation:
  - \(d\) controls messiness of input (missing fields, typos, multi‑lingual, mixed formats).
- Reasoning / planning:
  - \(d\) controls number of steps required or branching factor.

Then:

- For each generation, sample conditions at a **difficulty band** \(d \in [d_{\min}, d_{\max}]\) that is tied to population performance.
- As the population’s median performance surpasses a threshold at current difficulty, **shift the band upward**.

Example:

```python
difficulty = current_difficulty
if median_quality > 0.8 and difficulty < 0.9:
    difficulty += 0.05
```

You keep the **number of tasks constant** but continually make instances harder.

### 4.2 Adaptive sampling of “hard cases”

Use **hard‑example mining**:

- Maintain a buffer of “hard cases” where most of the current population fails (e.g., success rate < 10%).
- Each generation:
  - Evaluate prompts on a mix of:
    - Fresh cases generated at the current difficulty band.
    - A sample of previously discovered hard cases.
- Weight hard‑case performance more heavily in quality scores once basic performance is saturated on easier cases.

This ensures you reuse your small task types in ever‑harder variants.

### 4.3 Co‑evolving tasks / inputs (simple MCC for tasks)

If you can synthesize or retrieve inputs via the LLM itself or another script, you can run a **minimal‑criterion coevolution** for tasks too:

- Have a simple “task generator” population, where each “task genome” encodes how to generate or select inputs.
- Minimal criteria for tasks: they must be solvable by at least some fraction (e.g., 5–20%) of the current prompt population but not by all (to avoid trivial or impossible tasks).
- The prompt population is evaluated on the tasks that pass the task minimal criteria.

Even a rudimentary version (e.g., just adjusting parameters of input generators) greatly increases open‑endedness without large datasets.

---

## 5. Neutral Drift and Large Neutral Genomes

Open‑ended evolution typically benefits from **large neutral networks**: many genotypes with equal fitness that can be traversed by mutation without penalty, allowing eventual escape into new niches.

In prompt evolution:

- The “genome” is the **prompt program** (template, role, examples, instructions, etc.).
- Two prompts might perform identically on your small battery, but differ significantly in structure. This is your neutral network.

### 5.1 How to support neutral drift

1. **Accept neutral and slightly deleterious moves**:
   - Use selection that is not overly harsh (e.g., tournament size 2–3 instead of 5–10).
   - Include a **small fraction of random parent selection** from MC‑passing individuals, regardless of rank.
2. **Encourage structural redundancy**:
   - Keep prompts somewhat longer and more over‑specified than strictly necessary; this creates many neutral degrees of freedom (phrasing, ordering, synonyms) that can drift.
3. **Use edits that often preserve meaning**:
   - Mutation operators:
     - Synonym substitution.
     - Reordering bullet points.
     - Adding redundant clarifications (“Please think carefully before answering.”).
     - Varying temperature hints or style descriptors without changing task semantics.

### 5.2 Genome design for neutral space

Design your internal representation (genome) to be **modular and overcomplete**, not a single string:

- Modules:
  - System role text.
  - High‑level strategy (chain‑of‑thought, program‑aided, tool‑first, etc.).
  - Few‑shot examples bank.
  - Output schema / formatting spec.
  - Meta‑instructions (self‑evaluation, verification).

Store each module as structured fields; your generator concatenates them into a final prompt string. Mutation and crossover then operate at field‑level:

- Mutate only the few‑shot examples.
- Swap high‑level strategies between parents.
- Add/remove one meta‑instruction.

This dramatically enlarges the neutral space while preserving functionality.

### 5.3 Maintain a “neutral drift” sub‑population

Optionally, maintain a small sub‑population (e.g., 10% of total) that:

- Is selected only by **minimal criteria**, not by quality.
- Undergoes **heavier mutation** rates.
- Feeds into the main population occasionally as additional parents.

This mirrors “innovation reservoirs” in open‑ended EC systems.

---

## 6. Measuring Open‑Endedness: Bedau’s Evolutionary Activity & MODES

You asked specifically about:

- **Bedau’s evolutionary activity statistics**.
- **MODES toolbox**.

These give quantitative checks that your system is truly open‑ended, not just briefly explorative.

### 6.1 Bedau’s evolutionary activity statistics (A, N, D, etc.)

Bedau et al. propose statistics to classify evolutionary systems as:

- Class 1–4, where **Class 4** shows ongoing innovation (open‑ended evolution).

Core ideas:

- **Adaptive activity**: how long lineages of “adaptive” innovations persist and how often they appear.
- **Diversity**: number of distinct types (here, behavior phenotypes).
- **Novelty**: production of new types over time.

Mapping to LLM prompt evolution:

1. Define “type” as a **discretized behavior descriptor** (or cluster).
   - E.g., cluster behavior vectors into K clusters; each cluster is a type.
2. Each individual belongs to a type; track **lineages** (parent → child mapping).
3. Mark an **innovation** event when a new type appears that is **fitter (quality) than all previous types in its lineage’s history** (or crosses a fixed performance threshold for the first time).
4. Compute Bedau‑style stats over generations:
   - **Cumulated activity**: total lifespan of all innovative types.
   - **New type rate**: how often new types arise.
   - **Diversity over time**: number of active types vs generation.
5. Look for:
   - **Unbounded or slowly growing activity**.
   - Persistent production of new types instead of early plateau.

Implementation notes:

- Use a sliding window over recent generations (e.g., 100) to avoid counting noise.
- Visualize: plot types vs time (heatmap), activity curves, diversity curves.

### 6.2 MODES toolbox (mass, organization, diversity, evolvability, complexity)

MODES is a general toolbox for quantifying open‑endedness along five axes:

- **Mass**: number of entities.
- **Organization**: structure / modularity.
- **Diversity**: variety of entities.
- **Evolvability**: capacity to generate heritable phenotypic variation.
- **Complexity**: multi‑scale structure and function.

Applied to prompt evolution:

- **Mass**:
  - Population size and number of archived elite prompts.
  - Ideally, stable or slowly growing with resource constraints.
- **Organization**:
  - Modularity metrics on genome structure.
  - For structured prompts, count modules, their reuse, and dependency graph complexity.
  - Track if prompts evolve from simple monolithic templates to more modular, conditional strategies (e.g., IF/ELSE logic in prompt programs).
- **Diversity**:
  - Shannon entropy over behavior types.
  - Average pairwise distance in behavior space.
  - Number of occupied cells in a behavior grid (MAP‑Elites coverage).
- **Evolvability**:
  - For a sample of individuals, generate multiple mutated offspring and measure:
    - Variation in behavior descriptors.
    - Fraction of mutations that remain above minimal criteria.
    - Fraction that yield improvements on at least one task.
- **Complexity**:
  - Multi‑scale:
    - Prompt structural complexity (number of modules, depth of nested instructions).
    - Behavioral complexity (e.g., solution path length on reasoning tasks, number of sub‑steps).
  - Use simple proxies at first (e.g., parse tree depth of prompt as text).

You can approximate MODES metrics by:

1. At each generation, log:
   - Behavioral descriptors.
   - Structural genome features.
   - Parent–child relationships.
   - Task scores.
2. Offline, run scripts to compute:
   - Diversity and coverage.
   - Evolvability experiments on archived individuals.
   - Trends in modularity and complexity measures.

What to look for as “good” signs:

- Diversity and coverage do not collapse to a tiny region.
- Evolvability remains high (mutations often create new behaviors that pass MC).
- Complexity and organization measures drift upward over long timescales rather than plateau quickly.

---

## 7. Putting It Together: A Concrete On‑Prem Design

Here is a minimal, actionable blueprint tailored to your setup.

### 7.1 Setup

- LLM: local **llama3.2‑style** small model via Ollama.
- Representation:
  - Each individual = JSON describing:
    - `system_role`, `meta_instructions`, `strategy_type`, `examples[]`, `output_schema`, etc.
  - Generator turns JSON → concatenated prompt string used with the model.
- Task battery:
  - 3–10 task types, each with condition generator parameterized by difficulty.

### 7.2 Evolution loop

1. **Initialize population**:
   - 100–200 individuals with random but valid prompt structures.
   - Seed a few hand‑designed baselines as reference.

2. **Each generation**:

   - Sample tasks:
     - For each task type, generate several instances at current difficulty band.
     - Include some “hard case” replay items.
   - Evaluate each individual:
     - Run prompts on tasks via Ollama with fixed decoding config.
     - Compute per‑task scores and any safety/format checks.
     - Compute behavior descriptors from outputs and logs.
   - Minimal‑criteria filter:
     - Use dynamic threshold (percentile) on best per‑task score.
     - Enforce safety and basic format criteria.
   - Update archive:
     - For each MC‑passing individual, insert/update in behavior grid:
       - Choose cell by discretized behavior vector.
       - Keep highest‑quality occupant per cell.
   - Selection:
     - Draw parents from archive based on a mix of quality and novelty.
   - Variation:
     - Apply structural mutations and crossovers at module level.
     - Maintain small “neutral drift” group with higher mutation rate and no quality pressure.
   - Update difficulty:
     - If median quality on current difficulty band > threshold (e.g., 0.8), raise difficulty.
   - Logging:
     - Save behavior descriptors, task scores, lineage info.

3. **Every K generations** (e.g., 20):

   - Compute Bedau‑style activity statistics and MODES approximations.
   - Visualize behavior coverage and diversity.
   - Check for saturation:
     - If diversity and novelty collapse, increase mutation rate or broaden behavior descriptor space.

---

## 8. Practical Best‑Practice Checklist

- **Avoid scalar “global accuracy” fitness**; always mix minimal criteria + quality + novelty.
- **Make behavior descriptors broad, multi‑layered** (structure, dynamics, semantics), but prune those with zero variance.
- **Use dynamic minimal criteria** based on population percentiles, not fixed absolute thresholds.
- **Raise difficulty on conditions, not just add tasks**, using parametric input generators and hard‑case replay.
- **Support neutral drift** by:
  - Modular genome representation.
  - Accepting neutral/slightly negative mutations.
  - Keeping a small drift sub‑population.
- **Quantify open‑endedness** periodically using:
  - Diversity/coverage metrics.
  - Bedau‑style adaptive activity (lineage of innovative types).
  - MODES‑style evolvability and complexity trends.

If you share your specific task battery (even abstractly), I can sketch concrete behavior descriptors and difficulty parameters per task, plus example JSON schemas for the prompt genome and mutation operators.


### Citations
1. https://www.llama.com/docs/how-to-guides/prompting/
2. https://www.youtube.com/watch?v=eDN6fAWLNNE
3. https://ollama.readthedocs.io/en/quickstart/
4. https://agenticai-flow.com/en/posts/local-llm-ollama-llamacpp-guide/
5. https://ai.meta.com/blog/meta-llama-3/
6. https://www.youtube.com/watch?v=VC6QCEXERpU
7. https://openaccess.uoc.edu/server/api/core/bitstreams/2b4736d4-dda5-4cac-b069-20bfe98ebdc7/content
8. https://riunet.upv.es/server/api/core/bitstreams/8e4704de-02bf-4e56-a24d-8f2ed0dec68b/content
