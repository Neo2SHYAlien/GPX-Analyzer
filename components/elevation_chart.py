import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def get_color(grade):
    if grade >= 18: return "black"
    elif grade >= 16: return "blue"
    elif grade >= 14: return "darkgreen"
    elif grade >= 12: return "magenta"
    elif grade >= 10: return "red"
    elif grade >= 8: return "orangered"
    elif grade >= 6: return "deepskyblue"
    elif grade >= 4: return "springgreen"
    elif grade >= 2: return "yellow"
    elif grade >= 0: return "lightgray"
    elif grade >= -2: return "lightgreen"
    elif grade >= -4: return "mediumseagreen"
    elif grade >= -6: return "cyan"
    elif grade >= -8: return "cornflowerblue"
    elif grade >= -10: return "dodgerblue"
    else: return "blue"

def plot_elevation_colored_by_slope(df):
    distances_km = df["distance"] / 1000
    elevations = df["ele"]
    grades = df["grade"]

    fig, ax = plt.subplots(figsize=(10, 3))
    for i in range(1, len(df)):
        ax.plot(distances_km[i-1:i+1], elevations[i-1:i+1],
                color=get_color(grades[i]), linewidth=2)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile Colored by Grade")
    ax.grid(True)

    st.pyplot(fig)