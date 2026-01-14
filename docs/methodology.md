# Methodology

## 1. Feature Representation

For each pixel  at time , a feature vector is constructed to capture both instantaneous state and temporal change:

* **NDVI/NBR:** Capture vegetation health and burn/disturbance ratios.
* **BSI (Bare Soil Index):** Specifically identifies soil exposure in mining contexts.
* **Temporal Features:** Slopes and variances filter out natural phenological cycles (seasons) from abrupt land-clearing events.



## 2. Baseline Learning

A mine-specific model is trained on a "clean" historical period.

* **Statistical Baseline:** Establishes the expected range of spectral values for "normal" land.
* **Baseline Mask:** Identifies pre-existing mining footprints to ensure the system only flags *new* disturbances.


## 3. Temporal Anomaly Scoring

The model computes a deviation score . A high score indicates that the pixel’s current spectral signature significantly contradicts its historical baseline.

> **Note:** This step identifies *spectral change*; it does not yet classify the change as excavation.


## 4. Temporal State Inference

To filter transient noise (shadows, sensor errors), anomaly scores are processed through a state machine:


**Logic Constraints:**

* **State Locking:** A pixel only transitions to "Excavated" if the anomaly persists for  consecutive cloud-free observations.
* **Directionality:** Uses spectral constraints (e.g., NDVI must decrease while BSI increases) to ensure the change is consistent with land clearing.



## 5. Spatial Object Formation

Pixel-level masks are grouped into vector polygons using 8-connectivity labeling.

* **MMU Filtering:** Objects smaller than the Minimum Mapping Unit (0.2 ha) are discarded as salt-and-pepper noise.
* **Temporal Tracking:** Each object is assigned a `start_date` based on its first appearance and a `confidence` score that grows as the object persists over time.



## 6. Aggregation & Violation Detection

* **Mine-Level Metrics:** Cumulative excavated area is calculated by dissolving all objects within the mine boundary.
* **Violation Logic:** Objects are spatially intersected with **No-Go Zones**.
* **Event Semantics:**
* **First Violation:** Initial intersection with a protected zone.
* **Expansion:** Increase in violation area beyond legal mining area.
* **Stabilization:** No significant growth detected over  steps.

