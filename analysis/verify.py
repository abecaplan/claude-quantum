"""
verify.py — independent verification of a CHSH result.

This deliberately does NOT trust the run script. It re-derives the expected witness curve from
scratch with an independent pure-NumPy statevector simulation (its own gate definitions, explicit
little-endian Pauli ordering), then checks results/chsh.json against:

  * statevector_sim run: |S| peak in [2.80, 2.85] near theta = 0.75pi or 1.75pi, AND the run's
    own S1/S2 arrays agree with the independent theory curve within tolerance.
  * hardware run:        |S| peak > 2 by >= 5 sigma, and the peak sits in a plausible theta lobe.

Exit code 0 = all assertions pass; non-zero = something failed.

Usage:
    python analysis/verify.py [path/to/chsh.json]   # default results/chsh.json
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import _common as C  # noqa: E402


# ---- independent theory (pure NumPy, no qiskit) ------------------------------------------
I2 = np.eye(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
_PAULI = {"I": I2, "X": X, "Z": Z}


def _ry(t):
    return np.array([[np.cos(t / 2), -np.sin(t / 2)],
                     [np.sin(t / 2),  np.cos(t / 2)]], dtype=complex)


def _op(s):  # qiskit little-endian: s[0]=qubit1, s[1]=qubit0
    return np.kron(_PAULI[s[0]], _PAULI[s[1]])


def _state(theta):
    psi = np.zeros(4, dtype=complex)
    psi[0] = 1.0                                   # |00>, index = q1*2 + q0
    psi = np.kron(I2, H) @ psi                     # H on q0
    cx = np.array([[1, 0, 0, 0],
                   [0, 0, 0, 1],
                   [0, 0, 1, 0],
                   [0, 1, 0, 0]], dtype=complex)   # CX control q0 -> target q1
    psi = cx @ psi
    psi = np.kron(I2, _ry(theta)) @ psi            # RY(theta) on q0
    return psi


def _ev(psi, op):
    return float(np.real(np.conj(psi) @ op @ psi))


def theory_S(theta):
    psi = _state(theta)
    zz, zx, xz, xx = (_ev(psi, _op(s)) for s in ("ZZ", "ZX", "XZ", "XX"))
    s1 = zz - zx + xz + xx
    s2 = zz + zx - xz + xx
    return s1, s2


def _fail(msg):
    print(f"  FAIL: {msg}")
    return False


def verify(path="results/chsh.json") -> bool:
    d = C.load_json(path)
    run_type = d.get("run_type", "?")
    phases = np.asarray(d["phases_rad"], dtype=float)
    S1 = np.asarray(d["S1"], dtype=float)
    S2 = np.asarray(d["S2"], dtype=float)
    peak = float(d["S_peak_abs"])
    theta_peak = float(d["S_peak_theta_rad"])
    theta_over_pi = theta_peak / np.pi

    print(f"verifying {path}  (run_type={run_type})")
    print(f"  reported |S|_peak = {peak:.4f} at theta = {theta_over_pi:.3f} pi")

    ok = True

    # (a) Theory sanity: on a FINE grid the witness must reach the Tsirelson bound 2.8284.
    fine = np.linspace(0.0, 2.0 * np.pi, 20001)
    fine_peak = float(np.max(np.abs([theory_S(t) for t in fine])))
    print(f"  independent theory peak (fine grid) = {fine_peak:.4f}  (expect {C.QUANTUM_BOUND:.4f})")
    if abs(fine_peak - C.QUANTUM_BOUND) > 1e-3:
        ok = _fail(f"independent theory itself off ({fine_peak:.4f}) — bug in verify.py")

    # (b) Independent theory sampled at the RUN's own phases (for the agreement check below).
    th_S1 = np.array([theory_S(t)[0] for t in phases])
    th_S2 = np.array([theory_S(t)[1] for t in phases])
    th_grid_peak = float(np.max(np.abs(np.vstack([th_S1, th_S2]))))
    print(f"  independent theory peak (run grid)  = {th_grid_peak:.4f}")

    # Peak theta must sit in a violation lobe (0.25/0.75/1.25/1.75 pi all reach 2v2 on one witness).
    lobes = [0.25, 0.75, 1.25, 1.75]
    if not any(abs(theta_over_pi - L) < 0.12 for L in lobes):
        ok = _fail(f"peak theta {theta_over_pi:.3f} pi not near a violation lobe {lobes}")

    if run_type == "statevector_sim":
        if not (2.80 <= peak <= 2.85):
            ok = _fail(f"sim peak {peak:.4f} outside [2.80, 2.85]")
        # The run's arrays must match independent theory (this is the strong, independent check).
        max_dev = float(np.max(np.abs(S1 - th_S1)))
        max_dev = max(max_dev, float(np.max(np.abs(S2 - th_S2))))
        print(f"  max deviation run-vs-theory = {max_dev:.2e}")
        if max_dev > 1e-3:
            ok = _fail(f"sim curve deviates from independent theory by {max_dev:.2e}")
        # S1(theta=0) ~ 2.0
        if abs(S1[0] - 2.0) > 0.02:
            ok = _fail(f"S1(theta=0) = {S1[0]:.4f}, expected ~2.0")

    elif run_type == "hardware":
        if not (peak > C.CLASSICAL_BOUND):
            ok = _fail(f"hardware peak {peak:.4f} does not exceed 2")
        z = d.get("violation_significance_sigma")
        if z is None:
            ok = _fail("hardware run has no significance (need per-point std)")
        elif z < 5.0:
            ok = _fail(f"hardware violation only {z} sigma (< 5)")
        else:
            print(f"  hardware violation significance = {z} sigma")
        # Sanity: a real device shouldn't beat the noiseless ceiling.
        if peak > C.QUANTUM_BOUND + 0.05:
            ok = _fail(f"hardware peak {peak:.4f} exceeds Tsirelson bound — suspect a bug")
    else:
        ok = _fail(f"unknown run_type '{run_type}'")

    print("VERIFY: PASS" if ok else "VERIFY: FAIL")
    return ok


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "results/chsh.json"
    sys.exit(0 if verify(target) else 1)
