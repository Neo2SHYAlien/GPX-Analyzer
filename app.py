import streamlit as st
from components.gpx_parser import parse_gpx
from components.elevation_chart import plot_elevation_colored_by_slope
from components.stats_panel import show_stats
from components.map_display import display_route_map

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

st.title("GPX Route Analyzer 📍")

<<<<<<< HEAD
file1 = st.file_uploader("Upload first GPX file", type=["gpx"], key="file1")
file2 = st.file_uploader("Upload second GPX file (optional)", type=["gpx"], key="file2")
=======
uploaded_file = st.file_uploader("Upload a GPX file", type=["gpx"])
uploaded_file2 = st.file_uploader("Upload second GPX (optional)", type=["gpx"])

>>>>>>> 9426b76c9a3fe3cb18c237d688e70cea09f9c131

if file1:
    gpx_data1 = file1.read().decode("utf-8")
    df1, stats1 = parse_gpx(gpx_data1)

    if file2:
        gpx_data2 = file2.read().decode("utf-8")
        df2, stats2 = parse_gpx(gpx_data2)
    else:
        df2, stats2 = None, None

    st.subheader("📊 Statistics")
    show_stats(stats1, stats2)

    st.subheader("📈 Elevation Profile (colored by slope)")
    plot_elevation_colored_by_slope(df1, df2)

    st.subheader("🗺️ Route Map (colored by slope)")
    display_route_map(df1, df2)

else:
<<<<<<< HEAD
    st.info("Please upload at least one .gpx file to begin.")
=======
    st.info("Please upload a .gpx file to begin.")
>>>>>>> 9426b76c9a3fe3cb18c237d688e70cea09f9c131
