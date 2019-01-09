from django.test import TestCase
from searchStock.models import *
import dataReader
import searchStock.modelReader as searchModel
import searchStock.predictCreator as searchPredict

# Create your tests here.
class DataTest(TestCase):
    def simple_test(self):
        print('know how to test!')
        print(Stock.objects.all())
        print(Predict.objects.all())
        
    def full_test(self):
        print('demonstrate that this is the new database!')
        print(Stock.objects.all())
        
        print('read the data from csv')
        dataReader.read_csv('data/ACN.csv')
        print(Stock.objects.all())
        
        print('prepare the predictions for the judgement')
        searchPredict.add_predicts_for_stock('ACN')
        
        print(Predict.objects.all())
        result = searchModel.predict_new_data('ACN', [151.21, 152.72, 153.91])
        print(result)
        result = searchModel.predict_new_data('ACN', 157.33)
        print(result)
        
        print('predict success!')
