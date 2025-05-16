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

from utils.gps_signal_analysis import run_gps_signal_analysis

st.set_page_config(layout="wide", page_title="GPX Analyzer 📍")

# ───────────────────────── GPX INPUT
with st.sidebar:
    st.title("Upload GPX File")
    uploaded_file = st.file_uploader("Choose a GPX file", type=["gpx"])
    use_example = st.checkbox("Use example GPX file", value=False)

    gpx_data = None
    if use_example:
        example_path = os.path.join("data", "example.gpx")
        if os.path.exists(example_path):
            with open(example_path, "r", encoding="utf-8") as f:
                gpx_data = f.read()
        else:
            st.error("Missing example file in /data/example.gpx")
    elif uploaded_file:
        try:
            gpx_data = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(f"❌ Error decoding GPX: {e}")

# Parse and reduce only once
df_reduced, stats = None, None
if gpx_data:
    try:
        df_reduced, stats = parse_gpx(gpx_data)
    except Exception as e:
        st.error(f"❌ Error processing GPX file: {e}")

# ───────────────────────── TABS
tab1, tab2 = st.tabs(["🏔️ Hills & Climbs", "📡 GPS Signal Quality"])

# ───────────────────────── TAB 1
with tab1:
    if df_reduced is not None:
        t = Timer()
        df_reduced["plot_grade"] = get_smoothed_grade(df_reduced)
        t.log("Calculated and smoothed slope")

        climbs_df = detect_significant_segments(df_reduced, kind="climb")
        descents_df = detect_significant_segments(df_reduced, kind="descent")
        t.log("Detected climbs and descents")

        for seg_df, is_climb in [(climbs_df, True), (descents_df, False)]:
            if not seg_df.empty:
                seg_df["category"] = seg_df.apply(lambda row: classify_climb_category(row["length_m"], abs(row["avg_slope"])), axis=1)
                seg_df["max_slope"] = seg_df.apply(lambda row: df_reduced["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].max(), axis=1)
                seg_df["min_slope"] = seg_df.apply(lambda row: df_reduced["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1].min(), axis=1)

        t.log("Categorized and enriched segments")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🗺️ Route Map")
            update_display_route_map(df_reduced, tile_style="OpenStreetMap", climbs_df=climbs_df, descents_df=descents_df, color_by_slope=True)
            display_legend()
            t.log("Rendered map")

        with col2:
            st.subheader("📈 Elevation Profile")
            update_plot_elevation_colored_by_slope(df_reduced, climbs_df=climbs_df, descents_df=descents_df, color_by_slope=True, simplified=False)
            t.log("Rendered elevation chart")
            st.subheader("📊 Statistics")
            show_stats(stats)
            t.log("Rendered stats panel")

        st.subheader("⛰️ Climbs and Descents")
        col1, col2 = st.columns(2)
        with col1:
            if not climbs_df.empty:
                st.markdown("**Climbs**")
                st.dataframe(climbs_df[["start_km", "end_km", "elev_gain", "length_m", "avg_slope", "category"]],
                             use_container_width=True)
            else:
                st.info("No climbs detected.")
        with col2:
            if not descents_df.empty:
                st.markdown("**Descents**")
                st.dataframe(descents_df[["start_km", "end_km", "elev_loss", "length_m", "avg_slope", "category"]],
                             use_container_width=True)
            else:
                st.info("No descents detected.")

        st.subheader("🔎 Segment Details")
        show_segment_summary_and_details(climbs_df, df_reduced, kind="climb")
        show_segment_summary_and_details(descents_df, df_reduced, kind="descent")

        with open("execution_log.txt", "r") as f:
            st.download_button("📥 Download Log", data=f.read(), file_name="execution_log.txt")
    else:
        st.info("📂 Upload or select a GPX file to begin.")

# ───────────────────────── TAB 2
with tab2:
    if df_reduced is not None:
        run_gps_signal_analysis(df_reduced)
    else:
        st.info("📂 Upload or select a GPX file to begin.")
