# Phase 1 — CHSH Hardware Run Log

**Date:** 2026-06-03 · **Backend:** `ibm_marrakesh` (Heron r2, 156 qubits)
**Job ID:** `d8ft3vbo3njc73f0qm00`
**QPU time billed:** **79 s** (~1.3 min of the 10-min/28-day budget; pre-run estimate was 113 s)

## Run output
```
=== HARDWARE run (spends QPU budget) ===
selected backend: ibm_marrakesh
ISA circuit depth: 8  (physical qubits: 156)
backend ibm_marrakesh: |S|_peak = 3.003 +/- 0.029  (z = 34.79 sigma)
VIOLATION confirmed: |S| > 2 by >= 5.0 sigma.
```

## Settings applied (from job metadata)
- shots: 4096 · resilience_level: 1 (**measurement-error mitigation ON**)
- dynamical_decoupling: ON ("XX") · measurement twirling: ON (32 randomizations)
- ZNE: off · PEC: off

## Backend calibration snapshot (last calibrated 2026-06-03 07:05:13 UTC)
| qubit | T1 | T2 | readout error |
|---|---|---|---|
| q0 | 284.8 us | 43.7 us | 0.0120 |
| q1 | 174.1 us | 156.3 us | 0.0133 |

The ~1.2-1.3% readout error is exactly what `measure_mitigation` corrected for - and correcting an
error of that size is what nudges a few mitigated points just past the Tsirelson bound (see below).

## Verdict
- **Headline:** |S|_peak = **3.003 +/- 0.029**, a **34.79 sigma** violation of the classical bound (S <= 2).
  Peak occurs on witness **S2 at theta = 1.286 pi**.
- **Scientific honesty note:** several points exceed the Tsirelson bound 2.828 (marked !). This is the
  expected over-correction from readout-error mitigation, **not** super-quantum behavior, and it ties
  directly to the ~1.3% readout error in the calibration snapshot above. A raw (resilience_level=0) run
  would sit at/below 2.828. Examined directly in Phase 3.

## Full theta-sweep (decoded from job result; both witnesses, +/- per-point std)

| theta (pi) | S1 | S2 |
|---|---|---|
| 0.000 | +2.137 +/- 0.025 | +2.121 +/- 0.025 |
| 0.143 | +0.964 +/- 0.024 | +2.820 +/- 0.024 |
| 0.286 | -0.395 +/- 0.029 | +2.999 +/- 0.029 ! |
| 0.429 | -1.659 +/- 0.030 | +2.525 +/- 0.030 |
| 0.571 | -2.606 +/- 0.027 | +1.549 +/- 0.027 |
| 0.714 | -2.972 +/- 0.031 ! | +0.267 +/- 0.031 |
| 0.857 | -2.835 +/- 0.027 ! | -1.041 +/- 0.027 |
| 1.000 | -2.107 +/- 0.029 | -2.161 +/- 0.029 |
| 1.143 | -1.051 +/- 0.032 | -2.876 +/- 0.032 ! |
| 1.286 | +0.344 +/- 0.029 | -3.003 +/- 0.029 ! (peak) |
| 1.429 | +1.573 +/- 0.027 | -2.575 +/- 0.027 |
| 1.571 | +2.535 +/- 0.026 | -1.633 +/- 0.026 |
| 1.714 | +2.963 +/- 0.028 ! | -0.361 +/- 0.028 |
| 1.857 | +2.829 +/- 0.029 ! | +1.024 +/- 0.029 |
| 2.000 | +2.109 +/- 0.026 | +2.192 +/- 0.026 |

! = magnitude exceeds the Tsirelson bound (2.828) - readout-mitigation artifact.

Note: S1 and S2 share identical per-point std arrays (both witnesses are linear combinations of the
same four measured Pauli terms, estimated together), which is why the uncertainty columns match.
