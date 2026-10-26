import pandas as pd
from .evaluate import metrics
from .physics_model import ROOT, FEATURES, TARGET, load_params, strength
from .predict import predict
from .validation import validate, ValidationResult


def load_literature():
    frames = [pd.read_csv(path) for path in sorted((ROOT / 'data/literature').glob('*.csv'))]
    if not frames:
        raise ValueError('Literature template is missing.')
    return pd.concat(frames, ignore_index=True)


def compare_literature(df, bundle=None):
    if df.empty:
        return {'n': 0, 'rows': df.copy(), 'metrics': {}, 'per_study': [], 'report': ValidationResult(df.copy(), df.copy(), df.copy())}
    # Review is an explicit human decision, including for incomplete extractions.
    # Preserve pending rows in the report before numeric/schema validation.
    reviewed = df.get('reviewed', pd.Series('', index=df.index)).fillna('').astype(str).str.strip().str.lower().eq('yes')
    pending = df.loc[~reviewed].copy()
    if not pending.empty:
        pending['csv_row'] = pending.index + 2
        pending['reason'] = 'human review pending: reviewed must be yes'
    if reviewed.any():
        report = validate(df.loc[reviewed], expected_origin='EXPERIMENTAL_LITERATURE', literature=True)
        original_csv_rows = list(df.loc[reviewed].index + 2)
        for bucket in (report.accepted, report.rejected, report.excluded):
            if not bucket.empty:
                bucket['csv_row'] = bucket['csv_row'].map(lambda n: original_csv_rows[n - 2])
        report.excluded = pd.concat([report.excluded, pending], ignore_index=True)
    else:
        report = ValidationResult(df.iloc[:0].copy(), df.iloc[:0].copy(), pending)
    rows = report.accepted.copy()
    p = bundle['metadata']['physics_params'] if bundle else load_params()
    domain = bundle['metadata']['domain'] if bundle else p['domain']
    outside = pd.Series(False, index=rows.index)
    for f in FEATURES:
        outside |= ~rows[f].between(*domain[f])
    extra = rows.loc[outside].copy()
    if not extra.empty:
        extra['reason'] = 'outside simulator/model domain'
        report.excluded = pd.concat([report.excluded, extra], ignore_index=True)
    rows = rows.loc[~outside].copy()
    report.accepted = rows.copy()
    if rows.empty:
        return {'n': 0, 'rows': rows, 'metrics': {}, 'per_study': [], 'report': report}
    rows['simulator_mpa'] = strength(*(rows[f].to_numpy() for f in FEATURES), params=p)
    columns = ['simulator_mpa']
    if bundle:
        rows['surrogate_mpa'], _ = predict(bundle, rows)
        columns.append('surrogate_mpa')
    summary = {col: metrics(rows[TARGET], rows[col]) for col in columns}
    study = rows.get('study_id', pd.Series('', index=rows.index)).fillna('').astype(str).str.strip()
    rows['comparison_study'] = study.where(study.ne(''), rows.source_id)
    per_study = []
    for name, group in rows.groupby('comparison_study'):
        for col in columns:
            per_study.append({'study': name, 'model': col, 'n': len(group), **metrics(group[TARGET], group[col])})
    return {'n': len(rows), 'rows': rows, 'metrics': summary, 'per_study': per_study, 'report': report}
