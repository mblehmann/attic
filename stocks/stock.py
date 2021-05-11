from pubsub import pub
from yfinance import Ticker

from stocks.transaction import BuyTransaction, SellTransaction, DividendTransaction, TaxTransaction


class Results:

    def __init__(self, event, **kwargs):
        self._event = event
        self._gains = kwargs.get('gains', 0)
        self._dividends = kwargs.get('dividends', 0)
        self._fees = kwargs.get('fees', 0)
        self._taxes = kwargs.get('taxes', 0)

    def set_subscriptions(self, symbol):
        pub.subscribe(self.provide_data, 'select.{}'.format(symbol))

    def provide_data(self, symbol=None):
        pub.sendMessage('stock.{}'.format(self._event), data=self.data)

    @property
    def event(self):
        return self._event

    @property
    def data(self):
        return {
            'profit': self.profit,
            'gains': self._gains,
            'dividends': self._dividends,
            'fees': self._fees,
            'taxes': self._taxes
        }

    @property
    def profit(self):
        return self._gains + self._dividends - (self._fees + self._taxes)

    def reset(self):
        self._gains = 0
        self._dividends = 0
        self._fees = 0
        self._taxes = 0

    def add_result(self, gain=0.0, dividend=0.0, fee=0.0, tax=0.0):
        self._gains += gain
        self._dividends += dividend
        self._fees += fee
        self._taxes += tax
        self.provide_data()


class Wallet:

    def __init__(self, **kwargs):
        self._shares = kwargs.get('shares', 0)
        self._buy_price = kwargs.get('buy_price', 0)
        self._results = kwargs.get('results', Results('results'))
        self._transactions = kwargs.get('transactions', {})
        self._projection = Results('projection')
        self._current_price = None
        self._last_dividend = None

    def set_subscriptions(self, symbol):
        pub.subscribe(self.provide_data, 'select.{}'.format(symbol))
        pub.subscribe(self.buy, 'buy.{}'.format(symbol))
        pub.subscribe(self.sell, 'sell.{}'.format(symbol))
        pub.subscribe(self.dividend, 'dividend.{}'.format(symbol))
        pub.subscribe(self.tax, 'tax.{}'.format(symbol))
        pub.subscribe(self.remove_transaction, 'remove.{}'.format(symbol))

        self._results.set_subscriptions(symbol)
        self._projection.set_subscriptions(symbol)

    def set_projection_data(self, price, dividend):
        self._current_price = price
        self._last_dividend = dividend
        self.update_projection(self.appreciation, self._last_dividend)

    @property
    def shares(self):
        return self._shares

    @property
    def buy_price(self):
        return self._buy_price

    @property
    def results(self):
        return self._results

    @property
    def projection(self):
        return self._projection

    @property
    def transactions(self):
        return self._transactions

    @property
    def position(self):
        return {
            'shares': self._shares,
            'avgBuyPrice': self._buy_price,
            'invested': self.invested,
            'marketValue': self.market_value,
            'growth': self.growth
        }

    @property
    def transaction_data(self):
        return {t.id: t.data for t in self._transactions.values()}

    @property
    def invested(self):
        return self._shares * self._buy_price

    @property
    def market_value(self):
        return self._shares * self._current_price

    @property
    def appreciation(self):
        return self.market_value - self.invested

    @property
    def growth(self):
        return self.appreciation / self.invested * 100 if self.invested > 0 else 0

    def execute_shares(self, amount, value=0):
        invested = self.invested
        self._shares += amount
        if amount > 0:
            self._buy_price = (invested + value) / self._shares
        self.update_projection(self.appreciation, self._last_dividend)

    def undo_shares(self, amount, value=0):
        invested = self.invested
        self._shares += amount
        if amount < 0:
            self._buy_price = (invested - value) / self._shares if self._shares > 0 else 0
        self.update_projection(self.appreciation, self._last_dividend)

    def add_transaction(self, transaction):
        self._transactions[transaction.id] = transaction
        self.provide_data()

    def remove_transaction(self, ids):
        for tid in ids:
            transaction = self._transactions.pop(tid)
            if isinstance(transaction, BuyTransaction):
                self.undo_buy(transaction)
            elif isinstance(transaction, SellTransaction):
                self.undo_sell(transaction)
            elif isinstance(transaction, DividendTransaction):
                self.undo_dividend(transaction)
            elif isinstance(transaction, TaxTransaction):
                self.undo_tax(transaction)
        self.provide_data()

    def update_projection(self, appreciation, dividend):
        self._projection.reset()
        projected_tax = appreciation * 0.275
        projected_dividend = self._shares * dividend
        projected_fee = 4.95 if self._shares else 0
        self._projection.add_result(gain=appreciation, dividend=projected_dividend,
                                    fee=projected_fee, tax=projected_tax)

    def provide_data(self, symbol=None):
        pub.sendMessage('stock.position', data=self.position)
        pub.sendMessage('stock.transactions', data=self.transaction_data)

    def buy(self, stock, day, amount, price, fee):
        t = BuyTransaction(day, amount, price, fee)
        self.execute_shares(t.amount, t.value)
        self._results.add_result(fee=t.fee)
        self.add_transaction(t)

    def sell(self, stock, day, amount, price, fee, tax):
        if amount > self._shares:
            pub.sendMessage('error',
                            message='Cannot sell more shares than owned ({} > {})'.format(amount, self._shares))
        else:
            t = SellTransaction(day, amount, price, fee, tax, self._buy_price)
            self.execute_shares(-t.amount)
            self._results.add_result(gain=t.gain, fee=t.fee, tax=t.tax)
            self.add_transaction(t)

    def dividend(self, stock, day, dividend, tax):
        t = DividendTransaction(day, dividend, tax)
        self._results.add_result(dividend=t.dividend, tax=t.tax)
        self.add_transaction(t)

    def tax(self, stock, day, tax):
        t = TaxTransaction(day, tax)
        self._results.add_result(tax=t.tax)
        self.add_transaction(t)

    def undo_buy(self, t):
        self.undo_shares(-t.amount, t.value)
        self._results.add_result(fee=-t.fee)

    def undo_sell(self, t):
        self.undo_shares(t.amount)
        self._results.add_result(gain=-t.gain, fee=-t.fee, tax=-t.tax)

    def undo_dividend(self, t):
        self._results.add_result(dividend=-t.dividend, tax=-t.tax)

    def undo_tax(self, t):
        self._results.add_result(tax=-t.tax)


