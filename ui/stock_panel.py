from time import time
from tkinter import *
from tkinter.ttk import *

from pubsub import pub


class HeaderFrame:

    def __init__(self, parent):
        self._frame = LabelFrame(parent, text='Header', width=200, height=200)
        self._symbol = Label(self._frame, font=('', 24))
        self._name = Label(self._frame)
        self._price = Label(self._frame, font=('', 24))

    def set_stock(self, symbol, name, price):
        self._symbol['text'] = symbol
        self._name['text'] = name
        self._price['text'] = price

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._symbol.grid(column=0, row=0, sticky=(N, S, W))
        self._name.grid(column=0, row=1, sticky=(N, S, W))
        self._price.grid(column=1, row=0, rowspan=2, sticky=(N, E, S))


class InfoFrame:

    def __init__(self, parent, label):
        self._frame = LabelFrame(parent, text=label, width=200, height=200)
        self._fields = {}

    def add_field(self, field, value=''):
        self._fields[field] = Label(self._frame, text=value)
        return self

    def set_value(self, field, value):
        self._fields[field]['text'] = value

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(1, weight=1)
        for index, (label, widget) in enumerate(self._fields.items()):
            Label(self._frame, text=label).grid(column=0, row=index, stick=(N, S, W))
            widget.grid(column=1, row=index, stick=(N, E, S))


class TransactionFrame:

    def __init__(self, parent):
        self._frame = LabelFrame(parent, text='Transactions', width=200, height=200)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)


class StockPanel:

    def __init__(self, parent):
        self._frame = LabelFrame(parent, text='Stock', width=200, height=200)
        self._header_frame = HeaderFrame(self._frame)
        self._overview_frame = InfoFrame(self._frame, 'Overview') \
            .add_field('Market Capitalization') \
            .add_field('Volume') \
            .add_field('Earnings-per-Share') \
            .add_field('Price-per-Earnings') \
            .add_field('Last Dividend') \
            .add_field('Dividend Yield')
        self._position_frame = InfoFrame(self._frame, 'Position') \
            .add_field('Shares', '150') \
            .add_field('Avg. Buy Price', '€ 19.85') \
            .add_field('Invested', '€ 2,977.50') \
            .add_field('Market Value', '€ 6,376.50')
        self._result_frame = InfoFrame(self._frame, 'Results') \
            .add_field('Profit', '€ 0.00') \
            .add_field('Sell', '€ 0.00') \
            .add_field('Dividends', '€ 0.00') \
            .add_field('Fees', '€ 2.50') \
            .add_field('Taxes', '€ 0.00')
        self._projection_frame = InfoFrame(self._frame, 'Projection') \
            .add_field('Gain', '€ 3,399.00 (114.16%)') \
            .add_field('Fees', '€ 2.50') \
            .add_field('Taxes', '€ 934.73') \
            .add_field('Profit', '€ 2,461.78 (82.68%)') \
            .add_field('Dividends', '€ 277,50')
        self._transaction_frame = TransactionFrame(self._frame)

        pub.subscribe(self.show_stock, 'show stock')

    def show_stock(self, data, begin):
        self._header_frame.set_stock(data['symbol'], data['longName'], '€ {:.2f}'.format(data['regularMarketPrice']))
        self._overview_frame.set_value('Market Capitalization', '€ {:,.2f}B'.format(data['marketCap'] / 1000000000.0))
        self._overview_frame.set_value('Volume', '{:,}'.format(data['averageVolume']))
        self._overview_frame.set_value('Earnings-per-Share', '€ {:.2f}'.format(data['trailingEps']))
        self._overview_frame.set_value('Price-per-Earnings', '€ {:.2f}'.format(data['trailingPE']))
        self._overview_frame.set_value('Last Dividend', '€ {:.2f}'.format(data['trailingAnnualDividendRate']))
        self._overview_frame.set_value('Dividend Yield', '{:.2f}%'.format(data['trailingAnnualDividendYield'] * 100))
        print(time() - begin)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._header_frame.grid(column=0, row=0, columnspan=2, sticky=(N, E, S, W))
        self._overview_frame.grid(column=0, row=1, sticky=(N, E, S, W))
        self._position_frame.grid(column=1, row=1, sticky=(N, E, S, W))
        self._result_frame.grid(column=0, row=2, sticky=(N, E, S, W))
        self._projection_frame.grid(column=1, row=2, sticky=(N, E, S, W))
        self._transaction_frame.grid(column=0, row=3, columnspan=2, sticky=(N, E, S, W))
