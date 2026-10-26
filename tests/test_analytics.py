from io import StringIO
import pytest
from analytics import load_data, summarize


def test_bundled_data_and_accounting():
    df = load_data()
    assert len(df) == 240
    m = summarize(df)
    assert m['profit'] == pytest.approx(m['revenue'] - df.Operating_Cost_NGN.sum())
    assert df.Occupancy_pct.between(0,100).all()
    assert df.Travel_Date.min().month == 1
    assert df.Travel_Date.max().month == 6


def test_known_metrics():
    df = load_data().iloc[:1].copy()
    df['Total_Revenue_NGN'] = 100
    df['Operating_Cost_NGN'] = 40
    df['Profit_NGN'] = 60
    assert summarize(df)['margin_pct'] == 60
    assert summarize(df.iloc[:0])['revenue'] == 0


@pytest.mark.parametrize('column,value', [('Vehicle_Capacity',0),('Distance_km',0),('Customer_Rating',6),('Passenger_Count',999),('Total_Revenue_NGN',float('inf'))])
def test_invalid_data(column,value):
    df = load_data().iloc[:1].copy()
    df[column] = value
    with pytest.raises(ValueError):
        load_data(StringIO(df.to_csv(index=False)))


def test_missing_schema():
    with pytest.raises(ValueError,match='Missing columns'):
        load_data(StringIO('Trip_ID\na\n'))
