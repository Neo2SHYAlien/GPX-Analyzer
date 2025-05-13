# FILE: app.py

import streamlit as st
from components.gpx_parser import parse_gpx
from components.stats_panel import show_stats
from components.elevation_chart import get_smoothed_grade, update_plot_elevation_colored_by_slope
from components.map_display import display_legend, update_display_route_map
from components.climb_detector import detect_significant_segments

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

with st.sidebar:
    st.title("Upload GPX File")
    uploaded_file = st.file_uploader("Choose a GPX file", type=["gpx"])
    tile_style = st.selectbox("Map Style", [
        "OpenStreetMap",
        "CartoDB positron",
        "CartoDB dark_matter"
    ])
    show_slope_colors = st.checkbox("Color route by slope", value=True)

if uploaded_file:
    gpx_data = uploaded_file.read().decode("utf-8")
    df, stats = parse_gpx(gpx_data)

    df["plot_grade"] = get_smoothed_grade(df)

    climbs_df = detect_significant_segments(df, kind="climb")
    descents_df = detect_significant_segments(df, kind="descent")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗽️ Route Map")
        update_display_route_map(df, tile_style=tile_style, climbs_df=climbs_df, descents_df=descents_df, color_by_slope=show_slope_colors)
        display_legend()

    with col2:
        st.subheader("📈 Elevation Profile")
        update_plot_elevation_colored_by_slope(df, climbs_df=climbs_df, descents_df=descents_df)
        st.subheader("📊 Statistics")
        show_stats(stats)

    st.subheader("⛰️ Climbs and Descents")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Climbs**")
        if climbs_df.empty:
            st.info("No climbs detected.")
        else:
            st.dataframe(climbs_df[["start_km", "end_km", "elev_gain", "length_m", "avg_slope"]], use_container_width=True)

    with col2:
        st.markdown("**Descents**")
        if descents_df.empty:
            st.info("No descents detected.")
        else:
            st.dataframe(descents_df[["start_km", "end_km", "elev_loss", "length_m", "avg_slope"]], use_container_width=True)

else:
    st.info("Please upload a GPX file to begin.")
