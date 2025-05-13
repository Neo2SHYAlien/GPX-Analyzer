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

def plot_elevation_colored_by_slope(df1, df2=None):
    fig, ax = plt.subplots(figsize=(10, 4))

    for i in range(1, len(df1)):
        ax.plot(
            df1["distance"].iloc[i-1:i+1] / 1000,
            df1["ele"].iloc[i-1:i+1],
            color=get_color(df1["grade"].iloc[i]),
            linewidth=2
        )

    if df2 is not None:
        ax.plot(
            df2["distance"] / 1000,
            df2["ele"],
            color=get_color(df2["grade"].iloc[i]),
            linestyle='--',
            linewidth=2
        )
        ax.legend()

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile Colored by Grade")
    ax.grid(True)

    st.pyplot(fig)