import streamlit as st
from components.gpx_parser import parse_gpx
from components.elevation_chart import plot_elevation_colored_by_slope
from components.stats_panel import show_stats
from components.map_display import display_route_map, display_legend
from components.climb_detector import detect_climbs

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

with st.sidebar:
    st.title("Upload GPX File")
    uploaded_file = st.file_uploader("Choose a GPX file", type=["gpx"])
    tile_style = st.selectbox("Map Style", [
        "OpenStreetMap",
        "Stamen Terrain",
        "Stamen Toner",
        "Stamen Watercolor",
        "CartoDB positron",
        "CartoDB dark_matter"
    ])

if uploaded_file:
    gpx_data = uploaded_file.read().decode("utf-8")
    df, stats = parse_gpx(gpx_data)
    climbs_df = detect_climbs(df)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗺️ Route Map")
        display_route_map(df, tile_style=tile_style)
        display_legend()

    with col2:
        st.subheader("📈 Elevation Profile")
        plot_elevation_colored_by_slope(df, climbs_df=climbs_df)
        st.subheader("📊 Statistics")
        show_stats(stats)

    st.subheader("⛰️ Detected Climbs")
    if climbs_df.empty:
        st.info("No climbs detected with current thresholds.")
    else:
        st.dataframe(climbs_df[["start_km", "end_km", "elev_gain", "length_m", "avg_slope"]], use_container_width=True)

else:
    st.info("Please upload a GPX file to begin.")
