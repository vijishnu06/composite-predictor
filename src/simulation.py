"""Model-based scenario comparisons, not finite-element simulations."""
import numpy as np
import pandas as pd
from .physics_model import FEATURES
from .predict import predict


def compare(bundle, scenarios):
    result = scenarios.copy().reset_index(drop=True)
    values, warnings = predict(bundle, result)
    result['estimate_mpa'] = values
    result['difference_mpa'] = values - values[0]
    result['difference_pct'] = (values - values[0]) / values[0] * 100 if values[0] != 0 else np.nan
    return result, warnings


def sensitivity(bundle, baseline, feature, points=60):
    frame = pd.DataFrame([baseline] * points)
    frame[feature] = np.linspace(*bundle['metadata']['domain'][feature], points)
    frame['estimate_mpa'], _ = predict(bundle, frame)
    return frame
