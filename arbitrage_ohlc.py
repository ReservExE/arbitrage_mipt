import pandas as pd
import numpy as np
from datetime import datetime
import requests

import plotly.subplots as sp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

#coinbase
#binance
#kraken
#kucoin
#bitfinex

#coinbase-binance
#coinbase-kraken
#coinbase-kucoin
#coinbase-bitfinex
#binance-kraken
#binance-kucoin
#binance-bitfinex
#kraken-kucoin
#kraken-bitfinex
#kucoin-bitfinex

START_TEST = '2022-12-01'
END_TEST = '2022-12-15'

MARKET = 'ETHUSDT'
MARKET_KUCOIN = 'ETH-USDT'
MARKET_BITFINEX = 'tETHUSD'

START_TIME = int(datetime.strptime('2022-12-16', '%Y-%m-%d').timestamp())
FINISH_TIME = int(datetime.strptime('2022-12-17', '%Y-%m-%d').timestamp())

START_TIME_EXT = int(datetime.strptime('2022-12-16', '%Y-%m-%d').timestamp() * 1000)
FINISH_TIME_EXT = int(datetime.strptime('2022-12-17', '%Y-%m-%d').timestamp() * 1000)

TICK_INTERVAL_KUCOIN = '1hour'
TICK_INTERVAL_BINANCE = '1h'
TICK_INTERVAL_KRAKEN = '60'
TICK_INTERVAL_BITFINEX = '1h'

def get_unix_timestamp(datestamp: str, platform: str=None) -> int:
    if platform == 'binance':
        return int(datetime.strptime(datestamp, '%Y-%m-%d').timestamp() * 1000)
    elif platform == 'bitfinex':
        return int(datetime.strptime(datestamp, '%Y-%m-%d').timestamp() * 1000)
    elif platform == 'coinbase':
        return datestamp + 'T00:00:00'
    
    return int(datetime.strptime(datestamp, '%Y-%m-%d').timestamp())

def ms_to_dt_local(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000)

