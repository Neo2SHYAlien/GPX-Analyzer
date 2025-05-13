# FILE: app.py

import streamlit as st
import matplotlib.pyplot as plt

from components.core.gpx_parser import parse_gpx
from components.core.climb_detector import detect_significant_segments
from components.core.utils import classify_climb_category

import os
print("DIR:", os.listdir("components/ui"))
from components.ui.elevation_chart import get_smoothed_grade, update_plot_elevation_colored_by_slope
from components.ui.map_display import update_display_route_map
from components.ui.stats_panel import show_stats
from components.ui.segment_details import show_segment_summary_and_details



st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

# ───────────────────────── SIDEBAR
with st.sidebar:
    st.title("Upload GPX File")
    uploaded_file = st.file_uploader("Choose a GPX file", type=["gpx"])
    tile_style = st.selectbox("Map Style", [
        "OpenStreetMap", "CartoDB positron", "CartoDB dark_matter"
    ])
    show_slope_colors = st.checkbox("Color route by slope", value=True)

# ───────────────────────── MAIN LOGIC
if uploaded_file:
    gpx_data = uploaded_file.read().decode("utf-8")
    df, stats = parse_gpx(gpx_data)
    df["plot_grade"] = get_smoothed_grade(df)

    # Detect segments
    climbs_df = detect_significant_segments(df, kind="climb")
    descents_df = detect_significant_segments(df, kind="descent")

    # Compute extra features
    climbs_df["category"] = climbs_df.apply(lambda row: classify_climb_category(row["length_m"], row["avg_slope"]), axis=1)
    descents_df["category"] = descents_df.apply(lambda row: classify_climb_category(row["length_m"], abs(row["avg_slope"])), axis=1)

    climbs_df["max_slope"] = climbs_df.apply(lambda row: df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].max(), axis=1)
    climbs_df["min_slope"] = climbs_df.apply(lambda row: df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].min(), axis=1)
    descents_df["max_slope"] = descents_df.apply(lambda row: df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].max(), axis=1)
    descents_df["min_slope"] = descents_df.apply(lambda row: df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].min(), axis=1)

    # ───────────────────────── COLUMNS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗺️ Route Map")
        update_display_route_map(df, tile_style=tile_style,
                                 climbs_df=climbs_df,
                                 descents_df=descents_df,
                                 color_by_slope=show_slope_colors)
        if show_slope_colors:
            # display_legend()
            # pass  # Legend is not implemented in this version
            st.markdown("**Legend:**")

    with col2:
        st.subheader("📈 Elevation Profile")
        update_plot_elevation_colored_by_slope(df,
                                               climbs_df=climbs_df,
                                               descents_df=descents_df,
                                               color_by_slope=show_slope_colors)
        st.subheader("📊 Statistics")
        show_stats(stats)

    # ───────────────────────── TABLES & SEGMENTS
    st.subheader("⛰️ Climbs and Descents")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Climbs**")
        st.dataframe(climbs_df[["start_km", "end_km", "elev_gain", "length_m", "avg_slope", "category"]],
                     use_container_width=True)

    with col2:
        st.markdown("**Descents**")
        st.dataframe(descents_df[["start_km", "end_km", "elev_loss", "length_m", "avg_slope", "category"]],
                     use_container_width=True)

    # ───────────────────────── EXPANDERS WITH HISTOGRAMS
    st.subheader("🔎 Segment Details")
    show_segment_summary_and_details(climbs_df, df, kind="climb")
    show_segment_summary_and_details(descents_df, df, kind="descent")

else:
    st.info("Please upload a GPX file to begin.")