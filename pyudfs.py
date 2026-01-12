#
# Python Scripts & UDFs
# for usage with xlwings
#
import numpy as np
import pandas as pd
import xlwings as xw

def test():
    wb = xw.Book.caller()
    sht = wb.sheets.active
    sht.range('A1').value = 'Hi from xlwings.'

@xw.func
def hello(name):
    return 'Hello {}.'.format(name)

@xw.func
@xw.arg('x', doc='x is an integer or float.')
def square(x):
    ''' Function that returns the square of x.
    '''
    return x ** 2

@xw.func
@xw.ret(expand='table')
def generate_rnd(rows, cols):
    return np.random.standard_normal((int(rows), int(cols)))

@xw.func
@xw.arg('data', np.ndarray)
def calculate_mean(data):
    return data.mean()

@xw.func
@xw.arg('data', np.ndarray)
def calculate_std(data):
    return data.std()

@xw.func
@xw.arg('data', pd.DataFrame, index=False, header=True)
@xw.ret(expand='table', index=True, header=True)
def calculate_correlations(data):
    return data.corr()

raw = pd.read_csv('http://hilpisch.com/aiif_eikon_eod_data.csv', index_col=0, parse_dates=True).dropna()

@xw.func
@xw.arg('symbols', np.ndarray)
@xw.ret(expand='table')
def retrieve_financial_data(symbols, interval, sta, sto):
    data = raw[symbols].resample(interval, label='right').last()
    data = data[(data.index >= sta) & (data.index <= sto)]
    return data
