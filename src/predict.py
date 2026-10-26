import numpy as np
import pandas as pd
from .physics_model import FEATURES, ESTIMATE_LABEL


def prediction_label(bundle):
    if bundle["metadata"]["data_origin"] == "SIMULATED":
        return ESTIMATE_LABEL
    return "Experimental-upload model estimate (MPa) — generalisation not established; not a measured tensile strength"


def predict(bundle, inputs):
    if bundle is None:
        raise ValueError("Load or train a model first.")
    frame = pd.DataFrame(inputs) if not isinstance(inputs, pd.DataFrame) else inputs.copy()
    if frame.empty or not set(FEATURES).issubset(frame.columns):
        raise ValueError("Provide all three input features.")
    warnings = []
    for feature in FEATURES:
        frame[feature] = pd.to_numeric(frame[feature], errors="coerce")
        low, high = bundle["metadata"]["domain"][feature]
        if not np.isfinite(frame[feature]).all() or not frame[feature].between(low, high).all():
            raise ValueError(f"{feature}: supported domain is {low:g}–{high:g}.")
        if ((frame[feature] - low <= (high - low) * 0.05) | (high - frame[feature] <= (high - low) * 0.05)).any():
            warnings.append(f"Near domain edge: {feature}.")
    values = np.asarray(bundle["model"].predict(frame[FEATURES]), dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("Model produced a nonphysical estimate; inspect model performance or choose another input.")
    return values, warnings
