import folium
from streamlit_folium import st_folium

def get_color(grade):
    if grade >= 18:
        return "#8B0000"  # Deep Red
    elif grade >= 10:
        return "#FF8C00"  # Orange
    elif grade >= 2:
        return "#FFFF00"  # Yellow
    elif grade >= 0:
        return "#ADFF2F"  # Light Green
    elif grade >= -2:
        return "#ADD8E6"  # Light Blue
    elif grade >= -10:
        return "#0000FF"  # Blue
    else:
        return "#00008B"  # Dark Blue


def display_route_map(df1, df2=None):
    center = [df1["lat"].iloc[len(df1)//2], df1["lon"].iloc[len(df1)//2]]
    m = folium.Map(location=center, zoom_start=13, control_scale=True)

    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='OpenStreetMap',
        opacity=0.1,
        name="Base Map"
    ).add_to(m)

    latlngs1 = df1[["lat", "lon"]].values.tolist()
    grades1 = df1["grade"].tolist()
    for i in range(1, len(latlngs1)):
        segment = [latlngs1[i-1], latlngs1[i]]
        color = get_color(grades1[i])
        folium.PolyLine(segment, color=color, weight=4, opacity=1).add_to(m)

    if df2 is not None:
        latlngs2 = df2[["lat", "lon"]].values.tolist()
        color = get_color(grades1[i])
        folium.PolyLine(latlngs2, color=color, weight=3, opacity=1).add_to(m)

    st_folium(m, width=800, height=500)
