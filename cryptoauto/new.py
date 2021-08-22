import time
import pyupbit
import datetime
import requests

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

def ticker_selection(flag): ###changed
    """24시간 누적 거래대금 최대 티커 선별"""
    tickers = pyupbit.get_tickers(fiat="KRW")
    res = requests.request('GET', 'https://api.upbit.com/v1/ticker', params={'markets': ','.join(tickers)})
    ticker_dat = res.json()
    traded = {}
    ticker_data = list()
    ticker_trade_price = 0
    
    for i in ticker_dat:
        if 0.01 < i['signed_change_rate']:
            ticker_data.append(i)

    ticker = ''

    if flag == 1:
        for i in ticker_data:
            traded[i['market']] = i['acc_trade_price']###changed
            if ticker_trade_price < i['acc_trade_price']:
                ticker = i['market']
                ticker_trade_price = i['acc_trade_price']
    elif flag == 2:
        for i in ticker_data:
            traded[i['market']] = i['acc_trade_price_24h'] - i['acc_trade_price']###changed
            if ticker_trade_price < i['acc_trade_price_24h'] - i['acc_trade_price']:
                ticker = i['market']
                ticker_trade_price = i['acc_trade_price_24h'] - i['acc_trade_price']
    else:
        return None
    return ticker

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade Start")

time.sleep(7)
pick = ''
now_pick = ''
now_price = 0

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now() + datetime.timedelta(hours=9)
        start_time = get_start_time("KRW-BTC") - datetime.timedelta(minutes=3) # 최근 시간봉 시작시간
        end_time = start_time + datetime.timedelta(hours=1) - datetime.timedelta(minutes=3)

        df_tmp = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=1) # UTC 00:00

        # 0~6 => flag 1, 12~18 => flag 2
        if df_tmp.index[0] < now < df_tmp.index[0] + datetime.timedelta(hours=12):
            flag = 1
            krw = get_balance("KRW") # 잔고 조회
            if krw > 5000: # 최소거래금액
                ticker = ticker_selection(flag)

            if bool(ticker):
                k = 0
                if start_time < now < end_time - datetime.timedelta(seconds=10): ## 무한루프 방지(차트보고 바꿀수도)
                    pick = ticker
                    target_price = get_target_price(pick, k) ## 매수 목표가 계산
                    current_price = get_current_price(pick) ## 현재가 조회
                    if target_price < current_price:
                        btc = get_balance("BTC")
                        if btc > 0.00008: # 최소거래금액 이상
                            upbit.sell_market_order("KRW-BTC", btc*0.9995) # 수수료 고려
                        krw = get_balance("KRW") # 잔고 조회
                        if krw > 5000 and pick != now_pick: # 최소거래금액
                            upbit.buy_market_order(pick, krw*0.9995) # 수수료 고려
                            print(now, " : buy ", pick)
                            now_pick = pick
                            now_price = current_price
                    now_amount = upbit.get_balance(now_pick[4:])
                    if bool(now_amount):
                        if now_price * 1.06 < get_current_price(now_pick):
                            upbit.sell_market_order(now_pick, amount)
                            print("Good!")
                        elif get_current_price(now_pick) < now_price * 1.03:
                            upbit.sell_market_order(now_pick, amount)
                            print("Bad!")
                else: # 매도
                    amount = upbit.get_balance(pick[4:])
                    if amount > 0:
                        upbit.sell_market_order(pick, amount)
                        # most_traded_old = most_traded(20, now, flag)
                        print(now, " : sell ", pick)
                        ticker = ''
                    else:
                        print(now, " nothing to sell, ", pick)
                        # most_traded_old = most_traded(20, now, flag)
            else:
                time.sleep(1)

        elif df_tmp.index[0] + datetime.timedelta(hours=12) < now < df_tmp.index[0] + datetime.timedelta(hours=24):
            flag = 2
            krw = get_balance("KRW") # 잔고 조회
            if krw > 5000: # 최소거래금액
                ticker = ticker_selection(flag)

            if bool(ticker):
                k = 0
                if start_time < now < end_time - datetime.timedelta(seconds=10): ## 무한루프 방지(차트보고 바꿀수도)
                    pick = ticker
                    target_price = get_target_price(pick, k) ## 매수 목표가 계산
                    current_price = get_current_price(pick) ## 현재가 조회
                    if target_price < current_price:
                        btc = get_balance("BTC")
                        if btc > 0.00008: # 최소거래금액 이상
                            upbit.sell_market_order("KRW-BTC", btc*0.9995) # 수수료 고려
                        krw = get_balance("KRW") # 잔고 조회
                        if krw > 5000: # 최소거래금액
                            upbit.buy_market_order(pick, krw*0.9995) # 수수료 고려
                            print(now, " : buy ", pick)
                else: # 매도
                    amount = upbit.get_balance(pick[4:])
                    if amount > 0:
                        upbit.sell_market_order(pick, amount)
                        print(now, " : sell ", pick)
                        ticker = ''
                    else:
                        print(now, " nothing to sell, ", pick)
            else:
                time.sleep(1)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
