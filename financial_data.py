#
# Simple Financial Data Class
#
import pandas as pd

class FinancialData:
    url = 'https://hilpisch.com/pyalgo_eikon_eod_data.csv'
    def __init__(self, symbol):
        self.symbol = symbol
        self.retrieve_data()
        self.prepare_data()
    def retrieve_data(self):
        self.raw = pd.read_csv(self.url, index_col=0,
                               parse_dates=True)
    def prepare_data(self):
        self.data = pd.DataFrame(self.raw[self.symbol]).dropna()
        self.data['SMA'] = self.data[self.symbol].rolling(100).mean()
    def plot_data(self, cols=None):
        if cols is None:
            cols = [self.symbol]
        self.data[cols].plot(figsize=(10, 6), title=self.symbol)
        
if __name__ == '__main__':
    fd = FinancialData('AAPL.O')
    print(fd.data.tail())