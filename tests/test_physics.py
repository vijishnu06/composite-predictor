import numpy as np
import pytest
from src.physics_model import load_params, strength
from src.simulate_data import generate


def test_identities():
    p = load_params()
    sm = min(55, 2.4 * 1750 / 73)
    assert strength(50, 0, 0) == pytest.approx(0.5 * 1750 + 0.5 * sm)
    assert strength(50, 0, 90) == pytest.approx(40)
    assert strength(50, 4, 0) / strength(50, 0, 0) == pytest.approx(np.exp(-p['k_void_fibre_per_pct'] * 4))
    assert strength(50, 4, 90) / strength(50, 0, 90) == pytest.approx(np.exp(-p['k_void_matrix_per_pct'] * 4))


def test_reproducible():
    assert generate(40, 42).equals(generate(40, 42))
    assert not generate(40, 42).equals(generate(40, 43))
    assert set(generate(40).data_origin) == {'SIMULATED'}


@pytest.mark.parametrize('inputs', [(50, 0, -1), (101, 0, 0), (50, float('nan'), 0)])
def test_invalid(inputs):
    with pytest.raises(ValueError):
        strength(*inputs)
