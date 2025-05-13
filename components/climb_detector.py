import pandas as pd

def detect_significant_segments(df, kind="climb", min_gain=30, min_slope=3, min_length=300):
    segments = []
    in_segment = False
    start_idx = 0
    gain = 0.0
    length = 0.0

    slope_sign = 1 if kind == "climb" else -1

    for i in range(1, len(df)):
        slope = df["plot_grade"].iloc[i]
        elev_diff = df["ele"].iloc[i] - df["ele"].iloc[i - 1]
        dist = df["distance"].iloc[i] - df["distance"].iloc[i - 1]

        is_valid = (slope * slope_sign >= 1)

        if is_valid:
            if not in_segment:
                in_segment = True
                start_idx = i - 1
                gain = 0.0
                length = 0.0

            gain += max(0, elev_diff) if kind == "climb" else max(0, -elev_diff)
            length += dist

        elif in_segment:
            avg_slope = (gain / length) * 100 if length > 0 else 0
            if gain >= min_gain and length >= min_length and avg_slope >= min_slope:
                segments.append({
                    "type": kind,
                    "start_km": df["distance"].iloc[start_idx] / 1000,
                    "end_km": df["distance"].iloc[i] / 1000,
                    "elev_gain" if kind == "climb" else "elev_loss": gain,
                    "length_m": length,
                    "avg_slope": avg_slope * slope_sign,
                    "start_idx": start_idx,
                    "end_idx": i
                })
            in_segment = False

    return pd.DataFrame(segments)
