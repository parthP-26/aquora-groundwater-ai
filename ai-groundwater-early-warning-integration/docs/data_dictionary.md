# Data dictionary

Telemetry source fields: `Station` (station identifier), `Data Acquisition Time` (six-hourly telemetry timestamp), `Groundwater Level Telemetry 6 Hourly (meter)` (groundwater measurement in metres), `Latitude`, `Longitude`, `District`, `Tehsil`, `Block`, and `Village`. The pipeline filters `District` to `JAIPUR`, treats values at or below `-900` as invalid sentinel values, and creates canonical `location_id`, `observation_date`, and `groundwater_level` fields.
