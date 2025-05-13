import matplotlib.pyplot as plt
import streamlit as st
from components.core.utils import apply_slope_smoothing, get_color

def get_smoothed_grade(df):
    return apply_slope_smoothing(df)["plot_grade"]

def update_plot_elevation_colored_by_slope(df, climbs_df=None, descents_df=None, color_by_slope=True):
    st.markdown(f"*Slope smoothed over ~300 meters*")
    df = apply_slope_smoothing(df)

    fig, ax = plt.subplots(figsize=(10, 4))

    for i in range(1, len(df)):
        x = df["distance"].iloc[i-1:i+1] / 1000
        y = df["ele"].iloc[i-1:i+1]
        color = get_color(df["plot_grade"].iloc[i]) if color_by_slope else "#999999"
        ax.fill_between(x, 0, y, color=color, alpha=0.8)

    if climbs_df is not None and not climbs_df.empty:
        for _, row in climbs_df.iterrows():
            ax.axvline(x=row["start_km"], color="black", linestyle="--", alpha=0.7)
            ax.axvline(x=row["end_km"], color="black", linestyle="--", alpha=0.7)

    if descents_df is not None and not descents_df.empty:
        for _, row in descents_df.iterrows():
            ax.axvline(x=row["start_km"], color="blue", linestyle=":", alpha=0.5)
            ax.axvline(x=row["end_km"], color="blue", linestyle=":", alpha=0.5)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile" + (" (Smoothed Slope)" if color_by_slope else ""))
    ax.grid(True)
    st.pyplot(fig)
