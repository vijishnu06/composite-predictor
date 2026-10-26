"""Local engineering dashboard. Run: python -m streamlit run app.py"""
import io
import json
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from src.data_loader import read_csv, save_upload
from src.physics_model import ROOT, FEATURES, ESTIMATE_LABEL, load_params, strength
from src.simulate_data import generate
from src.validation import validate
from src.train import train, save_model, load_model
from src.predict import predict, prediction_label
from src.simulation import compare, sensitivity
from src.plotting import performance
from src.literature_validation import load_literature, compare_literature

st.set_page_config(page_title='Composite Predictor', page_icon='🔬', layout='wide')
st.markdown('''<style>
/* Preserve Streamlit's paired foreground/background colors in both themes. */
[data-testid="stMetric"] {padding:18px;border-radius:10px;border:1px solid #8495a8}
</style>''', unsafe_allow_html=True)
st.title('Defect-Aware Composite Predictor')
st.caption('E-glass / epoxy · Unidirectional laminate · Tensile strength in MPa')

if 'bundle' not in st.session_state:
    st.session_state.bundle = None
    if (ROOT / 'models/metadata.json').exists():
        try:
            st.session_state.bundle = load_model()
        except (ValueError, OSError, KeyError) as exc:
            st.session_state.load_error = str(exc)
bundle = st.session_state.bundle
if bundle is None or bundle['metadata']['data_origin'] == 'SIMULATED':
    st.warning('SIMULATION-BASED PROTOTYPE')
    st.caption(ESTIMATE_LABEL)
else:
    st.warning('EXPERIMENTAL-UPLOAD MODEL · Generalisation must be assessed on independent studies.')
if st.session_state.get('load_error'):
    st.info(st.session_state.load_error)

names = ['Overview', 'Dataset', 'Train & Evaluate', 'Predict', 'Scenario Comparison', 'Model Performance', 'Literature Check', 'Physics Explained', 'About & Limitations']
tabs = st.tabs(names)
labels = ['Fibre volume fraction (%)', 'Void content (%)', 'Fibre/load misalignment angle (degrees)']


def report_view(report):
    st.write(report.counts)
    for category in ['rejected', 'excluded']:
        rows = getattr(report, category)
        if not rows.empty:
            with st.expander(f'{category.title()} rows and reasons ({len(rows)})'):
                st.dataframe(rows, hide_index=True)


def metric_table(meta):
    return pd.DataFrame([{'Model': name, 'Evaluation': split, **values}
                         for name, splits in meta['metrics'].items()
                         for split, values in splits.items() if values is not None])


def inputs(prefix):
    domain = bundle['metadata']['domain'] if bundle else load_params()['domain']
    defaults = [45.0, 2.0, 5.0]
    cols = st.columns(3)
    return {f: cols[i].number_input(labels[i], min_value=0.0, max_value=100.0 if i < 2 else 90.0,
            value=float(min(max(defaults[i], domain[f][0]), domain[f][1])), step=0.5, key=f'{prefix}_{f}')
            for i, f in enumerate(FEATURES)}


with tabs[0]:
    st.header('Explore a documented simulator with machine learning')
    st.write('This undergraduate prototype learns a nominal micromechanics model. Its held-out scores measure reproduction of simulated targets; they do not establish the strength of a manufactured laminate.')
    cols = st.columns(3)
    cols[0].metric('Input features', '3')
    cols[1].metric('Default simulated rows', '2,000')
    cols[2].metric('Eligible reviewed literature rows', '0')
    st.markdown('1. Inspect the simulated dataset.\n2. Train and compare two models.\n3. Explore estimates and scenarios.\n4. Add verified literature rows for a separate comparison.')
    if bundle:
        st.success(f"Loaded model: {bundle['metadata']['model_type']} · {bundle['metadata']['data_origin']}")
    st.info('No confidence interval is claimed. Random-forest tree spread is not a prediction interval.')

with tabs[1]:
    st.header('Data provenance and validation')
    choice = st.radio('Training dataset', ['Simulated CSV', 'Experimental CSV upload'], horizontal=True)
    active = None
    if choice == 'Simulated CSV':
        if st.button('Generate / regenerate simulated CSV'):
            generate().to_csv(ROOT / 'data/simulated/simulated_e_glass_epoxy.csv', index=False)
            st.success('Generated 2,000 simulated rows. Existing model is unchanged until you press Train.')
        path = ROOT / 'data/simulated/simulated_e_glass_epoxy.csv'
        if path.exists():
            active = read_csv(path)
        else:
            st.info('Generate the dataset to begin.')
    else:
        st.info('Required origin: EXPERIMENTAL_UPLOAD. Include study_id for study-grouped evaluation. Literature rows must stay in the Literature Check tab. Fewer than 30 rows or only one study cannot establish generalisation.')
        uploaded = st.file_uploader('Experimental measurements (CSV only)', type=['csv'])
        if uploaded is not None:
            try:
                active = read_csv(io.BytesIO(uploaded.getvalue()))
                if st.button('Save a unique local copy of this upload'):
                    st.success(f'Saved {save_upload(uploaded.getvalue()).name}')
            except ValueError as exc:
                st.error(str(exc))
    if active is not None:
        try:
            report = validate(active, expected_origin='SIMULATED' if choice == 'Simulated CSV' else 'EXPERIMENTAL_UPLOAD')
            report_view(report)
            st.dataframe(report.accepted.head(100), hide_index=True)
            if report.rejected.empty and not report.accepted.empty:
                st.session_state.training_data = active
            else:
                st.session_state.pop('training_data', None)
                st.warning('Correct rejected rows before training in the dashboard. No rows are silently removed.')
        except ValueError as exc:
            st.session_state.pop('training_data', None)
            st.error(str(exc))
    else:
        st.session_state.pop('training_data', None)

