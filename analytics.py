"""Validated loading and reproducible transport metrics."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).with_name("Nigeria_Transport_Analytics_Dataset.csv")
DIMENSIONS = ["Origin_City", "Destination_City", "Transport_Mode", "Weather", "Road_Condition", "Trip_Status"]
NUMERIC = ["Distance_km", "Fuel_Consumed_L", "Passenger_Count", "Vehicle_Capacity",
           "Total_Revenue_NGN", "Operating_Cost_NGN", "Delay_min", "Customer_Rating"]

def load_data(source=DATA_PATH):
    df = pd.read_csv(source)
    required = ["Trip_ID", "Travel_Date", *DIMENSIONS, *NUMERIC]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    if df.empty:
        raise ValueError("Dataset must contain at least one trip.")
    if df[required].isna().any().any():
        raise ValueError("Required fields contain missing values.")
    df["Travel_Date"] = pd.to_datetime(df["Travel_Date"], errors="raise")
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col], errors="raise")
    import numpy as np
    if not np.isfinite(df[NUMERIC].to_numpy()).all():
        raise ValueError("Numeric fields must be finite.")
    if df["Trip_ID"].duplicated().any():
        raise ValueError("Trip_ID must be unique.")
    if (df[NUMERIC] < 0).any().any():
        raise ValueError("Numeric fields must be nonnegative.")
    if (df[["Distance_km", "Vehicle_Capacity"]] <= 0).any().any():
        raise ValueError("Distance and vehicle capacity must be positive.")
    if (df.Passenger_Count > df.Vehicle_Capacity).any() or (df.Customer_Rating > 5).any():
        raise ValueError("Passengers exceed capacity or rating exceeds 5.")
    df["Profit_NGN"] = df.Total_Revenue_NGN - df.Operating_Cost_NGN
    df["Occupancy_pct"] = 100 * df.Passenger_Count / df.Vehicle_Capacity
    df["Fuel_L_per_100km"] = 100 * df.Fuel_Consumed_L / df.Distance_km
    df["Route"] = df.Origin_City + " → " + df.Destination_City
    return df


def summarize(df):
    revenue = float(df.Total_Revenue_NGN.sum())
    profit = float(df.Profit_NGN.sum())
    return dict(trips=len(df), passengers=int(df.Passenger_Count.sum()), revenue=revenue,
                profit=profit, margin_pct=100 * profit / revenue if revenue else 0,
                delay_min=float(df.Delay_min.mean()) if len(df) else 0,
                occupancy_pct=100 * df.Passenger_Count.sum() / df.Vehicle_Capacity.sum() if len(df) else 0)
