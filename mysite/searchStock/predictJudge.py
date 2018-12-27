from searchStock.models import *
import numpy as np
# import searchStock.modelReader as sm

dict_mean = {
    'ACN': 0.0007224897656551936,
    'AAPL': 0.001358091167529238,
    'AMD': 0.0008149032822253641, 
    'AOS': 0.0008417039074782383,
    'APA': 0.00023259277493087167,
    'MMM': 0.00034649110176090004,
}

dict_std = {
    'ACN': 0.01907066478572148,
    'AAPL': 0.02307455555352063,
    'AMD': 0.03953238922500301,
    'AOS': 0.021019597466740952,
    'APA': 0.02321610491798477,
    'MMM': 0.013854008157222167,
}

def calculate_final(result_list):
    start = 1.0
    for num in result_list:
        start *= (1+num)
    return start

def count_unreliable(stock_name, result_list):
    up_limit = dict_mean[stock_name] + 3*dict_std[stock_name]
    low_limit = dict_mean[stock_name] - 3*dict_std[stock_name]
    count = 0
    for num in result_list:
        if num > up_limit or num < low_limit:
            count += 1
    return count


def judge(stock_name, result_list):
    predicts = Predict.objects.all()
    average_list = [p.predict_average for p in predicts]
    median_list = [p.predict_median for p in predicts]
    final_list = [p.predict_final for p in predicts]
    unreliable_list = [p.predict_unreliable for p in predicts]
    std_list = [p.predict_std for p in predicts]
    
    average_value = np.average(result_list)
    median_value = np.median(result_list)
    std_value = np.std(result_list)
    final_value = calculate_final(result_list)
    count_value = count_unreliable(stock_name, result_list)
    
    return {
        'average': relative_value(average_list, average_value),
        'median': relative_value(median_list, median_value),
        'final': relative_value(final_list, final_value),
        'std': relative_value(std_list, std_value),
        'unreliable': unreliable_value(count_value),
    }
    
    
def unreliable_value(count_value):
    return 0 if count_value >= 5 else 100 - count_value * 20

def relative_value(data_list, value_to_judge):
    small_count = smaller_number(data_list, value_to_judge)
    return small_count/ len(data_list) * 100.0

def smaller_number(data_list, value_to_judge):
    small_count = 0
    for num in data_list:
        if num < value_to_judge:
            small_count += 1
    return small_count
    