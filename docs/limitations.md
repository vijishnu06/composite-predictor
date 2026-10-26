# Limitations and responsible interpretation

This is a surrogate of an assumed simulator. Eight literature table summaries are included as pending, incomplete extracts; none currently qualifies for comparison. Experimental validation remains outstanding. A high simulated-test R² can arise simply because the surrogate approximates the formula well.

The model omits fibre-length distributions, local waviness, interfacial debonding, residual stress, cure, strain rate, moisture, temperature, geometry, processing and damage evolution. UD assumptions do not represent woven or random-mat reinforcement. Off-axis angle is not identical to local fibre misalignment. The mixture formula and separate void knock-down are simplified assumptions, with volume definitions needing review against each source.

Sampling assumes independent, uniform inputs. Real manufacturing may couple these quantities. Gaussian scatter and nominal parameters are uncalibrated. No uncertainty interval is provided; random-forest tree dispersion is not a valid prediction interval. Importance and sensitivity describe the fitted model, not causation. The simulator's mild/strong void sensitivities cannot be claimed to match published findings without extraction and calibration.

Model selection uses a holdout, so its score is not an untouched final benchmark. Extrapolation results are a separate stress test; the app still blocks inputs beyond its declared domain. Linear Regression can produce nonphysical outputs, which are blocked. Range checks alone cannot identify sparse regions within the domain.

Real uploads need independent studies and enough rows; a single study cannot establish generalisation. Literature comparisons depend on correct extraction, comparable architectures, definitions, conditions and test standards. A few matching rows do not prove broad validation. Test-only synthetic fixtures are software checks, never scientific evidence.

Before validation claims: collect traceable measurements with all inputs, audit provenance/units, define inclusion rules, reserve independent studies, calibrate only on the calibration subset, assess held-out error and uncertainty, and document failures and applicable conditions. No structural design or safety decision should rely on this prototype.

Joblib files can execute code when loaded. This app has no model-upload feature and only loads its own local model directory. Hash checks catch accidental corruption; they do not authenticate files. Do not replace local artifacts with untrusted files. Dependency versions may differ across machines; retrain locally after installation.
