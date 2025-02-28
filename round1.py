# Imports

import time
start_time = time.time()

# Using Polars as it's much faster than Pandas
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

df = pl.read_csv("../data/sensor_data.csv")
df

print(df.null_count())
print("Number of Unique Sensor IDs: ", df["sensor_id"].n_unique())

df_with_combined = df.with_columns(
    (pl.col("sensor_reading") + pl.col("control_value")).alias("combined_value")
)

df_with_combined = df_with_combined.drop("sensor_id", "temperature", "pressure", "humidity", "performance_metric", "env_index", "adjusted_sensor")

# Calculate statistics for all columns at once
stats = {
    "mean": df_with_combined.select(pl.mean(df_with_combined.columns)),
    "median": df_with_combined.select(pl.median(df_with_combined.columns)),
    "min": df_with_combined.select(pl.min(df_with_combined.columns)),
    "max": df_with_combined.select(pl.max(df_with_combined.columns)),
    "std": df_with_combined.select(pl.std(df_with_combined.columns))
}

# Create statistics dataframe with proper syntax (list of dictionaries)
stat_df = pl.DataFrame([
    {
        "Reading": "Sensor Readings",
        "Mean": stats["mean"]["sensor_reading"][0],
        "Median": stats["median"]["sensor_reading"][0],
        "Min": stats["min"]["sensor_reading"][0],
        "Max": stats["max"]["sensor_reading"][0],
        "Standard Deviation": stats["std"]["sensor_reading"][0],
    },
    {
        "Reading": "Control Values",
        "Mean": stats["mean"]["control_value"][0],
        "Median": stats["median"]["control_value"][0],
        "Min": stats["min"]["control_value"][0],
        "Max": stats["max"]["control_value"][0],
        "Standard Deviation": stats["std"]["control_value"][0],
    },
    {
        "Reading": "Combined Values",
        "Mean": stats["mean"]["combined_value"][0],
        "Median": stats["median"]["combined_value"][0],
        "Min": stats["min"]["combined_value"][0],
        "Max": stats["max"]["combined_value"][0],
        "Standard Deviation": stats["std"]["combined_value"][0],
    }
])

print(stat_df)

fig = sp.make_subplots(rows=3, cols=1, 
                       subplot_titles=("Sensor Readings", "Control Values", "Combined Values"))

# Add histograms
fig.add_trace(go.Histogram(x=df["sensor_reading"], marker_color='blue'), row=1, col=1)
fig.add_trace(go.Histogram(x=df["control_value"], marker_color='red'), row=2, col=1)
fig.add_trace(go.Histogram(x=df_with_combined["combined_value"], marker_color='green'), row=3, col=1)

fig.update_layout(height=800, width=1200)

fig.write_html("histograms.html")

print("--- Time Taken ---")
print("--- %s seconds ---" % (time.time() - start_time))