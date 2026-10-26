# Run the composite model demonstration

Extract the ZIP first. Open the `composite-predictor` folder and double-click **START_DEMO.bat**. Python must be installed and available through `py` or `python`. The first run needs internet access to install dependencies into a local `.venv`. If Python is missing, install Python 3.11 or newer and enable its command-line launcher, then retry. The original target is Python 3.11; verification details are in `docs/verification.md`.

The launcher reuses the saved model when compatible. Otherwise it retrains from the supplied SIMULATED CSV using your installed library versions. Keep the console open. Open the localhost address printed by Streamlit, usually http://localhost:8501. Stop with Ctrl+C. Set this up before the faculty review; a second run can reuse the environment without installing packages.

## Demonstrate in this order

1. Overview: explain that this is an educational simulator-surrogate model.
2. Dataset: show 2,000 SIMULATED rows, three features and the generated strength target.
3. Train & Evaluate: show the Linear Regression and Random Forest comparison. Training is an explicit button action; it is not needed for every prediction.
4. Predict: use fibre 45%, void 2%, angle 5°. Increase only voids to 6%. Restore 2% voids and increase only angle to 20°.
5. Scenario Comparison: compare defect scenarios with the baseline.
6. Predict: enter fibre 90% to show domain rejection, then restore 45%.
7. Physics Explained: change one of the six material properties and press **Calculate direct simulator experiment**. This uses the equation directly and does not change the saved three-feature ML model.
8. Literature Check: explain why the eight pending extracts are incomplete for comparison and why eligible n remains zero.

`demo/demo_results.csv` records nine cases from the supplied trained model. The separate speaking guide explains the slides and likely faculty questions. On a fresh local retrain, small output differences may occur with software versions.

## Console demonstration

After the setup, from the extracted folder:

```powershell
.\.venv\Scripts\python.exe demo_cli.py
```

To train manually, use `.\.venv\Scripts\python.exe -m src.train`. If port 8501 is busy, run `.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502`.

## What the files contain

`app.py` is the dashboard; `src/` contains the simulator, training and inference code. `models/model.joblib` is the fitted estimator; `models/metadata.json` records its inputs, provenance, metrics and version. `data/simulated/` contains the reproducible training CSV. The six additional material controls belong to a direct simulator experiment; they are not additional trained Random Forest features.

Outputs describe an assumed simulator. They have not been validated as measured strengths of real laminates.
