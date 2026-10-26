# Nigeria Transport Analytics 🚌

An interactive Python dashboard for exploring transport operations, profitability and service quality. Built from the included 240-trip analysis notebook, with reusable analytics, CSV validation and automated tests.

## Run locally

Requires Python 3.11 or 3.12. Run these commands from the project folder:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux instead:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Features

- Date, transport mode, origin, destination and status filters
- Revenue, operating profit, passenger and delay KPIs
- Monthly financial trends and route profitability rankings
- Weather/road delay comparisons, occupancy and fuel intensity
- Validated replacement CSV uploads and filtered CSV downloads
- Original notebook retained for exploratory analysis

## Data and limitations

The supplied CSV contains 240 records, 23 original columns and dates from January 1 through June 27, 2026. Its provenance and redistribution licence were not supplied. Treat it as demonstration data, not independently verified operational evidence. Some city pairs have implausibly short distances. Confirm the data's source and your right to publish it before public redistribution. No open-source licence has been assigned on the owner's behalf.

Revenue is the supplied Total_Revenue_NGN. Operating profit is revenue minus Operating_Cost_NGN; operating margin is total operating profit divided by total revenue. Occupancy uses total passengers divided by total vehicle capacity. Fuel intensity uses total fuel divided by total distance, multiplied by 100. An empty upload/filter result does not produce misleading charts. Route rankings depend on the selected sample; charts show associations, not causal effects or national estimates. This is an analytics application, not a booking, payment or live fleet-tracking service.

## Tests and notebook

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m jupyterlab nigeria_transport_project.ipynb
```

The notebook expects to be run from this folder. Its previous stored outputs have been cleared for reproducibility. GitHub Actions runs the tests on pushes and pull requests.

## Publish to GitHub

Create an empty repository named `nigeria-transport-analytics` in your GitHub account, then run from this folder (replace YOUR_USERNAME):

```bash
git init -b main
git add .
git commit -m "Build Nigeria transport analytics dashboard"
git remote add origin https://github.com/YOUR_USERNAME/nigeria-transport-analytics.git
git push -u origin main
```

If you use GitHub's web upload, extract the ZIP first, then upload this folder's contents. Ensure `.github/workflows/ci.yml` is included if you want CI.

## Deploy an interactive demo

In Streamlit Community Cloud, connect the GitHub repository, select branch `main`, and set the entrypoint to `app.py`. The app reads the bundled CSV relative to its source location; no credentials or external data service are needed. Check current hosting terms and availability when deploying.

## Layout

- `app.py` — Streamlit interface
- `analytics.py` — data validation and summary calculations
- `tests/` — metric, validation and dashboard checks
- `Nigeria_Transport_Analytics_Dataset.csv` — original sample data
- `nigeria_transport_project.ipynb` — original exploration
- `.github/workflows/ci.yml` — automated checks
