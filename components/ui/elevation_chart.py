import matplotlib.pyplot as plt
import streamlit as st
from components.core.utils import apply_slope_smoothing, get_color

def get_smoothed_grade(df):
    return apply_slope_smoothing(df)["plot_grade"]

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def update_plot_elevation_colored_by_slope(df, climbs_df=None, descents_df=None, color_by_slope=True, simplified=False):
    import streamlit as st
    from components.core.utils import get_color, apply_slope_smoothing

    st.markdown("*Slope smoothed over ~300 meters*")
    df = apply_slope_smoothing(df)

    fig, ax = plt.subplots(figsize=(10, 4))

    if simplified:
        # Draw base elevation with neutral gray
        ax.plot(df["distance"] / 1000, df["ele"], color="#999999", linewidth=1.5, alpha=0.7)

        # Draw simplified climb segments
        if climbs_df is not None:
            for _, row in climbs_df.iterrows():
                segment = df[(df["distance"] / 1000 >= row["start_km"]) & (df["distance"] / 1000 <= row["end_km"])]
                x = segment["distance"] / 1000
                y = segment["ele"]
                ax.fill_between(x, y, color="#FFA500", alpha=0.4)

        # Draw simplified descent segments
        if descents_df is not None:
            for _, row in descents_df.iterrows():
                segment = df[(df["distance"] / 1000 >= row["start_km"]) & (df["distance"] / 1000 <= row["end_km"])]
                x = segment["distance"] / 1000
                y = segment["ele"]
                ax.fill_between(x, y, color="#87CEFA", alpha=0.3)

    else:
        # Detailed coloring by gradient
        for i in range(1, len(df)):
            x = df["distance"].iloc[i-1:i+1] / 1000
            y = df["ele"].iloc[i-1:i+1]
            color = get_color(df["plot_grade"].iloc[i]) if color_by_slope else "#999999"
            ax.fill_between(x, 0, y, color=color, alpha=0.8)

        if climbs_df is not None:
            for _, row in climbs_df.iterrows():
                ax.axvline(x=row["start_km"], color="black", linestyle="--", alpha=0.7)
                ax.axvline(x=row["end_km"], color="black", linestyle="--", alpha=0.7)

        if descents_df is not None:
            for _, row in descents_df.iterrows():
                ax.axvline(x=row["start_km"], color="blue", linestyle=":", alpha=0.5)
                ax.axvline(x=row["end_km"], color="blue", linestyle=":", alpha=0.5)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile")
    ax.grid(True)
    st.pyplot(fig)


