# Build verification

Verified on Windows, Python 3.14.0. Python 3.11 is the requested deployment target but was not installed in the build environment, so it was not directly tested. Install requirements and retrain in your local Python 3.11 environment as described in README.

## Software checks

- 21 pytest tests passed in a complete run from the project directory on 25 October 2026. A collection attempt from the workspace parent could not import src; the corrected project-directory invocation passed all tests.
- Streamlit AppTest passed: all nine tabs render; estimate button produces an MPa value; out-of-domain input is rejected; scenario comparison produces difference columns. The six additional material controls produce the expected 498.7 MPa direct simulator baseline and respond to a changed material input. Literature eligibility remains zero.
- Headless server returned HTTP 200 from its health endpoint and was stopped. Sandbox-local networking blocked the first attempt; verification succeeded with localhost access. Development mode was explicitly disabled for the workspace dependency installation.
- Tests use simulated or explicitly labelled synthetic fixtures. Eight source-linked literature table extracts remain pending review and missing required inputs; zero are eligible for comparison. No literature rows enter model training.
- NumPy/joblib emitted deprecation warnings during model loading; persistence round-trip passed. Model files are version-sensitive: regenerate/retrain after installing locally.

## Environment

- numpy: 2.5.4
- pandas: 3.0.6
- scikit-learn: 1.9.0
- matplotlib: 3.11.1
- joblib: 1.5.3
- streamlit: 1.66.1
- pytest: 9.1.1

## Trained artifact

- Origin: SIMULATED; 2,000 simulated rows, 1600 training / 400 random holdout.
- Selected estimator: Random Forest.
- Random holdout RMSE: 18.2137 MPa.
- Vf extrapolation RMSE: 28.6331 MPa.
- These are surrogate-versus-simulator scores, not experimental validation.

Surrogate-model estimate of the simulator (simulated data) — not a measured or validated tensile strength of a real laminate

The reusable literature template contains one header line and zero data rows. Eight pending extracts live in a separate CSV. Independent, traceable compatible measurements, calibration and held-out scientific evaluation remain necessary before validation claims.
