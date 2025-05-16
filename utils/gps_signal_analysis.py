import pandas as pd
import gpxpy
import requests
import folium
from folium.plugins import HeatMap
from geopy.distance import geodesic
import branca.colormap as cm
from streamlit_folium import st_folium
import streamlit as st
import altair as alt


def run_gps_signal_analysis(gpx_data, radius=50):
    st.title("📡 GPS Signal Quality Analyzer")

    # ────── Parse GPX
    try:
        gpx = gpxpy.parse(gpx_data)
        data = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if point.time:
                        data.append({
                            'lat': point.latitude,
                            'lon': point.longitude,
                            'ele': point.elevation,
                            'time': point.time
                        })
        df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error reading GPX: {e}")
        return

    if df.empty:
        st.warning("No points found in GPX.")
        return

    def reduce_df(df, max_points=500):
        step = max(1, len(df) // max_points)
        return df.iloc[::step].reset_index(drop=True)

    df = reduce_df(df)
    st.markdown(f"🔢 Points after reduction: {len(df)}")

    # ────── Bounding Box & Overpass Query
    min_lat, max_lat = df['lat'].min(), df['lat'].max()
    min_lon, max_lon = df['lon'].min(), df['lon'].max()
    bbox_key = f"{min_lat:.5f}-{min_lon:.5f}-{max_lat:.5f}-{max_lon:.5f}"

    if 'building_cache' not in st.session_state:
        st.session_state['building_cache'] = {}

    if bbox_key in st.session_state['building_cache']:
        buildings_df = st.session_state['building_cache'][bbox_key]
    else:
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
          way["building"]({min_lat},{min_lon},{max_lat},{max_lon});
          relation["building"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out center;
        """
        try:
            response = requests.get(overpass_url, params={'data': query}, timeout=25)
            response.raise_for_status()
            raw_data = response.json()
        except Exception as e:
            st.error(f"Overpass API error: {e}")
            return

        buildings = []
        for el in raw_data['elements']:
            lat_ = el.get('lat') or el.get('center', {}).get('lat')
            lon_ = el.get('lon') or el.get('center', {}).get('lon')
            if lat_ is None or lon_ is None:
                continue
            tags = el.get('tags', {})
            h = tags.get('height')
            l = tags.get('building:levels')
            height = None
            levels = None
            if h:
                try:
                    height = float(h)
                except:
                    pass
            if l and levels is None:
                try:
                    levels = int(l)
                except:
                    pass
            buildings.append({
                'lat': lat_,
                'lon': lon_,
                'height': height,
                'levels': levels
            })
        buildings_df = pd.DataFrame(buildings)
        st.session_state['building_cache'][bbox_key] = buildings_df

    if buildings_df.empty:
        st.warning("No buildings found in the area.")
        return

    # ────── Risk Calculation
    heatmap_data = []
    risk_scores = []

    for i, row in df.iterrows():
        lat, lon = row['lat'], row['lon']
        nearby = buildings_df[buildings_df.apply(
            lambda b: geodesic((lat, lon), (b['lat'], b['lon'])).meters < radius, axis=1)]
        sum_height = nearby['height'].fillna(nearby['levels'].fillna(0) * 3).sum()
        heatmap_data.append([lat, lon, sum_height])
        risk_scores.append(sum_height)

    df['risk_score'] = pd.Series(risk_scores).rolling(window=5, center=True).mean().fillna(method='bfill').fillna(method='ffill')

    gps_score = "✅ High"
    danger_ratio = (df['risk_score'] >= 60).mean()
    if danger_ratio > 0.5:
        gps_score = "❌ Low"
    elif danger_ratio > 0.2:
        gps_score = "⚠️ Medium"

    st.markdown(f"### 📡 Estimated GPS Precision: {gps_score}")

    # ────── Map
    center = [df.iloc[0]['lat'], df.iloc[0]['lon']]
    m = folium.Map(location=center, zoom_start=15)

    # Route colored by risk
    for i in range(len(df) - 1):
        lat1, lon1 = df.loc[i, ['lat', 'lon']]
        lat2, lon2 = df.loc[i + 1, ['lat', 'lon']]
        avg_risk = (df.loc[i, 'risk_score'] + df.loc[i + 1, 'risk_score']) / 2
        if avg_risk < 30:
            color = 'green'
        elif avg_risk < 60:
            color = 'orange'
        else:
            color = 'red'
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color=color, weight=5, opacity=0.9).add_to(m)

    # Color map for buildings
    heights = buildings_df['height'].dropna().tolist()
    min_h, max_h = min(heights or [0]), max(heights or [30])
    colormap = cm.linear.YlOrRd_09.scale(min_h, max_h)
    colormap.caption = 'Building Height (m)'
    colormap.add_to(m)

    for _, b in buildings_df.iterrows():
        h = b['height'] if pd.notnull(b['height']) else (b['levels'] or 0) * 3
        color = colormap(h) if h else '#999999'
        folium.CircleMarker(location=[b['lat'], b['lon']], radius=5, color=color,
                            fill=True, fill_color=color, fill_opacity=0.8).add_to(m)

    HeatMap(heatmap_data, radius=25, blur=15, max_zoom=17).add_to(m)

    st.markdown("### 🗺️ Map: Buildings & Risk Zones")
    st_folium(m, width=1000, height=600)

    # ────── Charts
    st.markdown("### 📈 Risk Score by Point")
    st.altair_chart(
        alt.Chart(df.reset_index()).mark_line().encode(
            x=alt.X('index', title='Point Index'),
            y=alt.Y('risk_score', title='Total Nearby Building Height (smoothed)')
        ).properties(height=250, width=800),
        use_container_width=True
    )

    st.markdown("### 📊 Histogram of GPS Risk Levels")
    df['risk_level'] = pd.cut(df['risk_score'], bins=[-1, 30, 60, float('inf')], labels=['Low', 'Medium', 'High'])
    st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('risk_level:N', title='Risk Level'),
            y=alt.Y('count():Q', title='Number of Points'),
            color='risk_level:N'
        ).properties(height=250, width=600),
        use_container_width=True
    )

    # ────── Download
    st.download_button("⬇️ Download Buildings CSV", buildings_df.to_csv(index=False), file_name="buildings.csv")
