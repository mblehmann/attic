from abc import abstractmethod
from tkinter import *
from tkinter.ttk import *

from pubsub import pub


class HeaderFrame:

    def __init__(self, parent):
        self._frame = Frame(parent, padding=5)
        self._symbol = Label(self._frame, font=('', 24))
        self._name = Label(self._frame)
        self._price = Label(self._frame, font=('', 24))
        pub.subscribe(self.set_stock, 'stock.overview')

    def set_stock(self, data):
        self._symbol['text'] = data.get('symbol', '-')
        self._name['text'] = data.get('longName', '-')
        self._price['text'] = '€ {:.2f}'.format(data.get('regularMarketPrice', 0))

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._symbol.grid(column=0, row=0, sticky=(N, S, W))
        self._name.grid(column=0, row=1, sticky=(N, S, W))
        self._price.grid(column=1, row=0, rowspan=2, sticky=(N, E, S))


class InfoFrame:

    def __init__(self, parent, label, event, fields):
        self._frame = LabelFrame(parent, text=label, width=200, height=200)
        self._fields = {field: Label(self._frame) for field in fields}
        pub.subscribe(self.show_data, 'stock.{}'.format(event))

    def set_value(self, field, value):
        self._fields[field]['text'] = value

    @abstractmethod
    def show_data(self, data):
        pass

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(1, weight=1)
        for index, (label, widget) in enumerate(self._fields.items()):
            Label(self._frame, text=label).grid(column=0, row=index, stick=(N, S, W))
            widget.grid(column=1, row=index, stick=(N, E, S))


class OverviewInfoFrame(InfoFrame):

    def __init__(self, parent, label, event):
        super().__init__(parent, label, event, ['Market Capitalization', 'Volume', 'Earnings-per-Share',
                                                'Price-per-Earnings', 'Last Dividend', 'Dividend Yield'])

    def show_data(self, data):
        self.set_value('Market Capitalization', '€ {:,.2f}B'.format(data.get('marketCap', 0) / 1000000000.0))
        self.set_value('Volume', '{:,}'.format(data.get('averageVolume', 0)))
        self.set_value('Earnings-per-Share', '€ {:.2f}'.format(data.get('trailingEps', 0)))
        self.set_value('Price-per-Earnings', '€ {:.2f}'.format(data.get('trailingPE', 0)))
        self.set_value('Last Dividend', '€ {:.2f}'.format(data.get('trailingAnnualDividendRate', 0)))
        self.set_value('Dividend Yield', '{:.2f}%'.format(data.get('trailingAnnualDividendYield', 0) * 100))


class PositionInfoFrame(InfoFrame):

    def __init__(self, parent, label, event):
        super().__init__(parent, label, event, ['Shares', 'Avg. Buy Price', 'Invested', 'Market Value', 'Growth'])

    def show_data(self, data):
        self.set_value('Shares', data.get('shares', 0))
        self.set_value('Avg. Buy Price', '€ {:,.2f}'.format(data.get('avgBuyPrice', 0)))
        self.set_value('Invested', '€ {:,.2f}'.format(data.get('invested', 0)))
        self.set_value('Market Value', '€ {:,.2f}'.format(data.get('marketValue', 0)))
        self.set_value('Growth', '{:.2f}%'.format(data.get('growth', 0)))


class ResultsInfoFrame(InfoFrame):

    def __init__(self, parent, label, event):
        super().__init__(parent, label, event, ['Profit', 'Gain', 'Dividends', 'Fees', 'Taxes'])

    def show_data(self, data):
        self.set_value('Profit', '€ {:,.2f}'.format(data.get('profit', 0)))
        self.set_value('Gain', '€ {:,.2f}'.format(data.get('gains', 0)))
        self.set_value('Dividends', '€ {:,.2f}'.format(data.get('dividends', 0)))
        self.set_value('Fees', '€ {:,.2f}'.format(data.get('fees', 0)))
        self.set_value('Taxes', '€ {:,.2f}'.format(data.get('taxes', 0)))


class TransactionFrame:

    def __init__(self, parent):
        self._frame = Frame(parent, padding=5)
        self._columns = ['transaction', 'day', 'amount', 'price', 'total_cost', 'value', 'dividend', 'fee', 'tax']
        self._transactions = Treeview(self._frame, show='headings', columns=self._columns)
        for column in self._columns:
            if column in ['transaction', 'day', 'amount']:
                self._transactions.column(column, anchor=CENTER, minwidth=87, width=87)
            else:
                self._transactions.column(column, anchor=E, minwidth=87, width=87)
            self._transactions.heading(column, text=column.capitalize().replace('_', ' '))
        self._button = Button(self._frame, text='Remove', command=lambda: self.remove_transaction())
        self._symbol = None

        pub.subscribe(self.show_transactions, 'stock.transactions')
        pub.subscribe(self.set_stock, 'select')

    def set_stock(self, symbol):
        self._symbol = symbol
        self._transactions.delete(*self._transactions.get_children())

    def show_transactions(self, data):
        remove_transactions = [t for t in self._transactions.get_children() if t not in data]

        if remove_transactions:
            self._transactions.delete(remove_transactions)

        for tid, transaction in data.items():
            if tid not in list(self._transactions.get_children()):
                self.add_transaction(transaction)

    def add_transaction(self, transaction):
        data = []
        for column in self._columns:
            if column in transaction:
                if column in ['total_cost', 'price', 'value', 'dividend', 'fee', 'tax']:
                    data.append('€ {:,.2f}'.format(transaction[column]))
                elif column in ['day']:
                    data.append(transaction[column].strftime('%d.%m.%Y'))
                else:
                    data.append(transaction[column])
            else:
                data.append('-')

        self._transactions.insert('', 'end', id=transaction['id'], values=tuple(data))

    def remove_transaction(self):
        if self._transactions.selection():
            pub.sendMessage('remove.{}'.format(self._symbol), ids=self._transactions.selection())

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self._transactions.grid(column=0, row=0, sticky=(N, E, S, W))
        self._button.grid(column=0, row=1, pady=5)


class StockPanel:

    def __init__(self, parent):
        self._frame = Frame(parent, padding=5)
        self._header_frame = HeaderFrame(self._frame)
        self._overview_frame = OverviewInfoFrame(self._frame, 'Overview', 'overview')
        self._position_frame = PositionInfoFrame(self._frame, 'Position', 'position')
        self._result_frame = ResultsInfoFrame(self._frame, 'Results', 'results')
        self._projection_frame = ResultsInfoFrame(self._frame, 'Projection', 'projection')
        self._transaction_frame = TransactionFrame(self._frame)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.columnconfigure(2, weight=1)
        self._frame.columnconfigure(3, weight=1)
        self._frame.rowconfigure(2, weight=1)
        self._header_frame.grid(column=0, row=0, columnspan=1, sticky=(N, E, S, W))
        self._overview_frame.grid(column=0, row=1, sticky=(N, E, S, W), padx=5)
        self._position_frame.grid(column=1, row=1, sticky=(N, E, S, W), padx=(0, 5))
        self._result_frame.grid(column=2, row=1, sticky=(N, E, S, W), padx=(0, 5))
        self._projection_frame.grid(column=3, row=1, sticky=(N, E, S, W), padx=(0, 5))
        self._transaction_frame.grid(column=0, row=2, columnspan=4, sticky=(N, E, S, W))
