from collections import OrderedDict
from enum import Enum, auto
from re import match
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from pubsub import pub
from tkcalendar import DateEntry


def check_float(new_value):
    return match('^[0-9]*\\.?[0-9]{0,2}$', new_value) is not None


def check_integer(new_value):
    return match('^[0-9]*$', new_value) is not None


class FieldType(Enum):
    Date = auto()
    Float = auto()
    Integer = auto()


class InputFrame:

    def __init__(self, parent, label):
        self._frame = LabelFrame(parent, text=label)
        self._field_frame = Frame(self._frame)
        self._button_frame = Frame(self._frame)

        self._fields = OrderedDict()
        self._buttons = []

    @property
    def data(self):
        return {field.lower(): entry.get() for field, entry in self._fields.items()}

    def add_field(self, label, field_type):
        if field_type == FieldType.Date:
            entry = DateEntry(self._field_frame, date_pattern='dd.MM.yyyy', justify='center', width=10)
        elif field_type == FieldType.Float:
            entry = Entry(self._field_frame, justify='right', width=10, validate='key',
                          validatecommand=(self._frame.register(check_float), '%P'))
            entry.insert(0, '0.00')
        elif field_type == FieldType.Integer:
            entry = Entry(self._field_frame, justify='right', width=10, validate='key',
                          validatecommand=(self._frame.register(check_integer), '%P'))
            entry.insert(0, '0')
        else:
            return self
        self._fields[label] = entry
        return self

    def add_button(self, label, ignored_fields=None):
        self._buttons.append(Button(self._button_frame, text=label,
                                    command=lambda: self.create_event(label, ignored_fields)))
        return self

    def create_event(self, label, ignored_fields):
        missing_values = [field for field, entry in self._fields.items() if not entry.get()]
        if missing_values:
            messagebox.showinfo(message='Could not execute the action {}'.format(label),
                                detail='Missing fields:\n{}'.format('\n'.join(missing_values)))
        else:
            data = self.data
            try:
                for field in ignored_fields:
                    data.pop(field.lower())
            except TypeError:
                pass
            pub.sendMessage(label, **data)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self._field_frame.grid(column=0, row=0)
        self._button_frame.grid(column=0, row=1)
        for index, (label, entry) in enumerate(self._fields.items()):
            Label(self._field_frame, text=label).grid(column=0, row=index)
            entry.grid(column=1, row=index)
        for index, button in enumerate(self._buttons):
            button.grid(column=index, row=0)


class InputPanel:

    def __init__(self, parent):
        self._frame = Frame(parent)

        self._transaction_frame = InputFrame(self._frame, 'Stock Transactions') \
            .add_field('Day', FieldType.Date) \
            .add_field('Amount', FieldType.Integer) \
            .add_field('Price', FieldType.Float) \
            .add_field('Fee', FieldType.Float) \
            .add_field('Tax', FieldType.Float) \
            .add_button('Buy', ['Tax']) \
            .add_button('Sell')

        self._operation_frame = InputFrame(self._frame, 'Stock Operations') \
            .add_field('Day', FieldType.Date) \
            .add_field('Value', FieldType.Float) \
            .add_field('Tax', FieldType.Float) \
            .add_button('Dividend') \
            .add_button('Tax', ['Tax'])

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.rowconfigure(0, weight=1)
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)

        self._transaction_frame.grid(column=0, row=0, sticky=(N, E, S, W))
        self._operation_frame.grid(column=1, row=0, sticky=(N, E, S, W))
