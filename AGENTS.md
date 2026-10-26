

## Project
**Defect-Aware ML for Predicting Tensile Strength of E-Glass/Epoxy Composites** (fibre volume fraction, void content, fibre misalignment angle → tensile strength in MPa). Undergraduate open-elective project. Python 3.11, Streamlit, pandas, NumPy, scikit-learn, Matplotlib, Joblib, pytest. Windows-friendly, runs locally, no paid services.

## Data strategy (Plan C) — the most important rule
No open dataset covers all three inputs, and there is no lab data. So the project has two strictly separate data layers:

1. **Simulated training data** — generated from a documented micromechanics model (below). Every row has `data_origin = SIMULATED`. ML models are trained on this by default.
2. **Literature validation data** — real published measurements, kept in `data/literature/`, with `data_origin = EXPERIMENTAL_LITERATURE`. Used ONLY to compare against the simulator and the trained models. Never mixed into training, never relabelled.

**Honesty rules (never break these):**
- Never invent experimental values, papers, authors, DOIs or citations. If a value is not verified, it does not go in the data.
- Ship `data/literature/literature_template.csv` with the header row ONLY (no example rows). The user fills it manually from papers.
- Everywhere a prediction appears, label it "Surrogate-model estimate of the simulator (simulated data) — not a measured or validated tensile strength of a real laminate".
- Never claim the model is experimentally validated. Only state literature-comparison metrics once real rows exist, with the row count n.
- No fake confidence intervals. Random-forest tree spread is not a prediction interval.
- Feature importance and sensitivity plots are model behaviour, not proof of causation.

## Physics model (`src/physics_model.py`, parameters in `config/physics_params.json`)
Models a UD E-glass/epoxy laminate. All parameters are **nominal modelling assumptions**, each documented in `docs/physics_model.md` with a plain-language explanation; none are measurements. Defaults:

| Parameter | Default | Meaning |
|---|---|---|
| fibre_strength_mpa | 1750 | effective fibre strength in composite |
| fibre_modulus_gpa | 73 | E-glass modulus |
| matrix_strength_mpa | 55 | epoxy tensile strength |
| matrix_modulus_gpa | 2.4 | epoxy modulus |
| transverse_strength_mpa (Y) | 40 | across-fibre strength |
| shear_strength_mpa (S) | 60 | in-plane shear strength |
| k_void_fibre_per_pct | 0.010 | void sensitivity, fibre-dominated strength |
| k_void_matrix_per_pct | 0.040 | void sensitivity, matrix-dominated strength |
| eta_full_until_vf_pct / eta_at_70 | 55 / 0.80 | fibre efficiency falls linearly above 55 % Vf to 0.80 at 70 % |
| noise_cov | 0.05 | multiplicative scatter, fixed seed |

Calculation order (Vf as fraction, Vv in %, θ = angle between fibres and load, 0° = fibres parallel to load):
1. Matrix stress at fibre failure: `sigma_m_prime = min(matrix_strength, E_m * (fibre_strength / E_f))`.
2. `X = eta(Vf) * Vf * fibre_strength + (1 - Vf) * sigma_m_prime`.
3. Void knock-downs: `X_v = X * exp(-k_fibre * Vv)`; `Y_v = Y * exp(-k_matrix * Vv)`; `S_v = S * exp(-k_matrix * Vv)`.
4. Off-axis Tsai–Hill: `1/sigma^2 = cos^4θ/X_v^2 + (1/S_v^2 - 1/X_v^2) sin^2θ cos^2θ + sin^4θ/Y_v^2`.
5. Multiply by `(1 + noise)` for the dataset only (not for the pure physics function).

Simulation domain (config): Vf 20–65 %, void 0–8 %, angle 0–45°. Default 2000 rows, seed 42.
Because voids reduce tensile strength only mildly in some published glass/epoxy studies, void sensitivity must stay an adjustable parameter, and the docs must say it is meant to be calibrated against literature data when available.

## Repository layout
```
app.py  requirements.txt  README.md  AGENTS.md  .gitignore
config/physics_params.json
data/{simulated,literature,uploads}/   models/
src/{__init__,physics_model,simulate_data,data_loader,validation,train,evaluate,predict,simulation,literature_validation,plotting}.py
tests/test_{physics,validation,training,prediction,simulation,literature}.py
docs/{methodology,physics_model,data_sources,limitations,viva_notes,cv_description,github_steps}.md
```

## Data schema
Required columns: `data_origin, fibre_type, matrix_type, fibre_volume_fraction_pct, void_content_pct, misalignment_angle_deg, tensile_strength_mpa, source_id, source_reference`.
Optional: `specimen_id, study_id, manufacturing_method, fibre_architecture, epoxy_grade, test_standard, test_temperature_c, notes`.
Validation: missing columns, empty file, non-numeric values, percentages outside 0–100, negative strength, angle outside 0–90, duplicates, missing source info, non-E-glass/epoxy rows. Blank is never treated as zero. Never silently drop rows: report accepted / rejected / excluded counts with reasons. Never overwrite uploads.
Literature rows with woven or random-mat architecture are flagged "architecture not represented by the UD simulator" and excluded from the comparison by default.

