import matplotlib.pyplot as plt
import streamlit as st


def show_segment_summary_and_details(df, full_df, kind="climb") -> None:
    if df.empty:
        st.info(f"No {kind}s detected.")
        return

    for i, row in df.iterrows():
        title = f"{kind.capitalize()} {i + 1} • {row['length_m']:.0f} m, {row.get('elev_gain', row.get('elev_loss', 0)):.0f} m"
        summary = (
            f"📍 **Start:** {row['start_km']:.2f} km\n"
            f"🏁 **End:** {row['end_km']:.2f} km\n"
            f"📏 **Length:** {row['length_m']:.0f} m\n"
            f"⛰️ **Gain/Loss:** {row.get('elev_gain', row.get('elev_loss', 0)):.1f} m\n"
            f"📐 **Avg Slope:** {row['avg_slope']:.1f} %\n"
            f"📉 **Min Slope:** {row['min_slope']:.1f} %\n"
            f"📈 **Max Slope:** {row['max_slope']:.1f} %\n"
            f"🏷️ **Category:** {row['category']}"
        )

        with st.expander(f"🔽 {title}"):
            st.markdown(summary)
            st.markdown("**Distribución de pendientes en el tramo:**")
            grades = full_df["plot_grade"].iloc[row["start_idx"] : row["end_idx"] + 1]
            fig, ax = plt.subplots(figsize=(6, 2.5))
            ax.hist(grades, bins=15, color="gray", edgecolor="black")
            ax.set_xlabel("Pendiente (%)")
            ax.set_ylabel("Frecuencia")
            ax.set_title("Histograma de pendientes")
            st.pyplot(fig)
