from datetime import datetime
import pandas as pd
import aiohttp
import asyncio
from time import sleep
from dto import PRICE_DATA_DTO

MARKET = 'ETHUSDT'
MARKET_ALT = 'ETH-USD'
MARKET_ALT_2 = 'ETH-USDT'


class Parser:
    def __init__(self):
        self.urls = [
            f'https://api.binance.com/api/v3/ticker/bookTicker?symbol={MARKET}',
            f'https://api.kraken.com/0/public/Ticker?pair={MARKET}',
            f'https://api.pro.coinbase.com/products/{MARKET_ALT}/ticker',
            f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={MARKET_ALT_2}'
            ]
        self.data = PRICE_DATA_DTO
        self.markets = ['Binance', 'Coinbase', 'Kraken', 'Kucoin']
        
    async def __async_parse(self):
        result = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                async with session.get(url) as resp:
                    result.append(await resp.json())
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S"), result
    
    def __compile(self) -> dict:
        time, resp = asyncio.run(self.__async_parse()) 
        self.data['Time'].append(time) 
        
        for res in resp:
            if 'result' in res.keys():
                self.data['Kraken']['Bid'].append(float(res['result'][f'{MARKET}']['b'][0]))
                self.data['Kraken']['Ask'].append(float(res['result'][f'{MARKET}']['a'][0]))
                self.data['Kraken']['Spread'].append(float(res['result'][f'{MARKET}']['a'][0]) - float(res['result'][f'{MARKET}']['b'][0]))
            elif 'ask' in res.keys():
                self.data['Coinbase']['Bid'].append(float(res['bid']))
                self.data['Coinbase']['Ask'].append(float(res['ask']))
                self.data['Coinbase']['Spread'].append(float(res['ask']) - float(res['bid']))
            elif 'data' in res.keys():
                self.data['Kucoin']['Bid'].append(float(res['data']['bestBid']))
                self.data['Kucoin']['Ask'].append(float(res['data']['bestAsk']))
                self.data['Kucoin']['Spread'].append(float(res['data']['bestAsk']) - float(res['data']['bestBid']))
            elif 'askPrice' in res.keys():
                self.data['Binance']['Bid'].append(float(res['bidPrice']))
                self.data['Binance']['Ask'].append(float(res['askPrice']))
                self.data['Binance']['Spread'].append(float(res['askPrice']) - float(res['bidPrice']))
        
    def get_data(self):
        self.__compile()
        return self.data
    
if __name__ == '__main__':
    parser = Parser()
    while(True):
        parser.compile()
        print(parser.get_data())
        sleep(5)
        