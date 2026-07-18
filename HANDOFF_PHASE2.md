# Quantum Vibes — Phase 2 Handoff & Program Reference

**Document:** `HANDOFF_PHASE2.md`
**Date:** 2026-07-18
**Purpose:** Reference document first, decision support second. Consolidates all project state, brainstorming, candidate experiments, platform facts, strategic threads, sources, and discussion history from 2026-06-03 through 2026-07-18, so that Phase 2 exploration can resume from exactly where it left off.
**Relationship to repo:** Complements `STATE.md`, `HANDOFF.md`, `README.md`, and `results/run_log_phase1.md`. For *completed work*, the repo is ground truth. For *brainstorm content and forward plans*, this document is the consolidated record.

**Evidence tiers used throughout:**

- `[repo]` — verified in the repository / merged PRs
- `[chat]` — documented in a source conversation or a distilled handoff of one
- `[training]` — recalled from model knowledge; citation plausible but unchecked
- `[VERIFY]` — must be checked against live IBM documentation, the account dashboard, or the primary source before being used in planning

---

## 1. Where we left off — state, intent, and plan

### 1.1 Ground truth (as of 2026-07-18)

Phase 1 is closed and clean. The CHSH Bell test ran on real hardware on 2026-06-03 (`ibm_marrakesh`, IBM Heron r2, 156 qubits), producing a peak **|S| = 3.003 ± 0.029 — a 34.8σ violation of the classical bound S ≤ 2** — using 79 seconds of QPU time. `[repo]` A documentation pass merged on 2026-07-06 (PR #3): full README with physics explainer, honesty notes on the readout-mitigation overshoot past the Tsirelson bound, a historical comparison table back to Freedman–Clauser 1972, plus a self-contained landing page at `docs/index.html`. `[repo]` Working tree clean; no open PRs or issues. `[repo]`

Budget: the standard Open Plan provides 10 minutes of QPU time per month. Phase 1's 79 seconds was spent in June, so **July's ~10-minute budget is untouched**. `[repo]`

### 1.2 The decision as it stood

Two brainstorm passes in June produced two tracks that were never fully reconciled:

- **June 5 — the WIDE arc.** A three-beat program built on the assumption that a 180-minute promotional tier applied to the account: Beat 1 wide GHZ / genuine-multipartite-entanglement witness, Beat 2 utility-scale kicked TFIM, Beat 3 discrete time crystal (recommended headline: "emergent phase invisible below ~tens of sites, best signal-to-effort"). `[chat]`
- **June 11 — echoes-first.** Six candidates re-ranked against the *actual* budget, with the finding that the 180-minute promo is **not available to this account**. **Mini Quantum Echoes (30–40 qubits, first-order OTOC) was marked as the selected direction** — the only frontier-grade experiment that fits inside the free budget (~60–150 s estimated). Everything WIDE-scale was explicitly tagged "blocked until 180-min tier." `[chat]`

**Net state: the project left off having selected mini Quantum Echoes as Phase 2's experiment**, with the next concrete step already named — a Qiskit notebook for the 30–40-qubit echo with a shot-budget tracker — and the WIDE arc parked as the budget-gated future program. The June 5 vs June 11 budget conflict is the top verification item (see §7, Q1); the June 11 finding is later and account-specific, so it wins pending a dashboard check.

### 1.3 The vision, as documented in June

Four threads, in escalating ambition. These were articulated most clearly at the time and are preserved here close to their original framing.

**Thread 1 — the narrative spine: an escalating arc of entanglement.** The through-line is *lineage*: CHSH proved 2-qubit entanglement is real and unfakeable; the next experiment scales that to N-qubit scrambling. Mini echoes was selected partly *because* it is the direct descendant ("2-qubit entanglement → N-qubit scrambling") and because it answers Google's explicit invitation that Quantum Echoes be "verifiable on other hardware." The GHZ version of the same story ("2 entangled qubits → 60") was ranked second narrative-wise. Framing discipline insisted on throughout: this is **protocol replication in the classically verifiable regime, explicitly *not* advantage replication** — the advantage claim lives in the second-order OTOC, which is out of budget reach. `[chat]`

**Thread 2 — Publication A, the scientific artifact.** A rigorous mini-echoes writeup running the *same circuits* three ways: (a) Heron hardware, (b) exact statevector simulation, (c) tensor-network/MPS simulation — positioned against the classical-methods frontier (TNMC reproduces first-order OTOC to ~95 qubits; TNBP shown unable to simulate the echoes experiment), with the RNG-sampling machinery explicit in the methods. The contribution is independent cross-platform verification. Novelty hinge: no public free-tier mini-echoes replication was found in searches at the time — this is the claim, and it needs re-verification. `[chat]` `[VERIFY]`

**Thread 3 — Publication B, the meta/accessibility narrative.** "Vibe-coded quantum experiments": a non-specialist runs a Bell violation and then a scrambling experiment with full rigor via conversational AI. Key recorded insight: CHSH itself is hello-world on IBM Quantum; **the invisible asset is the verification labor** — API version-checking, documentation validation, iterative testing. The two-experiment escalating arc *is* the story. Note: whether to publish at all remains **optional/undecided** (carried from `STATE.md`, never resolved). `[chat]`

**Thread 4 — the platform, deferred but the endgame.** A toggle-based validated-experiment platform: user describes an experiment → mandatory feasibility assessor (qubit count / topology / QPU-seconds pre-check) → mandatory simulate-first gate on a noise-modeled fake backend → isolated IBM API adapter layer. CHSH + mini-echoes are the two seed toggles, deliberately covering both circuit families (Sampler-correlation and Estimator-echo). Recorded judgment: **the ~20 pre-brainstormed experiments (split into 10-minute and 180-minute lists, from prior Opus/Grok sessions) are the real asset, not the toggle UI** — and those lists are not in any current document; they need retrieval. Publication B is essentially the platform's founding story; the platform is Publication B productized. Explicit instruction on record: deferred, **do not build yet**. `[chat]`

**Binding these together — the methodological identity:** sim gate → budget-guarded hardware run → schema-stable JSON contract → independent verifier, with expected-vs-actual-vs-classical framing and honesty notes preserved (the mitigation overshoot is documented, never trimmed). The June 5 pass added one new discipline for the wide regime: guard against **silent over-mitigation** via a raw / mitigated / tensor-network ablation on every wide beat. `[chat]`

### 1.4 Immediate next actions (as they stood)

1. **Verify the budget** on the IBM dashboard: does the 180-min promo apply to this account? This single fact decides whether WIDE is a live track or a wishlist. `[VERIFY]`
2. **Retrieve the ~20-experiment lists** (10-min and 180-min versions) from prior Opus/Grok sessions. `[chat]`
3. **Quantify heavy-hex SWAP/depth overhead** of echo circuits at 30–40q in simulation before committing any QPU. `[chat]`
4. **Settle the simulator** for 40q echo circuits (exact statevector caps ~30q in practice; MPS fidelity at echo-level entanglement untested). `[chat]`
5. **Decide repo topology:** extend the existing repo or fork for Phase 2. `[chat]`
6. Then: build the mini-echoes Qiskit notebook with shot-budget tracker (in Claude Code, against the repo). `[chat]`

---

## 2. Phase 1 record (completed work)

All items `[repo]` or `[chat]` (June 5 project-overview conversation, which summarized `HANDOFF.md`).

**Result.** CHSH/Bell inequality test on `ibm_marrakesh` (IBM Heron r2): peak |S| = 3.003 ± 0.029, a 34.79σ violation of the classical bound S ≤ 2, run 2026-06-03 using 79 seconds of Open Plan QPU time.

**Method.** Single parameterized circuit swept across 15 angles (θ-sweep) at 4,096 shots each. Error handling active on the run: TREX readout mitigation, dynamical decoupling, and measurement twirling. Full θ-sweep table, job metadata, and calibration snapshot in `results/run_log_phase1.md`.

**Verification discipline (established in Phase 1, carried forward as project law).**

- Physics independently verified in pure NumPy before any framework code ran.
- A noiseless-simulator gate was required to reproduce the expected result before touching QPU time.
- Independent verification script (`verify.py`) built and debugged — including catching a grid-versus-continuum bug and adding negative tests.
- The readout-mitigation overshoot artifact (~6.6% past the Tsirelson bound 2√2) was documented honestly rather than trimming affected data points.

**Architecture.** Compute/presentation split: credentials live entirely in the compute layer (Google Colab as credential holder); the public-facing layer renders only from committed JSON. Qiskit 2.x on IBM's `ibm_quantum_platform` channel; GitHub as source of truth for all code. A git coordination issue (Claude Code's feature-branch workflow vs. Colab's direct commits to main) was resolved by aligning both tools to commit to main.

**Governance philosophy.** AI-assisted but human-directed: Claude acted as principal investigator/architect; the human made all real decisions — experiment choice, rigor standard, credentials, and pulling the hardware trigger.

**Documentation (2026-07-06, PR #3).** Full README: physics explainer, honesty notes on the mitigation overshoot, historical comparison table back to Freedman–Clauser 1972. Self-contained landing page at `docs/index.html`.

**README "What's next" (the three officially listed follow-ons, none started).**

1. **GHZ scaling** — from 2 entangled qubits to many, where the quantum-vs-classical gap grows exponentially with qubit count (framed as the main follow-on).
2. **Mitigation study** — a dedicated raw-vs-mitigated run to directly probe why the mitigated peak overshot 2√2.
3. **Reusable framework** — generalize the sim-gate → budget-guarded run → schema-stable JSON → independent-verifier pattern into an open-source scaffold.

Note how cleanly these map onto the June brainstorms: (1) → W1/GHZ candidates, (2) → the over-mitigation ablation doctrine, (3) → the platform thread.

---
## 3. Candidate experiment catalog (full reference)

Two families emerged across the June passes: **narrow** (≤10 qubits, exact-simulation verifiable, minimal infrastructure) and **wide** (30–150 qubits, statistically verified, exploits the hardware). Narrow candidates were ranked for pipeline reuse; wide candidates for actually using a 156-qubit device. QPU costs are estimates unless noted. All entries `[chat]` unless tagged otherwise.

### 3.1 Selected direction — Mini Quantum Echoes / first-order OTOC

*Status: selected on June 11 as the Phase 2 experiment. Fits the standard free budget.*

- **Qubits:** 30–40, chain on heavy-hex.
- **Circuit:** kicked-Ising Trotter forward evolution (4–8 steps) → butterfly X perturbation on one qubit → inverse evolution (U†) → measure echo on a probe qubit. Double-depth (forward + backward) echo structure.
- **QPU cost:** ~25–35 circuits × ~4k shots ≈ **60–150 s** — fits the ~10-min monthly budget with re-run margin.
- **Verification:** deliberately in the classically simulable regime — exact statevector to ~30q, MPS/tensor-network beyond. A **no-butterfly control** run (identical circuit, no perturbation) provides a pure hardware-error baseline.
- **New infrastructure:** Aer noise-model validation pipeline, EstimatorV2 + TREX, light Pauli twirling, single-Batch submission.
- **Ranking rationale:** direct lineage from CHSH (2-qubit entanglement → N-qubit scrambling); answers Google's "verifiable on other hardware" invitation; honest framing is *protocol replication in the verifiable regime*, explicitly **not** advantage replication.
- **Published precedent:** arXiv 2510.01983 — 60-qubit OTOC on `ibm_fez`: 250 circuits × 16k shots with twirling + TREX. That is the published-grade benchmark and itself costs ~15–40+ minutes (out of free budget). `[chat]` `[VERIFY]`
- **Explicitly out of reach:** second-order OTOC — the actual advantage claim; SNR demands ~10–100× the shots. 180-min-plan territory at minimum.
- **Next concrete step (already offered, not built):** Qiskit notebook for the 30–40q echo with a shot-budget tracker.

### 3.2 The WIDE arc (budget-gated: requires the 180-min tier)

The June 5 program for exploiting the full 156-qubit register. Design pivot: give up exact verification, adopt scalable statistical verification. All Batch-compatible, non-variational, reusing the EstimatorV2/SamplerV2 + transpile-to-ISA + JSON-contract pipeline.

**W1 — Wide GHZ / cat state + GME witness (Beat 1).**
30 → 120 qubits. Shallow circuit; long-range entanglement via dynamic circuits (mid-circuit measurement + feed-forward, Bäumer protocol; "temporary uncomputation") to avoid SWAP chains. QPU: low — the parity/MQC scan is one swept PUB. Verification: GHZ fidelity F = (P + C)/2 via parity oscillations or multiple-quantum coherences; **F > 0.5 certifies genuine multipartite entanglement**; Direct Fidelity Estimation; no exact sim. New infra: dynamic circuits, scalable-witness analysis, noise-aware compilation. Rationale: the wide analogue of CHSH — the smallest unfakeable proof that the *whole register* is coherent; teaches scalable verification. IBM reference: 120q, F = 0.56(3), Nov 2025. `[VERIFY]`

**W2 — Utility-scale kicked TFIM (Beat 2).**
100–156 qubits on the native heavy-hex lattice. ZZ layers on native edges + global X kicks; Trotter sweep; depth-limited (~5k two-qubit-gate ceiling). QPU: minutes (IBM: 100q / depth-100 runs accurately on Heron). Verification: tensor-network (light-cone MPS) cross-check; ZNE + TREX + DD; mitigation ablation. New infra: full mitigation stack, MPS simulator, lattice→heavy-hex mapping. Rationale: the canonical 2023 quantum-utility experiment, now free-tier-replicable per IBM `[VERIFY]`; directly extends the existing Phase-4 TFIM spec.

**W3 — Discrete time crystal (Beat 3, June 5's recommended headline).**
50–133 qubits. W2's circuit + disorder + deliberately imperfect π-pulses; 50–100 Floquet cycles. Verification: site-resolved autocorrelator ⟨Zᵢ(0)Zᵢ(t)⟩, robustness-to-perturbation test, tensor-network comparison. New infra: minimal over W2. Rationale: an emergent phase (period-doubling / spontaneous time-translation-symmetry breaking) invisible below ~tens of sites — best signal-to-effort; reuses the W2 engine. Frontier context: clean 2D DTC tracked 100+ cycles; the surprising finding that structured noise can *stabilize* the oscillations; ties to the 121q "cat scar" DTC literature. `[VERIFY]`

**W4 — OTOC / mini Quantum Echoes at width (Beat-3 alternative).**
50–100 qubits, same echo structure as §3.1 but scaled. Most frontier-aligned (Google Oct 2025, 65–103q) but deepest circuit ⇒ highest noise risk. Moderate–high QPU.

**W5 — Measurement-induced phase transition (MIPT).**
22 → 70 qubits. Hybrid random circuit with tunable mid-circuit measurement rate *p*; volume-law ↔ area-law entanglement transition. Cost is the trap: the naive tomography route is ~5,200 device-hours at 14q; **the only viable route is scalable cross-entropy benchmarking on a Clifford-hybrid construction (<8 device-hours at 22q)**, possibly with a space-time duality mapping. Avoid post-selection. Highest novelty, highest risk.

### 3.3 The June 11 budget-realistic ranking (items 2–6)

Ranked after the promo was found unavailable; all blocked at free-tier scale except as noted.

2. **Kicked Ising utility replication** (IBM 2023 Nature): 100+ qubits, ZNE with Clifford-point ground truth; ~20–40 min QPU → blocked until 180-min tier. Same Trotter machinery as mini-echoes (forward-only), so §3.1 partially amortizes it.
3. **GHZ with mid-circuit error detection** ("Big Cats" method): 30–60q achievable (IBM's 120q at 0.56 fidelity required their adaptive compiler); dynamic syndrome measurement, post-selection, parity oscillations + DFE; ~15–30 min → blocked. Ranked #2 narrative-wise ("2 entangled qubits → 60").
4. **Dynamic circuits static-vs-dynamic comparison:** teleported CNOT, constant-depth GHZ; 100+q scale possible; ~10–20 min → blocked.
5. **Magnetic materials simulation** (ORNL/IBM, Mar 2026, ~50q Heron r2): Heisenberg/Ising on heavy-hex; feasible at scale on the 180-min tier. `[VERIFY]`
6. **Discrete time crystal:** 50–100q, 1D Floquet chain, ~20–30 cycles, period-doubling signature; 180-min tier.

### 3.4 Narrow candidates (deprioritized — verifiable but don't use the hardware)

- **GHZ + Mermin inequality (3–7q).** Direct CHSH generalization; violation grows exponentially with N; shallow (H + CNOT ladder); SamplerV2; exactly verifiable; near-zero new infra. Was the best *narrow* next step; superseded by W1/mini-echoes.
- **Teleportation with mid-circuit measurement + feed-forward (3q)** and **repetition-code / bit-flip QEC (≥5q).** Introduce dynamic circuits cheaply; retained as **de-risking warm-ups for W1**.
- **E91 (Ekert) QKD.** Reinterprets the *existing* CHSH data as a cryptographic primitive (the S-violation certifies key security). Near-zero cost; pairs strongly with a writeup (W1+E91 as an "entanglement → cryptographic certificate" arc).
- **Quantum-kernel toy classification, RCS+XEB, VQE H₂.** Runnable but require honesty caveats (no real advantage at these scales; Session limits bite for variational loops).

### 3.5 Explicitly out of scope (state this in any public framing)

RSA/Shor at meaningful sizes; Grover at interesting sizes; fault-tolerant QEC; certified randomness (requires a classical-supercomputer referee); anything "consciousness-interfacing" (that is wet-lab biophysics, not gate-model QC). Rationale: NISQ depth and error-correction requirements exceed 156 noisy physical qubits; tiny toy instances are educational only.

---

## 4. Hardware & platform facts

All items `[chat]` and **all** `[VERIFY]` against current IBM documentation and the account dashboard — several are load-bearing for experiment selection.

**Backends & specs**

- Open Plan exposes `ibm_kingston`: Heron r2, 156 qubits, 340k CLOPS, median two-qubit error 2.03×10⁻³. (Phase 1 ran on `ibm_marrakesh`, also Heron r2 156q `[repo]`.) Whether kingston is actually Open-Plan-accessible to this account: unconfirmed.
- Heron r3 quoted at ~1.17×10⁻³ two-qubit error — **source was the pasted Grok overview, not chat-era searches; verify with extra care.**
- Comparison: Heron ~2×10⁻³ vs Google Willow ~1.5×10⁻³ (~1.3× worse per gate); heavy-hex vs Willow's square lattice ⇒ SWAP-overhead penalty for non-native connectivity.
- Heavy-hex lattice: 2–3 neighbors per qubit; long-range operations require SWAP chains (depth cost) or dynamic circuits.
- T2 ≈ 100 µs; gate times ~20–30 ns ⇒ practical depth ceiling ~3,000–5,000 gates.
- 156 **physical** qubits = 0 logical qubits. Error *mitigation*, not correction.

**Budget & execution modes**

- Standard Open Plan: **10 minutes QPU per month**, job mode. Current state: July budget untouched (~10 min available). `[repo]`
- Promotion (announced Mar 2026): one-time **180 minutes over 12 months**, triggered after 20 minutes of use, explicitly for utility-scale replication, opening `ibm_kingston`. **June 11 finding: not available to this account.** Conflict adjudication: June 11 is later and account-specific, so it wins pending a dashboard check. This is open question Q1.
- **Session mode forbidden on the free tier; Batch allowed.** Batch is ideal for swept PUBs; only QPU time counts, compilation is free. Consequence: anything variational (VQE/QAOA/kernel training) optimizes on Aer, spending QPU only on final validated circuits.
- Cost heuristics: a few-thousand-shot batch ≈ 1–3 s of QPU; avoid PEC entirely (exponential overhead); ZNE ≈ 3–5× shot overhead.

**Simulation ceilings**

- Exact statevector: theoretical ceiling ≈ 50 qubits (~18 PB of amplitudes); practical ceiling on available machines ≈ 30 qubits (June 11 working figure).
- Beyond that: MPS / tensor-network simulation — fidelity at echo-level entanglement is untested for this project's circuits (open question Q9).
- The 2^N amplitude cost applies specifically to the **entangled subspace**; separable clusters factor (2^a + 2^b, not 2^(a+b)). This is the precise sense in which wide entangled circuits escape classical simulation. `[chat, June 11 pedagogy]`

---
## 5. Verification & mitigation doctrine

The project's methodological identity, consolidated. Established in Phase 1 `[repo]`, extended for the wide regime in June `[chat]`.

**Invariant across all phases**

1. **Sim gate:** no circuit touches QPU until a noiseless (then noise-modeled) simulation reproduces the expected result.
2. **Budget guards:** hard-coded QPU-seconds guards in every experiment script.
3. **Schema-stable JSON as contract** between compute and presentation layers; the public layer renders only from committed JSON.
4. **Independent verifier** (`verify.py` pattern): recomputes the physics from raw results by an independent path; includes negative tests.
5. **Expected vs. actual vs. classical** framing on every result.
6. **Data honesty:** artifacts (e.g., the ~6.6% mitigation overshoot past 2√2) are documented, never trimmed.

**Regime-dependent verification layer** (the only part that changes between narrow and wide)

- Narrow (≤~10q): exact classical simulation, laptop-recomputable.
- Wide (30q+): scalable statistical methods — Direct Fidelity Estimation, parity oscillations, multiple-quantum coherences (MQC), cross-entropy benchmarking (XEB), tensor-network (light-cone MPS) cross-checks.
- Echoes-specific: the **no-butterfly control** as hardware-error baseline.

**Mitigation policy**

- Stack for wide runs: ZNE + TREX + dynamical decoupling (+ light Pauli twirling for echoes). Avoid PEC.
- **New failure mode to guard (added June 5): silent over-mitigation.** Every wide beat's pre-mortem includes a raw / mitigated / tensor-network ablation. This also *is* the README's "mitigation study" follow-on, promoted to standing doctrine.

---

## 6. Strategic threads (full detail)

**Publication A — scientific artifact.** Rigorous mini-echoes replication: identical circuits on (a) Heron hardware, (b) exact statevector, (c) MPS/tensor-network, with RNG-sampling machinery explicit in methods. Positioned against the classical-methods frontier: TNMC reproduces first-order OTOC to ~95q; TNBP shown unable to simulate the echoes experiment `[chat]` `[VERIFY]`. Contribution: independent cross-platform verification of the Quantum Echoes protocol in the classically verifiable regime. Novelty hinge: no public free-tier replication found in June searches `[VERIFY — this is the claim]`.

**Publication B — meta/accessibility narrative.** "Vibe-coded quantum experiments": a non-specialist runs Bell violation → scrambling experiment with full rigor via conversational AI. The two-experiment escalating arc is the story; the invisible asset is the verification labor (API version-checking, documentation validation, iterative testing). CHSH alone is hello-world; the rigor pipeline is not.

**Publication status:** whether to publish at all remains **optional/undecided**, carried from `STATE.md` and never resolved. If pursued, honest AI-assisted framing throughout. Additional pairing option: W1 + E91 as an "entanglement → cryptographic certificate" writeup.

**Platform/framework (deferred — do not build yet).**

- Concept: toggle-based, pre-validated experiment platform. Flow: describe experiment → mandatory feasibility assessor (qubits / topology / QPU-seconds) → mandatory simulate-first gate on a noise-modeled fake backend → runnable toggles → isolated IBM API adapter layer.
- Seeds: CHSH + mini-echoes (covering the Sampler-correlation and Estimator-echo circuit families).
- Recorded judgment: the **~20 pre-brainstormed experiments** (10-min and 180-min lists, from prior Opus/Grok sessions) are the core asset, not the UI. **Lists not present in any current document — retrieval required.**
- Relationship: Publication B is the platform's founding story; the platform is Publication B productized. The README's "reusable framework" follow-on is this thread's repo-native expression.
- Transfer note: the CHSH pipeline (JSON contracts, verifier, spec/human/API doc convention, expected-vs-actual-vs-classical) transfers to WIDE unchanged; **only the verification layer must be rebuilt** (exact sim → statistical witness + tensor network).

**Phase-numbering question.** The original roadmap's Phase 2 was the *presentation pipeline* (CHSH only). Unresolved: does the new experiment replace Phase 2, or does presentation ship first? Phases 5–7 (batch consolidation, Actions automation, polish) unchanged. A `WIDE_PROJECT_HANDOFF.md` (circuit primitives, JSON schemas, build phases) was offered on June 5 but never written.

**Cross-project tie-in.** M27 — the first research-project milestone of the personal research OS — has a proposed focus on exactly this cluster (discrete time crystals, OTOC/echoes, measurement-induced phase transitions) as a stress-test of that system. Decision open on whether this project doubles as M27. `[context: separate research-OS thread]`

**Landscape caveat.** The quantum-advantage tracker landscape moves monthly (IBM/Algorithmiq submissions; Gambetta's stated expectation of rigorous verification of advantage by end of 2026 `[chat]` `[VERIFY]`). Treat all "who's ahead" claims as dated snapshots.

---

## 7. Open questions & discrepancies (consolidated)

1. **Budget (top priority, decides WIDE):** 10 min/month standard `[repo]` vs. 180 min/12 months promo `[chat, June 5]` vs. "promo not available to this account" `[chat, June 11]`. Adjudication: June 11 wins (later, account-specific) — **but check the dashboard before locking any plan**. Also verify the promo trigger mechanics (reportedly fires after 20 min of use) if it turns out to be available.
2. **Backend:** stay on `ibm_marrakesh` or move to `ibm_kingston`? Is kingston actually Open-Plan-accessible now?
3. **Phase 2 definition:** presentation pipeline vs. new experiment — or re-number.
4. **Headline experiment if/when WIDE unlocks:** DTC (June 5 recommendation) vs. OTOC-at-width (June 11's most frontier-aligned) vs. MIPT (highest novelty/risk). Note the two passes' recommendations differ; mini-echoes at 30–40q is the *current* selection regardless.
5. **Over-mitigation ablation:** formalize the raw/mitigated/TN ablation as a standing pre-mortem item for every beat.
6. **Repo topology:** extend the existing repo or fork for Phase 2 / WIDE.
7. **Tensor-network simulator choice:** MPS library and bond-dimension policy — undecided.
8. **Heavy-hex overhead:** quantify SWAP/depth cost of echo circuits at 30–40q in simulation before committing QPU.
9. **40q simulability:** exact statevector caps ~30q in practice; MPS fidelity at echo-level entanglement untested. Which simulator anchors verification at 40q?
10. **Novelty check for Publication A/B:** does any public free-tier mini-echoes replication exist? (None found in June; arXiv 2510.01983 is academic, paid-scale.)
11. **Source discrepancy:** Willow described as 103 vs. 105 qubits across sources; 65q used for the headline advantage figure. Pin down when citing.
12. **Retrieve the ~20-experiment lists** (10-min and 180-min) from prior Opus/Grok sessions.
13. **M27 linkage:** does this project double as the research-OS stress-test milestone?

---

## 8. Queued study sessions (pedagogy — pointers only)

- Bell-state algebra; gate-by-gate amplitude tracking (Hadamard, CNOT, phase gates).
- Full numeric Grover walkthrough.
- Mini-echoes circuit math (the formal version of the echo protocol).
- Formal linear-algebra layer (states as vectors, gates as unitaries, projection operators).
- Heavy-hex mapping & light-cone MPS truncation.
- Bäumer long-range-entanglement protocol (dynamic circuits).
- MQC / parity-oscillation fidelity estimation.

Conceptual ground already covered (June 11, recorded as solid): superposition, measurement, entanglement and Bell states, Hilbert-space dimensionality, complex amplitudes/phase and interference, Born rule, the RNG model of measurement, oracles demystified, and the key insight that 2^N cost applies to the entangled subspace only.

---

## 9. Source register

Original sources as cited across the discussions. Citations were surfaced via in-chat web searches or pasted overviews and have **not** been re-fetched for this document — treat every entry as `[VERIFY]` before quoting in any public artifact.

**Primary experimental literature**

1. **Google "Quantum Echoes"** — OTOC-based verifiable quantum advantage, *Nature*, Oct 2025. Willow processor (103q; some sources say 105q); 65q used for the headline advantage figure; claimed 13,000× speedup over best classical (contested in the tensor-network community); "quantum-verifiable" (repeatable/cross-checkable on other quantum hardware, unlike 2019 RCS); molecular-ruler proof-of-principle cross-checked against NMR at UC Berkeley. The direct target of the mini-echoes replication.
2. **arXiv 2510.01983** — 60-qubit OTOC on `ibm_fez`; 250 circuits × 16k shots; twirling + TREX. The published-grade benchmark for the protocol on IBM hardware.
3. **IBM quantum utility experiment** — kicked transverse-field Ising on 127q Eagle, *Nature* 2023 (Kim et al., Nature 618 `[training]`); ZNE with Clifford-point ground truth; matches real-material data (e.g., KCuF₃ spin dynamics via neutron scattering `[chat, Grok overview]`). Target of W2.
4. **IBM 120-qubit GHZ** — F = 0.56(3), Nov 2025; adaptive compiler ("Big Cats" method); dynamic-circuit long-range entanglement (Bäumer protocol `[training: E. Bäumer et al., IBM, dynamic circuits for long-range entanglement]`); "temporary uncomputation." Target/reference of W1.
5. **Discrete time crystals** — early superconducting results at ~50–133q (Google 2021 Mi et al. `[training]`; subsequent IBM work); 121q "cat scar" DTC; recent finding that structured noise can stabilize oscillations; current frontier: clean 2D DTC over 100+ Floquet cycles on Heron. Target of W3.
6. **ORNL/IBM magnetic-materials simulation** — ~50q Heron r2, Mar 2026; Heisenberg/Ising on heavy-hex.
7. **Freedman–Clauser 1972** — first experimental Bell test (PRL 28, 938 `[training]`); anchor of the README's historical comparison table. `[repo]`
8. **CHSH 1969** — Clauser–Horne–Shimony–Holt (PRL 23, 880 `[training]`); Tsirelson bound 2√2. Phase 1's physics.
9. **Gidney 2025** — RSA-2048 factoring resource estimate: <~1M noisy physical qubits `[training: arXiv 2025]`. Grounds the "no Shor" scope exclusion.
10. **Classical-methods frontier for echoes** — TNMC reproduces first-order OTOC to ~95q; TNBP shown unable to simulate the echoes experiment. Grounds Publication A's positioning.
11. **Quantinuum/JPMorgan certified randomness (2025)** — surveyed June 5; excluded from scope (needs classical-supercomputer referee).
12. **IBM Open Plan promotion announcement (Mar 2026)** — 180 min / 12 months for utility-scale replication; opens `ibm_kingston`. Availability to this account disputed (Q1).
13. **IBM advantage tracker / Gambetta statement** — community-run tracker with IBM/Algorithmiq submissions; expectation of rigorously verified advantage by end of 2026.

**Project-internal sources**

- Repo: `README.md`, `STATE.md`, `HANDOFF.md`, `results/run_log_phase1.md`, `docs/index.html`, PR #3; earlier `QUANTUM_PROJECT_HANDOFF_v1.md`.
- Distilled handoffs of the June 5 and June 11 conversations (produced 2026-07-18, in-chat distillation).
- Grok 156-qubit overview document (pasted 2026-07-18): utility-scale framing, 2^156 Hilbert-space exposition, per-experiment "why width matters" arguments, Shor/Grover caveat. **Sole source of the Heron r3 ~1.17×10⁻³ figure.**

---

## 10. Discussion log — per-conversation summaries

**2026-06-03 — Phase 1 hardware run.** `[repo]` CHSH executed on `ibm_marrakesh`; results and pipeline as recorded in §2.

**~2026-06-04/05 — "Quantum physics experiments project overview."** Comprehensive summary of all project documents with `HANDOFF.md` as the deepest narrative source (alongside `QUANTUM_PROJECT_HANDOFF_v1.md`); recorded the seven-phase roadmap, the governance philosophy (AI as PI/architect, human makes all real decisions), the Phase 1 verification story (NumPy pre-verification, sim gate, grid-vs-continuum bug, negative tests, honest overshoot documentation), the compute/presentation split, and the git-coordination fix. Second request in that chat: a background essay — CHSH physics and history, comparison to the Nobel-winning experiments' charts, "spooky action at a distance," and a candid assessment of where vibe-coding a quantum experiment sits in the landscape — high register, non-expert audience.

**2026-06-05 — "Quantum computing experiments for IBM's open plan."** Two research passes. *Pass 1, frontier survey:* advantage milestones (Google Willow / Quantum Echoes, IBM utility, certified randomness), QEC milestones (below-threshold surface code, IBM qLDPC roadmap), cryptography (Gidney 2025, E91, post-quantum standards), many-body simulation (DTC, Floquet, VQE), quantum-AI integration (kernels, ML-assisted decoding), and quantum-biology/consciousness (Orch-OR, microtubule superradiance, Fisher's Posner hypothesis) — with the explicit position that gate-model QPUs cannot test consciousness claims; that is wet-lab biophysics. *Pass 2, width analysis:* corrected the budget model (found the 180-min promo and `ibm_kingston`), identified that the prior shortlist was small *by verifiability design*, articulated the exact-verification → scalable-statistical-verification pivot, and synthesized the WIDE arc (W1–W5) plus the narrow tier shortlist (GHZ/Mermin, DTC-at-small-N, mini-echoes, teleportation, repetition code, E91). Offered `FRONTIER_SURVEY.md` and `WIDE_PROJECT_HANDOFF.md` as companion docs (not written).

**2026-06-06 — "Google quantum OTOC and time-reversal mechanics."** Conceptual deep-dive on the Quantum Echoes paper: "out-of-time-order" as non-monotonic operator time indices (t, 0, t, 0) necessitating the forward/backward structure; Loschmidt-echo and NMR spin-echo as the clean analogies; the epistemic caveat that "time reversal" is an engineered inverse unitary, not thermodynamic reversal; the paper's two claims (verifiable observable with claimed 13,000× speedup; molecular-ruler proof-of-principle with Berkeley) with the speedup/hardness contestation flagged. Calibrated to the CHSH-on-Heron background. No decisions; pure background for §3.1.

**2026-06-11 — "Quantum computing experiments on IBM's free plan."** Two threads. *Experimental:* assessed five frontier experiments on Heron-class hardware; found the promo unavailable to this account; ranked candidates against the real ~8-min remaining budget; **selected mini Quantum Echoes at 30–40q** with the full spec of §3.1, the arXiv 2510.01983 precedent, the no-advantage framing discipline, and the Publication A concept (hardware vs. statevector vs. tensor-network cross-verification). *Pedagogical:* extended tutorial (superposition → measurement → entanglement → Hilbert space → phase/interference → Born rule → RNG measurement model → Bell states → oracles), with the key recorded insight that 2^N applies to the entangled subspace only; preferred explanatory style documented (flag simplifications explicitly; simplified and complete versions in parallel; intuition before formalism). Also sketched the platform idea (§6), noted the ~20-experiment lists, flagged interest in the two-publication structure, and queued the study sessions of §8.

**2026-07-06 — Documentation pass.** `[repo]` PR #3 merged: README + landing page. Repo left clean with the three "What's next" candidates listed.

**2026-07-18 — This session.** Repo-state review pasted; the June 5 and June 11 conversations distilled into handoff form; Grok 156q overview added; all three synthesized; the budget conflict adjudicated (June 11 wins pending dashboard check); the vision threads reconstructed in their original framing; this document produced as the consolidated Phase 2 reference.

---

*End of handoff. Next action: verify Q1 (budget) on the IBM dashboard, then proceed to the mini-echoes notebook build in Claude Code against the repo.*
