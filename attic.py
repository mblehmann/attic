import json

from stocks.stock import StockPortfolio, StockEncoder, StockDecoder


class Attic:

    def __init__(self):
        self._stocks = StockPortfolio()

    def save(self, filename):
        with open(filename, 'w') as file_output:
            json.dump(self._stocks, file_output, cls=StockEncoder, indent=4, separators=(',', ': '))

    def load(self, filename):
        with open(filename) as file_input:
            self._stocks = json.load(file_input, cls=StockDecoder)


if __name__ == '__main__':
    attic = Attic()
    attic.load('stocks/test.json')

    print(attic._stocks.cost_value)
    print(attic._stocks.market_value)
    print(attic._stocks.fees)
    print(attic._stocks.dividends)
