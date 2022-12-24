from datetime import datetime
import pandas as pd
import aiohttp
import asyncio

MARKET = 'ETHUSDT'
MARKET_ALT = 'ETH-USD'
MARKET_ALT_2 = 'ETH-USDT'

PRICE_DATA_DTO = {
        'Time': None,
        'Binance': {
            'Bid': 0,
            'Ask': 0
        },
        'Coinbase': {
            'Bid': 0,
            'Ask': 0
        },
        'Kraken': {
            'Bid': 0,
            'Ask': 0
        },
        'Kucoin': {
            'Bid': 0,
            'Ask': 0
        },
        'Bitfinex': {
            'Bid': 0,
            'Ask': 0
        }
    }

async def async_parse():
    result = []
    urls = [
    f'https://api.binance.com/api/v3/ticker/price?symbol={MARKET}',
    f'https://api.kraken.com/0/public/Ticker?pair={MARKET}',
    f'https://api.pro.coinbase.com/products/{MARKET_ALT}/ticker',
    f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={MARKET_ALT_2}'
    ]
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as resp:
                result.append(await resp.json())
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S"), result

def complie() -> dict:
    new_data = PRICE_DATA_DTO
    time, resp = asyncio.run(async_parse()) 
    
    new_data['Time'] = time
    for res in resp:
        if 'result' in res.keys():
            new_data['Kraken']['Bid'] = res['result'][f'{MARKET}']['b'][0]
            new_data['Kraken']['Ask'] = res['result'][f'{MARKET}']['a'][0]
        elif 'ask' in res.keys():
            new_data['Coinbase']['Ask'] = res['ask']
            new_data['Coinbase']['Bid'] = res['bid']
        elif 'data' in res.keys():
            new_data['Kucoin']['Bid'] = res['data']['bestBid']
            new_data['Kucoin']['Ask'] = res['data']['bestAsk']
        elif 'price' in res.keys():
            new_data['Binance']['Bid'] = res['price']
            new_data['Binance']['Bid'] = res['price']
    return new_data

class parse:
    def __init__(self):
        


if __name__ == '__main__':
    print(complie())