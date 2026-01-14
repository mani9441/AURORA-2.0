import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from pathlib import Path
import os


# config
DATA_DIR = Path("data/mines")

# auto-detect mines like MINE_1, MINE_2 ...
mine_ids = sorted([p.name for p in DATA_DIR.iterdir() if p.is_dir()],reverse= 1)


# Side bar
st.sidebar.title("Mine Excavation Monitoring")

mine_id = st.sidebar.selectbox(
    "Select Mine",
    mine_ids
)

# Load mine time series
mine_ts = pd.read_csv(DATA_DIR / mine_id / "mine_timeseries.csv")
mine_ts["date"] = pd.to_datetime(mine_ts["date"])

date_str = st.sidebar.selectbox(
    "Select Date",
    mine_ts["date"].dt.strftime("%Y-%m-%d").tolist()
)

selected_date = pd.to_datetime(date_str)


# Load data
objects = gpd.read_file(DATA_DIR / mine_id / "objects.geojson")
# Load data
objects = gpd.read_file(DATA_DIR / mine_id / "objects.geojson")

# Check if 'date' column exists before conversion
if "date" in objects.columns:
    objects["date"] = pd.to_datetime(objects["date"])
else:
    # Create an empty date column if it's missing to avoid downstream crashes
    st.warning(f"Warning: 'date' column missing in objects.geojson for {mine_id}")
    objects["date"] = pd.Series(dtype='datetime64[ns]')





def safe_read_csv(path, expected_columns):
    """Reads a CSV safely, returning an empty DF with headers if file is empty/missing."""
    if path.exists() and os.path.getsize(path) > 0:
        try:
            df = pd.read_csv(path)
            # Check if headers actually match; if not, return empty with headers
            if df.empty:
                return pd.DataFrame(columns=expected_columns)
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    else:
        # File doesn't exist or is 0 bytes
        return pd.DataFrame(columns=expected_columns)

# Define expected columns for your alerts
alert_cols = ["date", "mine_id", "zone_id", "violation_area_ha", "event_type", "confidence"]
ts_cols = ["date", "total_excavated_area_ha"]

# --- Load data using the safe function ---
alerts_path = DATA_DIR / mine_id / "no_go_alerts.csv"
alerts = safe_read_csv(alerts_path, alert_cols)

mine_ts_path = DATA_DIR / mine_id / "mine_timeseries.csv"
mine_ts = safe_read_csv(mine_ts_path, ts_cols)

# Now convert dates safely
if not alerts.empty and "date" in alerts.columns:
    alerts["date"] = pd.to_datetime(alerts["date"])

if not mine_ts.empty and "date" in mine_ts.columns:
    mine_ts["date"] = pd.to_datetime(mine_ts["date"])




# AOIs
baseline_aoi = gpd.read_file(DATA_DIR / mine_id / "baseline_aoi.geojson")
monitoring_aoi = gpd.read_file(DATA_DIR / mine_id / "monitoring_aoi.geojson")
nogos = gpd.read_file(DATA_DIR / mine_id / "no_go_zones.geojson")


# Force CRS
# Force CRS to EPSG:4326 for folium
objects = objects.to_crs(epsg=4326)
baseline_aoi = baseline_aoi.to_crs(epsg=4326)
monitoring_aoi = monitoring_aoi.to_crs(epsg=4326)
nogos = nogos.to_crs(epsg=4326)




# Excavation Map
st.header("Excavation Map")

# Center map on monitoring AOI
bounds = monitoring_aoi.total_bounds
minx, miny, maxx, maxy = bounds

m = folium.Map(tiles="CartoDB positron")
m.fit_bounds([[miny, minx], [maxy, maxx]])

# ... (after creating the Folium Map 'm') ...

# 1. Baseline AOI Layer (The "Before" state)
folium.GeoJson(
    baseline_aoi,
    name="Baseline Footprint",
    style_function=lambda x: {
        "color": "green",
        "weight": 2,
        "dashArray": "5, 5",
        "fillOpacity": 0.1
    },
    tooltip="Historical Baseline Area"
).add_to(m)

