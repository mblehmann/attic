from time import time
from tkinter import *
from tkinter.ttk import *

from pubsub import pub


class ListPanel:

    def __init__(self, parent, label, stocks):
        self._var = StringVar()
        self.set_stocks(stocks)

        self._frame = LabelFrame(parent, text=label)
        self._list = Listbox(self._frame, listvariable=self._var, exportselection=False, selectmode='browse')
        self._list.bind("<<ListboxSelect>>", lambda x: self.select_stock(x.widget.curselection()))

    @property
    def current_stock(self):
        return self._list.get(self._list.curselection())

    def select_stock(self, index):
        pub.sendMessage('select stock', stock=self._list.get(index), begin=time())

    def set_stocks(self, stocks):
        self._var.set(stocks)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._list.grid(column=0, row=0)
