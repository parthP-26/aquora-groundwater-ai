# Architecture

Raw CSV → Member 1 validation/cleaning/features → Member 2 forecast artifacts and Member 3 stress/anomaly/alert artifacts → Member 6 SHAP/report artifacts → Member 5 API/PostGIS → Member 4 React/Leaflet dashboard. CSV contracts in `api-contracts/` are the integration boundary.
