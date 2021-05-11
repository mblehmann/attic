import json
from tkinter import *
from tkinter.ttk import *

from pubsub import pub

from input_panel import InputPanel
from list_panel import PortfolioPanel
from stock_panel import StockPanel
from stocks.stock import Portfolio
from stocks.stock_coder import StockEncoder, StockDecoder


class Iris:

    def __init__(self):
        self._root = Tk()
        self._root.title('Stock Manager')
        self._root.geometry('1200x640')

        self._root.option_add('*tearOff', FALSE)
        self._menu_bar = self.create_menu_bar(self._root)
        self._root['menu'] = self._menu_bar

        self._list_panel = PortfolioPanel(self._root)
        self._stock_panel = StockPanel(self._root)
        self._input_panel = InputPanel(self._root)

        self._list_panel.grid(column=0, row=0, sticky=(N, E, S, W))
        Separator(self._root, orient=VERTICAL).grid(column=1, row=0, sticky=(N, S))
        self._stock_panel.grid(column=2, row=0, sticky=(N, E, S, W))
        Separator(self._root, orient=VERTICAL).grid(column=3, row=0, sticky=(N, S))
        self._input_panel.grid(column=4, row=0, sticky=(N, E, S, W))

        self._root.columnconfigure(2, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._portfolio = None
        self.new()

    def create_menu_bar(self, parent):
        menu_bar = Menu(parent)
        menu_file = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new)
        menu_file.add_command(label='Save', command=self.save)
        menu_file.add_command(label='Load', command=self.load)
        return menu_bar

    def new(self):
        self._portfolio = Portfolio()
        pub.sendMessage('portfolio.update', stocks=self._portfolio.stocks)

    def save(self):
        json.dump(self._portfolio, open('gustock.json', 'w'), cls=StockEncoder, indent=4)

    def load(self):
        self._portfolio = json.load(open('gustock.json'), cls=StockDecoder)
        pub.sendMessage('portfolio.update', stocks=self._portfolio.stocks)

    def run(self):
        self._root.mainloop()


if __name__ == '__main__':
    iris = Iris()
    iris.run()
