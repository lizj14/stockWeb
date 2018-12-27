import numpy as np
import os
import pandas as pd
import random
import time

random.seed(time.time())


class Stockdata(object):
    def __init__(self,
                 stock_sym,):
        self.stock_sym = stock_sym
        self.input_size=1
        self.normalized=True
        # Read csv file
        if stock_sym is not None:
            raw_df = pd.read_csv(os.path.join("data", "%s.csv" % stock_sym))
            self.raw_seq = raw_df['Close'].tolist()
            self.raw_seq = np.array(self.raw_seq)
            self.train_X= self._prepare_data(self.raw_seq)

    #def info(self):
    #    return "StockDataSet [%s] train: %d test: %d" % (
    #        self.stock_sym, len(self.train_X), len(self.test_y))

    def _prepare_data(self, seq):
        # split into items of input_size
        seq = [np.array(seq[i * self.input_size: (i + 1) * self.input_size])
               for i in range(len(seq) // self.input_size)]

        if self.normalized:
            seq = [seq[0] / seq[0][0] - 1.0] + [
                curr / seq[i][-1] - 1.0 for i, curr in enumerate(seq[1:])]
        # print('after prepare: ')
        # print(seq)
        return seq

class StockDataList(Stockdata):
    def __init__(self, data_list):
        Stockdata.__init__(self, stock_sym=None)
        self.raw_seq = np.array(data_list)
        self.train_X = self._prepare_data(self.raw_seq)
    
    def __str__(self):
        return '%s \n %s' % (self.raw_seq, self.train_X)
