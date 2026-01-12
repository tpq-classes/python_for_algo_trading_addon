#
# Monitoring Client
# for SMAAlgoTrader Class
#
# Oanda Master Class
#
# The Python Quants GmbH
#
import zmq
from pprint import pprint

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://161.35.18.54:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    msg = socket.recv_string()
    if msg.startswith('{'):
        pprint(msg)
    else:
        print(msg)