with tabs[2]:
    st.header('Train once, evaluate on held-out rows')
    st.write('Selection: lowest held-out RMSE. Simulated data use a random 80/20 split plus a separate Vf < 55% → Vf ≥ 55% extrapolation test. Experimental uploads use a study-grouped holdout; the extrapolation result is not computed for those uploads.')
    if st.button('Train and save selected model', type='primary', disabled='training_data' not in st.session_state):
        try:
            with st.spinner('Training and evaluating…'):
                new_bundle, report = train(st.session_state.training_data)
                save_model(new_bundle)
                st.session_state.bundle = new_bundle
                st.session_state.pop('load_error', None)
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
    if bundle:
        st.dataframe(metric_table(bundle['metadata']), hide_index=True)
        st.write('Chosen model:', bundle['metadata']['model_type'])
        st.write('Split:', bundle['metadata']['split'])
        st.write('Training / held-out rows:', bundle['metadata']['train_count'], '/', bundle['metadata']['test_count'])
        for message in bundle['metadata']['warnings']:
            st.warning(message)
        st.caption('The saved model retains the held-out split and is not refitted on the entire dataset. The selection holdout is not an independent final benchmark.')

with tabs[3]:
    st.header('Tensile-strength estimate')
    st.write('Enter volume percentages, not weight percentages. Angle is the fibre direction relative to the tensile load. A value of 0° means aligned loading.')
    st.caption('Demo baseline: 45% fibre, 2% voids, 5° angle. Compare 45 / 6 / 5 for increased voids, then 45 / 2 / 20 for off-axis loading. Change one input at a time.')
    baseline = inputs('predict')
    if bundle:
        st.caption(prediction_label(bundle))
        st.write('Supported input domain:', bundle['metadata']['domain'])
    else:
        st.info('Load or train a model first; no estimate is available.')
    if st.button('Estimate tensile strength', disabled=bundle is None):
        try:
            values, warnings = predict(bundle, pd.DataFrame([baseline]))
            st.metric('Surrogate estimate (MPa)', f'{values[0]:.1f}')
            for message in warnings:
                st.warning(message)
            st.subheader('Sensitivity: model behaviour, not causation')
            for f, label in zip(FEATURES, labels):
                sweep = sensitivity(bundle, baseline, f)
                st.caption('Fixed: ' + ', '.join(f'{labels[i]} = {baseline[other]:g}' for i, other in enumerate(FEATURES) if other != f))
                st.line_chart(sweep.set_index(f)['estimate_mpa'], x_label=label, y_label='Surrogate estimate (MPa)')
        except ValueError as exc:
            st.error(str(exc))

with tabs[4]:
    st.header('Model-based scenario comparison')
    st.caption('First row is the baseline. Differences describe model behaviour; this is not finite-element simulation.')
    defaults = pd.DataFrame({'scenario': ['Baseline', 'Lower voids', 'Better alignment'], FEATURES[0]: [45., 45., 45.], FEATURES[1]: [4., 1., 4.], FEATURES[2]: [10., 10., 2.]})
    scenarios = st.data_editor(defaults, num_rows='dynamic', key='scenarios', hide_index=True)
    if bundle:
        st.caption(prediction_label(bundle))
    if st.button('Compare scenarios', disabled=bundle is None):
        try:
            result, warnings = compare(bundle, scenarios)
            st.dataframe(result, hide_index=True)
            st.bar_chart(result.set_index('scenario')['estimate_mpa'], y_label='Surrogate estimate (MPa)')
            for message in warnings:
                st.warning(message)
        except ValueError as exc:
            st.error(str(exc))

with tabs[5]:
    st.header('Held-out model performance')
    if bundle:
        meta = bundle['metadata']
        st.caption(prediction_label(bundle))
        st.dataframe(metric_table(meta), hide_index=True)
        st.write('Extrapolation train/test counts:', meta['extrapolation_counts'])
        selected = st.selectbox('Inspect evaluated model', list(meta['evaluation']))
        result = meta['evaluation'][selected]
        fig = performance(result['actual'], result['predicted'])
        st.pyplot(fig)
        plt.close(fig)
        st.subheader('Random Forest feature importance')
        st.bar_chart(pd.DataFrame({'importance': meta['rf_feature_importance']}, index=labels))
        st.caption('Importance depends on this dataset and fitted model. It does not prove physical causation.')
        with st.expander('Provenance and model metadata'):
            st.json({k: v for k, v in meta.items() if k != 'evaluation'})
    else:
        st.info('Train a model to see held-out metrics.')

