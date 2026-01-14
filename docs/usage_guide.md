# Usage Guide

## Environment Setup

```bash
conda create -n mining python=3.12
conda activate mining
pip install -r requirements.txt
```



## Running the Pipeline (Per Mine)

1. **Select Mine:** Define the mine polygon coordinates.
2. **Generate AOIs:** Create baseline and monitoring areas.
3. **Download Data:** Fetch Sentinel-2 imagery for the specified bounds.
4. **Execute Pipeline:** Run notebooks/scripts in the following order:
* `baseline` → `anomaly scoring` → `state inference`
* `object formation` → `aggregation` → `no-go detection`



**OR** run the `FULL_PIPELINE.ipynb` to execute all steps at once.

> **Note:** All outputs are automatically saved to:
> `data/mines/<MINE_ID>/`


## Running the UI

Run the dashboard from the **project root** to ensure data paths resolve correctly:

```bash
streamlit run ui/app.py

```

The UI automatically detects available mines in the `data/mines/` directory and loads precomputed results.

