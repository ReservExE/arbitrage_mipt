#Plotly/Dash
import plotly.graph_objects as go
import dash
from dash.dependencies import Output, Input
from dash import dcc, html

#Parser class
import arbitrage_finder as arb


#def update_data():
#    global arbitrage
#    global data
#    global arbitrage_history
#    arbitrage = arb_obj.Arbitrage()
#    data, arbitrage_history = arbitrage.get_metrics()
arbitrage = arb.Arbitrage()
app = dash.Dash(__name__)

colors = {
    'background': 'rgb(229, 230, 228, 1)',
    'text': 'rgb(69, 72, 81, 1)'
}

app.layout = html.Div([
        html.Div([
            html.Div(id='latest-timestamp', style={"padding": "20px"}),
            dcc.Interval(id='data-update', interval=10000, n_intervals=0),
            dcc.Store(id='price_data', data={}),
            dcc.Store(id='arbitrage_data', data={}),
            dcc.Store(id='trades_data', data={})
        ]),

        html.Div([
            html.Div(dcc.Graph(id='live-graph')),
            html.Div(dcc.Graph(id='live-table')),
            html.Div(dcc.Graph(id='arbitrage-table')),
        ])
    ])
    
@app.callback(Output(component_id='latest-timestamp', component_property='children'),
              Output(component_id='price_data', component_property='data'),
              Output(component_id='arbitrage_data', component_property='data'),
              Output(component_id='trades_data', component_property='data'),
              Input('data-update', 'n_intervals')) 
def update_data(n):
    data, arbitrage_history, trades = arbitrage.get_metrics()
    return data['Time'][-1], data, arbitrage_history, trades

@app.callback(Output(component_id='live-graph', component_property='figure'),
              Input('price_data', 'data'),
              Input('arbitrage_data', 'data')
              ) 
def update_graph(data, arbitrage_history):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Time'],
        y=data['Kraken']['Bid'],
        error_y=dict(
            type='data',
            array=data['Kraken']['Spread'],
            arrayminus=[0],
            thickness=2,
            visible=True),
        marker_color='rgb(76, 201, 240, 0.25)',
        name='Kraken',
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=data['Time'],
        y=data['Coinbase']['Bid'],
        error_y=dict(
            type='data',
            array=data['Coinbase']['Spread'],
            arrayminus=[0],
            thickness=2,
            visible=True),
        marker_color='rgb(72, 149, 239, 0.25)',
        name='Coinbase',
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=data['Time'],
        y=data['Kucoin']['Bid'],
        error_y=dict(
            type='data',
            array=data['Kucoin']['Spread'],
            arrayminus=[0],
            thickness=2,
            visible=True),
        marker_color='rgb(67, 97, 238, 0.25)',
        name='Kucoin',
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=data['Time'],
        y=data['Binance']['Bid'],
        error_y=dict(
            type='data',
            array=data['Binance']['Spread'],
            arrayminus=[0],
            thickness=2,
            visible=True),
        marker_color='rgb(72, 12, 168, 0.25)',
        name='Binance',
        mode='markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=arbitrage_history['Time'],
        y=arbitrage_history['sell_price'],
        error_y=dict(
            type='data',
            arrayminus=arbitrage_history['diffabs'],
            array=[0],
            thickness=2,
            visible=True),
        name='Арбитраж',
        marker_color='rgb(247, 37, 133, 1)',
        text=arbitrage_history['diff'],
        mode='markers'
    ))
    
    fig.update_layout(
    title = 'Ряд цен-Bid на пару ETH/USDT',
    yaxis=dict(
        title='Курс ETH/USDT'),
    xaxis=dict(
        title='Время выгрузки'),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    ),
    
    fig.update_xaxes(
        dtick = 3600000.0
    )
    return fig

@app.callback(Output(component_id='live-table', component_property='figure'),
              Input('trades_data', 'data'))
def update_table(trades_data):
    table = go.Figure(data=[go.Table(
    header=dict(values=['min_ask', 'max_bid'],
                align='left',
                fill_color=colors['background'],
                font = dict(color=colors['text'], size = 11)
                ),
    cells=dict(values=[str(trades_data['min_ask']['market']) + ": " + str(trades_data['min_ask']['value']), # 1st column
                       str(trades_data['max_bid']['market']) + ": " + str(trades_data['max_bid']['value'])], # 2nd column
               line_color=colors['background'],
               fill_color=colors['background'],
               font = dict(color=colors['text'], size = 11),
               align='left'))
    ])
    return table

@app.callback(Output(component_id='arbitrage-table', component_property='figure'),
              Input('arbitrage_data', 'data'))
def update_table(arbitrage_data):
    table = go.Figure(data=[go.Table(
    header=dict(values=['Time', 'buy_at', 'buy_price', 'sell_at', 'sell_price', 'diff, %', 'diffabs'],
                align='left',
                fill_color=colors['background'],
                font = dict(color=colors['text'], size = 11)
                ),
    cells=dict(values=[arbitrage_data['Time'],
                       arbitrage_data['buy_at'],
                       arbitrage_data['buy_price'],
                       arbitrage_data['sell_at'],
                       arbitrage_data['sell_price'],
                       arbitrage_data['diff'],
                       arbitrage_data['diffabs'],
                       ], 
               line_color=colors['background'],
               fill_color=colors['background'],
               font = dict(color=colors['text'], size = 11),
               align='left'))
    ])
    return table

if __name__ == '__main__':
    app.run_server(debug=True)
