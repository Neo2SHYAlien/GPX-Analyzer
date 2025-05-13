import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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

def plot_elevation_colored_by_slope(df):
    detailed = st.checkbox("Check detailed slope (unsmoothed)", value=False)

    total_distance_m = df["distance"].iloc[-1]
    meters_per_point = total_distance_m / len(df)
    target_smoothing_meters = 200

    window = max(10, int(target_smoothing_meters / meters_per_point))

    df["plot_grade"] = df["grade"].rolling(window=window, center=True).mean().fillna(method="bfill").fillna(method="ffill")


    fig, ax = plt.subplots(figsize=(10, 4))

    for i in range(1, len(df)):
        x = df["distance"].iloc[i-1:i+1] / 1000
        y = df["ele"].iloc[i-1:i+1]
        ax.fill_between(x, 0, y, color=get_color(df["plot_grade"].iloc[i]), alpha=0.8)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile (Area Colored by Slope)")
    ax.grid(True)
    st.pyplot(fig)