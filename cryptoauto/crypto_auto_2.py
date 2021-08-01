#-*-coding:utf-8-*-
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

import time
import datetime
import pyupbit
import numpy as np

# import telepot

# class TeleBot:
#     def __init__(self, tToken, tChannel):
#         self.token = tToken
#         self.bot = telepot.Bot(self.token)
#         self.channel = tChannel

#     def send(self, msg):
#         self.bot.sendMessage(self.channel, msg)

class UpbitBot:
    def __init__(self, aKey, sKey): #, tToken, tChannel):
        self.access_key = aKey
        self.secret_key = sKey
        self.server_url = 'https://api.upbit.com'
        # self.telebot = TeleBot(tToken, tChannel)
        self.exception_list = []
        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)
        self.upbit_list = []
        for i in pyupbit.get_tickers():
            if i[:4] == 'KRW-':
                self.upbit_list.append(i)
        self.hubos = []#self.get_max_rise_coins()

    # 내 계좌 조회
    def myBalance(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorize_token}
        res = requests.get(self.server_url + '/v1/accounts', headers=headers)
        return res.json()
    
    # 코인 리스트 추출 (가장 높은 상승률 순 정렬)
    def get_max_rise_coins(self):
        tickers = pyupbit.get_tickers()
        coins = []
        for i in tickers:
            if i[:4] == 'KRW-':
                coins.append(i)
        res = requests.request('GET', 'https://api.upbit.com/v1/ticker', params={'markets': ','.join(coins)})
        data = res.json() # 원화 마켓 전체 오늘 일봉 가져오기
        data.sort(key=(lambda x: x['signed_change_rate']), reverse=True) # 상승률 순 정렬
        now_time = str(datetime.datetime.now().hour).zfill(2)
        max_coins = []
        for i in data:
            if ( now_time != i['trade_time_kst'][:2] ):# or ( i['market'] in self.exception_list ): # 시봉 갱신이 안됐거나 or 예외목록에 있거나
                pass
            else:
                max_coins.append(i['market'])
        #return max_coins
        self.hubos = max_coins
    
    # 호가 단위 계산
    def calc_price_unit(self, order_price):
        price_unit = 0.01
        if order_price < 10:
            price_unit = 0.01
        elif order_price < 100:
            price_unit = 0.1
        elif order_price < 1000:
            price_unit = 1
        elif order_price < 10000:
            price_unit = 5
        elif order_price < 100000:
            price_unit = 10
        elif order_price < 500000:
            price_unit = 50
        elif order_price < 1000000:
            price_unit = 100
        elif order_price < 2000000:
            price_unit = 500
        else:
            price_unit = 1000
        return price_unit

    # 호가 단위 금액 계산
    def calc_price(self, order_price):
        price_unit = self.calc_price_unit(order_price)
        ret = int(order_price / price_unit + 1) * price_unit
        return round(ret, 3)

    # k값 별 수익률(ror) 계산 (일정금액 투자 기준)
    def k_ror_sum(self, data_frame, kvalue, p_unit):
        data_frame['range'] = np.ceil( (data_frame['high'] - data_frame['low']) * kvalue / p_unit ) * p_unit
        data_frame['beforerange'] = (data_frame['high'] - data_frame['low'])
        data_frame['target'] = data_frame['open'] + data_frame['range'].shift(1)
        data_frame['ror'] = np.where(data_frame['high'] >= data_frame['target'],
                                    np.minimum(data_frame['close'], data_frame['open'] + data_frame['beforerange'].shift(1) ) / data_frame['target'] - 0.0015, # 슬리피지 0.5%
                                    1)
        ror = (data_frame['ror'] - 1).cumsum()[-2] + 1 # 수익 합
        return ror
    
    # k값 별 수익률(ror) 계산 (복리 수익)
    def k_ror_prod(self, data_frame, kvalue, p_unit):
        data_frame['range'] = np.ceil( (data_frame['high'] - data_frame['low']) * kvalue / p_unit ) * p_unit
        data_frame['beforerange'] = (data_frame['high'] - data_frame['low'])
        data_frame['target'] = data_frame['open'] + data_frame['range'].shift(1)
        data_frame['ror'] = np.where(data_frame['high'] >= data_frame['target'],
                                    np.minimum(data_frame['close'], data_frame['open'] + data_frame['beforerange'].shift(1) ) / data_frame['target'] - 0.0015, # 슬리피지 0.5%
                                    1)
        ror = data_frame['ror'].cumprod()[-2] # 수익 곱
        return ror

    # 1주(168시간) 내 최고 수익률 k 값 찾기
    def calc_k_value(self, market):
        df = pyupbit.get_ohlcv(market, interval="minutes60", count=24)# 하루로 테스트 count=168)
        punit = self.calc_price_unit(df.iloc[-1]['open'])
        # 이전 봉의 range * 0.1 이 호가 단위보다 작으면 무시
        if (df.iloc[-2]['high'] - df.iloc[-2]['low']) < ( self.calc_price_unit(df.iloc[-2]['high']) * 10 ):
            return -1
        max_ror = 1
        result = -1
        for k in np.arange(0, 1.0, 0.1):
            ror = self.k_ror_prod(df, round(k,1), punit)
            if ror > max_ror:
                max_ror = ror
                result = round(k, 1)
        if result == 0: # 이미 이전에 무지성 상승한 것으로 판단
            return -1
        max_ror = 1
        result = -1
        for k in np.arange(0.1, 1.0, 0.1):
            ror = self.k_ror_sum(df, round(k,1), punit)
            if ror > max_ror:
                max_ror = ror
                result = round(k,1)
        return result

    # target 계산
    def get_target_price(self, ticker, k):
        df = pyupbit.get_ohlcv(ticker, interval="minutes60", count=2)
        target_price = self.calc_price(df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k)
        current_price = df.iloc[1]['close']
        # if datetime.datetime.now().minute < 5:
        #     self.telebot.send(ticker + '\n목표가: '+str(target_price)+'('+str(k)+')')
        if df.iloc[1]['high'] > (df.iloc[1]['open'] + df.iloc[0]['high'] - df.iloc[0]['low']):
            # 이미 쐈어요 ㅠㅠ
            self.exception_list.append(ticker)
            return False
        else:
            return ( current_price > target_price )
    
    # 봇 데이터 리셋 (봉 갱신)
    def reset(self):
        self.exception_list = []
        self.hubos = self.get_max_rise_coins()

    def sleep_until_next(self):
        time.sleep( (59 - now.minute)*60 + 60 - now.second )
        self.reset()

