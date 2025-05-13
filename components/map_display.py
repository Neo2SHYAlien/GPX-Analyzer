import folium
from streamlit_folium import st_folium

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
    elif grade >= 0: return "gray"
    elif grade >= -2: return "lightgreen"
    elif grade >= -4: return "mediumseagreen"
    elif grade >= -6: return "cyan"
    elif grade >= -8: return "cornflowerblue"
    elif grade >= -10: return "dodgerblue"
    else: return "blue"

def display_route_map(df1, df2=None):
    center = [df1["lat"].iloc[len(df1)//2], df1["lon"].iloc[len(df1)//2]]
    m = folium.Map(location=center, zoom_start=13, control_scale=True)

    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='OpenStreetMap',
        opacity=0.5,
        name="Base Map"
    ).add_to(m)

    latlngs1 = df1[["lat", "lon"]].values.tolist()
    grades1 = df1["grade"].tolist()
    for i in range(1, len(latlngs1)):
        segment = [latlngs1[i-1], latlngs1[i]]
        color = get_color(grades1[i])
        folium.PolyLine(segment, color=color, weight=4).add_to(m)

    if df2 is not None:
        latlngs2 = df2[["lat", "lon"]].values.tolist()
        folium.PolyLine(latlngs2, color="black", weight=3, opacity=0.7, dash_array="5,5").add_to(m)

    st_folium(m, width=800, height=500)
