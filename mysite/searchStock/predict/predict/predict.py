import time
import random
import numpy as np
# import os
import pandas as pd
from searchStock.predict.predict.Stock_data import Stockdata, StockDataList
import tensorflow as tf
    
def predict(dataInput, modelFileName):
    
    learning_rate = tf.placeholder(tf.float32, None, name="learning_rate")
    keep_prob = tf.placeholder(tf.float32, None, name="keep_prob")
    
    # Stock symbols are mapped to integers.
    symbols = tf.placeholder(tf.int32, [None, 1], name='stock_labels')
    
    inputs = tf.placeholder(tf.float32, [None, 30, 1], name="inputs")
    pred=tf.Variable(tf.truncated_normal([1, 1]),name="pred")
    target_symbol="test"
    # stock_data_list = [Stockdata(target_symbol)]
    stock_data_list = [StockDataList(dataInput)]
    merged_test_X = []
    merged_test_labels = []
    for label_, d_ in enumerate(stock_data_list):
        merged_test_X += list(d_.train_X)
        merged_test_labels += [[label_]] * len(d_.train_X)
    merged_test_X = np.array(merged_test_X)
    merged_test_X=np.reshape(merged_test_X,(1,30,1))
    merged_test_labels = np.array(merged_test_labels)
    test_data_feed = {
        inputs: merged_test_X,
        keep_prob:1.0,
        symbols: merged_test_labels,
    }
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph(
            # 'searchStock/predict/predict/%s/test.ckpt.meta' % modelFileName)
            'searchStock/predict/predict/ACN/test.ckpt.meta')
        new_saver.restore(
            # sess, "searchStock/predict/predict/%s/test.ckpt"%modelFileName)
            sess, "searchStock/predict/predict/ACN/test.ckpt")
        for i in range(30):
            sess.run(tf.global_variables_initializer())
            prediction=sess.run([pred],test_data_feed)
            merged_test_X=np.reshape(merged_test_X,(30))
            merged_test_X=np.append(merged_test_X[1:],prediction)
            merged_test_X = np.reshape(merged_test_X, (1, 30, 1))
            merged_test_X = np.array(merged_test_X)
            test_data_feed = {
                 inputs: merged_test_X,
                 symbols: merged_test_labels,
            }
            
    # reshape the data.
    result = [float(x)/100 for x in merged_test_X[0]]
    return result
    # return merged_test_X
