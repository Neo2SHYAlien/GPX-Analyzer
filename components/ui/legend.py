from streamlit.components.v1 import html


def display_legend() -> None:
    legend_html = """
    <div style='padding:10px; background:white; border-radius:8px; font-size:14px;
                box-shadow: 0 0 8px rgba(0,0,0,0.2); width: fit-content;'>
        <b>Legend: Gradient (%)</b><br>
        <div><span style='background:#8B0000; width:20px; display:inline-block;'>&nbsp;</span> ≥ 18%</div>
        <div><span style='background:#FF8C00; width:20px; display:inline-block;'>&nbsp;</span> 10–17%</div>
        <div><span style='background:#FFFF00; width:20px; display:inline-block;'>&nbsp;</span> 2–9%</div>
        <div><span style='background:#ADFF2F; width:20px; display:inline-block;'>&nbsp;</span> 0–1%</div>
        <div><span style='background:#ADD8E6; width:20px; display:inline-block;'>&nbsp;</span> -1 to -2%</div>
        <div><span style='background:#0000FF; width:20px; display:inline-block;'>&nbsp;</span> -3 to -10%</div>
        <div><span style='background:#00008B; width:20px; display:inline-block;'>&nbsp;</span> < -10%</div>
    </div>
    """
    html(legend_html, height=230)
