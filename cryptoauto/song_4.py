import time
import pyupbit
import datetime
import requests
import operator

access = "9afurEZJQTqYlNq9an45r2xaB1nNFF6xbTPS7or9"
secret = "3fQEcrOLhdWT2Krh122OmR7fuibQ3xNqsDjUi7uV"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes240", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return round(target_price * 0.9995)

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes240", count=1) # 시간봉
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

def most_traded(cnt, now): ###changed
    """24시간 누적 거래대금 최대 티커 선별"""
    tickers = pyupbit.get_tickers(fiat="KRW")
    res = requests.request('GET', 'https://api.upbit.com/v1/ticker', params={'markets': ','.join(tickers)})
    ticker_data = res.json()
    traded = {}
    most_traded_set = set()
    df_tmp = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=1) # UTC 00:00

    if df_tmp.index[0] < now < df_tmp.index[0] + datetime.timedelta(hours=4):
        for i in ticker_data:
            if i['market'] not in ["KRW-BTC", "KRW-ETH", "KRW-XRP"]:
                traded[i['market']] = i['acc_trade_price']###changed
    elif df_tmp.index[0] + datetime.timedelta(hours=12) < now < df_tmp.index[0] + datetime.timedelta(hours=16):
        for i in ticker_data:
            if i['market'] not in ["KRW-BTC", "KRW-ETH", "KRW-XRP"]:
                traded[i['market']] = i['acc_trade_price_24h'] - i['acc_trade_price']###changed
    else: return most_traded_set

    # if df_tmp.index[0] < now < df_tmp.index[0] + datetime.timedelta(hours=12):
    #     for i in ticker_data:
    #         if i['market'] not in ["KRW-BTC", "KRW-ETH", "KRW-XRP"]:
    #             traded[i['market']] = i['acc_trade_price']###changed
    # else:
    #     for i in ticker_data:
    #         if i['market'] not in ["KRW-BTC", "KRW-ETH", "KRW-XRP"]:
    #             traded[i['market']] = i['acc_trade_price_24h'] - i['acc_trade_price']###changed

    sorted_traded = sorted(traded.items(), key=operator.itemgetter(1), reverse=True)
    
    for i in range(cnt):
        most_traded_set.add(sorted_traded[i][0])
    return most_traded_set

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
print("Autotrade Start")

most_traded_old = most_traded(27, datetime.datetime.now())
pick = "KRW-BTC"
flag = 0

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # 최근 시간봉 시작시간
        end_time = start_time + datetime.timedelta(hours=4)
        if not flag:
            most_traded_set = most_traded(18, now)
            most_traded_set -= most_traded_old #거래량 급증 코인 확인
            ticker = ticker_selection(most_traded_set)

        if bool(ticker):
            pick = ticker
            k = -0.1
            if start_time < now < end_time - datetime.timedelta(seconds=10): ## 무한루프 방지(차트보고 바꿀수도)
                if not flag:
                    target_price = get_target_price(pick, k) ## 매수 목표가 계산
                current_price = get_current_price(pick) ## 현재가 조회
                if target_price < current_price:
                    btc = get_balance("BTC")
                    if btc > 0.00008: # 최소거래금액 이상
                        upbit.sell_market_order("KRW-BTC", btc*0.9995) # 수수료 고려
                    krw = get_balance("KRW") # 잔고 조회
                    if krw > 5000: # 최소거래금액
                        upbit.buy_market_order(pick, krw*0.9995) # 수수료 고려
                        flag = 1
                        print(now, " : buy ", pick)
                if (current_price < target_price * 0.97) or (target_price * 1.1 < current_price): ###changed
                    amount = upbit.get_balance(pick[4:])
                    if amount > 0:
                        upbit.sell_market_order(pick, amount)
                        print(now, " : sell ", pick)
                        flag = 0
            else: # 매도
                amount = upbit.get_balance(pick[4:])
                if amount > 0:
                    upbit.sell_market_order(pick, amount)
                    flag = 0
                    print(now, " : sell ", pick)
                else:
                    print(now, " nothing to sell, ", pick)
                    most_traded_old = most_traded(27, now)
                    pick = "KRW-BTC"
            time.sleep(1)
        else:
            pick = "KRW-BTC"
            k = 0.5
            if start_time < now < end_time - datetime.timedelta(seconds=10): ## 무한루프 방지(차트보고 바꿀수도)
                if not flag:
                    target_price = get_target_price(pick, k) ## 매수 목표가 계산
                current_price = get_current_price(pick) ## 현재가 조회
                if target_price < current_price:
                    krw = get_balance("KRW") # 잔고 조회
                    if krw > 5000: # 최소거래금액
                        upbit.buy_market_order(pick, krw*0.9995) # 수수료 고려
                        flag = 1
                        print(now, " : buy ", pick)
                if (current_price < target_price * 0.99) or (target_price * 1.02 < current_price): ###changed
                    amount = upbit.get_balance(pick[4:])
                    if amount > 0:
                        upbit.sell_market_order(pick, amount)
                        flag = 0
                        print(now, " : sell ", pick)

            else: # 매도
                amount = upbit.get_balance(pick[4:])
                if amount > 0:
                    upbit.sell_market_order(pick, amount)
                    flag = 0
                    print(now, " : sell ", pick)
                else:
                    print(now, " nothing to sell, ", pick)
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)

