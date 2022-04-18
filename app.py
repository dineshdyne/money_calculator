import streamlit as st
import pandas as pd
import numpy as np
import math
from itertools import *
import streamlit.components.v1 as stc
#from more_itertools import *

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


def emi(p, r, n):
    return p * r * ((1+r)**n)/((1+r)**n - 1)


# #image = Image.open("images/tvs-logo.png")
# #st.sidebar.image(image, use_column_width=False)
st.sidebar.title(f"Investment Calculator")

st.header("Welcome!!!")
calc_type = st.sidebar.selectbox(
    'select type', options=['INVESTMENT', 'REPAYMENT'])
if calc_type == 'INVESTMENT':
    select_tenure = st.slider("select tenure in yrs",
                              min_value=1, max_value=50, value=15, step=1)

    col1, col2 = st.columns([1, 1])
    stop_year = col1.number_input(
        "Investment Stop Year", min_value=0, max_value=select_tenure, step=1, value=select_tenure)
    inflation = col2.number_input(
        "Inflation (yearly) in percentage", min_value=0.0, max_value=14.0, value=5.5, step=0.1)

    monthly_inv = col1.number_input("Monthly inv", min_value=0, value=0)
    lumpsum = col1.number_input("Lumpsum", min_value=0, value=0)
    rate_of_increase = col2.number_input(
        "rate of Increase(yr)", min_value=0.0, max_value=100.0, step=0.1, value=0.0)

    rate_of_return = st.slider(
        "Rate of return", min_value=0.0, max_value=100.0, value=12.0, step=0.5)

    ret = sip(monthly_inv, select_tenure,
              rate_of_return, lumpsum, is_percent=True, inflation_rate=inflation, rate_of_increase=rate_of_increase, stop_year=stop_year)

    final_vals = ret['Amount every month'].iloc[-1].astype(int).to_dict()
    st.write(final_vals)

    st.plotly_chart(px.bar(ret['Amount every month'], y=[
        'invested', 'profit'], width=800, height=600))

    st.write(
        f"The Total : {int(final_vals['total'])} would amount to present day {int(final_vals['total']/((100+inflation)/100)**select_tenure)}")
elif calc_type == "REPAYMENT":
    select_tenure = st.slider("select tenure in yrs",
                              min_value=1, max_value=50, value=4, step=1)
    col1, col2 = st.columns([1, 1])
    loan_amt = col1.number_input(
        "Enter Loan Amt", min_value=0, step=1000, value=0)
    rate_of_interest = col2.slider(
        "Loan rate of interest", min_value=0.05, step=0.05, max_value=30.0)
    inflation = col2.number_input(
        "Inflation (yearly) in percentage", min_value=0.0, max_value=14.0, value=4.0, step=0.1)

    emi_amt = emi(loan_amt, rate_of_interest/1200, select_tenure*12)
    st.write(f"EMI {emi_amt}")
    col1, col2 = st.columns([1, 1])
    extra_payment = col1.number_input(
        "Enter extra payment", min_value=0, step=100)

    rate_of_increment = col2.slider(
        "Rate of increment", min_value=-20.0, step=0.5, value=0.0, max_value=20.0)
    emi_rate_of_increment = col2.slider(
        "EMI Rate of increment", min_value=0.0, step=0.1, value=0.0, max_value=20.0)

    principle = []
    interest = []
    extra = []
    emi_inc = []
    num_months = 0
    inf_invested = 0
    emi_extra = emi_amt
    while loan_amt > 0:
        num_months += 1
        int_comp = loan_amt*rate_of_interest/1200
        princ_comp = emi_amt-int_comp
        if num_months % 12 == 0:
            extra_payment = extra_payment*(1+rate_of_increment/100)
            emi_extra = emi_extra*(1+emi_rate_of_increment/100)
        emi_inc.append(emi_extra-emi_amt)
        inf_invested = inf_invested+(emi_extra+extra_payment) / \
            (1+inflation/1200)**(num_months)
        extra.append(extra_payment)
        #st.write(int_comp, princ_comp)
        loan_amt = loan_amt-(emi_extra-int_comp)-extra_payment
        # st.write(int(loan_amt))
        interest.append(int_comp)
        principle.append(princ_comp)
    st.write(int(loan_amt))
    st.write(f"number of months: {num_months}")

    df = pd.DataFrame(zip(principle,  extra, interest, emi_inc),
                      columns=['principle', 'extra', 'interest', 'emi_inc'])
    st.write(f"total paid :  {int(df.sum().sum())}")
    st.write(f"total paid : inflation adjusted {int(inf_invested)}")

    st.plotly_chart(
        px.bar(df, y=['principle', 'extra', 'interest', 'emi_inc'],
               #color_discrete_sequence=['green', 'blue', 'red', 'cyan']
               ))
