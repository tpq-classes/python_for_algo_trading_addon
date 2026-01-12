#
# Event-based Backtesting
# of Algorithmic Trading Strategies
#
# Base Classes
#
# The Python Quants GmbH
#
import tpqoa
import numpy as np
import pandas as pd

data_path = '../../../data/'

class FinancialData:
    def __init__(self, instrument, start, end, granularity):
        self.instrument = instrument
        self.start = start
        self.end = end
        self.granularity = granularity
        self.config_file = '../../../data/pyalgo.cfg'
        self.api = tpqoa.tpqoa('../../../data/pyalgo.cfg')
        self.filename = 'oanda_{}_{}_{}_{}.csv'.format(
                    instrument, start, end, granularity)
        self.prepare_data()

    def prepare_data(self):
        try:
            self.data = pd.read_csv(data_path + self.filename,
                                   index_col=0, parse_dates=True)
        except:
            raw_a = self.api.get_history(self.instrument,
                    self.start, self.end, self.granularity, 'A')
            raw_b = self.api.get_history(self.instrument,
                    self.start, self.end, self.granularity, 'B')
            self.data = pd.DataFrame({'ask': raw_a['c'], 'bid': raw_b['c']})
            self.data.to_csv(data_path + self.filename)
        self.data['mid'] = self.data.mean(axis=1)


class BacktestingBase(FinancialData):
    def __init__(self, instrument, start, end, granularity,
                 amount, verbose=True):
        super(BacktestingBase, self).__init__(instrument, start,
                                              end, granularity)
        self.initial_amount = amount  # initial cash
        self.amount = amount  # current cash balance
        self.size = 1  # position size (Oanda units)
        self.leverage = 1 # leverage of account
        self.position = 0  # current position
        self.units = 0  # number of units in position
        self.trades = 0  # number of trades
        self.wait = 0  # waiting periods after stop loss
        self.sls = 0  # number of stop losses
        self.verbose = verbose

    def get_date_price(self, bar):
        date = str(self.data.index[bar])
        bid = self.data['bid'].iloc[bar]
        ask = self.data['ask'].iloc[bar]
        return date, bid, ask

    def print_balance(self, bar):
        date, bid, ask = self.get_date_price(bar)
        print('{} | current cash balance is {:.2f}'.format(date, self.amount))

    def print_net_wealth(self, bar):
        date, bid, ask = self.get_date_price(bar)
        price = bid if self.position == 1 else ask
        nw = self.amount + self.units * price / self.leverage
        print('{} | current  net wealth  is {:.2f}'.format(date, nw))

    def place_buy_order(self, bar, units=None, amount=None):
        date, bid, ask = self.get_date_price(bar)
        if units is None:
            units = int(amount // ask)
        self.amount -= units * ask / self.leverage
        self.units += units
        self.trades += 1
        if self.verbose:
            print('{} | bought {} units for {:.5f}'.format(date, units, ask))
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def place_sell_order(self, bar, units=None, amount=None):
        date, bid, ask = self.get_date_price(bar)
        if units is None:
            units = int(amount // bid)
        self.amount += units * bid / self.leverage
        self.units -= units
        self.trades += 1
        if self.verbose:
            print('{} | sold   {} units for {:.5f}'.format(date, units, bid))
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def close_out(self, bar):
        date, bid, ask = self.get_date_price(bar)
        price = bid if self.position == 1 else ask
        self.amount += (self.units * price) * self.position / self.leverage
        self.units -= self.units
        self.trades += 1
        print('\n{} | *** CLOSING OUT ***'.format(date))
        print(66 * '=')
        print('{} | number of trades {}'.format(date, self.trades))
        print('{} | number of stops  {}'.format(date, self.sls))
        print('{} | initial cash balance {}'.format(date, self.initial_amount))
        self.print_balance(bar)
        perfg = (self.amount - self.initial_amount) / self.initial_amount * 100
        print('{} | net performance gross [%] {:.2f}'.format(date, perfg))
        perfe = ((self.amount - self.initial_amount) /
                 (self.size / self.leverage)) * 100
        print('{} | net performance equity [%] {:.2f}'.format(date, perfe))
        print(66 * '=')
        self.position = 0
        self.trades = 0
