import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def metrics(actual, predicted):
    return {"MAE_MPa": float(mean_absolute_error(actual, predicted)),
            "RMSE_MPa": float(np.sqrt(mean_squared_error(actual, predicted))),
            "R2": float(r2_score(actual, predicted)) if len(actual) > 1 and np.var(actual) > 0 else None}
