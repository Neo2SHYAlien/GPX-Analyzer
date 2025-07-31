import matplotlib.pyplot as plt
import streamlit as st

from components.core.utils import apply_slope_smoothing, get_color


def get_smoothed_grade(df):
    return apply_slope_smoothing(df)["plot_grade"]


def update_plot_elevation_colored_by_slope(
    df,
    climbs_df=None,
    descents_df=None,
    color_by_slope: bool = True,
    simplified: bool = False,
) -> None:
    st.markdown("*Slope smoothed over ~300 meters*")
    df = apply_slope_smoothing(df)

    fig, ax = plt.subplots(figsize=(10, 4))

    if simplified:
        _draw_simplified_segments(ax, df, climbs_df, descents_df)
    else:
        _draw_detailed_colored_profile(ax, df, climbs_df, descents_df, color_by_slope)

    ax.set_xlabel("Distance [km]")
    ax.set_ylabel("Elevation [m]")
    ax.set_title("Elevation Profile")
    ax.grid(True)
    st.pyplot(fig)


def _draw_simplified_segments(ax, df, climbs_df, descents_df) -> None:
    ax.plot(df["distance"] / 1000, df["ele"], color="#999999", linewidth=1.5, alpha=0.7)

    for segment_df, color in [(climbs_df, "#FFA500"), (descents_df, "#87CEFA")]:
        if segment_df is not None:
            for _, row in segment_df.iterrows():
                segment = df[
                    (df["distance"] / 1000 >= row["start_km"])
                    & (df["distance"] / 1000 <= row["end_km"])
                ]
                ax.fill_between(
                    segment["distance"] / 1000, segment["ele"], color=color, alpha=0.4
                )


def _draw_detailed_colored_profile(
    ax, df, climbs_df, descents_df, color_by_slope
) -> None:
    for i in range(1, len(df)):
        x = df["distance"].iloc[i - 1 : i + 1] / 1000
        y = df["ele"].iloc[i - 1 : i + 1]
        color = get_color(df["plot_grade"].iloc[i]) if color_by_slope else "#999999"
        ax.fill_between(x, 0, y, color=color, alpha=0.8)

    # Optional: mark climbs and descents
    for segment_df, color in [(climbs_df, "black"), (descents_df, "blue")]:
        if segment_df is not None:
            for _, row in segment_df.iterrows():
                style = "--" if color == "black" else ":"
                ax.axvline(x=row["start_km"], color=color, linestyle=style, alpha=0.6)
                ax.axvline(x=row["end_km"], color=color, linestyle=style, alpha=0.6)
