# This is the test of data API in Django.
# how to show the result?
# use python3 manage.py shell, into the Python shell, and then use the function.
import searchStock.modelReader as searchModel
import datetime

def test():
    print('---start to test---')
    # import 
    from searchStock.models import User, Method, Stock

    # show the whole table
    print(Method.objects.all())

    # how to add a new element
    new_method = Method(method_name='RNN')
    print(new_method)
    
    # the id number has not be given automatically. 
    print(new_method.id)
    
    # save into the table.
    # you can consider it as COMMIT in SQL.
    new_method.save()
    
    # given id.
    print(new_method.id)

    # verify the change
    print(Method.objects.all())
    
    print('---end test---')


def test_read():
    print('---start test of read data from database')
    from searchStock.models import User, Method, Stock
    
    print(Method.objects.all())
    
    # search according to id
    print(Method.objects.get(id=1))
    
    # search accroding to others
    try:
        p = Method.objects.get(method_name='RNN')
        print(p)
        print(Method.objects.get(method_name='CNN'))
    except Exception as e:
        print(e)
    
    print('---read test end---')
    
def test_read_stock():
    date1 = datetime.date(2018, 11, 21)
    #searchModel.read_price_date('ACN', date1)
    searchModel.read_prices('ACN', date1)

if __name__ == '__main__':
    test_read_stock()
    