# 2. Monitoring AOI Layer (The "Current" legal boundary)
folium.GeoJson(
    monitoring_aoi,
    name="Monitoring AOI",
    style_function=lambda x: {
        "color": "white",
        "weight": 2,
        "fillOpacity": 0
    }
).add_to(m)


# No-go zones
folium.GeoJson(
    nogos,
    name="No-Go Zones",
    style_function=lambda x: {
        "color": "orange",
        "weight": 2,
        "fillOpacity": 0.3
    }
).add_to(m)

# Excavation objects for selected date
objs_t = objects[objects["date"] == selected_date].copy()

# Convert datetime columns to string for folium
for col in objs_t.columns:
    if pd.api.types.is_datetime64_any_dtype(objs_t[col]):
        objs_t[col] = objs_t[col].astype(str)


if not objs_t.empty:
    folium.GeoJson(
        objs_t,
        name="Excavation Objects",
        style_function=lambda x: {
            "color": "red",
            "weight": 1,
            "fillOpacity": 0.6
        }
    ).add_to(m)
else:
    st.info("No excavation detected on this date.")

folium.LayerControl().add_to(m)

st_folium(m, width=900, height=520)

# comparison table

st.header("Baseline Comparison")
col1, col2 = st.columns(2)

# Calculate areas (Assuming your CRS is metric or you have area columns)
# If your GDF has an 'area_ha' column, use it; otherwise, this is for display
baseline_area = baseline_aoi.area.sum() # Note: Accurate only if CRS is in meters
monitoring_area = monitoring_aoi.area.sum()

with col1:
    st.subheader("Baseline State")
    st.write("Representing the stable mine footprint before monitoring.")
    
    # Check if column exists and has data
    if "area_ha" in baseline_aoi.columns and not baseline_aoi.empty:
        val = f"{baseline_aoi['area_ha'].iloc[0]:.2f} ha"
    else:
        val = "N/A"
        
    st.metric("Baseline Area", val)

with col2:
    st.subheader("Current Monitoring")
    st.write("Representing the active zone under surveillance.")
    
    if "area_ha" in monitoring_aoi.columns and not monitoring_aoi.empty:
        val = f"{monitoring_aoi['area_ha'].iloc[0]:.2f} ha"
    else:
        val = "N/A"
        
    st.metric("Monitoring Area", val)

    

# Mine level activity
st.header("Mine-Level Excavation Activity")

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(
    mine_ts["date"],
    mine_ts["total_excavated_area_ha"],
    marker="o",
    label="Total Excavated Area"
)
ax.set_xlabel("Date")
ax.set_ylabel("Area (ha)")
ax.set_title("Excavated Area Over Time")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# No go zone voilations
st.header("No-Go Zone Violations")

if alerts.empty:
    st.info("No violations detected.")
else:
    st.dataframe(alerts)

    for zone_id, zdf in alerts.groupby("zone_id"):
        st.subheader(f"No-Go Zone: {zone_id}")
        zdf = zdf.sort_values("date")
        st.line_chart(
            zdf.set_index("date")["violation_area_ha"]
        )


# Summary
st.header("Summary")

st.metric(
    "Total Excavated Area (ha)",
    round(mine_ts["total_excavated_area_ha"].max(), 2)
)

st.metric(
    "Total Violation Events",
    len(alerts)
)

st.download_button(
    label="Download No-Go Alert Log (CSV)",
    data=alerts.to_csv(index=False),
    file_name=f"{mine_id}_no_go_alerts.csv",
    mime="text/csv"
)

# 3. Add a legend explanation in the sidebar or main page
st.sidebar.markdown("""
---
**Map Legend:**
- 🟢 **Green Dashed**: Baseline Footprint
- ⚪ **White Solid**: Monitoring Boundary
- 🟠 **Orange Fill**: No-Go Zones
- 🔴 **Red Fill**: New Excavations
""")
