# paste the data_fetcher.py code from the instruction set above
import os, requests, time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)

def fetch_openaq(lat, lon, radius_km=50):
    url = "https://api.openaq.org/v2/measurements"
    params = {"coordinates": f"{lat},{lon}", "radius": radius_km * 1000, "limit": 1000}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    results = r.json().get("results", [])
    rows = []
    for rec in results:
        rows.append({
            "timestamp": rec["date"]["utc"], "lat": rec["coordinates"]["latitude"],
            "lon": rec["coordinates"]["longitude"],
            "parameter": rec["parameter"], "value": rec["value"]
        })
    return pd.DataFrame(rows)

def load_sample_data():
    sat = pd.read_csv(DATA_DIR / "sample_satellite.csv", parse_dates=["timestamp"])
    grd = pd.read_csv(DATA_DIR / "sample_ground.csv", parse_dates=["timestamp"])
    return sat, grd


def fetch_tempo_sample_or_real():
    if os.getenv("TEMPO_ENABLED", "false").lower() == "true":
        try:
            raise NotImplementedError("Implement TEMPO fetch with Earthdata credentials")
        except Exception:
            return load_sample_data()
    else:
        return load_sample_data()
