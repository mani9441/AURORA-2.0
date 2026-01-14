# System Overview — Adaptive Mining Excavation Monitoring

## Objective
This system automatically detects, quantifies, and monitors mining excavation activity over time using Sentinel-2 imagery. It further identifies and tracks violations occurring inside designated no-go zones.

The system is designed to be:
- Adaptive (mine-specific learning)
- Robust to seasonal variation
- Scalable across multiple mines
- Suitable for regulatory monitoring

---

## High-Level Architecture

The pipeline consists of eight stages:

1. AOI & Data Preparation  
2. Spectral Feature Extraction  
3. Baseline Learning  
4. Temporal Anomaly Scoring  
5. Temporal State Inference  
6. Spatial Object Formation  
7. Mine-Level & No-Go Zone Analytics  
8. Visualization & Reporting

Each mine is processed independently, enabling adaptive learning without global thresholds.

---

## Key Design Principles

- **Baseline-relative learning**: All change detection is relative to a mine-specific baseline.
- **Temporal persistence**: Excavation is detected only when changes persist across time.
- **Object-based reasoning**: Pixel-level noise is aggregated into meaningful excavation patches.
- **Separation of concerns**: Detection, aggregation, and visualization are decoupled.

---

## Outputs

- Excavation maps per date
- Mine-level excavation time series
- No-go zone violation alerts
- Interactive visualization dashboard
