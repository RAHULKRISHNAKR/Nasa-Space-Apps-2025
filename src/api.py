# paste api.py content from instruction set above
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, pandas as pd
app = FastAPI()

class ForecastRequest(BaseModel):
    lat: float
    lon: float
    hours: int = 48

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/forecast")
def forecast(req: ForecastRequest):
    try:
        arima = joblib.load("models/arima.pkl")
        return {"forecast": "using saved arima model (implement forecasting) " }
    except Exception:
        return {"forecast": [{"hour": i, "pm2_5": 10 + i} for i in range(req.hours)]}
