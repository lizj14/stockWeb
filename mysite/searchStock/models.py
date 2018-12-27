from django.db import models
# MAX_LEN = 20

# Create your models here.

# Stocks in the project
class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    
    def __str__(self):
        return 'stock: %s' % self.stock_name
    
# Method for predicting
class Method(models.Model):
    method_name = models.CharField(max_length=100)
    def __str__(self):
        return 'method: %s' % self.method_name

# the info of users
class User(models.Model):
    user_name = models.CharField(max_length=30)
    user_passwd = models.CharField(max_length=30)
    def __str__(self):
        return 'user: %s' % self.user_name


# price, record the status of stock.
class Price(models.Model):
    stock_key = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price_date = models.DateField('price date')
    price_open = models.FloatField()
    price_high = models.FloatField()
    price_low = models.FloatField()
    price_close = models.FloatField()
    price_adj_close = models.FloatField()
    price_volume = models.FloatField()
    
    def __str__(self):
        return 'price: stock %s. date: %s' % (
            self.stock_key.stock_name, self.price_date)
            
    def __lt__(self, other):
        return self.price_date < other.price_date


class Predict(models.Model):
    stock_key = models.ForeignKey(Stock, on_delete=models.CASCADE)
    predict_average = models.FloatField()
    predict_final = models.FloatField()
    predict_median = models.FloatField()
    predict_unreliable = models.IntegerField()
    predict_std = models.FloatField()
    
    def __str__(self):
        return 'predict: stock %s. avg: %s, final: %s, median: %s, unreliable: %s, std: %s' % (
            self.stock_key.stock_name, self.predict_average, self.predict_final,
            self.predict_median, self.predict_unreliable, self.predict_std)
