from api import Rest_api
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np


# 程式碼補全請參閱 hiskio python 實戰課程


def open_(ra, method, tickers, live_price, set_qty, qty, open_position, entry_price, true_mid, profit_buff):
    action = []
    if method == 'long':
        action.append('buy')
        open_position[0] = 1
    else:
        action.append('sell')
        open_position[0] = -1
    for i in range(1, len(tickers)):
        if action[0] == 'buy':
            action.append('sell')
            open_position[i] = -1
        elif action[0] == 'sell':
            action.append('buy')
            open_position[i] = 1
    for i in range(len(tickers)):
        entry_price[i] = live_price[i]
        qty[i] = set_qty
    with ThreadPoolExecutor() as executor:
        for i in range(len(action)):
            executor.submit(ra.place_order, tickers[i], action[i], set_qty, live_price[i])
    return open_position, entry_price, qty

def add_(ra, tickers, live_price, set_qty, qty, open_position, entry_price, true_mid, profit_buff):
    action = []
    print("ADD")
    for i in range(len(tickers)):
        if open_position[i] > 0:
            action.append('buy')
        elif open_position[i] < 0:
            action.append('sell')                   
    for i in range(len(tickers)):
        entry_price[i] = (entry_price[i] * qty[i] + live_price[i] * set_qty) / (qty[i] + set_qty)                       
        qty[i] += set_qty
    with ThreadPoolExecutor() as executor:
        for i in range(len(action)):
            executor.submit(ra.place_order, tickers[i], action[i], set_qty, live_price[i])
    return entry_price, qty

def inverse_(ra, tickers, live_price, set_qty, qty, open_position, entry_price, true_mid, profit_buff):
    action = []
    for i in range(len(tickers)):
        if open_position[i] > 0:
            action.append('sell')
            open_position[i] = -1
        elif open_position[i] < 0:
            action.append('buy') 
            open_position[i] = 1 
    inverse_qty_ = locals()
    for i in range(len(tickers)):
        inverse_qty_[i] = qty[i] + set_qty
        entry_price[i] = live_price[i]
        qty[i] = set_qty
    with ThreadPoolExecutor() as executor:
        for i in range(len(action)):
            executor.submit(ra.place_order, tickers[i], action[i], inverse_qty_[i], live_price[i])
    return open_position, entry_price, qty

def spread_strategy(ra, tickers, set_qty, qty, live_price, live_diff, diff_mid, open_position, entry_price, profit_buff, stop_add):
    # pass
