# paste streamlit_app.py content from instruction set above
import sys, pathlib
project_root = pathlib.Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Try both absolute and relative imports
try:
    from src.data_fetcher import load_sample_data, fetch_openaq  # absolute
except ModuleNotFoundError:
    try:
        from .data_fetcher import load_sample_data, fetch_openaq  # relative (if run as package)
    except Exception as e:  # final fallback
        raise

import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

st.title("AQ Forecast — Prototype")

# Inputs
lat = st.number_input("Latitude", value=10.0891)
lon = st.number_input("Longitude", value=76.5994)

# Initialize session state keys
if st.runtime.exists():  # type: ignore[attr-defined]
    # Normal Streamlit runtime; safe to initialize state
    if 'loaded' not in st.session_state:
        st.session_state.loaded = False
    if 'sat' not in st.session_state:
        st.session_state.sat = None
    if 'grd' not in st.session_state:
        st.session_state.grd = None
else:
    # Fallback placeholders when imported as a plain module (e.g., tests)
    class _Shim:
        loaded = False
        sat = None
        grd = None
    st.session_state = _Shim()  # type: ignore

load_clicked = st.button("Load data & Forecast")
if load_clicked:
    sat, grd = load_sample_data()
    st.session_state.sat = sat
    st.session_state.grd = grd
    st.session_state.loaded = True

# Show results if loaded previously (persist across reruns)
if getattr(st.session_state, 'loaded', False) and getattr(st.session_state, 'sat', None) is not None:
    sat = getattr(st.session_state, 'sat')
    grd = getattr(st.session_state, 'grd')
    st.write("Sample satellite rows:", len(sat), "ground rows:", len(grd))
    try:
        chart_df = sat.set_index("timestamp")["pm2_5"].head(48)
        st.line_chart(chart_df)
    except Exception as e:
        st.warning(f"Could not render chart: {e}")
    m = folium.Map(location=[lat, lon], zoom_start=10)
    st_folium(m, width=700, height=400)
    st.success("Prototype UI loaded. For full forecast, train models and call API.")
else:
    st.info("Click 'Load data & Forecast' to load sample data.")
