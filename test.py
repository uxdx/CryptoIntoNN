"""모듈 및 함수 검증을 위한 테스트 코드
"""
import time
import numpy as np
import pandas as pd
from requests.api import options
from utils.datasetmaker import Controller, PastFuture
from utils.marketdata import MarketDataProvider
from datasets import CustomDataset, PastFutureDataset
from typing import List

# Decorator
class Tester:
    def __init__(self, f):
        self.func = f
        self.test_start_time = time.time()
    def __call__(self):
        self.init_msg()
        self.func()
        self.ending_msg()
    def init_msg(self):
        print('Start "', self.func.__name__,'". ')
    def ending_msg(self):
        print('Finished "', self.func.__name__, '". ', time.time() - self.test_start_time, 'sec')


@Tester
def get_data_tester():
    df1 = MarketDataProvider().request_data()
    assert len(df1) == 37881
    start_time = '2021-01-14 00:00:00'
    end_time = '2021-07-16 00:00:00'
    df2 = MarketDataProvider(start_time,end_time,'Binance').request_data()
    assert len(df2) == 4386
    df3 = MarketDataProvider(start_time=start_time).request_data()
    assert len(df3) == 5351
    print(df3)
    df4 = MarketDataProvider(end_time=end_time).request_data()
    print(df4)
    
@Tester
def dataset_maker_tester():
    controller = Controller()
    options = {
        'market':'Binance',
        'start_time' : '2021-01-14 00:00:00',
        'end_time' : '2021-07-16 00:00:00',
        'symbol' : 'BTCUSDT',
        'interval' : '1h',
        'past_length' : 10,
        'future_length' : 5,
    }
    controller.construct_dataset(PastFuture, **options)

@Tester
def dataset_loader_tester():
    dataset = PastFutureDataset(symbol='BTCUSDT', interval='1h', start='2021-01-14 00:00:00', end='2021-07-16 00:00:00', past_length=10, future_length=5)
    data = dataset.data
    targets = dataset.targets
    print(data.shape)
    print(targets.shape)

if __name__ == '__main__':
    # get_data_tester()
    print(len(CustomDataset().data))