with tabs[6]:
    st.header('Separate literature comparison')
    st.write('Only rows with reviewed=yes enter comparison. Check each extraction against the PDF before changing this field. Every row needs all three inputs, a tensile strength, and a source reference with its table or page. Use EXPERIMENTAL_LITERATURE as the origin and UD or unidirectional as the architecture.')
    try:
        result = compare_literature(load_literature(), bundle)
        report_view(result['report'])
        st.metric('Eligible real literature rows (n)', result['n'])
        if result['n'] == 0:
            st.info('No eligible reviewed experimental measurements are available. Extracted rows may remain pending review or lack required inputs. See data/literature/extraction_log.md and docs/data_sources.md. This prototype has not been experimentally validated.')
        else:
            st.caption('Noise-free nominal simulator estimates are not measurements. A literature comparison alone does not establish experimental validation.')
            if bundle:
                st.caption(prediction_label(bundle))
            st.dataframe(result['rows'], hide_index=True)
            st.dataframe(pd.DataFrame(result['metrics']).T)
            st.dataframe(pd.DataFrame(result['per_study']), hide_index=True)
    except (ValueError, OSError) as exc:
        st.error(str(exc))

with tabs[7]:
    st.header('Physics explained')
    st.write('Fibres act like ropes held together by glue (epoxy). Air bubbles interrupt the material, like bubbles in a cake. Pulling aligned straws is different from pulling them at an angle: off-axis loading increasingly involves shear and transverse strength.')
    st.markdown('1. Limit matrix stress at fibre failure.\n2. Combine fibre and matrix contributions with a nominal fibre-efficiency factor.\n3. Apply adjustable exponential void knock-downs.\n4. Use off-axis Tsai–Hill to combine longitudinal, transverse and shear resistance.\n5. Add 5% multiplicative scatter only when generating training data.')
    st.latex(r'\sigma^{-2}=\frac{\cos^4\theta}{X_v^2}+\left(\frac{1}{S_v^2}-\frac{1}{X_v^2}\right)\sin^2\theta\cos^2\theta+\frac{\sin^4\theta}{Y_v^2}')
    st.write('All parameters are nominal assumptions. The angle is fibre direction relative to load, not a measured distribution of fibre waviness. Void sensitivities need calibration against verified literature when available.')
    st.json(load_params())
    st.subheader('Additional material inputs: direct simulator experiment')
    st.write('These six material inputs change a direct physics calculation. The saved three-feature Random Forest retains its original parameter snapshot. Results here are nominal simulator outputs; changing these controls does not update or retrain that model.')
    custom_inputs = inputs('physics')
    custom_params = load_params()
    specs = [('fibre_strength_mpa', 'Fibre tensile strength (MPa)'),
             ('fibre_modulus_gpa', 'Fibre modulus (GPa)'),
             ('matrix_strength_mpa', 'Matrix tensile strength (MPa)'),
             ('matrix_modulus_gpa', 'Matrix modulus (GPa)'),
             ('transverse_strength_mpa', 'Transverse strength (MPa)'),
             ('shear_strength_mpa', 'Shear strength (MPa)')]
    material_cols = st.columns(2)
    for i, (key, label) in enumerate(specs):
        custom_params[key] = material_cols[i % 2].number_input(label, min_value=0.001,
                value=float(custom_params[key]), step=1.0, key='material_' + key)
    if st.button('Calculate direct simulator experiment'):
        try:
            for feature, value in custom_inputs.items():
                lo, hi = custom_params['domain'][feature]
                if not lo <= value <= hi:
                    raise ValueError(f'{feature}: supported domain is {lo:g}–{hi:g}.')
            value = strength(*(custom_inputs[f] for f in FEATURES), params=custom_params)
            st.metric('Direct nominal simulator output (MPa)', f'{value:.1f}')
            st.caption('Assumed material properties; experimental validity has not been established. This value is not an ML prediction.')
        except ValueError as exc:
            st.error(str(exc))

with tabs[8]:
    st.header('Scope and limitations')
    st.write('Educational, simulation-based prototype for UD E-glass/epoxy. Eight literature table extracts are pending human review and missing required inputs; zero are eligible for comparison. Experimental validation and calibrated uncertainty remain future work.')
    st.write('Woven and random-mat architectures, fatigue, compression, damage progression, processing history and environmental effects are not represented. Passing software tests does not prove agreement with real composites.')
    st.write('Local use only. Load only the model artifacts created by this app; never replace them with downloaded or uploaded pickle/joblib files. Artifact hashes detect accidental changes, not a malicious file replacement.')
    st.caption('Documentation: README.md and docs/ · No paid services required.')
