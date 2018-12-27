# This is the script for read data in csv file of Stocks to fill in the database

import csv, re
from searchStock.models import Stock, Price
# from sys import argv
import searchStock.modelReader as sm
import datetime

def read_csv(file_name):

    
    # no longer use argv because of manage.py environment necessary.
    # file_name = argv[1]
    
    # analyse the name of the Stock
    print(file_name)
    match_result = re.search('[a-zA-Z0-9\_]*\.csv', file_name)
    print(match_result.group(0))
    stock_name_in = match_result.group(0).split('.')[0]
    
    # here get the name of the stock
    print(stock_name_in)
    
    try:
        stock = Stock.objects.get(stock_name=stock_name_in)
        print('get the stock name : %s' % stock_name_in)
    except Exception as e:
        stock = Stock(stock_name=stock_name_in)
        stock.save()

    print(stock)
    print(Stock.objects.all())
    
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    
        test = 0
        for row in reader:
            # test the usage of DictReader
            if test < 3:
                print(row)
                print(row['Date'])
                print(row['High'])
                # test += 1
            test += 1
            ''' read only first two elements while debugging.
            if test > 2:
                continue
            '''
            date_list = row['Date'].split('-')
            date_in = datetime.date(
                int(date_list[0]), int(date_list[1]), int(date_list[2]))
            
            # the data has been input before
            if stock.price_set.filter(
                price_date__year=date_in.year,
                price_date__month=date_in.month,
                price_date__day=date_in.day).count() != 0:
                print('the price data has existed at %s' % date_in)
            else:
                stock.price_set.create(
                    price_date=date_in,
                    price_open=float(row['Open']), 
                    price_high=float(row['High']),
                    price_low=float(row['Low']),
                    price_close=float(row['Close']),
                    price_adj_close=float(row['Adj Close']),
                    price_volume=float(row['Volume'])
                    )
            if test == 2:
                print(stock)
        
        # end debug print
        print(stock)
        print(stock.price_set.count())


def read_now():
    read_csv('data/AAPL.csv')
    read_csv('data/AMD.csv')
    read_csv('data/AOS.csv')
    read_csv('data/APA.csv')
    read_csv('data/MMM.csv')

if __name__ == '__main__':
    # read_csv('data/ACN.csv')
    
    # d1 = datetime.date(2005, 4, 7)
    # a = sm.predict_data('ACN', d1)
    # print(a)
    pass

def test_predict():
    d1 = datetime.date(2005, 4, 7)
    a = sm.predict_data('ACN', d1)
    return a
