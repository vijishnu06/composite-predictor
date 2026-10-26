"""Deterministic nominal UD laminate model; inputs in percent and degrees."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["fibre_volume_fraction_pct", "void_content_pct", "misalignment_angle_deg"]
TARGET = "tensile_strength_mpa"
ESTIMATE_LABEL = "Surrogate-model estimate of the simulator (simulated data) — not a measured or validated tensile strength of a real laminate"


def load_params():
    return json.loads((ROOT / "config/physics_params.json").read_text(encoding="utf-8"))


def strength(vf_pct, void_pct, angle_deg, params=None):
    """Return noise-free nominal tensile strength in MPa (scalar or array)."""
    p = load_params() if params is None else params
    vf, vv, angle = np.broadcast_arrays(*[np.asarray(x, dtype=float) for x in (vf_pct, void_pct, angle_deg)])
    if not all(np.isfinite(x).all() for x in (vf, vv, angle)):
        raise ValueError("Inputs must be finite numbers.")
    if ((vf < 0) | (vf > 100) | (vv < 0) | (vv > 100) | (angle < 0) | (angle > 90) | (vf + vv > 100)).any():
        raise ValueError("Invalid volume fractions or angle.")
    threshold = p["eta_full_until_vf_pct"]
    eta = 1 - (1 - p["eta_at_70"]) * np.clip((vf - threshold) / (70 - threshold), 0, 1)
    sm = min(p["matrix_strength_mpa"], p["matrix_modulus_gpa"] * p["fibre_strength_mpa"] / p["fibre_modulus_gpa"])
    x = (eta * vf / 100 * p["fibre_strength_mpa"] + (1 - vf / 100) * sm) * np.exp(-p["k_void_fibre_per_pct"] * vv)
    y = p["transverse_strength_mpa"] * np.exp(-p["k_void_matrix_per_pct"] * vv)
    s = p["shear_strength_mpa"] * np.exp(-p["k_void_matrix_per_pct"] * vv)
    c, t = np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))
    result = 1 / np.sqrt(c**4 / x**2 + (1 / s**2 - 1 / x**2) * t**2 * c**2 + t**4 / y**2)
    return float(result) if result.ndim == 0 else result
