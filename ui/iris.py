from abc import abstractmethod
from tkinter import *

from pubsub import pub
from yfinance import Tickers

from input_panel import InputPanel
from list_panel import ListPanel
from stock_panel import StockPanel


class Transaction:

    def __init__(self, day):
        self._day = day

    @property
    @abstractmethod
    def value(self):
        pass

    def dividends(self):
        pass

    def fees(self):
        pass

    def taxes(self):
        pass


class ShareTransaction(Transaction):

    def __init__(self, day, amount, price, fee):
        super().__init__(day)
        self._amount = amount
        self._price = price
        self._fee = fee

    @property
    def value(self):
        return self._amount * self._price


class BuyTransaction(ShareTransaction):

    def __init__(self, day, amount, price, fee):
        super().__init__(day, amount, price, fee)


class SellTransaction(ShareTransaction):

    def __init__(self, day, amount, price, fee, tax):
        super().__init__(day, amount, price, fee)
        self._tax = tax


class StockTransaction(Transaction):

    def __init__(self, day, value):
        super().__init__(day)
        self._value = value

    @property
    def value(self):
        return self._value


class DividendTransaction(StockTransaction):

    def __init__(self, day, value, tax):
        super().__init__(day, value)
        self._tax = tax


class TaxTransaction(StockTransaction):

    def __init__(self, day, value):
        super().__init__(day, value)


class Stock:

    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def buy(self, day, amount, price, fee):
        self._transactions.append(BuyTransaction(day, amount, price, fee))

    def sell(self, day, amount, price, fee, tax):
        self._transactions.append(SellTransaction(day, amount, price, fee, tax))

    def dividend(self, day, value, tax):
        self._transactions.append(DividendTransaction(day, value, tax))

    def tax(self, day, value):
        self._transactions.append(TaxTransaction(day, value))


class Iris:

    def __init__(self):
        self._root = Tk()
        self._root.title('Stock Manager')

        self._stocks = Tickers('BG.VI CAI.VI EBS.VI EVN.VI LNZ.VI POST.VI OMV.VI RBI.VI SPI.VI UQA.VI VIG.VI')
        self._transactions = {stock: Stock() for stock in self._stocks.symbols}

        self._list_panel = ListPanel(self._root, 'Stocks', self._stocks.symbols)
        self._stock_panel = StockPanel(self._root)
        self._input_panel = InputPanel(self._root)

        self._list_panel.grid(column=0, row=0, rowspan=2, sticky=(N, E, S, W))
        self._stock_panel.grid(column=1, row=0, sticky=(N, E, S, W))
        self._input_panel.grid(column=1, row=1, sticky=(N, E, S, W))

        pub.subscribe(self.buy, 'Buy')
        pub.subscribe(self.sell, 'Sell')
        pub.subscribe(self.dividend, 'Dividend')
        pub.subscribe(self.tax, 'Tax')
        pub.subscribe(self.select_stock, 'select stock')

    def buy(self, day, amount, price, fee):
        self._transactions[self._list_panel.current_stock].buy(day, amount, price, fee)
        self.print_transactions()

    def sell(self, day, amount, price, fee, tax):
        self._transactions[self._list_panel.current_stock].sell(day, amount, price, fee, tax)
        self.print_transactions()

    def dividend(self, day, value, tax):
        self._transactions[self._list_panel.current_stock].dividend(day, value, tax)
        self.print_transactions()

    def tax(self, day, value):
        self._transactions[self._list_panel.current_stock].tax(day, value)
        self.print_transactions()

    def print_transactions(self):
        print(self._transactions[self._list_panel.current_stock].transactions)

    def select_stock(self, stock, begin):
        pass
        # pub.sendMessage('show stock', data=self._stocks.tickers[stock].info, begin=begin)

    def run(self):
        self._root.mainloop()


if __name__ == '__main__':
    iris = Iris()
    iris.run()
