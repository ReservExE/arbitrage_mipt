#Данные о издержках на каждой бирже
FEES = {
    'kraken': {
        'Maker': 0.0016,
        'Taker': 0.0026,
    },
    'coinbase': {
        'Maker': 0.0060,
        'Taker': 0.0040,
    },
    'kucoin': {
        'Maker': 0.001,
        'Taker': 0.001,
    },
    'binance': {
        'Maker': 0.001,
        'Taker': 0.001
    },
    'bitfinex': {
        'Maker': 0.001,
        'Taker': 0.002,
    }
}

GRAPH_DTO = {
        'X': [],
        'Kraken': {
            'Y': []
        },
        'Coinbase': {
            'Y': []
        },
        'Binance': {
            'Y': []
        },
        'Kucoin': {
            'Y': []
        },
        'Bitfinex': {
            'Y': []
        }
    }

#Структура для хранения истории в классе парсера
PRICE_DATA_DTO = {
        'Time': [],
        'Binance': {
            'Bid': [],
            'Ask': [],
            'Spread': []
        },
        'Coinbase': {
            'Bid': [],
            'Ask': [],
            'Spread': []
        },
        'Kraken': {
            'Bid': [],
            'Ask': [],
            'Spread': []
        },
        'Kucoin': {
            'Bid': [],
            'Ask': [],
            'Spread': []
        },
        #'Bitfinex': {
        #    'Bid': [],
        #    'Ask': []
        #}
    }
#Структура для хранения арбитражных возможностей
ARBITRAGE_DATA_DTO = {
    'Time': [],
    'buy_at': [],
    'buy_price': [],
    'sell_at': [],
    'sell_price': [],
    'diff': [],
    'diffabs': [],
    }
#Структура для хранения баланса
BALANCE_DTO = {
        'Binance': {
            'USDT': 2000,
            'ETH': 1,
        },
        'Coinbase': {
            'USDT': 2000,
            'ETH': 1,
        },
        'Kraken': {
            'USDT': 2000,
            'ETH': 1,
        },
        'Kucoin': {
            'USDT': 2000,
            'ETH': 1,
        },
    }

trades = {
        'min_ask': {
            'market': None,
            'value': float('inf'),
        },
        'max_bid': {
            'market': None,
            'value': 0,
        }
        }