from tkinter import *
from tkinter.ttk import *

from pubsub import pub

from input_panel import InputFrame, FieldType


class StockInputFrame(InputFrame):

    def __init__(self, parent):
        super().__init__(parent, {'Symbol': FieldType.String}, 'Add')

    @property
    def data(self):
        return {key: value.upper() for key, value in super().data.items()}

    @property
    def action(self):
        return 'portfolio.add'

    def update_frame(self, option):
        pass

    def verify_data(self, data):
        if not data['symbol']:
            return ['Symbol']
        return []


class ListFrame:

    def __init__(self, parent):
        self._var = StringVar()

        self._frame = LabelFrame(parent, text='Portfolio')
        self._list = Listbox(self._frame, listvariable=self._var, exportselection=False, selectmode='browse')
        self._button = Button(self._frame, text='Remove', command=lambda: self.remove_stock())

        self._list.bind("<<ListboxSelect>>", lambda x: self.select_stock(x.widget.curselection()))
        self._list.selection_set(0)
        pub.subscribe(self.set_stocks, 'portfolio.update')

    @property
    def current_stock(self):
        if self._list.curselection():
            return self._list.get(self._list.curselection())
        else:
            return None

    def set_stocks(self, stocks):
        self._var.set(stocks)
        if self._list.size() == 0:
            self.select_stock(())
        elif not self.current_stock:
            self._list.selection_set(0)
            self.select_stock((0,))

    def remove_stock(self):
        if self.current_stock:
            pub.sendMessage('portfolio.remove'.format(self.current_stock), symbol=self.current_stock)

    def select_stock(self, index):
        if index and self._list.get(index):
            symbol = self._list.get(index)
            pub.sendMessage('select.{}'.format(symbol), symbol=symbol)
        else:
            pub.sendMessage('select.clear', symbol='')

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._list.grid(column=0, row=0, stick=(N, E, S, W))
        self._button.grid(column=0, row=1, pady=5)


class PortfolioPanel:

    def __init__(self, parent):
        self._frame = Frame(parent, padding=5)
        self._list = ListFrame(self._frame)
        self._input = StockInputFrame(self._frame)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._list.grid(column=0, row=0, sticky=(N, E, S, W))
        Separator(self._frame, orient=HORIZONTAL).grid(column=0, row=1, sticky=(E, W), pady=10)
        self._input.grid(column=0, row=2, sticky=(N, E, S, W))
