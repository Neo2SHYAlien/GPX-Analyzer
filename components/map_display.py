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

def display_route_map(df):
    latlngs = df[["lat", "lon"]].values.tolist()
    grades = df["grade"].tolist()

    center = latlngs[len(latlngs) // 2]
    m = folium.Map(location=center, zoom_start=13)

    for i in range(1, len(latlngs)):
        segment = [latlngs[i-1], latlngs[i]]
        color = get_color(grades[i])
        folium.PolyLine(segment, color=color, weight=4).add_to(m)
    folium.TileLayer(
    tiles='CartoDB positron',
    attr='CartoDB',
    name='Light',
    control=True,
    opacity=0.5  # this helps
).add_to(m)
    st_folium(m, width=800, height=500)
