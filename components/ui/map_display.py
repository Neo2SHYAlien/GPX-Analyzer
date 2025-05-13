import folium
from streamlit_folium import st_folium
from components.ui.elevation_chart import get_smoothed_grade
from components.core.utils import get_color

def update_display_route_map(df, tile_style="OpenStreetMap", climbs_df=None, descents_df=None, color_by_slope=True):
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
        color = get_color(grades[i]) if color_by_slope else "#999999"
        folium.PolyLine(segment, color=color, weight=4, opacity=1).add_to(m)

    if climbs_df is not None and not climbs_df.empty:
        for idx, row in climbs_df.iterrows():
            mid_idx = (row["start_idx"] + row["end_idx"]) // 2
            lat, lon = df.loc[mid_idx, ["lat", "lon"]]
            folium.Marker(
                location=[lat, lon],
                popup=f"Climb {idx+1}: {int(row['elev_gain'])}m ↑",
                icon=folium.DivIcon(html=f"<div style='font-size: 12px; color: red;'>{idx+1}</div>")
            ).add_to(m)

    if descents_df is not None and not descents_df.empty:
        for idx, row in descents_df.iterrows():
            mid_idx = (row["start_idx"] + row["end_idx"]) // 2
            lat, lon = df.loc[mid_idx, ["lat", "lon"]]
            folium.Marker(
                location=[lat, lon],
                popup=f"Descent {idx+1}: {int(row['elev_loss'])}m ↓",
                icon=folium.DivIcon(html=f"<div style='font-size: 12px; color: blue;'>{idx+1}</div>")
            ).add_to(m)

    folium.LayerControl().add_to(m)
    try:
        st_folium(m, width=800, height=500, use_container_width=True, key="main_map", return_last_map=False)
    except TypeError:
        st_folium(m, width=800, height=500, key="main_map")

    
from streamlit.components.v1 import html

# def display_legend():
#     legend_html = """
#     <div style="padding:10px; background:white; border-radius:8px; width:fit-content; font-size:14px;">
#         <b>Grade Legend (Slope %)</b><br>
#         <span style="background:#8B0000; width:20px; display:inline-block;">&nbsp;</span> ≥ 18%<br>
#         <span style="background:#FF8C00; width:20px; display:inline-block;">&nbsp;</span> 10–17%<br>
#         <span style="background:#FFFF00; width:20px; display:inline-block;">&nbsp;</span> 2–9%<br>
#         <span style="background:#ADFF2F; width:20px; display:inline-block;">&nbsp;</span> 0–1%<br>
#         <span style="background:#ADD8E6; width:20px; display:inline-block;">&nbsp;</span> -1 to -2%<br>
#         <span style="background:#0000FF; width:20px; display:inline-block;">&nbsp;</span> -3 to -10%<br>
#         <span style="background:#00008B; width:20px; display:inline-block;">&nbsp;</span> < -10%<br>
#     </div>
#     """
#     html(legend_html, height=200)
