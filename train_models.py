import pandas as pd
from src.data_fetcher import load_sample_data
from src.preprocess import resample_hourly
from src.model import train_simple_regression, train_arima

sat, grd = load_sample_data()
merged = sat.copy()
merged = merged.rename(columns={'pm2_5':'pm2_5'})
merged = resample_hourly(merged)
print('Input rows after resample:', merged.shape)
reg_ok = False
arima_ok = False
try:
    train_simple_regression(merged, target_col='pm2_5')
    print('Regression trained -> models/regression.pkl')
    reg_ok = True
except Exception as e:
    print('Regression train failed:', e)
try:
    train_arima(merged, col='pm2_5')
    print('ARIMA trained -> models/arima.pkl')
    arima_ok = True
except Exception as e:
    print('ARIMA train failed:', e)
print('SUMMARY:', {'regression': reg_ok, 'arima': arima_ok})
