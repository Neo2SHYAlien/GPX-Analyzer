def get_color(grade):
    if grade >= 18:
        return "#8B0000"
    elif grade >= 10:
        return "#FF8C00"
    elif grade >= 2:
        return "#FFFF00"
    elif grade >= 0:
        return "#ADFF2F"
    elif grade >= -2:
        return "#ADD8E6"
    elif grade >= -10:
        return "#0000FF"
    else:
        return "#00008B"

def apply_slope_smoothing(df, target_meters=300):
    meters_per_point = df["distance"].iloc[-1] / len(df)
    window = max(3, int(target_meters / meters_per_point))
    df["plot_grade"] = df["grade"].rolling(window=window, center=True).mean().bfill().ffill()
    return df