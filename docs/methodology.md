# Methodology

## 1. Feature Representation

For each pixel p at time t, a feature vector is constructed:

x(p,t) = [
  NDVI,
  NBR,
  BSI,
  SWIR1,
  SWIR2,
  ΔNDVI,
  ΔNBR,
  NDVI_slope,
  NDVI_variance
]

These features jointly capture vegetation loss, soil exposure, and temporal dynamics.

---

## 2. Baseline Learning

A mine-specific baseline model is trained using historical data assumed to represent normal conditions.

Two baseline products are generated:
- Baseline anomaly model (statistical / reconstruction-based)
- Baseline mining mask (pre-existing excavation)

---

## 3. Temporal Anomaly Scoring

For monitoring data, anomaly scores are computed per pixel and time step as deviation from the baseline model.

This step detects **change**, not excavation.

---

## 4. Temporal State Inference

Anomaly scores are converted into land-state sequences:

S(p,t) ∈ {Normal, Transition, Excavated}

Rules enforced:
- Vegetation decrease + anomaly increase
- Persistence over ≥ k observations

This removes seasonal noise and transient artifacts.

---

## 5. Spatial Object Formation

Binary excavation masks are converted into connected components.
Each object is characterized by:
- Geometry
- Area (ha)
- Start date
- Confidence (temporal persistence)

---

## 6. Aggregation & Violation Detection

- Excavation objects are aggregated over time to compute mine-level metrics.
- Spatial intersection with no-go zones produces violation time series.
- Event semantics (first violation, expansion, stabilization) generate alert logs.
