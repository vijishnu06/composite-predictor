# Literature sources and extraction guide

All six entries below are copied from the supplied prompt as **candidate, not yet extracted**. They have not been verified in this build. No authors, DOI corrections, bibliographic claims or measured values have been added. No web research was performed.
 (UNVERIFIED — no values extracted yet)
Copy these into `docs/data_sources.md` as "candidate, not yet extracted". Do not add authors, DOIs or values beyond what is written here.
1. Abdelal & Donaldson (2018), "Comparison of methods for the characterization of voids in glass fiber composites", Journal of Composite Materials, DOI 10.1177/0021998317710083. Glass/epoxy with 0.5–7 % voids; needs a check that tensile strength is reported.
2. Mehdikhani, Gorbatikh, Verpoest, Lomov (2019), "Voids in fiber-reinforced polymer composites: A review…", Journal of Composite Materials, DOI 10.1177/0021998318772152. A review used to trace primary studies.
3. "The Effects of Fibre Volume Fraction on a Glass-Epoxy Composite Material" (open access). Woven 0/90 E-glass/epoxy, ignition-loss Vf; architecture differs from the UD simulator.
4. "Fatigue behaviour of glass/epoxy laminates in the presence of voids" (ScienceDirect, PII S0142112316303164). Fatigue focus; use for tracing primary papers only.
5. "Experimental and numerical analysis of the Microstructure and mechanical properties of unidirectional glass fiber reinforced epoxy composites" (ScienceDirect, PII S0263822324000151). Ply-orientation tensile results; deliberate ply angles, not small misalignment.
6. Siddgonde, Kaushik, Ghosh, "Experimental and numerical characterization of E-glass/epoxy plain woven fabric composites containing void defects" (ScienceDirect, PII S1270963824008605). Woven; check for tensile values.


## Add verified measurements

1. Obtain the primary publication and read its materials, architecture and tensile test methods. Reviews and fatigue-only sources are leads, not substitutes for tensile measurements.
2. Confirm E-glass/epoxy, UD architecture, fibre/void volume definitions and fibre angle relative to tensile load. Woven, mat and unspecified architectures are excluded; do not relabel them UD.
3. Locate all three inputs and tensile strength for the same specimen or well-defined condition. If an input is missing, leave it blank and report the row as incomplete; never infer zero. Do not fabricate values to complete a row.
4. Copy the header-only template to a new CSV in data/literature. Set data_origin to EXPERIMENTAL_LITERATURE. Keep the original blank template as a reusable schema.
5. Record source_id and source_reference. Include publication identification plus exact table/figure and page in source_reference for every row. Values digitized from a figure require a note explaining digitization and its uncertainty. Verify conversions to percent, degrees and MPa.
6. Populate study_id, specimen_id, fibre_architecture, manufacturing_method, epoxy_grade, test_standard, test_temperature_c and notes whenever available. Distinguish individual specimens from means; do not duplicate a mean as several independent specimens.
7. Reconcile extraction against the original source and have another reader check it where possible. The CSV validator checks syntax, origins and ranges; it cannot independently verify a citation, measurement or scientific compatibility.
8. Open Literature Check. Inspect accepted/rejected/excluded counts and reasons. The app uses the saved model's parameter snapshot and domain (or current config without a model), reports eligible n and per-study metrics, and never mixes literature into training.
9. Keep calibration and independent validation sources separate for future scientific work. Describe results as literature comparisons with n; do not automatically claim experimental validation.

Eight source-linked table summaries are included in literature_rows.csv with reviewed=no. All lack required inputs and none qualifies for comparison. See extraction_log.md for the audit. The original template remains header-only. Synthetic fixtures in tests are explicitly test-only and do not constitute literature data.
