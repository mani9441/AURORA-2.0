# Aurora — Adaptive Mining Excavation Monitoring

Aurora is an AI-driven system for detecting and monitoring mining excavation activity using Sentinel-2 imagery. It identifies new excavation, quantifies expansion over time, and detects violations inside designated no-go zones.

---

## Key Features

- Adaptive, mine-specific learning
- Robust to seasonal vegetation changes
- Object-based excavation detection
- Automated no-go zone violation alerts
- Interactive web-based dashboard

---

## Repository Structure

- / — data processing & analytics
- ui/ — Streamlit visualization dashboard
- data/ — per-mine outputs
- docs/ — system and usage documentation

---

## Quick Start

```bash
conda activate mining
streamlit run ui/app.py
````

---

## Documentation

* System Overview: docs/system_overview.md
* Methodology: docs/methodology.md
* Usage Guide: docs/usage_guide.md
* UI Guide: docs/ui_guide.md

---

## Disclaimer

This system is intended for monitoring and decision support. Final regulatory decisions should incorporate field verification.





