import pytest
from src.train import train, save_model, load_model
from src.simulate_data import generate


def test_train_persistence(tmp_path):
    bundle, report = train(generate(100))
    meta = bundle['metadata']
    assert (meta['train_count'], meta['test_count']) == (80, 20)
    assert all(v['extrapolation'] is not None for v in meta['metrics'].values())
    assert meta['metrics'][meta['model_type']]['held_out']['RMSE_MPa'] == min(v['held_out']['RMSE_MPa'] for v in meta['metrics'].values())
    save_model(bundle, tmp_path)
    assert load_model(tmp_path)['metadata']['target_unit'] == 'MPa'
    (tmp_path / 'model.joblib').write_bytes(b'corrupt')
    with pytest.raises(ValueError, match='corrupted'):
        load_model(tmp_path)


def test_origins_and_groups():
    df = generate(60)
    df.loc[0, 'data_origin'] = 'EXPERIMENTAL_UPLOAD'
    with pytest.raises(ValueError, match='mixed-origin'):
        train(df)
    df['data_origin'] = 'EXPERIMENTAL_LITERATURE'
    with pytest.raises(ValueError, match='comparison-only'):
        train(df)
    df['data_origin'] = 'EXPERIMENTAL_UPLOAD'
    df['study_id'] = ['test-study-' + str(i // 10) for i in range(60)]
    meta = train(df)[0]['metadata']
    assert not set(meta['study_split']['train']) & set(meta['study_split']['test'])
    df['study_id'] = 'one'
    with pytest.raises(ValueError, match='Generalisation cannot be established'):
        train(df)
