import pandas as pd
from src.preprocess import resample_hourly

def test_resample_hourly():
    df = pd.DataFrame({'timestamp': pd.date_range('2025-09-20', periods=4, freq='h'), 'pm2_5':[10,11,12,13]})
    out = resample_hourly(df)
    freq_ok = (out.index.freqstr or '').lower() in ('h','1h')
    assert freq_ok, f"Unexpected freq: {out.index.freqstr}"
    assert not out['pm2_5'].isna().any()
