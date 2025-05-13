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

def plot_elevation_colored_by_slope(df1, df2=None):
    detailed = st.checkbox("Check detailed slope (unsmoothed)", value=False)

    # Always compute smoothed slope, optionally use raw
    df1["plot_grade"] = df1["grade"] if detailed else df1["grade"].rolling(window=5, center=True).mean().fillna(method="bfill").fillna(method="ffill")
    if df2 is not None:
        df2["plot_grade"] = df2["grade"] if detailed else df2["grade"].rolling(window=5, center=True).mean().fillna(method="bfill").fillna(method="ffill")

    fig, ax = plt.subplots(figsize=(10, 4))

    for i in range(1, len(df1)):
        x = df1["distance"].iloc[i-1:i+1] / 1000
        y = df1["ele"].iloc[i-1:i+1]
        ax.fill_between(x, 0, y, color=get_color(df1["plot_grade"].iloc[i]), alpha=0.8)

    if df2 is not None:
        for j in range(1, len(df2)):
            x = df2["distance"].iloc[j-1:j+1] / 1000
            y = df2["ele"].iloc[j-1:j+1]
            ax.fill_between(x, 0, y, color=get_color(df2["plot_grade"].iloc[j]), alpha=0.4)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile (Area Colored by Slope)")
    ax.grid(True)
    st.pyplot(fig)