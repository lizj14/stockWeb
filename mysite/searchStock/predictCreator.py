from searchStock.models import *
import numpy as np
import searchStock.modelReader as sm

from searchStock.predictJudge import dict_mean, dict_std, calculate_final, count_unreliable

def calculate_stock_data(stock_name):
    try:
        stock = Stock.objects.get(stock_name=stock_name)
        prices = stock.price_set.all()
        prices.order_by('price_date')
        price_list = [x.price_close for x in prices]
        price_seq = calculate_relative_data(price_list)
        return price_seq
    except Exception as e:
        print(e)
        return []

def calculate_relative_data(seq):
    # split into items of input_size
    new_seq = [0.0] + [curr/ seq[i] - 1.0 for i, curr in enumerate(seq[1:])]
    return new_seq
    
def calculate_regular_number(stock_name):
    price_seq = calculate_stock_data(stock_name)
    price_mean = np.average(price_seq)
    price_std = np.std(price_seq)
    return price_mean, price_std


# This is for prepare data for judging the stocks.
def add_predicts_for_stock(stock_name):
    try:
        stock = Stock.objects.get(stock_name=stock_name)
        price_list = stock.price_set.all()
        last_price = price_list[price_list.count()-1].price_close
        print('last price: %s' % last_price)
        for i in range(0, 5):
            ratio = 1.0 + (i-5)*0.04
            print('group %s for %s: %s' % (i, stock_name, last_price*ratio))
            sm.add_new_predict(stock_name, last_price*ratio)
    except Exception as e:
        print(e)


def add_predicts():
    for stock_name in ['ACN', 'AAPL', 'AMD', 'AOS', 'APA', 'MMM']:
        add_predicts_for_stock(stock_name)
