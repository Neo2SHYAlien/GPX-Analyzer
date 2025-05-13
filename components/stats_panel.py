import streamlit as st

def show_stats(stats1, stats2=None):
    def format_stats(stats):
        return f"""
        **Total Distance:** {stats['total_distance_km']:.2f} km  
        **Elevation Gain:** {stats['elevation_gain']:.1f} m  
        **Elevation Loss:** {stats['elevation_loss']:.1f} m  
        **Min Elevation:** {stats['min_elevation']:.1f} m  
        **Max Elevation:** {stats['max_elevation']:.1f} m  
        **Average Grade:** {stats['average_grade']:.2f} %  
        **Max Grade:** {stats['max_grade']:.2f} %  
        **Min Grade:** {stats['min_grade']:.2f} %
        **Average Speed:** {stats['average_speed']:.2f} km/h
        **Moving Time:** {stats['moving_time_min']:.1f} min  
        **Total Time:** {stats['total_time_min']:.1f} min  
        """

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### GPX File 1")
        st.markdown(format_stats(stats1))

    if stats2:
        with col2:
            st.markdown("### GPX File 2")
            st.markdown(format_stats(stats2))