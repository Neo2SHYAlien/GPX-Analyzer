import gpxpy
import pandas as pd
from geopy.distance import geodesic

def parse_gpx(gpx_content):
    gpx = gpxpy.parse(gpx_content)
    data = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append({
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "ele": point.elevation,
                    "time": point.time
                })
    df = pd.DataFrame(data)
    df["distance"] = 0.0
    df["grade"] = 0.0
    df["duration_sec"] = 0.0

    for i in range(1, len(df)):
        prev = (df.loc[i - 1, "lat"], df.loc[i - 1, "lon"])
        curr = (df.loc[i, "lat"], df.loc[i, "lon"])
        d = geodesic(prev, curr).meters
        df.loc[i, "distance"] = df.loc[i - 1, "distance"] + d
        elev_diff = df.loc[i, "ele"] - df.loc[i - 1, "ele"]
        df.loc[i, "grade"] = (elev_diff / d) * 100 if d > 0 else 0.0

        # Safe timestamp difference
        if pd.notnull(df.loc[i, "time"]) and pd.notnull(df.loc[i - 1, "time"]):
            df.loc[i, "duration_sec"] = (df.loc[i, "time"] - df.loc[i - 1, "time"]).total_seconds()
        else:
            df.loc[i, "duration_sec"] = 0.0

    stats = {
        "total_distance_km": df["distance"].iloc[-1] / 1000,
        "elevation_gain": df[df["grade"] > 0]["ele"].diff().clip(lower=0).sum(),
        "elevation_loss": -df[df["grade"] < 0]["ele"].diff().clip(upper=0).sum(),
        "min_elevation": df["ele"].min(),
        "max_elevation": df["ele"].max(),
        "average_grade": df["grade"].mean(),
        "max_grade": df["grade"].max(),
        "moving_time_min": df["duration_sec"][df["duration_sec"] < 300].sum() / 60,
        "total_time_min": df["duration_sec"].sum() / 60
    }

    return df, stats
