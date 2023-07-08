import streamlit as st
import pandas as pd
import numpy as np
import math
from itertools import *
import streamlit.components.v1 as stc
from funcs import *
import locale
#locale.setlocale(locale.LC_MONETARY, 'en_IN')

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




# #image = Image.open("images/tvs-logo.png")
# #st.sidebar.image(image, use_column_width=False)
st.sidebar.title(f"Financial Calculator")

st.markdown(f"""<h1 style="text-align:center">Welcome!!!</h1>""",unsafe_allow_html=True)


calc_type = st.sidebar.selectbox('select type', options=['INVESTMENT', 'REPAYMENT'])
if calc_type == 'INVESTMENT':
    

    col1, col2 = st.columns([1, 3])
    lumpsum = col1.number_input("Lumpsum", min_value=0, value=0)
    select_tenure = col2.slider("Select tenure in years",
                              min_value=1, max_value=50, value=15, step=1)
    col1, col2 = st.columns([1, 1])

    monthly_inv = col1.number_input(
        "Monthly inv", min_value=0, value=5000, step=100)
    
    rate_of_increase = col2.slider(
        "Rate of Increment(yearly)", min_value=0.0, max_value=100.0, step=0.1, value=0.0)

    col1, col2 = st.columns([1, 1])
    stop_year = col1.number_input(
        "Investment Closing Year", min_value=0, max_value=select_tenure, step=1, value=select_tenure)
    inflation = col2.number_input(
        "Inflation rate(yearly)", min_value=0.0, max_value=14.0, value=6.0, step=0.1)

    col1, col2,col3 = st.columns([1,4,1])
    rate_of_return = col2.slider(
        "Expected Rate of Return", min_value=0.0, max_value=100.0, value=12.0, step=0.5)

    ret = sip(monthly_inv, select_tenure,
              rate_of_return, lumpsum, is_percent=True, inflation_rate=inflation, rate_of_increase=rate_of_increase, stop_year=stop_year)

    final_vals = ret['Amount every month'].iloc[-1].astype(int)  # .to_dict()

    final_vals = final_vals.to_dict()

    col1,col2,col3,col4 =st.columns([1,1.5,1.5,1.5])

    col2.metric("Invested Amt",formatINR(final_vals["invested"]) )
    col3.metric("Ending Market Value",formatINR(final_vals['total']))
    col4.metric("Net Gain",formatINR(final_vals["profit"]))

    col1,col2,col3 =st.columns([1,1.8,1.8])
    col2.metric("Investment (Inflation Adjusted)", formatINR(final_vals["inflation_adj_invested"]))
    col3.metric("End Value (Inflation Adjusted)",formatINR(final_vals['total']/((100+inflation)/100)**select_tenure))
    #st.write(final_vals)
    st.plotly_chart(px.bar(ret['Amount every month'], y=[
        'invested', 'profit']), use_container_width=True)

    # st.markdown(
    #     f"""Total : <span style="color:green">{int(final_vals['total'])}</span>""", unsafe_allow_html=True)
    # st.write(
    #     f"""Equivalent to Present day: <span style="color:green">{int(final_vals['total']/((100+inflation)/100)**select_tenure)}</span>""", unsafe_allow_html=True)
elif calc_type == "REPAYMENT":
    
    col1, col2 = st.columns([1, 3])
    loan_amt = col1.number_input(
        "Enter Loan Amt", min_value=0, step=1000, value=0)
    select_tenure = col2.slider("Loan Term (in years)",
                              min_value=1, max_value=50, value=20, step=1)

    rate1,rate2=st.columns([1,1])
    rate_of_interest = rate1.slider(
        "Loan Interest Rate", min_value=0.05, value=8.0, step=0.05, max_value=30.0)
    inflation = rate2.number_input(
        "Inflation Rate", min_value=0.0, max_value=14.0, value=6.0, step=0.1)

    emi_amt = emi(loan_amt, rate_of_interest/1200, select_tenure*12)

    col1,col2,col3=st.columns([1,3.6,1])
    col_x,col_y=col2.columns([1,1])
    #col1,col2,col3,col4=st.columns([1,1.8,1.8,1],gap="medium")

    col_x.metric("EMI",formatINR( emi_amt, grouping=True),f"yearly: {formatINR(emi_amt*12, grouping=True)}","inverse")

    
    # st.markdown(
    #     f"""EMI : <span style="color:green">{emi_amt}</span>""", unsafe_allow_html=True)

    extra_payment = col_x.number_input(
        "Extra Monthly Repayment", min_value=0, step=100)

    col_y.metric("Interest Rate",rate_of_interest ,f"{rate_of_interest-inflation:.2f} from Inflation","inverse")
    rate_of_increment = col_y.slider(
        "Rate of increment", min_value=-20.0, step=0.5, value=0.0, max_value=20.0)

    emi_rate_of_increment = col2.slider(
        ">Increase EMI (yearly rate)", min_value=0.0, step=0.1, value=0.0, max_value=20.0)
    
    principle = []
    interest = []
    extra = []
    emi_inc = []
    num_months = 0
    inf_invested = 0
    emi_extra = emi_amt
    loan_amt_col=[]
    
    # import time
    # my_bar = st.progress(0, text="Running calculations")
    while (loan_amt > 0.1):
        
        
        num_months += 1
        # time.sleep(.01)
        # my_bar.progress(num_months,text="Running calculations")
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
        loan_amt_col.append(loan_amt)
    # st.write(int(loan_amt))
    df = pd.DataFrame(zip(principle,  extra, interest, emi_inc),
                      columns=['Principle', 'Extra_Repayment', 'Interest', 'EMI_increment'])
    # making sure all values are not zero in a col
    df = df.loc[:, (df != 0).any(axis=0)]


    col0,col1,col2,col3=st.columns([1,1.8,1.8,2])

    col1.metric("Months of Repayment",str(num_months),f"years saved:{select_tenure-num_months/12:.2f}")
    savings=formatINR(emi_amt*select_tenure*12-df.sum().sum(), grouping=True)

    col2.metric("Total Repayment.",formatINR( df.sum().sum(), grouping=True),f"savings: {savings}")
    col3.metric("Total repayment(inflation Adjusted)",formatINR( inf_invested, grouping=True))
    # st.markdown(
    #     f"""Number of Months: <span style="color: green">{num_months}</span>""", unsafe_allow_html=True)

    # st.markdown(
    #     f"""Total Paid :  <span style="color:green">{int(df.sum().sum())}</span>""", unsafe_allow_html=True)
    # st.markdown(
    #     f"""Total Paid : Inflation Adjusted <span style="color:green">{int(inf_invested)}</span>""", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; '>Chart Representation</h2>", unsafe_allow_html=True)
    st.plotly_chart(
        px.bar(df, y=list(df.columns),labels={"index":'Months',"value":"Monthly Payments"}
               #color_discrete_sequence=['green', 'blue', 'red', 'cyan']
               ), use_container_width=True)
    

