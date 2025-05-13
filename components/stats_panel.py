import streamlit as st

def show_stats(stats1, stats2=None):
    def format_stats(stats):
        precision_score = min(100.0, (stats["point_density"] / 0.5) * 100)

        return f"""
        **Total Distance:** {stats['total_distance_km']:.2f} km  
        **Elevation Gain:** {stats['elevation_gain']:.1f} m  
        **Elevation Loss:** {stats['elevation_loss']:.1f} m  
        **Min Elevation:** {stats['min_elevation']:.1f} m  
        **Max Elevation:** {stats['max_elevation']:.1f} m  
        **Average Grade:** {stats['average_grade']:.2f} %  
        **Max Grade:** {stats['max_grade']:.2f} %  
        **Moving Time:** {stats['moving_time_min']:.1f} min  
        **Total Time:** {stats['total_time_min']:.1f} min  
        **Number of Points:** {stats['num_points']}  
        **Point Density:** {stats['point_density']:.2f} points/meter  
        **Precision Score:** {precision_score:.1f} %
        """

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### GPX File 1")
        st.markdown(format_stats(stats1))

    if stats2:
        with col2:
            st.markdown("### GPX File 2")
            st.markdown(format_stats(stats2))