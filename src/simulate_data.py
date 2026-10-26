import numpy as np
import pandas as pd
from .physics_model import ROOT, FEATURES, TARGET, load_params, strength


def generate(n=None, seed=None, params=None):
    p = load_params() if params is None else params
    rng = np.random.default_rng(p["seed"] if seed is None else seed)
    n = p["n_rows"] if n is None else n
    if n < 1:
        raise ValueError("Row count must be positive.")
    df = pd.DataFrame({key: rng.uniform(*p["domain"][key], n) for key in FEATURES})
    # Gaussian multiplicative scatter; resample impossible nonpositive factors.
    factor = 1 + rng.normal(0, p["noise_cov"], n)
    while (factor <= 0).any():
        mask = factor <= 0
        factor[mask] = 1 + rng.normal(0, p["noise_cov"], mask.sum())
    df[TARGET] = strength(*(df[f].to_numpy() for f in FEATURES), params=p) * factor
    df["data_origin"] = "SIMULATED"
    df["fibre_type"], df["matrix_type"] = "E-glass", "epoxy"
    df["source_id"] = "NOMINAL_UD_SIMULATOR_V1"
    df["source_reference"] = "docs/physics_model.md; nominal assumptions, not measurements"
    df["fibre_architecture"] = "UD"
    return df


if __name__ == "__main__":
    path = ROOT / "data/simulated/simulated_e_glass_epoxy.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df = generate()
    df.to_csv(path, index=False)
    print(f"Wrote {len(df)} SIMULATED rows to {path}")
