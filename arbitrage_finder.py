import parse_data_class as parser
from dto import BALANCE_DTO, ARBITRAGE_DATA_DTO

class Arbitrage:
    def __init__(self):
        self.parser_object = parser.Parser()
        self.threshold = 0
        self.balance = BALANCE_DTO
        self.arbitrage_history = ARBITRAGE_DATA_DTO
        
    def __find_best_deal(self):
        self.parser_object.get_data()
        self.trades = {
            'min_ask': {
                'market': None,
                'value': float('inf'),
            },
            'max_bid': {
                'market': None,
                'value': 0,
            }
        }
        for market in self.parser_object.markets:
            if self.parser_object.data[market]['Bid'][-1] > self.trades['max_bid']['value']:
                self.trades['max_bid']['value'] = self.parser_object.data[market]['Bid'][-1]
                self.trades['max_bid']['market'] = market
                
            if self.parser_object.data[market]['Ask'][-1] < self.trades['min_ask']['value']:
                self.trades['min_ask']['value'] = self.parser_object.data[market]['Ask'][-1]
                self.trades['min_ask']['market'] = market
                
        diff = (self.trades['max_bid']['value'] / self.trades['min_ask']['value'] - 1) * 100
        diffabs = self.trades['max_bid']['value'] - self.trades['min_ask']['value']
        if diffabs > self.threshold:
            self.arbitrage_history['Time'].append(self.parser_object.data['Time'][-1])
            
            self.arbitrage_history['buy_price'].append(self.trades['min_ask']['value'])
            self.arbitrage_history['buy_at'].append(self.trades['min_ask']['market'])
            
            self.arbitrage_history['sell_price'].append(self.trades['max_bid']['value'])
            self.arbitrage_history['sell_at'].append(self.trades['max_bid']['market'])
            
            self.arbitrage_history['diff'].append(round(diff, 4))
            self.arbitrage_history['diffabs'].append(diffabs)
            
    def get_metrics(self):
        self.__find_best_deal()
        return self.parser_object.data, self.arbitrage_history, self.trades
            
if __name__ == '__main__':
    arbitrage = Arbitrage()
    print(arbitrage.get_metrics())