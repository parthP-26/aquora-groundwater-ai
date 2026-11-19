# AI-Based Groundwater Level Prediction and Water-Stress Early Warning System

Research and decision-support prototype for six-hourly station telemetry observations in Jaipur, Rajasthan. It predicts the next available station observation; it does not claim administrative-area forecasting and is not an official warning system.

## Dataset actually inspected

`gwl_tel_6_hourly_rajasthan_gw_rj_2021_2025.csv` is processed by filtering the actual `District` field to `JAIPUR`. The current processed data contains 114,296 valid records from 109 stations, from 2021-01-01 through 2025-12-31. The pipeline explicitly removes 449 `-999` sentinel readings and 286 rows missing required fields, recording both counts in the quality report.

## Quick start

```powershell
$env:GROUNDWATER_RAW_PATH='C:\path\to\ccf99842-1e29-4ea0-bd2a-0f1c6b7f7669.csv'
cd member-1-data-engineering; python scripts/run_data_pipeline.py
cd ../member-2-groundwater-prediction; python scripts/train_forecasting_models.py
cd ../member-3-water-stress-alerts; python scripts/run_stress_pipeline.py
cd ../member-6-explainability-decision-support; python scripts/generate_explanations.py; python scripts/generate_reports.py
cd ../member-5-backend-database; python scripts/load_processed_data.py; uvicorn backend.main:app --reload --port 8000
cd ../member-4-gis-frontend; npm install; npm run dev
```

Backend: http://localhost:8000 · Swagger: http://localhost:8000/docs · frontend: http://localhost:5173.

See `docs/` and each repository README for independent setup, validation, deployment, and handoff instructions.
