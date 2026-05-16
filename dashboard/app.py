import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Tesla EV Efficiency Dashboard")

# Load data
df = pd.read_csv("data/tesla_trip_data.csv")

# Create driving type column
df["driving_type"] = df["speed_mph"].apply(
    lambda x: "Highway" if x >= 60 else "City"
)

# Sidebar filters
st.sidebar.header("Filters")

selected_type = st.sidebar.selectbox(
    "Driving Type",
    ["All", "City", "Highway"]
)

min_temp = int(df["outside_temp_f"].min())
max_temp = int(df["outside_temp_f"].max())

selected_temp = st.sidebar.slider(
    "Maximum Temperature",
    min_temp,
    max_temp,
    max_temp
)

# Apply filters
if selected_type != "All":
    filtered_df = df[df["driving_type"] == selected_type]
else:
    filtered_df = df

filtered_df = filtered_df[
    filtered_df["outside_temp_f"] <= selected_temp
]

# Summary metrics
st.header("Summary Metrics")

average_efficiency = filtered_df["wh_per_mile"].mean()
average_speed = filtered_df["speed_mph"].mean()

st.metric("Average Wh/mi", round(average_efficiency, 1))
st.metric("Average Speed", round(average_speed, 1))

# Trip data
st.header("Trip Data")
st.write(filtered_df)

# Efficiency analysis
st.header("Efficiency Analysis")

fig, ax = plt.subplots()

ax.scatter(
    filtered_df["speed_mph"],
    filtered_df["wh_per_mile"]
)

ax.set_xlabel("Speed (mph)")
ax.set_ylabel("Wh/mi")
ax.set_title("Speed vs Efficiency")

st.pyplot(fig)

# Efficiency histogram
st.header("Efficiency Distribution")

fig2, ax2 = plt.subplots()

ax2.hist(filtered_df["wh_per_mile"], bins=5)

ax2.set_xlabel("Wh/mi")
ax2.set_ylabel("Frequency")
ax2.set_title("Efficiency Distribution")

st.pyplot(fig2)

# Engineering findings
st.header("Engineering Findings")

st.write("""
- Higher speeds generally increased Wh/mi.
- Highway driving conditions reduced efficiency.
- HVAC and temperature likely affect energy consumption.
- Elevation gain appears correlated with higher energy usage.
""")