# Viva notes: 15 likely questions

1. **What is the project?** A local dashboard that compares ML surrogates of a documented nominal UD E-glass/epoxy strength simulator.
2. **Why simulated data?** We have no lab data and no verified open dataset covering all three chosen inputs. Simulation supports software development without pretending measurements exist.
3. **Is it experimentally validated?** No. Simulated holdout scores measure approximation of the simulator only.
4. **What are the inputs and output?** Fibre volume fraction (%), void content (%), fibre-to-load angle (degrees), and tensile strength estimate (MPa).
5. **How is strength calculated?** A fibre/matrix mixture gives longitudinal strength, adjustable exponential void factors reduce strength components, and off-axis Tsai–Hill combines longitudinal, transverse and shear resistance.
6. **Are the parameters measured?** No; every default is a nominal assumption documented in physics_model.md.
7. **Why these two algorithms?** Linear Regression is a transparent baseline; a modest Random Forest can capture nonlinear behaviour. The held-out RMSE decides the winner.
8. **How do you prevent leakage?** Simulated rows have a held-out split, literature is never training data, and uploaded experimental studies are split by study_id. Future tuning still needs an independent final set.
9. **Why an extrapolation test?** Training below 55% Vf and testing at/above it reveals weakness outside the fitted fibre-fraction range. It is reported beside random-holdout results.
10. **What do MAE, RMSE and R² mean?** Average absolute error, square-root average squared error, and fit relative to the test mean. MAE/RMSE use MPa; R² can be negative or undefined.
11. **What does a sensitivity graph prove?** Only how this fitted model responds while other inputs are fixed. It does not prove causation.
12. **Why no confidence band?** We have no calibrated predictive uncertainty. Forest tree spread is not a prediction interval.
13. **Can woven literature be used?** It can be recorded with provenance, but is excluded from this UD simulator comparison by default.
14. **What does passing pytest prove?** Software behaviour such as formulas, validation, splitting, persistence and arithmetic. It does not prove physical accuracy.
15. **What is the next scientific step?** Collect verified matched measurements, review conditions and definitions, calibrate parameters on separate data and assess genuinely independent studies before any validation claim.