class Stock:

    def __init__(self, symbol, **kwargs):
        stock, market = symbol.split('.')
        self._wallet = kwargs.get('wallet', Wallet())
        self._ticker = Ticker(symbol)
        self._wallet.set_projection_data(self.current_price, self.last_dividend)

        pub.subscribe(self.select_stock, 'select.{}'.format(stock))
        self._wallet.set_subscriptions(stock)

    @property
    def wallet(self):
        return self._wallet

    @property
    def symbol(self):
        return self.info['symbol']

    @property
    def current_price(self):
        return self.info['regularMarketPrice']

    @property
    def last_dividend(self):
        return self.info['trailingAnnualDividendRate']

    @property
    def info(self):
        return self._ticker.info

    def select_stock(self, symbol):
        pub.sendMessage('stock.overview', data=self.info)


class Portfolio:

    def __init__(self, **kwargs):
        self._stocks = kwargs.get('stocks', {})

        pub.subscribe(self.add_stock, 'portfolio.add')
        pub.subscribe(self.remove_stock, 'portfolio.remove')
        pub.subscribe(self.clear_select, 'select.clear')

    @property
    def data(self):
        return self._stocks

    @property
    def stocks(self):
        return sorted(self._stocks.keys())

    def add_stock(self, symbol):
        self._stocks[symbol] = Stock('{}.VI'.format(symbol))
        pub.sendMessage('portfolio.update', stocks=self.stocks)

    def remove_stock(self, symbol):
        try:
            self._stocks.pop(symbol)
            pub.sendMessage('portfolio.update', stocks=self.stocks)
        except KeyError:
            pass

    def clear_select(self, symbol):
        pub.sendMessage('stock.overview', data={})
        pub.sendMessage('stock.position', data={})
        pub.sendMessage('stock.results', data={})
        pub.sendMessage('stock.projection', data={})
        pub.sendMessage('stock.transactions', data={})
