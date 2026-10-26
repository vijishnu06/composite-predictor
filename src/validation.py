"""Explicit, row-level acceptance, rejection and exclusion reports."""
from dataclasses import dataclass
import numpy as np
import pandas as pd
from .physics_model import FEATURES, TARGET

REQUIRED = ["data_origin", "fibre_type", "matrix_type", *FEATURES, TARGET, "source_id", "source_reference"]
OPTIONAL = ["specimen_id", "study_id", "manufacturing_method", "fibre_architecture", "epoxy_grade", "test_standard", "test_temperature_c", "notes"]


@dataclass
class ValidationResult:
    accepted: pd.DataFrame
    rejected: pd.DataFrame
    excluded: pd.DataFrame

    @property
    def counts(self):
        return {k: len(getattr(self, k)) for k in ("accepted", "rejected", "excluded")}


def validate(df, expected_origin=None, literature=False):
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    if df.empty:
        raise ValueError("Empty dataset: header only or no rows.")
    data = df.copy().reset_index(drop=True)
    duplicates = data.duplicated(keep="first")
    for col in [*FEATURES, TARGET]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    buckets = {"accepted": [], "rejected": [], "excluded": []}
    for idx, row in data.iterrows():
        reasons = []
        for col in [*FEATURES, TARGET]:
            if not np.isfinite(row[col]):
                reasons.append(f"{col}: missing/non-numeric/non-finite")
        for col in FEATURES[:2]:
            if pd.notna(row[col]) and not 0 <= row[col] <= 100:
                reasons.append(f"{col}: outside 0–100 %")
        if pd.notna(row[FEATURES[2]]) and not 0 <= row[FEATURES[2]] <= 90:
            reasons.append("angle outside 0–90 degrees")
        if row[TARGET] < 0:
            reasons.append("negative strength")
        if row[FEATURES[0]] + row[FEATURES[1]] > 100:
            reasons.append("fibre plus void volume exceeds 100 %")
        if str(row.fibre_type).strip().lower() != "e-glass" or str(row.matrix_type).strip().lower() != "epoxy":
            reasons.append("incompatible material: requires E-glass/epoxy")
        allowed = {"SIMULATED", "EXPERIMENTAL_LITERATURE", "EXPERIMENTAL_UPLOAD"}
        if row.data_origin not in allowed or (expected_origin and row.data_origin != expected_origin):
            reasons.append("unexpected data_origin")
        for col in ["source_id", "source_reference"]:
            if pd.isna(row[col]) or not str(row[col]).strip():
                reasons.append(f"missing {col}")
        if duplicates.iloc[idx]:
            reasons.append("duplicate row")
        item = row.to_dict()
        item["csv_row"] = idx + 2
        if reasons:
            item["reason"] = "; ".join(reasons)
            buckets["rejected"].append(item)
        elif literature and str(row.get("fibre_architecture", "")).strip().lower() not in {"ud", "unidirectional"}:
            item["reason"] = "architecture not represented by the UD simulator (or unspecified)"
            buckets["excluded"].append(item)
        else:
            buckets["accepted"].append(item)
    return ValidationResult(**{k: pd.DataFrame(v, columns=list(data.columns) + ["csv_row"] + ([] if k == "accepted" else ["reason"])) for k, v in buckets.items()})
