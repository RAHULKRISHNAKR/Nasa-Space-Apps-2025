# AQ Forecast Prototype

Prototype integrating (future) NASA TEMPO data (or fallback synthetic sample) with OpenAQ style ground measurements to produce simple PM2.5 forecasts.

## Features
- Sample satellite + ground CSV data for offline demo
- Simple preprocessing & hourly resample
- Baseline regression + ARIMA model training scripts
- FastAPI stub (`/health`, `/forecast`)
- Streamlit prototype UI with folium map
- Dockerfile + docker-compose

## Quick Start (Local)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.template .env  # (optional edit TEMPO credentials)
python train_models.py   # train baseline models
streamlit run src/streamlit_app.py
```

### FastAPI (optional)
```powershell
uvicorn src.api:app --reload --port 8000
```
Test:
```powershell
curl http://127.0.0.1:8000/health
```

## Docker
Ensure Docker Desktop is running, then:
```powershell
docker build -t aq-forecast-proto .
docker run -p 8501:8501 aq-forecast-proto
```
Or with compose:
```powershell
docker compose up --build
```

## TEMPO / Data Fallback
If `TEMPO_ENABLED=false` (default) the code loads `data/sample_satellite.csv` and `data/sample_ground.csv`.

## Troubleshooting
- Import errors: confirm virtualenv activated (`Get-Command python` shows venv path).
- ARIMA failure: small sample size — regression model still saved.
- Docker build cannot connect: start Docker Desktop.
- Streamlit map not showing: check network or browser mixed-content restrictions.

## Tests
```powershell
pytest -q
```

## Forecast Endpoint Example
```powershell
python - <<'PY'
from fastapi.testclient import TestClient
from src.api import app
c = TestClient(app)
resp = c.post('/forecast', json={'lat':10.0891,'lon':76.5994,'hours':4})
print(resp.json())
PY
```

## Roadmap
- Real TEMPO ingestion
- Feature engineering (meteorology, temporal lags)
- Model evaluation & metrics
- Deployment pipeline
