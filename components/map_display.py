import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

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


def display_route_map(df1, df2=None, tile_style="CartoDB positron"):
    center = [df1["lat"].iloc[len(df1)//2], df1["lon"].iloc[len(df1)//2]]
    m = folium.Map(location=center, zoom_start=13, control_scale=True, tiles=None)

    # Add user-selected tile layer with reduced opacity
    folium.TileLayer(
        tiles=tile_style,
        name=tile_style,
        opacity=0.5,
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
            folium.PolyLine(segment, color=color, weight=3, opacity=1, dash_array='5,10').add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=800, height=500)



def display_legend():
    legend_html = """
    <div style="padding:10px; background:white; border-radius:8px; width:fit-content; font-size:14px;">
        <b>Grade Legend (Slope %)</b><br>
        <span style="background:#8B0000; width:20px; display:inline-block;">&nbsp;</span> ≥ 18%<br>
        <span style="background:#FF8C00; width:20px; display:inline-block;">&nbsp;</span> 10–17%<br>
        <span style="background:#FFFF00; width:20px; display:inline-block;">&nbsp;</span> 2–9%<br>
        <span style="background:#ADFF2F; width:20px; display:inline-block;">&nbsp;</span> 0–1%<br>
        <span style="background:#ADD8E6; width:20px; display:inline-block;">&nbsp;</span> -1 to -2%<br>
        <span style="background:#0000FF; width:20px; display:inline-block;">&nbsp;</span> -3 to -10%<br>
        <span style="background:#00008B; width:20px; display:inline-block;">&nbsp;</span> < -10%<br>
    </div>
    """
    components.html(legend_html, height=200)
