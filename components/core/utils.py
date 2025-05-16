import pandas as pd

def get_color(grade):
    if grade >= 18:
        return "#8B0000"   # Dark Red
    elif grade >= 10:
        return "#FF8C00"   # Dark Orange
    elif grade >= 2:
        return "#FFFF00"   # Yellow
    elif grade >= 0:
        return "#ADFF2F"   # GreenYellow
    elif grade >= -2:
        return "#ADD8E6"   # LightBlue
    elif grade >= -10:
        return "#0000FF"   # Blue
    else:
        return "#00008B"   # Dark Blue

def apply_slope_smoothing(df, target_meters=300):
    meters_per_point = df["distance"].iloc[-1] / len(df)
    window = max(3, int(target_meters / meters_per_point))
    df["plot_grade"] = df["grade"].rolling(window=window, center=True).mean().bfill().ffill()
    return df

def classify_climb_category(length_m, avg_slope):
    length_km = length_m / 1000
    if length_km >= 10 and avg_slope >= 6:
        return "Hors Catégorie"
    elif length_km >= 8 and avg_slope >= 5:
        return "Category 1"
    elif length_km >= 5 and avg_slope >= 4:
        return "Category 2"
    elif length_km >= 3 and avg_slope >= 3:
        return "Category 3"
    elif length_km >= 2 and avg_slope >= 3:
        return "Category 4"
    elif length_km >= 1 and avg_slope >= 2:
        return "Category 5"
    elif length_km >= 0.5 and avg_slope >= 1:
        return "Category 6"
    else:
        return "Uncategorized"
