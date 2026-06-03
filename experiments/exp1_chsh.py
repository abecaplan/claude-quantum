"""
exp1_chsh.py — Phase 1 CHSH / Bell test.

Two paths, one construction:
  --sim       (default) noiseless StatevectorEstimator. The HARD GATE: |S| peak in [2.80, 2.85]
              near theta = 0.75pi (or 1.75pi), and S1(0) ~ 2.0. No token, no network.
  --hardware  least-busy real backend, ISA transpile + apply_layout, EstimatorV2 in JOB MODE.
              ONLY run this after the sim gate passes. Costs ~1-2 min of the 10-min monthly quota.

Execution mode (v2): Phase 1 is a SINGLE job, so it uses plain JOB MODE — `Estimator(mode=backend)` —
exactly as IBM's canonical CHSH tutorial does. The docs state batches give no benefit for a single
job, and job mode avoids the 10-min Open-Plan batch TTL ceiling and the historical instance+Batch
edge case. Batch is reserved for Phase 5 (running all three experiments in one pass). NEVER use
`Estimator(backend=...)` (deprecated since runtime 0.24, silently forces job mode); always `mode=`.
Sessions are forbidden on the Open Plan.

Both paths write the SAME schema to results/chsh.json (run_type distinguishes them). The JSON is
the contract Phase 2 reads — never the live run.

Usage:
    python experiments/exp1_chsh.py --sim
    python experiments/exp1_chsh.py --hardware        # only after the gate passes
    python experiments/exp1_chsh.py --sim --out results/chsh_sim.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

# Allow running as `python experiments/exp1_chsh.py` from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402


# Gate thresholds (spec §1, §7).
SIM_PEAK_LO, SIM_PEAK_HI = 2.80, 2.85
HW_MIN_SIGMA = 5.0


def _extract_evs_stds(pub_result):
    """
    Pull the (2, N) arrays out of a V2 PUB result, tolerant of minor API drift.
    Returns (S1, S2, S1_std, S2_std) as numpy arrays; stds default to zeros if absent.
    """
    data = pub_result.data
    evs = np.asarray(data.evs, dtype=float)          # expected shape (2, N)
    S1, S2 = evs[0], evs[1]
    try:
        stds = np.asarray(data.stds, dtype=float)
        S1_std, S2_std = stds[0], stds[1]
    except Exception:
        S1_std = np.zeros_like(S1)
        S2_std = np.zeros_like(S2)
    return S1, S2, S1_std, S2_std


def run_sim(n_phases: int = C.N_PHASES_DEFAULT):
    """Noiseless exact statevector sweep. No credentials, no network."""
    from qiskit.primitives import StatevectorEstimator

    qc, _ = C.chsh_circuit()
    obs_S1, obs_S2 = C.chsh_observables()
    phases, individual_phases = C.phase_grid(n_phases)

    estimator = StatevectorEstimator()
    # Same broadcasting pattern as the hardware path: observables (2,1) x params (N,) -> (2,N).
    pub = (qc, [[obs_S1], [obs_S2]], individual_phases)
    result = estimator.run(pubs=[pub]).result()
    S1, S2, S1_std, S2_std = _extract_evs_stds(result[0])

    return _assemble_payload(
        run_type="statevector_sim",
        backend_name="statevector_sim",
        phases=phases,
        S1=S1, S2=S2, S1_std=S1_std, S2_std=S2_std,
        shots=None, resilience_level=None, dynamical_decoupling=False,
        qubits_used=[0, 1],
    )


def run_hardware(n_phases: int = C.N_PHASES_DEFAULT, shots: int = C.DEFAULT_SHOTS):
    """
    Hardware sweep on the least-busy real backend, in JOB MODE (single job).

    Open Plan rules enforced: job mode (never Session); ISA transpile + apply_layout on the
    observables. `Estimator(mode=backend)` — never `backend=` (deprecated, silently job mode).
    """
    from qiskit_ibm_runtime import EstimatorV2 as Estimator

    qc, _ = C.chsh_circuit()
    obs_S1, obs_S2 = C.chsh_observables()
    phases, individual_phases = C.phase_grid(n_phases)

    service = C.get_service()
    backend = C.pick_backend(service)
    print(f"selected backend: {backend.name}")

    isa_circuit, (isa_S1, isa_S2) = C.to_isa(qc, [obs_S1, obs_S2], backend)
    print(f"ISA circuit depth: {isa_circuit.depth()}  (physical qubits: {isa_circuit.num_qubits})")

    resilience_level = 1  # default; readout mitigation already on -> clean violation.
    dd_enabled = False

    # JOB MODE: one PUB, one job, no context manager. Matches the IBM CHSH tutorial exactly.
    estimator = Estimator(mode=backend)            # MUST be mode=, never backend=
    estimator.options.default_shots = shots
    # resilience_level default = 1; set explicitly so the JSON metadata is honest.
    try:
        estimator.options.resilience_level = resilience_level
    except Exception:
        pass
    try:
        estimator.options.dynamical_decoupling.enable = True   # free fidelity on idle qubits
        dd_enabled = True
    except Exception:
        dd_enabled = False

    pub = (isa_circuit, [[isa_S1], [isa_S2]], individual_phases)
    result = estimator.run(pubs=[pub]).result()

    S1, S2, S1_std, S2_std = _extract_evs_stds(result[0])

    return _assemble_payload(
        run_type="hardware",
        backend_name=backend.name,
        phases=phases,
        S1=S1, S2=S2, S1_std=S1_std, S2_std=S2_std,
        shots=shots, resilience_level=resilience_level, dynamical_decoupling=dd_enabled,
        qubits_used=[0, 1],
    )


def _assemble_payload(run_type, backend_name, phases, S1, S2, S1_std, S2_std,
                      shots, resilience_level, dynamical_decoupling, qubits_used):
    peak = C.combined_peak(phases, S1, S2, S1_std, S2_std)
    z = C.significance(peak["S_peak_abs"], peak["S_peak_std"])

    return {
        "experiment": "chsh",
        "method": "estimator_sweep",
        "run_type": run_type,
        "backend": backend_name,
        "timestamp_utc": C.utc_now_iso(),
        "shots": shots,
        "resilience_level": resilience_level,
        "dynamical_decoupling": dynamical_decoupling,
        "phases_rad": [float(p) for p in phases],
        "S1": [float(v) for v in S1],
        "S1_std": [float(v) for v in S1_std],
        "S2": [float(v) for v in S2],
        "S2_std": [float(v) for v in S2_std],
        "S_peak_abs": round(peak["S_peak_abs"], 6),
        "S_peak_std": round(peak["S_peak_std"], 6),
        "S_peak_theta_rad": round(peak["S_peak_theta_rad"], 6),
        "S_peak_witness": peak["which"],
        "classical_bound": C.CLASSICAL_BOUND,
        "quantum_bound": round(C.QUANTUM_BOUND, 4),
        "violation": bool(peak["S_peak_abs"] > C.CLASSICAL_BOUND),
        "violation_significance_sigma": (None if z == float("inf") else round(z, 2)),
        "qubits_used": qubits_used,
        "software": C.software_versions(),
    }


def _check_sim_gate(payload) -> bool:
    peak = payload["S_peak_abs"]
    theta_over_pi = payload["S_peak_theta_rad"] / np.pi
    # S1(theta=0) is the first phase point of S1.
    s1_at_0 = payload["S1"][0]
    ok_peak = SIM_PEAK_LO <= peak <= SIM_PEAK_HI
    # Whichever witness wins the tie, the peak must sit at a genuine violation lobe.
    lobes = [0.25, 0.75, 1.25, 1.75]
    ok_theta = any(abs(theta_over_pi - L) < 0.12 for L in lobes)
    ok_s10 = abs(s1_at_0 - 2.0) < 0.05
    print(f"  |S| peak        = {peak:.4f}   (gate [{SIM_PEAK_LO}, {SIM_PEAK_HI}])  -> {'OK' if ok_peak else 'FAIL'}")
    print(f"  peak at theta   = {theta_over_pi:.3f} pi  (expect a 0.25/0.75/1.25/1.75 lobe) -> {'OK' if ok_theta else 'FAIL'}")
    print(f"  S1(theta=0)     = {s1_at_0:.4f}   (expect ~2.0)              -> {'OK' if ok_s10 else 'FAIL'}")
    return ok_peak and ok_theta and ok_s10


def main():
    ap = argparse.ArgumentParser(description="Phase 1 CHSH sweep")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--sim", action="store_true", help="noiseless statevector sweep (default)")
    mode.add_argument("--hardware", action="store_true", help="real backend (only after the gate)")
    ap.add_argument("--n", type=int, default=C.N_PHASES_DEFAULT, help="number of phase points")
    ap.add_argument("--shots", type=int, default=C.DEFAULT_SHOTS, help="shots (hardware)")
    ap.add_argument("--out", type=str, default="results/chsh.json", help="output JSON path")
    args = ap.parse_args()

    use_hardware = args.hardware  # sim is the default when neither flag is given

    if use_hardware:
        if args.shots > C.DEFAULT_SHOTS:
            sys.exit(f"refusing shots > {C.DEFAULT_SHOTS} (quota guard). Got {args.shots}.")
        print("=== HARDWARE run (spends QPU budget) ===")
        payload = run_hardware(n_phases=args.n, shots=args.shots)
        C.dump_json(args.out, payload)
        z = payload["violation_significance_sigma"]
        print(f"\nbackend {payload['backend']}: |S|_peak = {payload['S_peak_abs']:.3f} "
              f"+/- {payload['S_peak_std']:.3f}  (z = {z} sigma)")
        if payload["violation"] and z is not None and z >= HW_MIN_SIGMA:
            print(f"VIOLATION confirmed: |S| > 2 by >= {HW_MIN_SIGMA} sigma.")
        else:
            print("WARNING: violation not confirmed at >= 5 sigma — inspect the curve.")
    else:
        print("=== SIMULATOR run (noiseless, exact) — the correctness gate ===")
        payload = run_sim(n_phases=args.n)
        print("\nSIM GATE:")
        passed = _check_sim_gate(payload)
        C.dump_json(args.out, payload)
        if passed:
            print("\nSIM GATE PASSED — construction is correct; hardware run is unlocked.")
        else:
            sys.exit("\nSIM GATE FAILED — DO NOT run on hardware. Fix the construction first.")


if __name__ == "__main__":
    main()
