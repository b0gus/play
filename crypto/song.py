import time
import pyupbit
import datetime
import requests
import operator
import logging

logging.basicConfig(level='DEBUG')

access = "9afurEZJQTqYlNq9an45r2xaB1nNFF6xbTPS7or9"
secret = "3fQEcrOLhdWT2Krh122OmR7fuibQ3xNqsDjUi7uV"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes60", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return round(target_price * 0.9995)

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes60", count=1) # 시간봉
    start_time = df.index[0]
    return start_time

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes60", count=1) # 시간봉
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def most_traded(cnt): #상위 cnt개 티커 선별
    """1시간봉 누적 거래대금 최대 티커 선별 + 값 증가 추세 확인"""
    tickers = pyupbit.get_tickers(fiat="KRW")
    traded = {}
    price = {}
    for i in tickers:
        try:
            res = requests.request('GET', 'https://api.upbit.com/v1/candles/minutes/60', headers={"Accept": "application/json"}, params={'market': i})
            ticker_data = res.json()
            traded[i] = ticker_data[0]['candle_acc_trade_price']
            price[i] = (ticker_data[0]['trade_price'] - ticker_data[0]['opening_price']) / ticker_data[0]['opening_price']
        except Exception as e:
            logging.error(e)
            pass
    sorted_traded = sorted(traded.items(), key=operator.itemgetter(1), reverse=True)
    sorted_price = sorted(price.items(), key=operator.itemgetter(1), reverse=True)
    most_traded_set = set()
    price_set = set()
    for i in range(cnt):
        most_traded_set.add(sorted_traded[i][0])
        if sorted_price[i][1] > 0:
            price_set.add(sorted_price[i][0])
    return most_traded_set & price_set

def ticker_selection(most_traded_set):
    res = requests.request('GET', 'https://api.upbit.com/v1/ticker', params={'markets': most_traded_set})
    ticker = ''
    if bool(res):
        ticker_data = res.json()
        ticker_change_rate = 0
        for i in ticker_data:
            if i['signed_change_rate'] > ticker_change_rate:
                ticker = i['market']
                ticker_change_rate = i['signed_change_rate']
    return ticker

# 로그인
upbit = pyupbit.Upbit(access, secret)
print(" === Autotrade Start === ")

most_traded_old = most_traded(27)
pick = "KRW-BTC"

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # 최근 시간봉 시작시간
        end_time = start_time + datetime.timedelta(hours=1)
        
        most_traded_set = most_traded(18)
        most_traded_set -= most_traded_old #거래량 급증 코인 체크
        ticker = ticker_selection(most_traded_set)

        if bool(ticker):
            pick = ticker
            k = 0.3
            if start_time < now < end_time - datetime.timedelta(seconds=10): ## 무한루프 방지(차트보고 바꿀수도)
                target_price = get_target_price(pick, k) ## 매수 목표가 계산
                current_price = get_current_price(pick) ## 현재가 조회
                if target_price < current_price:
                    btc = get_balance("BTC")
                    if btc > 0.00008: # 최소거래금액 이상
                        upbit.sell_market_order("KRW-BTC", btc*0.9995) # 수수료 고려
                    krw = get_balance("KRW") # 잔고 조회
                    if krw > 5000: # 최소거래금액
                        upbit.buy_market_order(pick, krw*0.9995) # 수수료 고려
                        logging.info(now, " : buy ", pick)
            else: # 매도
                print(now, ", 매도 시그널", pick)
                amount = upbit.get_balance(pick[4:])
                if amount > 0:
                    upbit.sell_market_order(pick, amount)
                    logging.info(now, " : sell ", pick)
                else:
                    most_traded_old = most_traded(27)
                    pick = "KRW-BTC"
            time.sleep(1)
        else:
            pick = "KRW-BTC"
            k = 0.5
            # print("비트코인 문")
            if start_time < now < end_time - datetime.timedelta(seconds=10): ## 무한루프 방지(차트보고 바꿀수도)
                target_price = get_target_price(pick, k) ## 매수 목표가 계산
                current_price = get_current_price(pick) ## 현재가 조회
                if target_price < current_price:
                    krw = get_balance("KRW") # 잔고 조회
                    if krw > 5000: # 최소거래금액
                        upbit.buy_market_order(pick, krw*0.9995) # 수수료 고려
                        logging.info(now, " : buy ", pick)
            else: # 매도
                print(now, ", 매도 시그널", pick)
                amount = upbit.get_balance(pick[4:])
                if amount > 0:
                    upbit.sell_market_order(pick, amount)
                    logging.info(now, " : sell ", pick)
            time.sleep(1)
                    
    except Exception as e:
        print(e)
        logging.error(e)
        time.sleep(1)
