import gpxpy
import pandas as pd
from geopy.distance import geodesic
import math

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

    for i in range(1, len(df)):
        prev = (df.loc[i - 1, "lat"], df.loc[i - 1, "lon"])
        curr = (df.loc[i, "lat"], df.loc[i, "lon"])
        d = geodesic(prev, curr).meters
        df.loc[i, "distance"] = df.loc[i - 1, "distance"] + d
        elevation_diff = df.loc[i, "ele"] - df.loc[i - 1, "ele"]
        df.loc[i, "grade"] = (elevation_diff / d) * 100 if d > 0 else 0.0

    stats = {
        "total_distance_km": df["distance"].iloc[-1] / 1000,
        "elevation_gain": df[df["grade"] > 0]["ele"].diff().clip(lower=0).sum(),
        "elevation_loss": -df[df["grade"] < 0]["ele"].diff().clip(upper=0).sum(),
        "min_elevation": df["ele"].min(),
        "max_elevation": df["ele"].max()
    }

    return df, stats