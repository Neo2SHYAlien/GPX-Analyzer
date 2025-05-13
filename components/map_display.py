import folium
from streamlit_folium import st_folium
from components.elevation_chart import get_smoothed_grade

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

def display_route_map(df, tile_style="OpenStreetMap"):
    # Smooth the grade before plotting
    df["plot_grade"] = get_smoothed_grade(df)

    center = [df["lat"].iloc[len(df)//2], df["lon"].iloc[len(df)//2]]
    m = folium.Map(location=center, zoom_start=13, control_scale=True, tiles=None)

    folium.TileLayer(
        tiles=tile_style,
        name=tile_style,
        opacity=0.3,
        control=True
    ).add_to(m)

    latlngs = df[["lat", "lon"]].values.tolist()
    grades = df["plot_grade"].tolist()

    for i in range(1, len(latlngs)):
        segment = [latlngs[i-1], latlngs[i]]
        color = get_color(grades[i])
        folium.PolyLine(segment, color=color, weight=4, opacity=1).add_to(m)

    folium.LayerControl().add_to(m)
    st_folium(m, width=800, height=500)

def display_legend():
    from streamlit.components.v1 import html
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
    html(legend_html, height=200)