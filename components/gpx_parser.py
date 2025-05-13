import gpxpy
import pandas as pd
from geopy.distance import geodesic

def reduce_points_by_density(df, max_points_per_km=20):
    total_km = df["distance"].iloc[-1] / 1000
    max_points = int(total_km * max_points_per_km)
    if len(df) <= max_points:
        return df  # no need to reduce
    step = max(1, int(len(df) / max_points))
    reduced_df = df.iloc[::step].reset_index(drop=True)
    return reduced_df

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

    # Step 1: calculate rough distance to apply density reduction
    df["distance"] = 0.0
    for i in range(1, len(df)):
        prev = (df.loc[i - 1, "lat"], df.loc[i - 1, "lon"])
        curr = (df.loc[i, "lat"], df.loc[i, "lon"])
        df.loc[i, "distance"] = df.loc[i - 1, "distance"] + geodesic(prev, curr).meters

    # Step 2: reduce to max X points per km
    df = reduce_points_by_density(df, max_points_per_km=20)

    # Step 3: calculate slope and time
    df["grade"] = 0.0
    df["duration_sec"] = 0.0
    for i in range(1, len(df)):
        prev = (df.loc[i - 1, "lat"], df.loc[i - 1, "lon"])
        curr = (df.loc[i, "lat"], df.loc[i, "lon"])
        d = geodesic(prev, curr).meters
        elev_diff = df.loc[i, "ele"] - df.loc[i - 1, "ele"]
        df.loc[i, "grade"] = (elev_diff / d) * 100 if d > 0 else 0.0

        if pd.notnull(df.loc[i, "time"]) and pd.notnull(df.loc[i - 1, "time"]):
            df.loc[i, "duration_sec"] = (df.loc[i, "time"] - df.loc[i - 1, "time"]).total_seconds()
        else:
            df.loc[i, "duration_sec"] = 0.0

    total_distance = df["distance"].iloc[-1]
    num_points = len(df)
    point_density_per_km = num_points / (total_distance / 1000) if total_distance > 0 else 0
    point_density_per_100m = num_points / (total_distance / 100) if total_distance > 0 else 0

    stats = {
        "total_distance_km": total_distance / 1000,
        "elevation_gain": df[df["grade"] > 0]["ele"].diff().clip(lower=0).sum(),
        "elevation_loss": -df[df["grade"] < 0]["ele"].diff().clip(upper=0).sum(),
        "min_elevation": df["ele"].min(),
        "max_elevation": df["ele"].max(),
        "average_grade": df["grade"].mean(),
        "max_grade": df["grade"].max(),
        "moving_time_min": df["duration_sec"][df["duration_sec"] < 300].sum() / 60,
        "total_time_min": df["duration_sec"].sum() / 60,
        "num_points": len(df),
        "point_density_km": point_density_per_km,
        "point_density_100m": point_density_per_100m,
        "precision_score": min(100.0, (point_density_per_km / 20) * 100)
    }

    return df, stats
