import streamlit as st
from components.gpx_parser import parse_gpx
from components.elevation_chart import plot_elevation_colored_by_slope
from components.stats_panel import show_stats
from components.map_display import display_route_map

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

# Uploaders in the sidebar
with st.sidebar:
    st.title("Upload GPX File(s)")
    file1 = st.file_uploader("First GPX", type=["gpx"], key="file1")
    file2 = st.file_uploader("Second GPX (optional)", type=["gpx"], key="file2")

# Main app layout
if file1:
    gpx_data1 = file1.read().decode("utf-8")
    df1, stats1 = parse_gpx(gpx_data1)

    if file2:
        gpx_data2 = file2.read().decode("utf-8")
        df2, stats2 = parse_gpx(gpx_data2)
    else:
        df2, stats2 = None, None

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗺️ Route Map")
        display_route_map(df1, df2)

    with col2:
        st.subheader("📈 Elevation Profile")
        plot_elevation_colored_by_slope(df1, df2)
        st.subheader("📊 Statistics")
        show_stats(stats1, stats2)

else:
    st.info("Please upload at least one GPX file to begin.")
