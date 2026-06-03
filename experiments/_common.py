"""
_common.py — shared helpers for the quantum-experiments project (Phase 1: CHSH).

Design rules (from the project specs):
  * The PHYSICS (circuit + observables) is verified by exact NumPy statevector sim and is
    fixed here. The IBM/Qiskit *API surface* is version-sensitive, so every runtime call is
    treated as provisional. The simulator gate (verify.py / exp1_chsh.py --sim) is the real
    correctness check, not the API spelling.
  * Credentials are NEVER literals. We read a saved account, or env vars / Colab secrets that
    the human injects. Nothing secret is ever written to a committed file.
  * Open Plan rules: channel ibm_quantum_platform; Batch or Job only (NO Session); transpile
    to ISA and remap observables with apply_layout; init the primitive inside the Batch context.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# NOTE: qiskit is imported lazily inside the functions that need it, so the analysis/JSON
# helpers (and analysis/verify.py) run with only numpy installed.


# ----------------------------------------------------------------------------------------
# Physics — VERIFIED by exact NumPy statevector simulation (see analysis/verify.py).
#   State:   H(0) · CNOT(0,1) · RY(theta, 0)   -> Bell |Phi+> with Alice's basis swept.
#   Witness: S1 = <ZZ> - <ZX> + <XZ> + <XX>    -> max|S1| = 2.8284 at theta = 0.75pi (-2v2)
#                                                  and theta = 1.75pi (+2v2); S1(0) = +2.0
#            S2 = <ZZ> + <ZX> - <XZ> + <XX>    -> companion lobe, |peak| at theta = 1.25pi
#   NOTE Qiskit is little-endian: in "ZX", Z acts on qubit 1, X acts on qubit 0.
# ----------------------------------------------------------------------------------------

# Phase 1 run parameters (kept small so a hardware job can't trip the 10-min quota).
N_PHASES_DEFAULT = 15          # spec §2: trim from the tutorial's 21; still resolves the lobes
DEFAULT_SHOTS = 4096           # spec §4: shots <= 4096
QUANTUM_BOUND = 2.0 * np.sqrt(2.0)   # 2.8284... — noiseless ceiling (Tsirelson)
CLASSICAL_BOUND = 2.0


def chsh_circuit():
    """One parameterized circuit (not four). Returns (circuit, theta_parameter)."""
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter

    theta = Parameter("theta")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)         # |Phi+>
    qc.ry(theta, 0)     # sweep Alice's measurement basis
    return qc, theta


def chsh_observables():
    """The two CHSH witnesses as SparsePauliOp. Order matches the verified NumPy sim."""
    from qiskit.quantum_info import SparsePauliOp

    obs_S1 = SparsePauliOp.from_list([("ZZ", 1), ("ZX", -1), ("XZ", 1), ("XX", 1)])
    obs_S2 = SparsePauliOp.from_list([("ZZ", 1), ("ZX", 1), ("XZ", -1), ("XX", 1)])
    return obs_S1, obs_S2


def phase_grid(n: int = N_PHASES_DEFAULT):
    """phases (rad) and the per-binding parameter list the V2 primitives expect."""
    phases = np.linspace(0.0, 2.0 * np.pi, n)
    individual_phases = [[p] for p in phases]   # one 1-element binding per phase
    return phases, individual_phases


# ----------------------------------------------------------------------------------------
# Service / backend / ISA — all version-sensitive; guarded.
# ----------------------------------------------------------------------------------------

def get_service():
    """
    Return a QiskitRuntimeService WITHOUT any credential literal.

    Resolution order:
      1. If IBM_TOKEN and IBM_CRN are in the environment (e.g. injected from Colab secrets),
         construct the service from them in-memory (still never written to disk/repo).
      2. Otherwise fall back to a previously saved account (save_account was run once by the
         human, per the setup doc) on channel ibm_quantum_platform.
    """
    from qiskit_ibm_runtime import QiskitRuntimeService

    token = os.environ.get("IBM_TOKEN")
    crn = os.environ.get("IBM_CRN")
    if token and crn:
        return QiskitRuntimeService(
            channel="ibm_quantum_platform", token=token, instance=crn
        )
    # Saved account path (channel + instance already baked into the saved profile).
    return QiskitRuntimeService()


def pick_backend(service, min_qubits: int = 2):
    """Least-busy real, operational backend. Never hard-code a name (it may be in maintenance)."""
    return service.least_busy(
        operational=True, simulator=False, min_num_qubits=min_qubits
    )


def to_isa(qc, obs_list, backend, optimization_level: int = 3):
    """
    Transpile the circuit to the backend ISA AND remap every observable to the new layout.

    Returns (isa_circuit, [isa_obs, ...]).

    The apply_layout step is the single most common silent failure on hardware: skip it and the
    observable's qubit indices no longer match the transpiled circuit's physical qubits.
    """
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

    pm = generate_preset_pass_manager(
        target=backend.target, optimization_level=optimization_level
    )
    isa_circuit = pm.run(qc)
    isa_obs = [ob.apply_layout(layout=isa_circuit.layout) for ob in obs_list]
    return isa_circuit, isa_obs


# ----------------------------------------------------------------------------------------
# Analysis helpers (no qiskit needed) — used by both the run script and verify.py.
# ----------------------------------------------------------------------------------------

def combined_peak(phases, S1, S2, S1_std=None, S2_std=None):
    """
    Find the single headline CHSH value: the largest |S| over BOTH witnesses and all phases.

    Returns dict: {S_peak_abs, S_peak_std, S_peak_theta_rad, which ("S1"/"S2")}.
    If stds are not supplied (or are all ~0, e.g. exact sim), S_peak_std is 0.0.
    """
    S1 = np.asarray(S1, dtype=float)
    S2 = np.asarray(S2, dtype=float)
    stacked = np.vstack([np.abs(S1), np.abs(S2)])          # shape (2, N)
    flat_idx = int(np.argmax(stacked))
    which_i, phase_i = np.unravel_index(flat_idx, stacked.shape)

    peak_abs = float(stacked[which_i, phase_i])
    theta = float(phases[phase_i])
    which = "S1" if which_i == 0 else "S2"

    std = 0.0
    if which_i == 0 and S1_std is not None:
        std = float(np.asarray(S1_std, dtype=float)[phase_i])
    elif which_i == 1 and S2_std is not None:
        std = float(np.asarray(S2_std, dtype=float)[phase_i])

    return {
        "S_peak_abs": peak_abs,
        "S_peak_std": std,
        "S_peak_theta_rad": theta,
        "which": which,
    }


def significance(peak_abs: float, peak_std: float) -> float:
    """z = (|S|_peak - 2) / std. Returns inf when std is 0 (exact sim)."""
    if peak_std <= 0.0:
        return float("inf")
    return (peak_abs - CLASSICAL_BOUND) / peak_std


# ----------------------------------------------------------------------------------------
# JSON IO — the layer contract (spec §8). Never contains credentials.
# ----------------------------------------------------------------------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dump_json(path, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"wrote {p}")


def load_json(path) -> dict:
    with open(path) as f:
        return json.load(f)


def software_versions() -> dict:
    out = {}
    try:
        import qiskit
        out["qiskit"] = qiskit.__version__
    except Exception:
        out["qiskit"] = "unknown"
    try:
        import qiskit_ibm_runtime
        out["qiskit_ibm_runtime"] = qiskit_ibm_runtime.__version__
    except Exception:
        out["qiskit_ibm_runtime"] = "unknown"
    return out
