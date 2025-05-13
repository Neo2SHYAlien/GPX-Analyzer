import streamlit as st
import matplotlib.pyplot as plt

def get_color(grade):
    if grade >= 18:
        return "#7f0000"  # dark red
    elif grade >= 15:
        return "#b22222"  # firebrick
    elif grade >= 12:
        return "#ff4500"  # orange red
    elif grade >= 10:
        return "#ff8c00"  # dark orange
    elif grade >= 6:
        return "#ffd700"  # gold
    elif grade >= 2:
        return "#ffff00"  # yellow
    elif grade >= 0:
        return "#adff2f"  # green yellow
    elif grade >= -2:
        return "#90ee90"  # light green
    elif grade >= -6:
        return "#87ceeb"  # sky blue
    elif grade >= -10:
        return "#0000ff"  # blue
    elif grade >= -15:
        return "#0000cd"  # medium blue
    else:
        return "#00008b"  # dark blue


def apply_slope_smoothing(df, target_meters=500):
    meters_per_point = df["distance"].iloc[-1] / len(df)
    window = max(10, int(target_meters / meters_per_point))
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
