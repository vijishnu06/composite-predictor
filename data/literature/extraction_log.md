# Literature extraction log

Four supplied PDFs were searched for printed tables and body-text values. Source PDFs are kept locally in papers/ and excluded from Git and distribution ZIPs. Eight reported means were transcribed from one paper. All remain reviewed=no. No values were digitized from plots or inferred from missing measurements.

## Row audit

Page references below give the PDF page followed by the printed journal page. Material identity and LY556 epoxy grade come from PDF p.3, printed p.431. Each table prints fibre volume fraction as 55%. The first-page bibliographic text identifies the five authors, title and 2016 publication; no DOI is printed there, so the extraction source_reference deliberately omits a DOI value. The report bibliography can separately use publisher-verified DOI metadata.

### CSV row 2  Table 2
- Source: PDF p.5, journal p.433; UD lamina; fibre angle 0.
- Short table-cell text: `689 751 763 775 738 | Mean 743 | SD 30` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 743 MPa; printed SD: 30 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: UD lamina; printed mean and SD retained without recomputation; SD=30 MPa; specimens 1-5; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified.

### CSV row 3  Table 3
- Source: PDF p.6, journal p.434; UD lamina; fibre angle 90.
- Short table-cell text: `23 25 23 22 21 | Mean 23 | SD 1.33` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 23 MPa; printed SD: 1.33 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: UD lamina; printed mean and SD retained without recomputation; SD=1.33 MPa; specimens 11-15; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified. Outside current model angle domain (0-45 degrees).

### CSV row 4  Table 4
- Source: PDF p.6, journal p.434; UD lamina; fibre angle 45.
- Short table-cell text: `69 61 78 67 68 | Mean 69 | SD 5.46` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 69 MPa; printed SD: 5.46 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: UD lamina; printed mean and SD retained without recomputation; SD=5.46 MPa; specimens 21-25; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified.

### CSV row 5  Table 5
- Source: PDF p.6, journal p.434; UD laminate; fibre angle 0.
- Short table-cell text: `890 876 730 850 760 | Mean 821 | SD 64` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 821 MPa; printed SD: 64 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: UD laminate; printed mean and SD retained without recomputation; SD=64 MPa; specimens 31-35; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified.

### CSV row 6  Table 6
- Source: PDF p.6, journal p.434; UD laminate; fibre angle 90.
- Short table-cell text: `28 30 25 29 24 | Mean 27 | SD 2.32` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 27 MPa; printed SD: 2.32 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: UD laminate; printed mean and SD retained without recomputation; SD=2.32 MPa; specimens 41-45; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified. Outside current model angle domain (0-45 degrees). Row label says longitudinal but table title says 90-degree orientation; use table orientation, flag for human review.

### CSV row 7  Table 7
- Source: PDF p.6, journal p.434; UD laminate; fibre angle 45.
- Short table-cell text: `60 65 60 61 67 | Mean 63 | SD 3` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 63 MPa; printed SD: 3 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: UD laminate; printed mean and SD retained without recomputation; SD=3 MPa; specimens 51-55; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified.

### CSV row 8  Table 9
- Source: PDF p.7, journal p.435; quasi-isotropic; fibre angle not a single angle.
- Short table-cell text: `165 190 182 198 169 | Mean 181 | SD 12.4` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 181 MPa; printed SD: 12.4 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: quasi-isotropic; printed mean and SD retained without recomputation; SD=12.4 MPa; specimens 61-65; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified. Layup [0/45/90/-45]s, 1.6 mm, 8 layers.

### CSV row 9  Table 10
- Source: PDF p.7, journal p.435; quasi-isotropic; fibre angle not a single angle.
- Short table-cell text: `150 142 151 160 149 | Mean 150 | SD 5.75` MPa.
- Fibre-volume cell: `55%`.
- Saved strength mean: 150 MPa; printed SD: 5.75 MPa.
- Unknowns: void content and tensile-test temperature left blank. Human review: no.
- Notes: quasi-isotropic; printed mean and SD retained without recomputation; SD=5.75 MPa; specimens 71-75; void content not reported; no moisture-conditioned group identified in these tables; test temperature unspecified. Layup [90/0/-45/+45], 0.8 mm, 4 layers. Mixed layup angle left blank.

## Skipped values and sources

- Gopalakrishnan PDF pp.5-7, Tables 2-7, 9-10: individual specimen strengths were not exported because the requested unit is one row per reported mean. Their exact cell sequences are preserved above.
- Gopalakrishnan PDF p.7, Tables 8 and 11: summary strengths 743/821 MPa and 181/150 MPa duplicate the primary tables, so no duplicate rows were created.
- Gopalakrishnan PDF pp.5-7: elastic/shear moduli, Poisson ratios and failure loads are different targets and were not entered as tensile strength. Plotted mechanical responses on pp.8-16 were not digitized. Table 12 on p.11 concerns elastic constants, not additional strength means.
- Larco et al. PDF p.4, Table 1: 1750 MPa E-glass fibre and 55 MPa resin are constituent properties, not measured composite strengths. Do not use them as laminate targets or relabel nominal simulator defaults as calibrated values.
- Larco et al. PDF p.5, Eq.(7): fibre volume fractions 21.98, 25.33 and 32.33 are printed, but the supplied paper provides no paired numeric laminate ultimate tensile strengths in its results table. PDF p.6, Table 5 reports measured/theoretical elastic modulus, not tensile strength. No strength rows created. The material is 0/90 woven and outside UD architecture scope.
- Zuhudi et al. (2021), Void and Moisture Content of Fiber Reinforced Composites: review article. Table 1 (PDF p.5) compares measurement methods and Table 2 (p.9) lists study/material/test types. Percentage-change discussion on p.10 is not an absolute, matched E-glass/epoxy tensile-strength dataset. No secondary measurements exported.
- Dong (2016), Effects of Process-Induced Voids on the Properties of Fibre Reinforced Composites: numerical carbon/epoxy RVE and analytical work. PDF pp.7-8, Figs.12-14 are plot-only comparisons and involve other material/layup/conditioning contexts. Percentage changes in body text on p.8 and the 55 MPa matrix value on p.6 are not eligible absolute E-glass laminate tensile measurements. No rows created.

## Comparison eligibility

The app excludes all eight rows while reviewed=no. Even after review, every row needs an independently reported void-content value from the same condition before a complete three-input comparison is possible. Two 90-degree rows also exceed the current domain; two quasi-isotropic rows have unsupported architecture and an intentionally blank angle. No experimental calibration or validation metric has been computed.

## Human review checklist

Open each cited PDF page, verify the mean column and fibre fraction, check material/conditioning and layup, and only then change reviewed to yes. Retain unknown cells as blank. Do not add guessed zero voids. The app now requires reviewed=yes for comparison and continues to report rejected/excluded rows with reasons.
