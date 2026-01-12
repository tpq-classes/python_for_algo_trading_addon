#
# SMA Trader
# Cloud Deployment
#
# Oanda Master Class
#
# The Python Quants GmbH
#
import q
import zmq
import tpqoa
import numpy as np
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')


class SMAAlgoTrader(tpqoa.tpqoa):
    def __init__(self, config_file, granularity, SMA1, SMA2, units):
        super(SMAAlgoTrader, self).__init__(config_file)
        self.granularity = granularity
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.units = units
        self.min_length = self.SMA2
        self.position = 0
        self.pls = list()
        self.tick_data = pd.DataFrame()
    def _resample_data(self):
        self.data = self.tick_data.resample(self.granularity,
                                label='right').last().ffill()
    def _prepare_data(self):
        self.data['SMA1'] = self.data['mid'].rolling(self.SMA1).mean()
        self.data['SMA2'] = self.data['mid'].rolling(self.SMA2).mean()
        self.data['p'] = np.where(self.data['SMA1'] > self.data['SMA2'],
                                  'long', 'short')
    def report_trade(self, order, side):
        q(self.data.tail(3))
        q(order)
        time = order['time']
        units = order['units']
        price = order['price']
        pl = float(order['pl'])
        self.pls.append(pl)
        cpls = sum(self.pls)
        q(cpls)
        msg = '\n' + 90 * '=' + '\n'
        msg += f'{time} | *** GOING {side} ***\n'
        msg += f'{time} | units={units} | price={price}| P&L={pl:.4f} | CP&L={cpls:.4f}\n'
        msg += 90 * '=' + '\n'
        print(msg)
        socket.send_string(msg)
        socket.send_string(str(self.data.tail(3)) + '\n')
        socket.send_string(str(order))
    def on_success(self, time, bid, ask):
        print(self.ticks, end=' ')
        df = pd.DataFrame({'ask': ask, 'bid': bid,
                           'mid': (ask + bid) / 2},
                         index=[pd.Timestamp(time)])
        self.tick_data = self.tick_data.append(df)
        self._resample_data()
        self._prepare_data()
        if len(self.data.iloc[:-1]) > self.min_length:
            self.min_length += 1
            if self.position in [0, -1]:
                if self.data['p'].iloc[-2] == 'long':
                    order = self.create_order(self.stream_instrument,
                                units=(1 - self.position) * self.units,
                                             suppress=True, ret=True)
                    self.report_trade(order, 'LONG')
                    self.position = 1
            elif self.position in [0, 1]:
                if self.data['p'].iloc[-2] == 'short':
                    order = self.create_order(self.stream_instrument,
                                units=-(1 + self.position) * self.units,
                                             suppress=True, ret=True)
                    self.report_trade(order, 'SHORT')
                    self.position = -1
        if len(self.data) % 5 == 0:
            self.tick_data.to_csv('tick_data.csv')
            self.data.to_csv('data.csv')

                    
if __name__ == '__main__':
    sma = SMAAlgoTrader('oanda.cfg', granularity='5s',
                        SMA1=3, SMA2=6, units=1000)
    sma.stream_data('EUR_USD', stop=250)  # streaming & trading
    order = sma.create_order(sma.stream_instrument,
                         units=-sma.position * sma.units,
                         suppress=True, ret=True)  # closing the final position
    sma.report_trade(order, 'NEUTRAL')  # reporting the final trade
    sma.tick_data.to_csv('tick_data.csv')
    sma.data.to_csv('data.csv')