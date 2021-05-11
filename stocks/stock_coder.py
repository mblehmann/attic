import json
from datetime import datetime

from stocks.stock import Portfolio, Stock, Wallet, Results
from stocks.transaction import Transaction, BuyTransaction, SellTransaction, DividendTransaction, TaxTransaction


class StockEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Results):
            return self.encode_results(obj)
        elif isinstance(obj, Wallet):
            return self.encode_wallet(obj)
        elif isinstance(obj, Stock):
            return self.encode_stock(obj)
        elif isinstance(obj, Portfolio):
            return self.encode_portfolio(obj)
        elif isinstance(obj, Transaction):
            return self.encode_transaction(obj)
        elif isinstance(obj, datetime):
            return self.encode_datetime(obj)

        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def encode_results(obj):
        return {
            'type': 'Results',
            'event': obj.event,
            'gains': obj.data['gains'],
            'dividends': obj.data['dividends'],
            'fees': obj.data['fees'],
            'taxes': obj.data['taxes'],
        }

    @staticmethod
    def encode_wallet(obj):
        return {
            'type': 'Wallet',
            'shares': obj.shares,
            'buy_price': obj.buy_price,
            'results': obj.results,
            'transactions': obj.transactions,
        }

    @staticmethod
    def encode_stock(obj):
        return {
            'type': 'Stock',
            'symbol': obj.symbol,
            'wallet': obj.wallet,
        }

    @staticmethod
    def encode_portfolio(obj):
        return {
            'type': 'Portfolio',
            'stocks': obj.data,
        }

    @staticmethod
    def encode_transaction(obj):
        return {
            'type': 'Transaction',
            'data': obj.data,
        }

    @staticmethod
    def encode_datetime(obj):
        return {
            'type': 'Datetime',
            'day': obj.strftime('%d.%m.%Y')
        }


class StockDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'type' not in obj:
            return obj

        if obj['type'] == 'Results':
            return self.parse_results(obj)
        elif obj['type'] == 'Wallet':
            return self.parse_wallet(obj)
        elif obj['type'] == 'Stock':
            return self.parse_stock(obj)
        elif obj['type'] == 'Portfolio':
            return self.parse_portfolio(obj)
        elif obj['type'] == 'Transaction':
            return self.parse_transaction(obj)
        elif obj['type'] == 'Datetime':
            return self.parse_datetime(obj)
        return obj

    @staticmethod
    def parse_results(obj):
        return Results(**obj)

    @staticmethod
    def parse_wallet(obj):
        return Wallet(**obj)

    @staticmethod
    def parse_stock(obj):
        return Stock(**obj)

    @staticmethod
    def parse_portfolio(obj):
        return Portfolio(**obj)

    @staticmethod
    def parse_transaction(obj):
        if obj['data']['transaction'] == 'Buy':
            return BuyTransaction(**obj['data'])
        elif obj['data']['transaction'] == 'Sell':
            return SellTransaction(**obj['data'])
        elif obj['data']['transaction'] == 'Dividend':
            return DividendTransaction(**obj['data'])
        elif obj['data']['transaction'] == 'Tax':
            return TaxTransaction(**obj['data'])

    @staticmethod
    def parse_datetime(obj):
        return datetime.strptime(obj['day'], '%d.%m.%Y')
