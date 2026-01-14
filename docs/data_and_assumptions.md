# Data & Assumptions

## Data Sources

* **Sentinel-2 Level-2A:** Bottom-Of-Atmosphere (BOA) reflectance via Copernicus.
* **Legal Mine Boundaries:** Vector polygons defining the permitted operational footprint.
* **No-Go Zones:** Regulatory buffers or ecologically sensitive areas where excavation is strictly prohibited.



## Baseline Assumptions

* **Stability:** The baseline period is assumed to represent the "permitted state" of the mine.
* **Pre-existing Excavation:** Features existing during the baseline are encoded into the model; only **deviations** from this state trigger alerts.
* **Sensitivity:** Detection sensitivity is relative to the variance observed during the baseline period.



## Spatial Resolution Constraints

* **10m Pixel Size:** Detection is optimized for the B02, B03, B04, and B08 bands (10m).
* **Minimum Mapping Unit (MMU):** To mitigate sensor noise and "salt-and-pepper" effects, a minimum object size of **0.2 hectares** is enforced.



## Cloud & Quality Handling

* **SCL Masking:** The Sentinel-2 Scene Classification Layer (SCL) is used to filter clouds and shadows.
* **Temporal Persistence:** New detections must persist across multiple observations (configured via `stable_steps`) to be classified as "Excavation," effectively filtering out transient atmospheric artifacts.


> **Note on Coordinate Systems:** All spatial operations are performed using **WGS84 (EPSG:4326)** for global compatibility, but area calculations are derived from the fixed 10m pixel resolution to ensure metric accuracy.