## ML rules
- Models: Linear Regression (baseline) and Random Forest (`random_state=42`, modest size). Compare objectively; do not assume Random Forest wins.
- Default split: random 80/20 on simulated data **plus** an extrapolation test (train Vf < 55 %, test Vf ≥ 55 %). Report both.
- Selection rule: lowest held-out RMSE on the random split; report extrapolation RMSE beside it.
- Metrics: MAE (MPa), RMSE (MPa), R². Never report training-set metrics as test metrics.
- If the user uploads real experimental data, allow training on it with study-grouped splits (GroupKFold / GroupShuffleSplit). If only one study or fewer than 30 rows, show a "generalisation cannot be established" warning.
- Save to `models/`: model, feature names and units, metadata (type, timestamp, data hash, `data_origin`, train/test counts, metrics, filtering rules, physics-parameter hash, version). Load only models this app created; never load arbitrary uploaded model files.
- Never retrain on a Streamlit rerun; training happens only on a button press.

## App (Streamlit, clean engineering style)
Tabs: Overview · Dataset · Train & Evaluate · Predict · Scenario Comparison · Model Performance · Literature Check · Physics Explained · About & Limitations.
- Persistent banner: "SIMULATION-BASED PROTOTYPE" whenever the model's `data_origin` is SIMULATED.
- Predict: three inputs, a button, no number before a model is loaded. Block clearly out-of-domain inputs; warn near the edge.
- Scenario comparison: baseline plus alternatives, table, absolute and % difference, bar chart. Call it "model-based scenario comparison", not finite-element simulation.
- Sensitivity plots: void, fibre volume fraction, angle (others fixed and labelled with units).
- Model Performance: actual vs predicted, residuals, comparison table, extrapolation result, RF feature importance (with a non-causation note).
- Literature Check: shows n real rows, simulator vs measured and surrogate vs measured, per-study results; empty-state message explains how to add rows.
- Physics Explained: plain analogies (fibres = ropes held by glue; voids = air bubbles in a cake; misalignment = pulling straws at an angle).

## Candidate literature sources (UNVERIFIED — no values extracted yet)
Copy these into `docs/data_sources.md` as "candidate, not yet extracted". Do not add authors, DOIs or values beyond what is written here.
1. Abdelal & Donaldson (2018), "Comparison of methods for the characterization of voids in glass fiber composites", Journal of Composite Materials, DOI 10.1177/0021998317710083. Glass/epoxy with 0.5–7 % voids; needs a check that tensile strength is reported.
2. Mehdikhani, Gorbatikh, Verpoest, Lomov (2019), "Voids in fiber-reinforced polymer composites: A review…", Journal of Composite Materials, DOI 10.1177/0021998318772152. A review used to trace primary studies.
3. "The Effects of Fibre Volume Fraction on a Glass-Epoxy Composite Material" (open access). Woven 0/90 E-glass/epoxy, ignition-loss Vf; architecture differs from the UD simulator.
4. "Fatigue behaviour of glass/epoxy laminates in the presence of voids" (ScienceDirect, PII S0142112316303164). Fatigue focus; use for tracing primary papers only.
5. "Experimental and numerical analysis of the Microstructure and mechanical properties of unidirectional glass fiber reinforced epoxy composites" (ScienceDirect, PII S0263822324000151). Ply-orientation tensile results; deliberate ply angles, not small misalignment.
6. Siddgonde, Kaushik, Ghosh, "Experimental and numerical characterization of E-glass/epoxy plain woven fabric composites containing void defects" (ScienceDirect, PII S1270963824008605). Woven; check for tensile values.

## Tests (pytest, small and fast)
Physics identities (θ=0 and Vv=0 gives X; θ=90° gives Y; void factor = 1 at 0 % voids; reproducible with fixed seed), CSV loading, missing columns, invalid numbers, percentage/angle limits, incompatible materials, training on a small fixture, model save/load, prediction type and units, scenario arithmetic, untrained-model handling, out-of-domain blocking, literature-comparison metrics. Passing tests prove the software works, not that the model matches real composites.

## Token-saving rules for Codex (follow strictly)
- Do not print whole files back; summarise changes in 5 lines or fewer.
- Use targeted edits, not full-file rewrites, for small fixes.
- Search with `rg`; do not re-read the whole repo each phase.
- Run `pytest -q` once per phase. On failure, re-run only the failing test.
- No web browsing and no new heavy dependencies; keep `requirements.txt` to the stack above.
- Make sensible small decisions without asking. Ask only if scientific validity is at stake.
- Stop at the end of each phase and wait for the next prompt. Phase replies: 150 words or fewer.

---
