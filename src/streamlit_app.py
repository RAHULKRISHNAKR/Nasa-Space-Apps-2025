# paste streamlit_app.py content from instruction set above
import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
from src.data_fetcher import load_sample_data, fetch_openaq

st.title("AQ Forecast — Prototype")

lat = st.number_input("Latitude", value=10.0891)
lon = st.number_input("Longitude", value=76.5994)

if st.button("Load data & Forecast"):
    sat, grd = load_sample_data()
    st.write("Sample satellite rows:", len(sat), "ground rows:", len(grd))
    st.line_chart(sat.set_index("timestamp")["pm2_5"].head(48))
    m = folium.Map(location=[lat, lon], zoom_start=10)
    st_folium(m, width=700, height=400)
    st.success("Prototype UI loaded. For full forecast, train models and call API.")
