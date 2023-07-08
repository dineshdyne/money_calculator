
import pandas as pd

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
    return {'Amount @ Maturity': amount,
            'Amount every month': pd.DataFrame(amount_every_month, columns=['total', 'invested', 'profit', 'inflation_adj_invested'])}

def emi(p, r, n):
    return p * r * ((1+r)**n)/((1+r)**n - 1)


def formatINR(number,**kwargs):
    number = float(number)
    number = round(number,2)
    is_negative = number < 0
    number = abs(number)
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    value = "".join([r] + d)
    if is_negative:
       value = '-' + value
    return '₹'+ value



