# Defect-Aware ML for E-Glass/Epoxy Composites

**SIMULATION-BASED PROTOTYPE.** A local Streamlit dashboard for an undergraduate open-elective project. Inputs are fibre volume fraction (%), void content (%) and fibre/load angle (degrees); output is tensile strength (MPa).

> Surrogate-model estimate of the simulator (simulated data) — not a measured or validated tensile strength of a real laminate

The supplied model is trained only on simulated data. Eight traceable literature table extracts are pending human review and missing required inputs; zero are eligible for comparison. The reusable literature template remains header-only. Test metrics measure agreement with simulated targets.

**For the faculty demonstration:** clone this repository or download and extract its ZIP, open this folder and double-click `START_DEMO.bat`. Python must be installed; first setup needs internet for packages. See `DEMO_START_HERE.md`. The package includes the saved model, data, code and recorded demo cases.

## Windows setup (PowerShell)

Install Python 3.11, extract the ZIP, and open PowerShell in the extracted `composite-predictor` folder. These commands avoid PowerShell activation-policy changes:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.simulate_data
.\.venv\Scripts\python.exe -m src.train
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501). Stop with Ctrl+C. Rebuilding the bundled model locally is recommended because scikit-learn model artifacts are version-sensitive. The app rejects a version mismatch and lets you retrain through its Train tab.

Optional activation: `.\.venv\Scripts\Activate.ps1`. If blocked by your PowerShell policy, keep using the explicit executable commands above; no policy change is needed.

Run software tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Python 3.11 is the requested target; the build environment supplied Python 3.14. See `docs/verification.md` for the actual verification environment and results. Dependencies are limited to the requested stack; Streamlit installs its own transitive dependencies.

## Dashboard

Nine tabs cover Overview, Dataset, Train & Evaluate, Predict, Scenario Comparison, Model Performance, Literature Check, Physics Explained, and About & Limitations. Training runs only on an explicit button press or CLI command. It is never triggered by changing a slider or rerunning the dashboard.

The two evaluated models are Linear Regression and Random Forest. The lowest random-holdout RMSE determines the saved simulated-data model. Both models also get a separate Vf-extrapolation test. The saved estimator is the holdout-fitted estimator, not a full-data refit.

Scenario differences and sensitivity curves describe model behaviour, not causation or finite-element analysis. No uncertainty interval is fabricated.

## Data and provenance

- `data/simulated/`: 2,000 reproducible nominal simulator rows, seed 42, `SIMULATED`.
- `data/literature/`: header-only template plus eight pending, incomplete table extracts; comparison requires human review and complete compatible inputs.
- `data/uploads/`: unique, never-overwritten CSV copies saved by an explicit button.
- `models/`: selected estimator and JSON metadata, hashes, units, training/test counts, held-out predictions, metrics and parameter snapshot.

Uploads require all schema columns and `EXPERIMENTAL_UPLOAD`; training also requires `study_id`. GroupShuffleSplit separates studies. One study is blocked because a group holdout is impossible; fewer than 30 rows trigger a generalisation warning. All training stays within the configured simulator domain. Uploaded models are not accepted. Only trust artifacts generated locally by this app: a hash is an integrity check, not an authentication mechanism.

Rejected and excluded rows are reported with reasons. The dashboard requires rejected rows to be corrected before training. The CLI reports validation counts and trains accepted rows; mixed origins, literature training and out-of-domain rows are blocked. Woven, random-mat and unknown literature architectures are excluded from UD comparisons.

## Adjusting the simulator

Edit `config/physics_params.json`, regenerate data, and retrain. Generation uses independent uniform feature draws, then Gaussian multiplicative scatter with nominal coefficient of variation 0.05. Nonpositive scatter factors are resampled. Physics-only estimates are deterministic. See `docs/physics_model.md` for every assumption.

Before claiming validation, obtain traceable matched UD E-glass/epoxy measurements with all inputs, review test conditions and volume definitions, calibrate parameters on separate data, and assess an independent study-level validation set with appropriate uncertainty. The shipped project has not done this.

Documentation: `docs/methodology.md`, `physics_model.md`, `data_sources.md`, `limitations.md`, `viva_notes.md`, `cv_description.md`, `github_steps.md`.

The Physics Explained tab also accepts six nominal material properties for a direct simulator experiment. These controls do not alter the saved three-feature Random Forest. Its material parameters stay fixed at its recorded training snapshot. A model that treats those properties as ML features requires a new dataset and retraining.

## Report and presentation

- [Editable SRM report](deliverables/Report.docx)
- [Report PDF](deliverables/Report_Print.pdf)
- [20-slide presentation](deliverables/Presentation_20_Slides.pptx)
- [Separate speaker notes](deliverables/Separate_Speaker_Notes.docx)
- [Gamma presentation](https://gamma.app/docs/033ddgmx4h22zj5)

Replace the administrative placeholders in the report before printing and export a new PDF after editing.
