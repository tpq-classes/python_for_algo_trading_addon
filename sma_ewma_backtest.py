#
# Event-based Backtesting
# of Algorithmic Trading Strategies
#
# SMA & EWMA-based Trading Strategy
#
# The Python Quants GmbH
#

from backtest_base import *

class SmaEwmaBacktester(BacktestingBase):

    def prepare_statistics(self):
        self.data['SMA'] = self.data['mid'].rolling(self.SMA).mean()
        self.data['EWMA'] = self.data['mid'].ewm(alpha=self.alpha).mean()

    def run_strategy(self, SMA, alpha, size, leverage, stop_loss, max_wait):
        self.SMA = SMA
        self.alpha = alpha
        self.size = size
        self.leverage = leverage
        self.stop_loss = stop_loss
        self.max_wait = max_wait
        self.position = 0
        self.trades = 0
        self.wait = 0
        self.sls = 0
        self.units = 0
        self.amount = self.initial_amount
        self.prepare_statistics()

        print('*** RUNNING STRATEGY ***')
        print('SMA = {} | alpha = {:.3f}'.format(self.SMA, self.alpha))
        print('start {} | end {} | bar {}'.format(
            self.start, self.end, self.granularity))
        print('size = {} | leverage = {} | stop loss {} | wait bars {}'.format(
            self.size, self.leverage, self.stop_loss, self.max_wait))

        for bar in range(self.SMA, len(self.data)):
            date, bid, ask = self.get_date_price(bar)
            if self.wait > 0 : self.wait -= 1
            elif self.position in [-1, 1]:
                price = bid if self.position == 1 else ask
                if self.position == 1:
                    p = (price - self.entry_price) / self.entry_price
                else:
                    p = (self.entry_price - price) / self.entry_price
                if p * self.leverage < -self.stop_loss:
                    if self.verbose:
                        print('\n{} | *** STOP LOSS ***'.format(date))
                    if self.position == 1:
                        self.place_sell_order(bar, units=self.units)
                    else:
                        self.place_buy_order(bar, units=-self.units)
                    # self.amount += (self.units * price) * self.position / self.leverage
                    self.units -= self.units
                    self.trades += 1
                    self.position = 0
                    self.wait = self.max_wait
                    self.sls +=1

            if self.position in [0, -1] and self.wait == 0:
                if self.data['SMA'].iloc[bar] > self.data['EWMA'].iloc[bar]:
                    if self.verbose:
                        print('\n{} | *** PLACING BUY ORDER ***'.format(date))
                    # going long based on amount (= Oanda units)
                    if self.position == -1:
                        self.place_buy_order(bar, units=-self.units)
                    self.place_buy_order(bar, amount=self.size)
                    self.entry_price = ask
                    self.position = 1

            elif self.position in [0, 1] and self.wait == 0:
                if self.data['SMA'].iloc[bar] < self.data['EWMA'].iloc[bar]:
                    if self.verbose:
                        print('\n{} | *** PLACING SELL ORDER ***'.format(date))
                    # going short based on amount (= Oanda units)
                    if self.position == 1:
                        self.place_sell_order(bar, units=self.units)
                    self.place_sell_order(bar, amount=self.size)
                    self.entry_price = bid
                    self.position = -1

        self.close_out(bar)
        S0 = self.data.iloc[self.SMA]['mid']
        ST = self.data.iloc[bar]['mid']
        ben_perf = (ST - S0) / S0 * 100
        print('benchmark performance [%] {:.2f}'.format(ben_perf))

if __name__ == '__main__':
    instrument = 'EUR_GBP'
    start = '2018-08-01'
    end = '2018-10-01'
    granularity = 'M10'
    sma = SmaEwmaBacktester(instrument, start, end, granularity,
                            10000, verbose=False)
    sma.run_strategy(50, 0.03, 20000, 20, 0.075, 5)
