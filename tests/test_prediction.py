import numpy as np
import pytest
from src.train import train
from src.simulate_data import generate
from src.predict import predict
from src.physics_model import FEATURES


def test_prediction():
    bundle, _ = train(generate(80))
    values, warnings = predict(bundle, dict(zip(FEATURES, [[40], [3], [15]])))
    assert isinstance(values[0], np.floating) and values[0] > 0
    assert not warnings
    with pytest.raises(ValueError, match='supported domain'):
        predict(bundle, dict(zip(FEATURES, [[66], [3], [15]])))
    assert predict(bundle, dict(zip(FEATURES, [[20], [3], [15]])))[1]
    with pytest.raises(ValueError, match='first'):
        predict(None, {})
