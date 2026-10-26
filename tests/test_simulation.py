import pytest
from src.train import train
from src.simulate_data import generate
from src.simulation import compare, sensitivity
from src.physics_model import FEATURES


def test_scenario_arithmetic_and_sensitivity():
    bundle, _ = train(generate(100))
    frame = generate(3)[FEATURES]
    out, _ = compare(bundle, frame)
    assert out.iloc[0].difference_mpa == 0
    assert out.iloc[1].difference_pct == pytest.approx((out.iloc[1].estimate_mpa / out.iloc[0].estimate_mpa - 1) * 100)
    for f in FEATURES:
        sweep = sensitivity(bundle, frame.iloc[0].to_dict(), f)
        assert len(sweep) == 60
        assert all(sweep[other].nunique() == 1 for other in FEATURES if other != f)
