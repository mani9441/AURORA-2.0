# Data & Assumptions

## Data Sources

- Sentinel-2 Level-2A (Copernicus)
- Legal mine boundary polygons
- No-go zone polygons (synthetic / regulatory buffers)

---

## Baseline Assumptions

- The baseline period represents stable mining conditions.
- Pre-existing excavation may be present but is treated as normal.
- Major new excavation during baseline may reduce sensitivity.

---

## Spatial Resolution Constraints

- Sentinel-2 resolution (10–20 m) limits detection of very small excavations.
- Object-level filtering mitigates pixel noise.

---

## Cloud Handling

- Basic cloud masking is applied.
- Persistent cloud cover may delay detection but does not cause false alerts.