if __name__ == "__main__":
    bot = UpbitBot("9afurEZJQTqYlNq9an45r2xaB1nNFF6xbTPS7or9", "3fQEcrOLhdWT2Krh122OmR7fuibQ3xNqsDjUi7uV")
    bot.reset()
    print('start')
    while True:
        try:
            now = datetime.datetime.now() + datetime.timedelta(hours=9) - datetime.timedelta(minutes=3)
            if now.minute > 57 or ( len(bot.exception_list) == len(bot.upbit_list) ):
                print('다음 봉 대기')
                bot.sleep_until_next()
                bot.reset()
                continue
            bot.get_max_rise_coins()
            for targetCoin in bot.hubos:
                if targetCoin in bot.exception_list:
                    continue
                k = bot.calc_k_value(targetCoin)
                if k != -1:
                    if bot.get_target_price(targetCoin, k):
                        my_krw = bot.upbit.get_balance(ticker="KRW")
                        if my_krw > 5000:
                            bot.upbit.buy_market_order(targetCoin, int(my_krw*0.9995))
                            print(targetCoin[4:] + ' 매수')
                        else:
                            print(targetCoin + '매수각 (잔고없음)')
                        bot.sleep_until_next()
                        amount = bot.upbit.get_balance(targetCoin[4:])
                        if amount > 0:
                            bot.upbit.sell_market_order(targetCoin, amount)
                        break
                else:
                    bot.exception_list.append(targetCoin)
                time.sleep(0.5)
            #bot.reset()
            if len(bot.exception_list) == len(bot.upbit_list):
                print('매수할 코인 없음')
                bot.sleep_until_next()
        except Exception as e:
            print(e)
            time.sleep(5)