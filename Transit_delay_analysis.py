import pandas as pd
from datetime import timedelta

# -------------------------------
# Step 1: Load GPS and Event Data
# -------------------------------

gps_df = pd.read_csv("final_gps_with_100_records_and_delays.csv")
events_df = pd.read_csv("final_road_events_for_100_records.csv")

# Convert Timestamp columns to datetime
gps_df["Timestamp"] = pd.to_datetime(gps_df["Timestamp"])
events_df["Timestamp"] = pd.to_datetime(events_df["Timestamp"])

# -------------------------------
# Step 2: Sort & Calculate Time Gaps
# -------------------------------

# Sort by Bus ID and Timestamp
gps_df.sort_values(by=["Bus_ID", "Timestamp"], inplace=True)

# Calculate time difference between GPS pings
gps_df["Time_Diff_Min"] = gps_df.groupby("Bus_ID")["Timestamp"].diff().dt.total_seconds() / 60

# -------------------------------
# Step 3: Flag Delays (>7 minutes)
# -------------------------------

gps_df["Is_Delayed"] = gps_df["Time_Diff_Min"] > 7

# Filter for delay records only
delays_df = gps_df[gps_df["Is_Delayed"]].copy()

# -------------------------------
# Step 4: Match Delays to Nearby Events
# -------------------------------

def find_nearby_event(delay_row, events_df):
    # Time window = ±5 min; spatial range ≈ 150 meters
    time_window = timedelta(minutes=5)
    lat_margin = 0.0015
    lon_margin = 0.0015

    # Filter events within time and space window
    nearby_events = events_df[
        (events_df["Timestamp"] >= delay_row["Timestamp"] - time_window) &
        (events_df["Timestamp"] <= delay_row["Timestamp"] + time_window) &
        (abs(events_df["Latitude"] - delay_row["Latitude"]) <= lat_margin) &
        (abs(events_df["Longitude"] - delay_row["Longitude"]) <= lon_margin)
    ]

    if not nearby_events.empty:
        return " | ".join(nearby_events["Event_Type"].unique())
    else:
        return "No Event Nearby"

# Apply function to each delayed row
delays_df["Nearby_Event"] = delays_df.apply(lambda row: find_nearby_event(row, events_df), axis=1)

# -------------------------------
# Step 5: Save Output
# -------------------------------

delays_df.to_csv("bus_delays_with_root_causes.csv", index=False)
print("✅ Analysis complete. Output saved to 'bus_delays_with_root_causes.csv'")
