import streamlit as st

def show_stats(stats):
    st.markdown(f"""
    **Total Distance:** {stats['total_distance_km']:.2f} km  
    **Elevation Gain:** {stats['elevation_gain']:.1f} m  
    **Elevation Loss:** {stats['elevation_loss']:.1f} m  
    **Min Elevation:** {stats['min_elevation']:.1f} m  
    **Max Elevation:** {stats['max_elevation']:.1f} m  
    """)