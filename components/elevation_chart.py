import streamlit as st
import matplotlib.pyplot as plt

def get_color(grade):
    if grade >= 18:
        return "#8B0000"  # Deep Red
    elif grade >= 10:
        return "#FF8C00"  # Orange
    elif grade >= 2:
        return "#FFFF00"  # Yellow
    elif grade >= 0:
        return "#ADFF2F"  # Light Green
    elif grade >= -2:
        return "#ADD8E6"  # Light Blue
    elif grade >= -10:
        return "#0000FF"  # Blue
    else:
        return "#00008B"  # Dark Blue

def apply_slope_smoothing(df, target_meters=300):
    meters_per_point = df["distance"].iloc[-1] / len(df)
    window = max(3, int(target_meters / meters_per_point))
    df["plot_grade"] = df["grade"].rolling(window=window, center=True).mean().bfill().ffill()
    return df

def plot_elevation_colored_by_slope(df, climbs_df=None):
    st.markdown(f"*Slope smoothed over ~300 meters*")
    df = apply_slope_smoothing(df)

    fig, ax = plt.subplots(figsize=(10, 4))

    for i in range(1, len(df)):
        x = df["distance"].iloc[i-1:i+1] / 1000
        y = df["ele"].iloc[i-1:i+1]
        ax.fill_between(x, 0, y, color=get_color(df["plot_grade"].iloc[i]), alpha=0.8)

    if climbs_df is not None and not climbs_df.empty:
        for _, row in climbs_df.iterrows():
            ax.axvline(x=row["start_km"], color="black", linestyle="--", alpha=0.7)
            ax.axvline(x=row["end_km"], color="black", linestyle="--", alpha=0.7)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile (Smoothed Slope)")
    ax.grid(True)
    st.pyplot(fig)

def get_smoothed_grade(df):
    return apply_slope_smoothing(df)["plot_grade"]