#-*-coding:utf-8-*-
import jwt
import uuid
import requests
import time
import datetime
import pyupbit
import numpy as np

class UpbitBot:
    def __init__(self, aKey, sKey):
        self.access_key = aKey
        self.secret_key = sKey
        self.server_url = 'https://api.upbit.com'
        self.exception_list = []
        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)
        self.upbit_list = []
        for i in pyupbit.get_tickers():
            if i[:4] == 'KRW-':
                self.upbit_list.append(i)
        self.hubos = []

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

    def get_max_rise_coins(self):
        tickers = pyupbit.get_tickers(fiat="KRW")
        res = requests.request('GET', 'https://api.upbit.com/v1/ticker', params={'markets': ','.join(tickers)})
        if res.status_code == 429:
            time.sleep(1)
            res=requests.request('GET','https://api.upbit.com/v1/ticker',params={'markets':','.join(tickers)})

        data = res.json()
        data.sort(key=(lambda x: x['signed_change_rate']), reverse=True)
        now_time = str(datetime.datetime.now().hour).zfill(2)
        max_coins = []
        for i in data:
            if ( now_time != i['trade_time_kst'][:2] ):
                pass
            else:
                max_coins.append(i['market'])
        self.hubos = max_coins

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

    def calc_price(self, order_price):
        price_unit = self.calc_price_unit(order_price)
        ret = int(order_price / price_unit + 1) * price_unit
        return round(ret, 3)

    def k_ror_sum(self, data_frame, kvalue, p_unit):
        data_frame['range'] = np.ceil( (data_frame['high'] - data_frame['low']) * kvalue / p_unit ) * p_unit
        data_frame['beforerange'] = (data_frame['high'] - data_frame['low'])
        data_frame['target'] = data_frame['open'] + data_frame['range'].shift(1)
        data_frame['ror'] = np.where(data_frame['high'] >= data_frame['target'],
                                    np.minimum(data_frame['close'], data_frame['open'] + data_frame['beforerange'].shift(1) ) / data_frame['target'] - 0.0015,
                                    1)
        ror = (data_frame['ror'] - 1).cumsum()[-2] + 1
        return ror

    def k_ror_prod(self, data_frame, kvalue, p_unit):
        data_frame['range'] = np.ceil( (data_frame['high'] - data_frame['low']) * kvalue / p_unit ) * p_unit
        data_frame['beforerange'] = (data_frame['high'] - data_frame['low'])
        data_frame['target'] = data_frame['open'] + data_frame['range'].shift(1)
        data_frame['ror'] = np.where(data_frame['high'] >= data_frame['target'],
                                    np.minimum(data_frame['close'], data_frame['open'] + data_frame['beforerange'].shift(1) ) / data_frame['target'] - 0.0015,
                                    1)
        ror = data_frame['ror'].cumprod()[-2]
        return ror

    def calc_k_value(self, market):
        df = pyupbit.get_ohlcv(market, interval="minutes60", count=24)
        punit = self.calc_price_unit(df.iloc[-1]['open'])
        if (df.iloc[-2]['high'] - df.iloc[-2]['low']) < ( self.calc_price_unit(df.iloc[-2]['high']) * 10 ):
            return -1
        max_ror = 1
        result = -1
        for k in np.arange(0, 1.0, 0.1):
            ror = self.k_ror_prod(df, round(k,1), punit)
            if ror > max_ror:
                max_ror = ror
                result = round(k, 1)
        if result == 0:
            return -1
        max_ror = 1
        result = -1
        for k in np.arange(0.1, 1.0, 0.1):
            ror = self.k_ror_sum(df, round(k,1), punit)
            if ror > max_ror:
                max_ror = ror
                result = round(k,1)
        return result

    def get_target_price(self, ticker, k):
        df = pyupbit.get_ohlcv(ticker, interval="minutes60", count=2)
        target_price = self.calc_price(df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k)
        current_price = df.iloc[1]['close']
        if df.iloc[1]['high'] > (df.iloc[1]['open'] + df.iloc[0]['high'] - df.iloc[0]['low']):
            self.exception_list.append(ticker)
            return False
        else:
            return ( current_price > target_price )

    def reset(self):
        self.exception_list = []
        self.hubos = self.get_max_rise_coins()

    def sleep_until_next(self):
        time.sleep( (59 - now.minute)*60 + 60 - now.second )
        self.reset()

if __name__ == "__main__":
    bot = UpbitBot("9afurEZJQTqYlNq9an45r2xaB1nNFF6xbTPS7or9", "3fQEcrOLhdWT2Krh122OmR7fuibQ3xNqsDjUi7uV")
    bot.reset()
    print('Start!')

    while True:
        try:
            now = datetime.datetime.now() + datetime.timedelta(hours=9)
            if now.minute > 57 or ( len(bot.exception_list) == len(bot.upbit_list) ):
                print(now, ' : wait for next bong')
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
                            print(now, " : " + targetCoin[4:] + ' Buy')
                        else:
                            print(now, " : " + targetCoin + 'Chance but no money')
                        bot.sleep_until_next()
                        amount = bot.upbit.get_balance(targetCoin[4:])
                        if amount > 0:
                            bot.upbit.sell_market_order(targetCoin, amount)
                        break
                else:
                    bot.exception_list.append(targetCoin)
                time.sleep(1)
            if len(bot.exception_list) == len(bot.upbit_list):
                print(now, " : No coin to buy")
                bot.sleep_until_next()
        except Exception as e:
            print(e)
            time.sleep(5)
