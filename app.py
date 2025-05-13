import streamlit as st
from components.gpx_parser import parse_gpx
from components.elevation_chart import plot_elevation_colored_by_slope, get_smoothed_grade
from components.stats_panel import show_stats
from components.map_display import display_route_map, display_legend, update_display_route_map
from components.climb_detector import  detect_significant_segments
from components.elevation_chart import update_plot_elevation_colored_by_slope


st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

with st.sidebar:
    st.title("Upload GPX File")
    uploaded_file = st.file_uploader("Choose a GPX file", type=["gpx"])
    tile_style = st.selectbox("Map Style", [
        "OpenStreetMap",
        "CartoDB positron",
        "CartoDB dark_matter"
    ])

if uploaded_file:
    gpx_data = uploaded_file.read().decode("utf-8")
    df, stats = parse_gpx(gpx_data)


    df["plot_grade"] = get_smoothed_grade(df)

    climbs_df = detect_significant_segments(df, kind="climb")
    descents_df = detect_significant_segments(df, kind="descent")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗺️ Route Map")
        # display_route_map(df, tile_style=tile_style)
        update_display_route_map(df, tile_style=tile_style, climbs_df=climbs_df, descents_df=descents_df)
        display_legend()

    with col2:
        st.subheader("📈 Elevation Profile")
        update_plot_elevation_colored_by_slope(df, climbs_df=climbs_df, descents_df=descents_df)
        st.subheader("📊 Statistics")
        show_stats(stats)

    st.subheader("⛰️ Detected Climbs")
    if climbs_df.empty:
        st.info("No climbs detected with current thresholds.")
    else:
        st.dataframe(climbs_df[["start_km", "end_km", "elev_gain", "length_m", "avg_slope"]], use_container_width=True)

    st.subheader("⛰️ Detected Descents")
    if descents_df.empty:
        st.info("No descents detected with current thresholds.")
    else:
        st.dataframe(descents_df[["start_km", "end_km", "elev_loss", "length_m", "avg_slope"]], use_container_width=True)

else:
    st.info("Please upload a GPX file to begin.")