def ms_to_dt_local_bitfinex(ms: int) -> datetime:
    return datetime.fromtimestamp(ms // 1000.0)

def ms_to_dt_local_kraken(ms: int) -> datetime:
    return datetime.fromtimestamp(ms)

#OHLC BINANCE
def get_ohlc_data_from_binance() -> pd.DataFrame:
    start_date = get_unix_timestamp(START_TEST, 'binance')
    finish_date = get_unix_timestamp(END_TEST, 'binance')
    
    url = f'https://api.binance.com/api/v3/klines?symbol={MARKET}&interval={TICK_INTERVAL_BINANCE}&startTime={start_date}&endTime={finish_date}'
    df = pd.read_json(url)
    df.columns = ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', 'Quote asset volume', 'Number of trades','Taker by base', 'Taker buy quote', 'Ignore']
    df["Opentime"] = df["Opentime"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    #df["Opentime"] = df["Opentime"].apply(lambda x: ms_to_dt_local(x))
    #df["Closetime"] = df["Closetime"].apply(lambda x: ms_to_dt_local(x))
    
    return df

#OHLC KRAKEN
def get_ohlc_data_from_kraken() -> pd.DataFrame: 
    start_date = get_unix_timestamp(START_TEST, 'kraken')
    finish_date = get_unix_timestamp(END_TEST, 'kraken')
    
    url = f'https://api.kraken.com/0/public/OHLC?pair={MARKET}&since={start_date}&interval={TICK_INTERVAL_KRAKEN}'
    resp = requests.get(url)
    df = pd.DataFrame(resp.json()['result'][f'{MARKET}'])
    df.columns = ['Opentime', 'Open', 'High', 'Low', 'Close', 'vwap', 'volume', 'count']
    #df["Opentime"] = df["Opentime"].apply(lambda x: ms_to_dt_local_kraken(x))
    df["Opentime"] = df["Opentime"].apply(lambda x: pd.to_datetime(x, unit='s'))
    
    return df

#OHLC kucoin
def get_ohlc_data_from_kucoin() -> pd.DataFrame:
    start_date = get_unix_timestamp(START_TEST, 'kucoin')
    finish_date = get_unix_timestamp(END_TEST, 'kucoin')    
    
    url = f'https://api.kucoin.com/api/v1/market/candles?type={TICK_INTERVAL_KUCOIN}&symbol={MARKET_KUCOIN}&startAt={start_date}&endAt={finish_date}'
    resp = requests.get(url)
    df = pd.DataFrame(resp.json()['data'])
    df.columns = ['Opentime', 'Open', 'Close', 'High', 'Low', 'Volume', 'Amount']
    #df['Opentime'] = df['Opentime'].astype('int')
    #df["Opentime"] = df["Opentime"].apply(lambda x: ms_to_dt_local_kraken(x))
    df["Opentime"] = df["Opentime"].apply(lambda x: pd.to_datetime(x, unit='s'))
    
    return df

#OHLC bitfinex
def get_ohlc_data_from_bitfinex() -> pd.DataFrame:
    start_date = get_unix_timestamp(START_TEST, 'bitfinex')
    finish_date = get_unix_timestamp(END_TEST, 'bitfinex')    
    
    url = f'https://api-pub.bitfinex.com/v2/candles/trade:{TICK_INTERVAL_BITFINEX}:{MARKET_BITFINEX}/hist?start={start_date}&end={finish_date}&sort=1'
    resp = requests.get(url)
    df = pd.DataFrame(resp.json())
    df.columns = ['Opentime', 'Open', 'Close', 'High', 'Low', 'Volume']
    df["Opentime"] = df["Opentime"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    
    return df

#OHLC coinbase
def get_ohlc_data_from_coinbase() -> pd.DataFrame:
    start_date = get_unix_timestamp(START_TEST, 'coinbase')
    finish_date = get_unix_timestamp(END_TEST, 'coinbase')
    tick = '3600'
    market = 'ETH-USD'
    
    url = f'https://api.pro.coinbase.com/products/{market}/candles?start={start_date}&end={finish_date}&granularity={tick}'
    resp = requests.get(url)
    df = pd.DataFrame(resp.json())
    df.columns = ['Opentime', 'Low', 'High', 'Open', 'Close', 'Volume']
    df["Opentime"] = df["Opentime"].apply(lambda x: pd.to_datetime(x, unit='s'))
    
    return url
    
def draw_ohlc_timeline():
    result = get_ohlc_data_from_binance()[['Opentime', 'Close']]
    result = result.merge(get_ohlc_data_from_kraken()[['Opentime', 'Close']], on='Opentime', how='left')
    result = result.merge(get_ohlc_data_from_kucoin()[['Opentime', 'Close']], on='Opentime', how='left')
    result = result.merge(get_ohlc_data_from_bitfinex()[['Opentime', 'Close']], on='Opentime', how='left')
    result.columns = ['Opentime', 'Binance_close', 'Kraken_close', 'Kucoin_close', 'Bitfinex_close']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result['Opentime'], y=result['Binance_close'], mode='lines+markers', name='Binance'))
    fig.add_trace(go.Scatter(x=result['Opentime'], y=result['Kraken_close'], mode='lines+markers', name='Kraken'))
    fig.add_trace(go.Scatter(x=result['Opentime'], y=result['Kucoin_close'], mode='lines+markers', name='Kucoin'))
    fig.add_trace(go.Scatter(x=result['Opentime'], y=result['Bitfinex_close'], mode='lines+markers', name='Bitfinex'))
    
    fig.update_xaxes(showgrid=True, linecolor='black', mirror=True, ticks="inside")
    fig.update_yaxes(showgrid=True, linecolor='black', mirror=True, gridcolor='LightGray')

    fig.update_layout(
    title=dict(
        text='Динамика цен ETH/USDT на криптобиржах',
        xref='paper'),
        
    xaxis=dict(
        title='Дата, час',
        tickmode='linear'),
        
    yaxis=dict(
        title='Цена, USDT'),
        
    plot_bgcolor='#ffffff',
    )

    fig.show()
    
    return result.dropna()

def draw_ohlc_timeline_test():
    fig = go.Figure()
    df = get_ohlc_data_from_binance()[['Opentime', 'Close']]
    fig.add_trace(go.Scatter(x=df['Opentime'], y=df['Close'], mode='lines+markers', name='Binance'))
    df = get_ohlc_data_from_kraken()[['Opentime', 'Close']]
    fig.add_trace(go.Scatter(x=df['Opentime'], y=df['Close'], mode='lines+markers', name='Kraken'))
    df = get_ohlc_data_from_kucoin()[['Opentime', 'Close']]
    fig.add_trace(go.Scatter(x=df['Opentime'], y=df['Close'], mode='lines+markers', name='Kucoin'))
    df = get_ohlc_data_from_bitfinex()[['Opentime', 'Close']]
    fig.add_trace(go.Scatter(x=df['Opentime'], y=df['Close'], mode='lines+markers', name='Bitfinex'))

    fig.update_xaxes(showgrid=True, linecolor='black', mirror=True, ticks="inside")
    fig.update_yaxes(showgrid=True, linecolor='black', mirror=True, gridcolor='LightGray')

    fig.update_layout(
    title=dict(
        text='Динамика цен ETH/USDT на криптобиржах',
        xref='paper'),
        
    xaxis=dict(
        title='Дата',
        tickmode='linear'),
        
    yaxis=dict(
        title='Дата, час'),

    font=dict(
        family='verdana'),
        
    plot_bgcolor='#ffffff',
    
    boxgap=1
    )

    fig.show()

if __name__ == '__main__':
    print(draw_ohlc_timeline())
    #print(get_ohlc_data_from_bitfinex())


















#print(get_klines_iter(START_TIME, FINISH_TIME))
#print(get_klines_iter('#2022-12-16', '2022-12-16'))
#time = ms_to_dt_local(1669345200000)
#print(time.strftime("%H:%M:%S"))



#def get_klines_iter(start, end):
#    df = pd.DataFrame()
#    startDate = end
#    while startDate>start:
#        #url = 'https://api.binance.com/api/v3/klines?symbol=' + \
#        #    market + '&interval=' + tick_interval + '&startTime=' + start + '&endTime=' + end
#        url = 'https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1h&endTime=1671138000000'
#        
#        df2 = pd.read_json(url)
#        df2.columns = ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', 'Quote asset volume', 'Number of trades','Taker by base', 'Taker buy quote', 'Ignore']
#        df = pd.concat([df2, df], axis=0, ignore_index=True, keys=None)
#        startDate = df.Opentime[0]   
#    df.reset_index(drop=True, inplace=True)    
#    return df 