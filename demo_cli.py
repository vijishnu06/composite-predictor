"""Console demonstration using the actual saved Random Forest and simulator."""
from pathlib import Path
import pandas as pd
from src.physics_model import FEATURES, strength, ESTIMATE_LABEL
from src.predict import predict
from src.train import load_model

def main():
    model = load_model()
    frame = pd.read_csv(Path(__file__).resolve().parent / 'demo/demo_results.csv')
    frame['surrogate_mpa'] = predict(model, frame)[0]
    frame['simulator_mpa'] = strength(*(frame[f].to_numpy() for f in FEATURES))
    print(ESTIMATE_LABEL)
    print(frame[['scenario', *FEATURES, 'surrogate_mpa', 'simulator_mpa']].round(2).to_string(index=False))

if __name__ == '__main__':
    main()
