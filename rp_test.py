#
# Test Python Module
# for xlwings & runpython
#
import numpy as np
import pandas as pd
import xlwings as xw

def simple_test():
    wb = xw.Book.caller()
    sht = wb.sheets.active
    sht.range('A1').value = 'RunPython.'

def write_list():
    wb = xw.Book.caller()
    sht = wb.sheets.active
    sht.range('A3').value = list(range(10))

def write_ndarray():
    wb = xw.Book.caller()
    sht = wb.sheets.active
    sht.range('A5').value = np.random.random(8)

def write_rnd():
    wb = xw.Book.caller()
    sht = wb.sheets.active
    rows = int(sht.range('C12').value)
    cols = int(sht.range('D12').value)
    rnd = np.random.randint(0, 100, (rows, cols))
    sht.range('A14').value = rnd

def clear_area():
    wb = xw.Book.caller()
    sht = wb.sheets.active
    sht.range('A14').expand().clear()
