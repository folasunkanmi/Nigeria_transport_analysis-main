# Nigeria Transport Analytics Dashboard

**Interactive Data Analytics Project** | Python • Streamlit • Pandas • Data Visualization

An interactive dashboard that analyses 240 inter-city transport trips across Nigeria. The project helps transport operators understand fuel efficiency, revenue performance, delays, and customer satisfaction — and turn those insights into better operational decisions.

---

## Business Problem

Transport companies in Nigeria operate in a challenging environment with high fuel costs, traffic delays, varying road conditions, and pressure to keep customers satisfied.  
Managers need clear answers to questions such as:

- Which routes and transport modes are most profitable?
- What causes the biggest delays?
- How do weather and road conditions affect performance?
- Where should we focus improvement efforts to increase revenue and customer ratings?

This project provides an interactive tool that answers these questions using real operational-style data.

---

## What This Project Delivers

### Interactive Streamlit Dashboard
- Filter by date, transport mode, origin, destination, and status
- Key Performance Indicators (KPIs): Revenue, Operating Profit, Passengers, Average Delay
- Monthly financial trends
- Route profitability rankings
- Weather & road condition impact on delays
- Occupancy rates and fuel intensity analysis
- Ability to upload a new CSV and download filtered results

### Supporting Analysis
- Original Jupyter Notebook for exploratory data analysis
- Clean, reusable analytics functions
- Automated tests for data validation and metrics

---

## Key Insights from the Data

- **Lagos routes** generate the highest total revenue.
- **Delays** increase significantly during Evening Peak hours and on poor road conditions.
- Customer satisfaction drops sharply when delays exceed **15 minutes**.
- BRT and high-capacity modes carry more passengers but have higher fuel consumption.
- Weather and road quality are strong drivers of operational performance.

---

## Business Recommendations

1. **Prioritise road quality** on high-delay corridors to reduce late arrivals.
2. **Add buffer time or extra capacity** during Evening Peak periods.
3. **Focus commercial attention** on high-revenue Lagos routes.
4. **Set a clear service target**: keep average delays under 15 minutes to protect customer ratings.
5. **Monitor fuel intensity** regularly, especially for high-volume transport modes.

---

## How to Run the Dashboard

```bash
git clone https://github.com/folasunkanmi/Nigeria_transport_analysis-main.git
cd Nigeria_transport_analysis-main

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

---

## Project Structure

```
Nigeria_transport_analysis-main/
├── app.py                              # Streamlit dashboard
├── analytics.py                        # Core calculations & validation
├── nigeria_transport_project.ipynb     # Exploratory analysis notebook
├── Nigeria_Transport_Analytics_Dataset.csv
├── requirements.txt
├── tests/                              # Automated tests
└── .github/workflows/                  # CI checks
```

---

## Tools & Skills Demonstrated

- Python & Pandas
- Streamlit (interactive dashboards)
- Data cleaning & validation
- Exploratory Data Analysis
- Business-oriented insights & recommendations
- Testing and reproducible workflows

---

## Author

**Folasunkanmi**  
Data Analyst & Aspiring Data Scientist  
Skills: Python • SQL • Excel • Power BI • Machine Learning • Streamlit  
GitHub: [folasunkanmi](https://github.com/folasunkanmi)

---

This project shows the ability to build not just analysis, but a practical tool that decision-makers can actually use.
