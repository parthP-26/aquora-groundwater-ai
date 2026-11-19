# AQUORA — AI-Based Groundwater Level Prediction & Water-Stress Early Warning System

> **A Decision Support System for Gram Panchayats using Machine Learning and Spatio-Temporal Analytics**  
> *Target Region: Jaipur District, Rajasthan (174 CGWB Monitoring Stations, 2015–2024)*

[![Live Demo](https://img.shields.io/badge/Live%20Platform-AQUORA-blue?style=for-the-badge&logo=googleearth)](index.html)
[![Model Accuracy](https://img.shields.io/badge/Validation%20Accuracy-96.3%25-emerald?style=for-the-badge)](index.html)
[![R2 Score](https://img.shields.io/badge/R%C2%B2%20Score-0.9990-indigo?style=for-the-badge)](index.html)
[![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](LICENSE)

---

## 📌 Project Overview

**AQUORA** is an end-to-end artificial intelligence and geospatial platform designed to empower Gram Panchayats and water resource authorities with actionable, localized groundwater intelligence. 

By fusing physical monitoring well records from the **Central Ground Water Board (CGWB)** with multi-variable climate data from **NASA POWER** (precipitation, temperature, relative humidity, surface pressure, solar radiation, and wind speed), AQUORA forecasts water table trajectories 1 to 3 months ahead, classifies aquifer stress tiers, detects sudden depletion anomalies, and explains the climatic vs. anthropogenic drivers behind water stress using SHAP (Explainable AI).

---

## 🚀 Key Modules & Architecture

```
[ CGWB Well Telemetry ]  +  [ NASA POWER Weather API ]  +  [ India-WRIS Spatial Layers ]
                                    │
                                    ▼
                Module 1: Preprocessing & Feature Engineering
               (Outlier Filtering, Spatial Join, Lag Features)
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
 Module 2: Forecasting      Module 3: Risk Class       Module 4: Anomaly Alert
  (XGBoost / HistGBoost)    (Random Forest / XGBoost)     (Isolation Forest)
  MAE: 0.124m | R²: 0.999    Accuracy: 96.67% | 4 Tiers   109 Depletion Alerts
         └──────────────────────────┬──────────────────────────┘
                                    │
                                    ▼
                     Module 5: Explainable AI (SHAP)
                (Global Feature Importance & Local Attribution)
                                    │
                                    ▼
               Module 6: Interactive GIS Decision Support
           (Enlarged Leaflet Map, Synchronized Index, Predictions Hub)
```

### Module Breakdown:
1. **Module 1 — Data Collection & Preprocessing:**
   - 2,426 quarterly monitoring observations (2015–2024) across 174 spatial wells in Jaipur District.
   - Merged with 15 engineered hydro-meteorological features (precipitation sum, lag depths, rolling means, evaporative stress).
2. **Module 2 — Groundwater Level Forecasting:**
   - Multi-step forward predictions (+30, +60, +90 days ahead).
   - Validated against physical steel-tape CGWB readings: **$R^2 = 0.9990$**, **$\text{MAE} = 0.124\text{m}$**, and **Willmott Index $d = 0.9997$**.
   - $96.3\%$ of holdout test predictions fall within $\pm 0.5\text{m}$ of field ground truth.
3. **Module 3 — Water-Stress Risk Classification:**
   - Classifies aquifers into four operational decision tiers:
     - 🟢 **Safe** ($< 15\text{m}$ depth): 48 wells
     - 🔵 **Moderate** ($15\text{m} - 30\text{m}$ depth): 16 wells
     - 🟠 **High Risk** ($30\text{m} - 50\text{m}$ depth): 41 wells
     - 🔴 **Critical** ($> 50\text{m}$ depth): 69 wells
4. **Module 4 — Anomaly Detection & Early Warning:**
   - Isolation Forest (150 estimators, $5\%$ contamination rate) detecting abnormal drawdown surges ($> 40\text{m}$ depletion or rapid seasonal drop).
5. **Module 5 — Explainable AI (XAI):**
   - SHAP attribution explaining local drivers for Panchayat officers (e.g. separating deficient monsoon recharge from commercial extraction).
6. **Module 6 — GIS Dashboard & Decision Support System:**
   - High-visibility interactive map with 100% synchronized color index and on-map legend.
   - Dedicated Station Forecasting Hub with directional drop indicators and 95% error margin bands.
   - Comprehensive Result Validation suite with scatter calibration and holdout comparison tables.

---

## 🛠️ Technology Stack

- **Machine Learning:** Scikit-Learn, XGBoost, HistGradientBoosting, Isolation Forest
- **Data Engineering:** Python, Pandas, NumPy, Joblib
- **Frontend / Visualization:** HTML5, Tailwind CSS, Leaflet.js, Chart.js, DM Mono & Plus Jakarta Sans typography
- **Server:** Node.js HTTP server / Python HTTP server
- **Deployment:** GitHub Pages, Vercel, Render, Docker

---

## 📂 Repository Structure

```
├── index.html                           # Production portal (root entry for GitHub Pages / Vercel)
├── groundwater_ai_portal.html           # Full compiled interactive AQUORA dashboard
├── build_ronas_dashboard.py             # Dashboard build compiler with synchronized map & index
├── train_groundwater_pipeline.py        # End-to-end ML model training pipeline
├── export_and_verify_saved_models.py    # Serializes and validates .joblib binaries
├── enrich_predictions_and_verification.py # Precomputes holdout verification & SHAP data
├── trained_model_results.json           # Master data payload embedding all metrics & telemetry
├── server_5180.js                       # Local testing server on port 5180
├── trained_models/                      # Serialized ML model binaries
│   ├── xgboost_forecaster.joblib
│   ├── xgboost_forecaster.json
│   ├── random_forest_forecaster.joblib
│   ├── water_stress_classifier.joblib
│   ├── isolation_forest_anomaly.joblib
│   ├── ridge_forecaster.joblib
│   └── model_metadata.json
└── member-1 through 6/                  # Microservice module packages
```

---

## 💻 Local Quickstart

### 1. Run the Interactive Dashboard
To launch the dashboard locally:
```bash
# Using Node.js
node server_5180.js
# Open http://localhost:5180 in your browser

# Or using Python:
python -m http.server 5180
# Open http://localhost:5180/index.html
```

### 2. Retrain Machine Learning Models
```bash
# Run full training and serialization pipeline
python export_and_verify_saved_models.py

# Recompile the interactive portal
python build_ronas_dashboard.py
```

---

## 🌐 How to Push to GitHub & Deploy

### Step 1: Initialize Git and Commit
Open PowerShell or your terminal in this directory and run:
```bash
git init
git add .
git commit -m "feat: initial commit for AQUORA groundwater prediction platform"
git branch -M main
```

### Step 2: Create a New GitHub Repository & Push
1. Go to [github.com/new](https://github.com/new).
2. Name your repository (e.g. `aquora-groundwater-ai` or `aquora`).
3. Leave "Initialize with README" **unchecked**.
4. Click **Create repository**.
5. Push your code using the commands provided by GitHub:
```bash
git remote add origin https://github.com/parthP-26/aquora-groundwater-ai.git
git push -u origin main
```

---

## 🚀 One-Click Deployment Options

### Option A: GitHub Pages (Free, Instant & Zero Configuration)
1. On your GitHub repository page, click **Settings** (top navigation tab).
2. In the left sidebar, click **Pages**.
3. Under **Build and deployment** → **Branch**:
   - Select `main` from the branch dropdown.
   - Select `/ (root)` from the folder dropdown.
4. Click **Save**.
5. Within 30 seconds, your platform will be live at:
   `https://parthP-26.github.io/aquora-groundwater-ai/`

---

### Option B: Deploy to Vercel (Automatic CI/CD)
1. Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click **Add New...** → **Project**.
3. Import your `aquora-groundwater-ai` repository.
4. Framework Preset: Choose **Other**.
5. Root Directory: `./` (leave default).
6. Click **Deploy**.
7. Vercel will automatically detect `index.html` and deploy with global CDN acceleration and custom domains.

---

### Option C: Deploy to Render / Docker
To deploy as a Dockerized web application:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install pandas numpy scikit-learn xgboost joblib
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000"]
```
Connect your GitHub repo to [Render.com](https://render.com) as a **Web Service** or **Static Site**.

---

## 📊 Result Validation Summary

| Metric | Measured Value | Standard Benchmark | Status |
| :--- | :--- | :--- | :--- |
| **Prediction Accuracy ($\pm 0.5\text{m}$)** | **96.3%** | $> 85.0\%$ | ✅ Exceeded |
| **Prediction Accuracy ($\pm 1.0\text{m}$)** | **97.5%** | $> 90.0\%$ | ✅ Exceeded |
| **Mean Absolute Error (MAE)** | **0.124 m** | $< 0.500\text{m}$ | ✅ Exceeded |
| **Coefficient of Determination ($R^2$)** | **0.9990** | $> 0.900$ | ✅ Exceeded |
| **Willmott's Index of Agreement ($d$)** | **0.9997** | $> 0.950$ | ✅ Exceeded |
| **Classification Accuracy (4 Tiers)** | **96.67%** | $> 88.0\%$ | ✅ Exceeded |

---

## 📜 Authors & Citation
- **Project Title:** *AI-Based Groundwater Level Prediction and Water-Stress Early Warning System for Gram Panchayats using Machine Learning and Spatio-Temporal Analytics*
- **Primary Data Sources:** Central Ground Water Board (CGWB), NASA POWER Climate Data API, India-WRIS.
