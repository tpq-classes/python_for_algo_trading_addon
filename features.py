#
# Preparing & Using Financial Features
# for OLS Regression and Machine Learning
#
import q
import numpy as np
import pandas as pd
from IPython import embed


class FinancialData:
    url = 'https://hilpisch.com/pyalgo_eikon_eod_data.csv'
    def __init__(self, symbol, feature, lags):
        self.symbol = symbol
        self.feature = feature
        self.lags = lags
        self.retrieve_data()
        self.prepare_data()
    def retrieve_data(self):
        self.raw = pd.read_csv(self.url, index_col=0,
                               parse_dates=True)
    def prepare_data(self):
        self.cols = list()
        self.data = pd.DataFrame(self.raw[self.symbol]).dropna()
        self.data['r'] = np.log(self.data / self.data.shift(1))
        for lag in range(1, self.lags + 1):
            col = f'lag_{lag}'
            self.data[col] = self.data[self.feature].shift(lag)
            self.cols.append(col)
        self.data.dropna(inplace=True)


if __name__ == '__main__':
    fd = FinancialData('.SPX', 'r', 3)
    embed()
    # q.d()
    print(fd.raw.tail())
    print(fd.data.head())
