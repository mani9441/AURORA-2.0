# Aurora — Adaptive Mining Excavation Monitoring

![DashBoard](docs/assets/image.png)

**Aurora** is an automated, AI-driven pipeline designed to detect and monitor mining excavation activity using Sentinel-2 multi-spectral imagery. By combining baseline-relative learning with temporal state inference, Aurora distinguishes actual land clearing from seasonal vegetation changes and transient atmospheric noise.

##  Key Features

* **Adaptive Learning:** Learns mine-specific spectral signatures to account for local soil and vegetation types.
* **Temporal State Inference:** Requires persistent observations to confirm excavation, effectively eliminating false positives from cloud shadows or moving machinery.
* **Object-Based Analytics:** Converts pixel-level detections into meaningful "Excavation Patches" with geometry, area, and confidence metrics.
* **Regulatory Guardrails:** Automated spatial intersection with **No-Go Zones** to trigger violation alerts (e.g., encroachment into forest buffers or water bodies).
* **Interactive Dashboard:** A Streamlit-based interface for spatial exploration and temporal trend analysis.



## 🏗 System Architecture

The pipeline processes each mine independently to ensure high localized accuracy:

1. **Data Fetching:** Automated Sentinel-2 Level-2A retrieval via Copernicus.
2. **Feature Extraction:** Calculation of Bare Soil (BSI), Vegetation (NDVI), and Moisture (NBR) indices.
3. **Anomaly Detection:** Statistical deviation analysis against a learned stable baseline.
4. **Spatial Formation:** Connected Component Analysis to vectorize detections into GeoJSON objects.
5. **Alerting:** Logic-based event detection (First Violation, Expansion, Stabilization).



## 📂 Repository Structure

```text
├── /          # Step-by-step pipeline execution
├── base_line_models/          # Pre trained baseline models
├── content/          # content from satellite and mine polygons provided
├── ui/                 # Streamlit dashboard (app.py)
├── data/
│   └── mines/          # Per-mine results (GeoJSON, CSV, Analytics)
├── docs/               # Detailed technical documentation
├── requirements.txt    # Project dependencies
└── README.md           # You are here

```



## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create and activate environment
conda create -n mining python=3.12 -y
conda activate mining

# Install dependencies
pip install -r requirements.txt

```

### 2. Run the Dashboard

To visualize precomputed results for available mines:

```bash
streamlit run ui/app.py

```



## 📖 Detailed Documentation

* **[System Overview](docs/system_overview.md)** — High-level architecture and design principles.
* **[Methodology](docs/methodology.md)** — Spectral indices, state machine logic, and object formation.
* **[Usage Guide](docs/usage_guide.md)** — How to set up new mines and run the processing scripts.
* **[UI Guide](docs/ui_guide.md)** — Navigating the map layers and interpreting alert logs.



## ⚖️ Disclaimer

*This system is intended for monitoring and decision support. Due to the 10m-20m spatial resolution of Sentinel-2, very small excavations or individual vehicles may not be detected. Final regulatory decisions should incorporate high-resolution imagery or field verification.*

