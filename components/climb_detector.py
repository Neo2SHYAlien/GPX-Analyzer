import pandas as pd

def detect_climbs(df, min_gain=30, min_slope=3, min_length=300):
    climbs = []
    in_climb = False
    start_idx = 0
    gain = 0.0
    length = 0.0
    dips_allowed = 5  # meters
    temp_gain = 0.0
    temp_length = 0.0

    for i in range(1, len(df)):
        slope = df["plot_grade"].iloc[i]
        elev_diff = df["ele"].iloc[i] - df["ele"].iloc[i - 1]
        dist = df["distance"].iloc[i] - df["distance"].iloc[i - 1]

        if slope >= 1 or (in_climb and (slope > -1 or elev_diff > -dips_allowed)):
            if not in_climb:
                in_climb = True
                start_idx = i - 1
                gain = 0.0
                length = 0.0
            gain += max(0, elev_diff)
            length += dist
        elif in_climb:
            avg_slope = (gain / length) * 100 if length > 0 else 0
            if gain >= min_gain and length >= min_length and avg_slope >= min_slope:
                climbs.append({
                    "start_km": df["distance"].iloc[start_idx] / 1000,
                    "end_km": df["distance"].iloc[i] / 1000,
                    "elev_gain": gain,
                    "length_m": length,
                    "avg_slope": avg_slope,
                    "start_idx": start_idx,
                    "end_idx": i
                })
            in_climb = False

    return pd.DataFrame(climbs)
