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


def display_route_map(df1, df2=None, tile_style="OpenStreetMap"):
    center = [df1["lat"].iloc[len(df1)//2], df1["lon"].iloc[len(df1)//2]]
    m = folium.Map(location=center, zoom_start=13, control_scale=True, tiles=None)

    # Add user-selected tile layer with reduced opacity
    folium.TileLayer(
        tiles=tile_style,
        name=tile_style,
        opacity=0.3,
        control=True
    ).add_to(m)

    # Plot the first GPX track with grade-based coloring
    latlngs1 = df1[["lat", "lon"]].values.tolist()
    grades1 = df1["grade"].tolist()
    for i in range(1, len(latlngs1)):
        segment = [latlngs1[i-1], latlngs1[i]]
        color = get_color(grades1[i])
        folium.PolyLine(segment, color=color, weight=5, opacity=1).add_to(m)

    # If a second GPX track is provided, plot it with a distinct style
    if df2 is not None:
        latlngs2 = df2[["lat", "lon"]].values.tolist()
        grades2 = df2["grade"].tolist()
        for i in range(1, len(latlngs2)):
            segment = [latlngs2[i-1], latlngs2[i]]
            color = get_color(grades2[i])
            folium.PolyLine(segment, color=color, weight=3, opacity=0.7, dash_array='5,10').add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=800, height=500)
