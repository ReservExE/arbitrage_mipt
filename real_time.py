import pandas as pd
import requests
import asyncio
import aiohttp
from datetime import datetime
from time import sleep

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
from dash.dependencies import Output, Input
from dash import dcc, html

MARKET = 'ETHUSDT'
MARKET_COINBASE = 'ETH-USD'
data = {
        'X': [],
        'Kraken': {
            'Y': []
        },
        'Coinbase': {
            'Y': []
        }

    }

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='graph-update',
        interval=5000,
        n_intervals=0
    )
])

async def async_parse():
    result = []
    urls = [
    f'https://api.binance.com/api/v3/ticker/price?symbol={MARKET}',
    f'https://api.kraken.com/0/public/Ticker?pair={MARKET}',
    f'https://api.pro.coinbase.com/products/{MARKET_COINBASE}/ticker',
    ]
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as resp:
                result.append(await resp.json())
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S"), result

def compile_row(resp: list, time) -> pd.DataFrame:
    df = pd.DataFrame(columns=['Time', 'Kraken_bid', 'Kraken_ask', 'Coinbase_bid', 'Coinbase_ask'])
    df.at[0, 'Time'] = time
    for res in resp:
        if 'result' in res.keys():
            df.at[0, 'Kraken_ask'] = res['result'][f'{MARKET}']['a'][0]
            df.at[0, 'Kraken_bid'] = res['result'][f'{MARKET}']['b'][0]
        elif 'ask' in res.keys():
            df.at[0, 'Coinbase_ask'] = res['ask']
            df.at[0, 'Coinbase_bid'] = res['bid']
    return df


@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'n_intervals')) 
def update_graph(n):
    time, resp = asyncio.run(async_parse())
    result = compile_row(resp, time)
    
    data['X'].append(time)
    data['Kraken']['Y'].append(float(result.iloc[0]['Kraken_ask']))
    data['Coinbase']['Y'].append(float(result.iloc[0]['Coinbase_ask']))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['X'],
        y=data['Kraken']['Y'],
        name='Kraken',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=data['X'],
        y=data['Coinbase']['Y'],
        name='Coinbase',
        mode='lines+markers'
    ))
    
    return fig

#def main():
#    MAIN_DF = pd.DataFrame(columns=['Time', 'Kraken_bid', 'Kraken_ask', 'Coinbase_bid', 'Coinbase_ask'])
#    while(True):
#        time, result = asyncio.run(async_parse())
#        MAIN_DF = MAIN_DF.append(compile_row(resp=result, time=time))
#        print(MAIN_DF)
#        sleep(10)
    
if __name__ == '__main__':
    app.run_server(debug=True)
