import streamlit as st
import pandas as pd
import numpy as np

from itertools import *
import streamlit.components.v1 as stc
from more_itertools import *

import plotly.express as px
st.set_page_config(  # Alternate names: setup_page, page, layout
    # Can be "centered" or "wide". In the future also "dashboard", etc.
    layout="wide",
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    # String or None. Strings get appended with "• Streamlit".
    page_title=f"Money Manager",
    page_icon=None,  # String, anything supported by st.image, or None.
)


def sip(investment, tenure, interest, amount=0, is_year=True, is_percent=True, inflation_rate=0, rate_of_increase=0, stop_year=None):
    tenure = tenure*12 if is_year else tenure
    interest = interest/100 if is_percent else interest
    interest /= 12
    amount_every_month = []
    invested = amount
    inf_invested = amount
    for month in range(tenure):
        nth_year = month % 12
        if nth_year == 0:
            investment = investment*(100+rate_of_increase)/100
        if stop_year*12 <= month:
            investment = 0
        invested = invested+investment
        inf_invested = inf_invested+investment / \
            (1+inflation_rate/1200)**(month)
        amount = (amount + investment)*(1+interest)
        amount_every_month.append(
            [amount, invested, amount-invested, inf_invested])
    return {'Amount @ Maturity': amount, 'Amount every month': pd.DataFrame(amount_every_month, columns=['total', 'invested', 'profit', 'inflation_adj_invested'])}


# #image = Image.open("images/tvs-logo.png")
# #st.sidebar.image(image, use_column_width=False)
st.sidebar.title(f"Investment Calculator")

st.header("Welcome!!!")
calc_type = st.sidebar.selectbox(
    'select type', options=['INVESTMENT', 'REPAYMENT'])
if calc_type == 'INVESTMENT':
    select_tenure = st.slider("select tenure in yrs",
                              min_value=1, max_value=50, value=4, step=1)
    inflation = st.number_input(
        "Inflation (yearly) in percentage", min_value=0.0, max_value=14.0, value=4.0, step=0.1)

    col1, col2 = st.columns([1, 1])
    lumpsum = col1.number_input("Lumpsum", min_value=0, value=0)
    monthly_inv = col1.number_input("Monthly inv", min_value=0, value=0)
    rate_of_increase = col1.number_input(
        "rate of Increase(yr)", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
    stop_year = col2.number_input(
        "Investment Stop Year", min_value=0, max_value=select_tenure, step=1, value=select_tenure)
    rate_of_return = col1.slider(
        "Rate of return", min_value=0.0, max_value=100.0, value=0.0, step=0.5)

    ret = sip(monthly_inv, select_tenure,
              rate_of_return, lumpsum, is_percent=True, inflation_rate=inflation, rate_of_increase=rate_of_increase, stop_year=stop_year)

    final_vals = ret['Amount every month'].iloc[-1].to_dict()
    col1.write(final_vals)

    col1.plotly_chart(px.bar(ret['Amount every month'], y=[
        'invested', 'profit'], width=600, height=600))

    st.write(
        f"The Total : {int(final_vals['total'])} would amount to present day ఈరోజు {int(final_vals['total']/((100+inflation)/100)**select_tenure)}")
elif calc_type == "REPAYMENT":
    select_tenure = st.slider("select tenure in yrs",
                              min_value=1, max_value=50, value=4, step=1)
    col1, col2 = st.columns([1, 1])
    lumpsum = col1.number_input("Lumpsum", min_value=0, value=0)
