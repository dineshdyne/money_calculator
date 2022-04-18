
# importing libraries
import os
import io
import re
import gc
import sys
import copy
import json
import math
import time
import base64
import urllib
import inspect
import numpy as np
import pandas as pd

from operator import *
from itertools import *
from functools import *
from statistics import *
from collections import *
#from matplotlib_venn import *

# from pandas.plotting import *
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


gc.collect()

print("Hello world!")


amount = float(input("Enter the monthly SIP amount: "))
yearlyRate = float(input("Enter the yearly rate of return: "))
years = int(input("Enter the number of years: "))
monthlyRate = yearlyRate/12/100
months = years * 12
futureValue = amount * ((((1 + monthlyRate)**(months))-1)
                        * (1 + monthlyRate))/monthlyRate
futureValue = round(futureValue)
print("The expected amount you will get is:", futureValue)


def sip(investment, tenure, interest, amount=0, is_year=True, is_percent=True, show_amount_list=False):
    tenure = tenure*12 if is_year else tenure
    interest = interest/100 if is_percent else interest
    interest /= 12
    amount_every_month = {}
    for month in range(tenure):
        amount = (amount + investment)*(1+interest)
        amount_every_month[month+1] = amount
    return {'Amount @ Maturity': amount, 'Amount every month': amount_every_month} if show_amount_list else {'Amount @ Maturity': amount}
