# System Overview — Adaptive Mining Excavation Monitoring

## Objective

This system automatically detects, quantifies, and monitors mining excavation activity over time using Sentinel-2 imagery. It identifies and tracks violations occurring inside designated no-go zones.

The system is designed to be:

* **Adaptive**: Mine-specific baseline learning.
* **Robust**: Filters out seasonal variation and atmospheric noise.
* **Scalable**: Handles multiple sites through independent processing.
* **Regulatory-Ready**: Generates audit-ready violation logs.



## High-Level Architecture

The pipeline follows a modular flow from raw data to actionable alerts:

1. **AOI & Data Preparation**: Definition of mine boundaries and retrieval of cloud-masked Sentinel-2 Level-2A data.
2. **Spectral Feature Extraction**: Calculation of vegetation and soil indices (NDVI, BSI, NBR).
3. **Baseline Learning**: Encoding the historical state of the mine site.
4. **Temporal Anomaly Scoring**: Quantifying deviation from the learned baseline.
5. **Temporal State Inference**: Confirming land-clearing through multi-observation persistence.
6. **Spatial Object Formation**: Vectorizing pixel masks into distinct excavation geometries.
7. **Mine-Level & No-Go Zone Analytics**: Calculating area growth and intersecting with protected zones.
8. **Visualization & Reporting**: Rendering results in an interactive dashboard.



## Key Design Principles

### 1. Baseline-Relative Learning

Instead of using fixed global thresholds, the system learns the unique "spectral signature" of a specific mine. This accounts for different soil types, regional vegetation, and lighting conditions.

### 2. Temporal Persistence

To avoid false alarms from moving machinery, temporary shadows, or slight registration errors, a change must be observed across several consecutive timestamps before being labeled as "Excavated."

### 3. Object-Based Reasoning

The pipeline uses **Connected Component Analysis** to turn thousands of pixels into discrete "objects." This allows for the calculation of geometry-specific metrics like compactness and total area (ha).


## Outputs

* **Excavation Maps**: GeoJSON/TIFF layers showing the spatial extent of clearing for every observation date.
* **Mine-Level Time Series**: CSV data tracking cumulative excavation growth (Hectares).
* **Violation Alerts**: Specific event logs (First Violation, Expansion) for No-Go Zones.
* **Interactive Dashboard**: A Streamlit interface for non-technical stakeholders to review temporal and spatial evidence.
