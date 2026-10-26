"""Synthetic test fixtures only; these are not experimental evidence."""
import pandas as pd
import pytest
from src.simulate_data import generate
from src.physics_model import FEATURES, TARGET, strength
from src.literature_validation import compare_literature
from src.train import train


def test_empty_and_architecture():
    df = generate(12)
    assert compare_literature(df.iloc[:0])['n'] == 0
    df['data_origin'] = 'EXPERIMENTAL_LITERATURE'
    df['reviewed'] = 'yes'
    df['source_reference'] = 'SYNTHETIC TEST-ONLY fixture, not a paper'
    df['study_id'] = 'TEST_ONLY'
    df[TARGET] = strength(*(df[f].to_numpy() for f in FEATURES))
    df.loc[0, 'fibre_architecture'] = 'woven'
    df.loc[1, FEATURES[0]] = 70
    result = compare_literature(df, train(generate(100))[0])
    assert result['n'] == 10
    assert result['report'].counts['excluded'] == 2
    assert result['metrics']['simulator_mpa']['RMSE_MPa'] == pytest.approx(0)
    assert result['per_study'][0]['n'] == 10
    assert len(result['per_study']) == 2


def test_unreviewed_rows_are_excluded_even_when_inputs_missing():
    df = generate(3).astype(object)
    df['data_origin'] = 'EXPERIMENTAL_LITERATURE'
    df['reviewed'] = ['no', '', 'yes']
    df.loc[0, 'void_content_pct'] = ''
    result = compare_literature(df)
    assert result['n'] == 1
    assert result['report'].counts == {'accepted': 1, 'rejected': 0, 'excluded': 2}
    assert set(result['report'].excluded.csv_row) == {2, 3}
    assert compare_literature(df.drop(columns='reviewed'))['n'] == 0
