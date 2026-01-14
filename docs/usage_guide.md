# Usage Guide

## Environment Setup

```bash
conda create -n mining python=3.12
conda activate mining
pip install -r requirements.txt
````

---

## Running the Pipeline (Per Mine)

1. Select mine polygon
2. Generate AOIs
3. Download Sentinel-2 data
4. Run pipeline notebooks / scripts in order:

   * baseline
   * anomaly scoring
   * state inference
   * object formation
   * aggregation
   * no-go detection
**OR**
Run FULL PIPELINE notebook


All outputs are saved under:
data/mines/<MINE_ID>/

---

## Running the UI

```bash
cd ui
streamlit run app.py
```

The UI automatically detects available mines and loads precomputed results.

````
