"""Run with: streamlit run app.py"""
import pandas as pd
import plotly.express as px
import streamlit as st
from analytics import load_data, summarize

st.set_page_config(page_title="Nigeria Transport Analytics", page_icon="🚌", layout="wide")
st.title("🚌 Nigeria Transport Analytics")
st.caption("Operations • profitability • service quality | Portfolio demonstration")
st.info("The bundled dataset has undocumented provenance and some implausible route distances. Treat it as demonstration data, not verified Nigerian transport statistics. Profit is revenue minus the supplied operating cost; it is not audited net profit.")
with st.sidebar:
    st.header("Explore trips")
    upload = st.file_uploader("Optional replacement CSV", type=["csv"])
try:
    df = load_data(upload) if upload is not None else load_data()
except (ValueError, TypeError, pd.errors.ParserError, UnicodeError) as error:
    st.error(f"Cannot load dataset: {error}")
    st.stop()
with st.sidebar:
    dates = st.date_input("Travel dates", value=(df.Travel_Date.min().date(), df.Travel_Date.max().date()), min_value=df.Travel_Date.min().date(), max_value=df.Travel_Date.max().date())
    selections = {}
    for col, label in [("Transport_Mode","Transport modes"), ("Origin_City","Origin cities"), ("Destination_City","Destination cities"), ("Trip_Status","Trip status")]:
        selections[col] = st.multiselect(label, sorted(df[col].unique()), help="Leave empty to include all.")
view = df.copy()
if len(dates) == 2:
    view = view[view.Travel_Date.between(pd.Timestamp(dates[0]), pd.Timestamp(dates[1]))]
for col, selected in selections.items():
    if selected:
        view = view[view[col].isin(selected)]
if view.empty:
    st.warning("No trips match these filters. Adjust your selections.")
    st.stop()
st.caption(f"{len(view):,} of {len(df):,} trips • {view.Travel_Date.min():%d %b %Y} – {view.Travel_Date.max():%d %b %Y}")
m = summarize(view)
for col, (label, value) in zip(st.columns(5), [("Trips",f"{m[\"trips\"]:,}"), ("Passengers",f"{m[\"passengers\"]:,}"), ("Revenue",f"₦{m[\"revenue\"]:,.0f}"), ("Operating profit",f"₦{m[\"profit\"]:,.0f}"), ("Average delay",f"{m[\"delay_min\"]:.1f} min")]):
    col.metric(label, value)
overview, operations, data = st.tabs(["Financial overview", "Operations & service", "Trip data"])
with overview:
    monthly = view.groupby(view.Travel_Date.dt.to_period("M"))[["Total_Revenue_NGN","Operating_Cost_NGN","Profit_NGN"]].sum().reset_index()
    monthly["Travel_Date"] = monthly.Travel_Date.astype(str)
    st.plotly_chart(px.line(monthly, x="Travel_Date", y=["Total_Revenue_NGN","Operating_Cost_NGN","Profit_NGN"], markers=True, title="Monthly revenue, cost and operating profit", labels={"value":"NGN","Travel_Date":"Month","variable":"Metric"}), width="stretch")
    routes = view.groupby("Route", as_index=False).agg(Profit_NGN=("Profit_NGN","sum"), Trips=("Trip_ID","count")).sort_values("Profit_NGN",ascending=False)
    st.plotly_chart(px.bar(routes.head(10), x="Profit_NGN", y="Route", orientation="h", title="Top routes by total operating profit", hover_data=["Trips"]), width="stretch")
    st.caption(f"Operating margin: {m[\"margin_pct\"]:.1f}%. Rankings reflect this sample and current filters; route volumes differ.")
with operations:
    a, b = st.columns(2)
    with a:
        delay = view.groupby(["Weather","Road_Condition"], as_index=False).Delay_min.mean()
        st.plotly_chart(px.bar(delay,x="Weather",y="Delay_min",color="Road_Condition",barmode="group",title="Average delay by conditions"),width="stretch")
    with b:
        st.plotly_chart(px.scatter(view,x="Delay_min",y="Customer_Rating",color="Transport_Mode",title="Delay and customer rating"),width="stretch")
    mode = view.groupby("Transport_Mode").agg(Trips=("Trip_ID","count"), Passengers=("Passenger_Count","sum"), Capacity=("Vehicle_Capacity","sum"), Distance_km=("Distance_km","sum"), Fuel_L=("Fuel_Consumed_L","sum"), Profit_NGN=("Profit_NGN","sum"))
    mode["Occupancy_pct"] = 100 * mode.Passengers / mode.Capacity
    mode["Fuel_L_per_100km"] = 100 * mode.Fuel_L / mode.Distance_km
    st.dataframe(mode.round(2),width="stretch")
    st.caption("Occupancy is total passengers / total available seats. Fuel intensity is total litres / total kilometres × 100. Associations do not establish causation.")
with data:
    st.dataframe(view,width="stretch",hide_index=True)
    st.download_button("Download filtered trips",view.to_csv(index=False).encode("utf-8-sig"),"filtered_transport_trips.csv","text/csv")
    st.markdown("Required upload columns: Trip_ID, Travel_Date, Origin_City, Destination_City, Transport_Mode, Weather, Road_Condition, Trip_Status, Distance_km, Fuel_Consumed_L, Passenger_Count, Vehicle_Capacity, Total_Revenue_NGN, Operating_Cost_NGN, Delay_min, Customer_Rating.")
