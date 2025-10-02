# paste model.py content from instruction set above
import joblib
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
import os

os.makedirs('models', exist_ok=True)

def train_simple_regression(df, target_col="pm2_5"):
    df = df.copy().dropna()
    df["prev"] = df[target_col].shift(1)
    df["ma3"] = df[target_col].rolling(3).mean()
    df.dropna(inplace=True)
    X = df[["prev", "ma3"]].values
    y = df[target_col].values
    model = LinearRegression().fit(X, y)
    joblib.dump(model, "models/regression.pkl")
    return model

def train_arima(df, col="pm2_5", order=(1,0,0)):
    ts = df[col].dropna()
    model = ARIMA(ts, order=order).fit()
    joblib.dump(model, "models/arima.pkl")
    return model
