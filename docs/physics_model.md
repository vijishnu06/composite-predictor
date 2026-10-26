# Nominal physics model

All numbers below are **modelling assumptions, not measurements**. They define an educational simulator for a UD laminate. They are not calibrated against experimental data. Fibres are analogous to ropes held by epoxy glue; voids resemble air bubbles interrupting a cake; angled fibres resemble straws pulled sideways.

| Configuration key | Default | Plain-language role / analogy |
|---|---:|---|
| fibre_strength_mpa | 1750 MPa | Effective strength of the ropes inside the composite, not an asserted measured single-fibre value. |
| fibre_modulus_gpa | 73 GPa | Rope stiffness; controls strain at nominal fibre failure. |
| matrix_strength_mpa | 55 MPa | Maximum load the glue can carry in this mixture approximation. |
| matrix_modulus_gpa | 2.4 GPa | Glue stiffness; determines its stress at fibre failure. |
| transverse_strength_mpa | 40 MPa | Nominal cross-rope resistance, Y. |
| shear_strength_mpa | 60 MPa | Nominal resistance to sliding neighbouring ropes, S. |
| k_void_fibre_per_pct | 0.010 per percentage point | Adjustable rate at which bubbles weaken the rope-dominated direction. |
| k_void_matrix_per_pct | 0.040 per percentage point | Adjustable rate at which bubbles weaken transverse and sliding resistance. |
| eta_full_until_vf_pct | 55% | Up to this fibre fraction, the assumed rope efficiency is 1. |
| eta_at_70 | 0.80 | At 70% fibre, crowded ropes are assigned 80% efficiency; linear decrease above 55%. |
| noise_cov | 0.05 | Nominal 5% scatter around simulated values, like deliberate variation in repeated draws; not calibrated measurement uncertainty. |
| seed | 42 | Repeats the same pseudo-random draw sequence. |
| n_rows | 2000 | Number of synthetic training examples, not number of laboratory specimens. |
| domain.fibre_volume_fraction_pct | 20–65% | Range of assumed rope packing explored by the prototype. |
| domain.void_content_pct | 0–8% | Range of bubble content explored. |
| domain.misalignment_angle_deg | 0–45° | Range of fibre-to-load angle explored; 0° is parallel. |

Let f = Vf_pct / 100, v = void content in percentage points, and θ = angle converted to radians. Both moduli use GPa, so their ratio cancels units when multiplied by fibre strength in MPa.

```text
sigma_m_prime = min(matrix_strength, matrix_modulus * fibre_strength / fibre_modulus)
eta = 1 - (1 - eta_at_70) * clip((Vf_pct - eta_full_until_vf_pct) / (70 - eta_full_until_vf_pct), 0, 1)
X = eta * f * fibre_strength + (1 - f) * sigma_m_prime
X_v = X * exp(-k_void_fibre_per_pct * v)
Y_v = Y * exp(-k_void_matrix_per_pct * v)
S_v = S * exp(-k_void_matrix_per_pct * v)
1 / sigma² = cos(θ)^4 / X_v² + (1 / S_v² - 1 / X_v²) * sin(θ)² * cos(θ)² + sin(θ)^4 / Y_v²
```

At zero voids each exponential factor is 1. At 0° the result is X_v; at 90° it is Y_v. The latter is a mathematical test, outside the app's 0–45° training domain. Efficiency is clamped at 0.80 beyond 70%, although normal training never goes beyond 65%. The `(1 - f)` term follows the supplied nominal mixture formula; it does not explicitly subtract void volume from matrix volume. Void effects are introduced separately through empirical knock-downs. Volume definitions must therefore be reconciled before literature calibration.

The dataset alone multiplies the deterministic strength by `(1 + noise)`, with Gaussian noise standard deviation `noise_cov`. Nonpositive factors are resampled. This produces almost the specified Gaussian distribution at the default small scatter, truncated at zero for physical output. The pure physics function never adds randomness.

The prompt notes that some glass/epoxy studies report only mild void effects. No such evidence has been extracted or verified in this project. The void coefficients are deliberately adjustable and must be calibrated against appropriate verified data when available. The angle is a uniform off-axis orientation, not a stochastic local-misalignment or waviness model. Tsai–Hill is an assumed phenomenological interaction model; it does not simulate fracture evolution or manufacturing defects explicitly.

After changing parameters, regenerate and retrain. Existing artifacts preserve their original parameter snapshot for reproducible comparisons. Use physically sensible positive strengths/moduli, 0 ≤ noise_cov, and eta_full_until_vf_pct < 70; malformed configurations must be corrected before use.
