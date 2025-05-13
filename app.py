import streamlit as st
from components.gpx_parser import parse_gpx
from components.elevation_chart import plot_elevation_colored_by_slope
from components.stats_panel import show_stats
from components.map_display import display_route_map

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

st.title("GPX Route Analyzer 📍")

uploaded_file = st.file_uploader("Upload a GPX file", type=["gpx"])

if uploaded_file:
    gpx_data = uploaded_file.read().decode("utf-8")

    df, stats = parse_gpx(gpx_data)

    st.subheader("📊 Statistics")
    show_stats(stats)

    st.subheader("📈 Elevation Profile (colored by slope)")
    plot_elevation_colored_by_slope(df)

    st.subheader("🗺️ Route Map (colored by slope)")
    display_route_map(df)
else:
    st.info("Please upload a .gpx file to begin.")