from searchStock.models import *
import datetime
import json
from searchStock.predict.predict.predict import predict
from searchStock.predictJudge import *
import numpy as np
N = 30

def read_price_date(stock_name_in, price_date_in):
    try:
        stock = Stock.objects.get(stock_name=stock_name_in)
        price = Price.objects.get(stock_key=stock, price_date=price_date_in)
    except Exception as e:
        print('cannot find %s at %s' % (stock_name_in, price_date_in))
        return False
    # print('%s, %s' % (price, price.price_close))
    return True

def read_prices(stock_name_in, start_date):
    try:
        new_date = start_date - datetime.timedelta(days=1)
        stock = Stock.objects.get(stock_name=stock_name_in)
        prices = stock.price_set.exclude(price_date__lte=new_date)
        prices.order_by('price_date')
        # prices.sort()
        print(prices.count())
        # print(prices)
        # truncate
        if prices.count() > 30:
            prices = prices[:30]
        
        # price_dict = {}
        # for p in prices:
        #     price_dict[p.price_date.__str__()] = p.price_close
        # return json.dumps(price_dict)
        
        price_list = [p.price_close for p in prices]
        price_date = [p.price_date for p in prices]
        # print(price_list)
        # print(price_date)
        return price_list, price_date
    except Exception as e:
        print(e)
        return [], []

def read_recent_prices(stock_name_in):
    try:
        # new_date = start_date - datetime.timedelta(days=1)
        stock = Stock.objects.get(stock_name=stock_name_in)
        prices = stock.price_set.all()
        prices.order_by('price_date')
        # prices.sort()
        # print(prices.count())
        num = prices.count()
        # print(prices)
        # truncate
        # if prices.count() > 30:
        #    prices = prices[:30]
        prices = prices[num-30:]
        
        # price_dict = {}
        # for p in prices:
        #     price_dict[p.price_date.__str__()] = p.price_close
        # return json.dumps(price_dict)
        
        price_list = [p.price_close for p in prices]
        price_date = [p.price_date for p in prices]
        # print(len(price_list))
        # print(price_list)
        # print(price_date)
        return price_list, price_date
    except Exception as e:
        print(e)
        return [], []

def read_prices_json(stock_name_in, start_date):
    price_list, price_date = read_prices(stock_name_in, start_date)
    price_dict = {}
    for i in range(0, len(price_list)):
        price_dict[price_date[i].__str__()] = price_list[i]
    return json.dumps(price_dict)

def read_all_stocks():
    stocks = Stock.objects.all()
    stock_name_list = [s.stock_name for s in stocks]
    stock_json = json.dumps(stock_name_list)
    return stock_name_list
    
def read_all_methods():
    methods = Method.objects.all()
    method_name_list = [m.method_name for m in methods]
    method_json = json.dumps(method_name_list)
    return method_json
    # return method_name_list


def predict_data(stock_name_in, start_date):
    data_list, date_list = read_prices(stock_name_in, start_date)
    predict_result = predict(data_list, stock_name_in)
    return predict_result

def predict_data_with_new_data(stock_name_in, new_data_list):
    data_list, date_list = read_recent_prices(stock_name_in)
    # exclude the oldest data in the data_list
    data_list = data_list[len(new_data_list):]
    data_list += new_data_list
    # print(data_list)
    predict_result = predict(data_list, stock_name_in)
    return predict_result
    
def predict_data_with_new_day(stock_name_in, new_day_data):
    return predict_data_with_new_data(stock_name_in, [new_day_data])

def add_new_predict(stock_name, predict_value):
    if type(predict_value) == float or type(predict_value) == int:
        print('transfer')
        predict_value = [predict_value]
    result = predict_data_with_new_data(stock_name, predict_value)
    average_value = np.average(result)
    median_value = np.median(result)
    std_value = np.std(result)
    final_value = calculate_final(result)
    count_value = count_unreliable(stock_name, result)
    # print('%s, %s, %s, %s, %s' % (
    #     average_value, median_value, std_value, final_value, count_value))
    try:
        stock = Stock.objects.get(stock_name=stock_name)
        stock.predict_set.create(
            predict_average = average_value,
            predict_final = final_value,
            predict_median = median_value,
            predict_std = std_value,
            predict_unreliable = count_value
            )
    except Exception as e:
        print(e)
    return result
    
def predict_new_data(stock_name, new_data_list):
    result = add_new_predict(stock_name, new_data_list)
    judge_result = judge(stock_name, result)

    judge_list = [
        judge_result['average'],
        judge_result['median'],
        judge_result['final'],
        judge_result['std'],
        judge_result['unreliable']
    ]

    # return result, judge_result
    return result, judge_list

# def predict_data_json(stock_name_in, start_date):
#    predict_result = predict_data(stock_name_in, start_date)
#    return json.dumps(predict_result[0])
    
