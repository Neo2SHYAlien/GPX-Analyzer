import streamlit as st
import os

from components.core.logging import Timer
from components.core.gpx_parser import parse_gpx
from components.core.utils import classify_climb_category
from components.core.climb_detector import detect_significant_segments

from components.ui.elevation_chart import get_smoothed_grade, update_plot_elevation_colored_by_slope
from components.ui.map_display import update_display_route_map
from components.ui.stats_panel import show_stats
from components.ui.segment_details import show_segment_summary_and_details
from components.ui.legend import display_legend

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

# ───────────────────────── SIDEBAR
with st.sidebar:
    st.title("Upload GPX File")
    uploaded_file = st.file_uploader("Choose a GPX file", type=["gpx"])
    tile_style = st.selectbox("Map Style", [
        "OpenStreetMap", "CartoDB positron", "CartoDB dark_matter"
    ])
    show_slope_colors = st.checkbox("Color route by slope", value=True)
    simplified_view = st.checkbox("Simplified slope view (one color per climb/descent)", value=False)

    st.markdown("---")
    use_example = st.checkbox("Use example file (demo)", value=False)

    gpx_data = None
    if use_example:
        example_path = os.path.join("data", "example.gpx")
        if os.path.exists(example_path):
            with open(example_path, "r", encoding="utf-8") as f:
                gpx_data = f.read()
        else:
            st.error("Missing example file in /data/example.gpx")
    elif uploaded_file:
        gpx_data = uploaded_file.read().decode("utf-8")

# ───────────────────────── MAIN LOGIC
if gpx_data:
    t = Timer()
    try:
        df, stats = parse_gpx(gpx_data)
        t.log("Parsed GPX and computed stats")
    except Exception as e:
        st.error(f"❌ Error processing GPX file: {e}")
        st.stop()

    df["plot_grade"] = get_smoothed_grade(df)
    t.log("Calculated and smoothed slope")

    climbs_df = detect_significant_segments(df, kind="climb")
    descents_df = detect_significant_segments(df, kind="descent")
    t.log("Detected climbs and descents")

    for seg_df, is_climb in [(climbs_df, True), (descents_df, False)]:
        if not seg_df.empty:
            seg_df["category"] = seg_df.apply(lambda row: classify_climb_category(row["length_m"], abs(row["avg_slope"])), axis=1)
            seg_df["max_slope"] = seg_df.apply(lambda row: df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].max(), axis=1)
            seg_df["min_slope"] = seg_df.apply(lambda row: df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].min(), axis=1)

    t.log("Categorized and enriched segments")

    # ───────────────────────── COLUMNS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗺️ Route Map")
        update_display_route_map(df, tile_style, climbs_df, descents_df, color_by_slope=show_slope_colors)
        display_legend()
        t.log("Rendered map")

    with col2:
        st.subheader("📈 Elevation Profile")
        update_plot_elevation_colored_by_slope(
            df,
            climbs_df=climbs_df,
            descents_df=descents_df,
            color_by_slope=show_slope_colors,
            simplified=simplified_view
        )
        t.log("Rendered elevation chart")

        st.subheader("📊 Statistics")
        show_stats(stats)
        t.log("Rendered stats panel")

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

    t.log("Displayed data tables")

    st.subheader("🔎 Segment Details")
    show_segment_summary_and_details(climbs_df, df, kind="climb")
    show_segment_summary_and_details(descents_df, df, kind="descent")
    t.log("Rendered segment detail panels")

    # ───────────────────────── DOWNLOAD LOG
    with open("execution_log.txt", "r") as f:
        st.download_button("📥 Download Execution Log", data=f.read(), file_name="execution_log.txt")

else:
    st.info("📂 Upload or select a GPX file to begin.")
