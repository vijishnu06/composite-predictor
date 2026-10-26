import io
import pandas as pd
import pytest
from src.simulate_data import generate
from src.validation import validate
from src.data_loader import read_csv


def test_csv():
    df = read_csv(io.StringIO(generate(10).to_csv(index=False)))
    assert validate(df).counts == {'accepted': 10, 'rejected': 0, 'excluded': 0}


@pytest.mark.parametrize('column,value', [('void_content_pct', ''), ('fibre_volume_fraction_pct', 101), ('misalignment_angle_deg', 91), ('tensile_strength_mpa', -2), ('matrix_type', 'steel'), ('source_id', ''), ('void_content_pct', 'x'), ('tensile_strength_mpa', float('inf'))])
def test_reject(column, value):
    df = generate(10).astype(object)
    df.loc[0, column] = value
    report = validate(df)
    assert report.counts == {'accepted': 9, 'rejected': 1, 'excluded': 0}
    assert report.rejected.iloc[0].reason


def test_missing_empty_duplicates():
    with pytest.raises(ValueError, match='Missing columns'):
        validate(pd.DataFrame({'a': [1]}))
    with pytest.raises(ValueError, match='Empty'):
        read_csv(io.StringIO(''))
    with pytest.raises(ValueError, match='Empty'):
        validate(generate(10).iloc[:0])
    df = generate(10)
    assert validate(pd.concat([df, df.iloc[:1]])).counts['rejected'] == 1
