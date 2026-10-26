"""Explicit training command; never called implicitly on a dashboard rerun."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import joblib
import numpy as np
import sklearn
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from . import __version__
from .data_loader import read_csv
from .evaluate import metrics
from .physics_model import ROOT, FEATURES, TARGET, load_params
from .validation import validate


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def train(df):
    report = validate(df)
    clean = report.accepted.copy()
    if len(clean) < 10:
        raise ValueError("At least 10 accepted rows are required for a held-out split.")
    origins = set(clean.data_origin)
    if len(origins) != 1:
        raise ValueError("Data origins must remain separate; mixed-origin training is blocked.")
    origin = next(iter(origins))
    if origin == "EXPERIMENTAL_LITERATURE":
        raise ValueError("Literature rows are comparison-only and cannot be used for training.")
    p = load_params()
    outside = np.zeros(len(clean), dtype=bool)
    for f in FEATURES:
        outside |= ~clean[f].between(*p["domain"][f]).to_numpy()
    if outside.any():
        raise ValueError(f"{outside.sum()} accepted rows are outside the configured simulator domain; training blocked, no rows silently dropped.")
    warnings = []
    grouped = origin != "SIMULATED"
    idx = np.arange(len(clean))
    if grouped:
        if "study_id" not in clean or clean.study_id.isna().any() or clean.study_id.astype(str).str.strip().eq("").any():
            raise ValueError("Real-data training requires a nonblank study_id for every accepted row.")
        groups = clean.study_id.astype(str).str.strip()
        if groups.nunique() < 2:
            raise ValueError("Generalisation cannot be established: only one study; a study-grouped holdout requires at least two studies.")
        if len(clean) < 30:
            warnings.append("Generalisation cannot be established with fewer than 30 rows.")
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42).split(idx, groups=groups))
    else:
        tr, te = train_test_split(idx, test_size=0.2, random_state=42)
    if len(te) < 2 or len(tr) < 2:
        raise ValueError("Split needs at least two training and two test rows.")
    x, y = clean[FEATURES], clean[TARGET]
    candidates = {"Linear Regression": LinearRegression(), "Random Forest": RandomForestRegressor(n_estimators=120, min_samples_leaf=2, random_state=42, n_jobs=1)}
    results, fitted, evaluations = {}, {}, {}
    for name, model in candidates.items():
        model.fit(x.iloc[tr], y.iloc[tr])
        pred = model.predict(x.iloc[te])
        fitted[name] = model
        results[name] = {"held_out": metrics(y.iloc[te], pred), "extrapolation": None}
        evaluations[name] = {"actual": y.iloc[te].tolist(), "predicted": pred.tolist()}
        if not grouped:
            lo = x[FEATURES[0]] < 55
            if lo.sum() >= 2 and (~lo).sum() >= 2:
                extra = clone(model).fit(x.loc[lo], y.loc[lo])
                results[name]["extrapolation"] = metrics(y.loc[~lo], extra.predict(x.loc[~lo]))
    selected = min(results, key=lambda name: results[name]["held_out"]["RMSE_MPa"])
    domain = p["domain"] if not grouped else {f: [float(x.iloc[tr][f].min()), float(x.iloc[tr][f].max())] for f in FEATURES}
    metadata = {
        "creator": "composite-predictor", "version": __version__, "model_type": selected,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(), "data_origin": origin,
        "data_sha256": digest(df.to_csv(index=False).encode()),
        "physics_parameter_sha256": digest(json.dumps(p, sort_keys=True).encode()), "physics_params": p,
        "feature_names": FEATURES, "feature_units": ["%", "%", "degrees"], "target_unit": "MPa", "domain": domain,
        "train_count": len(tr), "test_count": len(te), "validation_counts": report.counts,
        "filtering_rules": "Row validation reported; mixed origins, literature training and out-of-domain rows blocked.",
        "selection_rule": "Lowest held-out RMSE; selected model retains holdout (no full-data refit).",
        "split": "study-grouped 80/20 of groups" if grouped else "random 80/20 of rows; seed 42",
        "extrapolation_counts": None if grouped else {"train": int((x[FEATURES[0]] < 55).sum()), "test": int((x[FEATURES[0]] >= 55).sum())},
        "metrics": results, "warnings": warnings, "evaluation": evaluations,
        "rf_feature_importance": fitted['Random Forest'].feature_importances_.tolist(),
        "python_version": platform.python_version(), "sklearn_version": sklearn.__version__,
        "study_split": {"train": sorted(set(groups.iloc[tr])), "test": sorted(set(groups.iloc[te]))} if grouped else None,
    }
    return {"model": fitted[selected], "metadata": metadata}, report


def save_model(bundle, directory=None):
    directory = ROOT / "models" if directory is None else Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "model.joblib"
    joblib.dump(bundle["model"], path)
    metadata = dict(bundle["metadata"], model_sha256=digest(path.read_bytes()))
    (directory / "metadata.json").write_text(json.dumps(metadata, indent=2, allow_nan=False), encoding="utf-8")


def load_model(directory=None):
    """Load app-owned local artifacts only. Never call with an upload path."""
    directory = ROOT / "models" if directory is None else Path(directory)
    meta = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    path = directory / "model.joblib"
    if meta.get("creator") != "composite-predictor" or meta.get("feature_names") != FEATURES or digest(path.read_bytes()) != meta.get("model_sha256"):
        raise ValueError("Unrecognized or corrupted model artifact; retrain in this app.")
    if meta.get("sklearn_version") != sklearn.__version__:
        raise ValueError("Saved scikit-learn version differs; retrain locally before loading.")
    return {"model": joblib.load(path), "metadata": meta}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(ROOT / "data/simulated/simulated_e_glass_epoxy.csv"))
    args = parser.parse_args()
    bundle, report = train(read_csv(args.csv))
    save_model(bundle)
    print(report.counts)
    if not report.rejected.empty:
        print(report.rejected[['csv_row', 'reason']].to_string(index=False))
    if not report.excluded.empty:
        print(report.excluded[['csv_row', 'reason']].to_string(index=False))
    print(bundle["metadata"]["model_type"], json.dumps(bundle["metadata"]["metrics"], indent=2))
