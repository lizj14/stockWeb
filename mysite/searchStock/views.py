from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from searchStock import modelReader
import datetime
import json

# Create your views here.

def index(request):
    return render(request,"login.html")

@csrf_exempt
def stock_name_submit(request):
    if request.method=='POST':
        stock_name=request.POST.get("stock_name")
        
        # start_date=datetime.date(2003,5,5)
        # print(stock_name)
        stock_price_attr1=modelReader.read_recent_prices(stock_name)
        stock_price_attr2=stock_price_attr1[0]
        print(len(stock_price_attr2))
        stock_price=','.join(str(i) for i in stock_price_attr2)
        # print(type(stock_price))
        print(stock_price)
        return HttpResponse(stock_price)

@csrf_exempt
def predict(request):
    stock_name=modelReader.read_all_stocks()
    return render(request,"predict_home.html",{"stock_name":stock_name})
    
@csrf_exempt
def result(request):
    if request.method=='POST':
        if request.method=='POST':
            stock_name=request.POST.get("stock_name")
            new_price_string=request.POST.get("input_price")
            new_price_list=list(map(float,new_price_string.split(',')))
            print(type(new_price_list))
            # new_price=float(request.POST.get("input_price"))
            print("这里是预测")
            print(stock_name)
            # print(new_price)
            # pre_price=modelReader.predict_data_with_new_day(stock_name,new_price_list);
            (pre_price2,value_result)=modelReader.predict_new_data(stock_name,new_price_list);
            print(type(pre_price2));
            for i in range(len(pre_price2)):
                pre_price2[i]=pre_price2[i]*100
            # print("new list 价格");
            # print(pre_price2);
            # print("评价");
            # print(value_result);
            # print("输出完毕");
            # pre_price=predict_price_attr1[0]
            # pre_price=','.join(str(i) for i in predict_price_attr2)
            # print(type(pre_price))
            # print(pre_price)
            # pre_price_json=json.dumps(pre_price)
            # print(pre_price_json)
    return  render(request,"predict_result.html",{'pre_price':json.dumps(pre_price2),'value_result':json.dumps(value_result)},)

