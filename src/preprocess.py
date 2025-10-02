# paste preprocess.py content from instruction set above
import pandas as pd
from geopy.distance import geodesic
import numpy as np

def nearest_station_merge(sat_df, ground_df, max_km=50):
    merged = []
    for idx, s in sat_df.iterrows():
        best = None
        best_dist = max_km + 1
        for jdx, g in ground_df.iterrows():
            d = geodesic((s.lat, s.lon), (g.lat, g.lon)).km
            if d < best_dist:
                best_dist = d
                best = g
        if best is not None and best_dist <= max_km:
            merged.append({**s.to_dict(), **best.to_dict(), "station_distance_km": best_dist})
    return pd.DataFrame(merged)

def resample_hourly(df):
    df = df.set_index("timestamp").sort_index()
    # Use lowercase 'h' to avoid FutureWarning on uppercase 'H' deprecation
    return df.resample("1h").mean().interpolate()
