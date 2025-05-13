import streamlit as st
import matplotlib.pyplot as plt

def show_segment_details(df, full_df, kind="climb"):
    if df.empty:
        st.info(f"No {kind}s detected.")
        return

    for i, row in df.iterrows():
        with st.expander(f"Ver más - {kind.capitalize()} {i+1} ({row['length_m']:.0f} m, {row['avg_slope']:.1f}%)"):
            st.markdown(f"**Categoría:** {row['category']}")
            st.markdown(f"**Inicio:** {row['start_km']:.2f} km")
            st.markdown(f"**Fin:** {row['end_km']:.2f} km")
            st.markdown(f"**Longitud:** {row['length_m']:.0f} m")
            st.markdown(f"**Ganancia/Pérdida:** {row.get('elev_gain', row.get('elev_loss', 0)):.1f} m")
            st.markdown(f"**Pendiente media:** {row['avg_slope']:.1f} %")

            st.markdown("**Distribución de pendientes en el tramo:**")
            grades = full_df["plot_grade"].iloc[row["start_idx"]:row["end_idx"]+1]
            fig, ax = plt.subplots(figsize=(6, 2.5))
            ax.hist(grades, bins=15, color="gray", edgecolor="black")
            ax.set_xlabel("Pendiente (%)")
            ax.set_ylabel("Frecuencia")
            ax.set_title("Histograma de pendientes")
            st.pyplot(fig)
