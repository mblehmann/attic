from abc import abstractmethod
from datetime import datetime
from enum import Enum, auto
from re import match
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from pubsub import pub
from tkcalendar import DateEntry


def check_float(new_value):
    return match('^[0-9]+\\.?[0-9]{0,5}$', new_value) is not None


def check_integer(new_value):
    return match('^[0-9]+$', new_value) is not None


def convert_value(value):
    try:
        return datetime.strptime(value, '%d.%m.%Y')
    except ValueError:
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value


class FieldType(Enum):
    Date = auto()
    Float = auto()
    Integer = auto()
    String = auto()


class InputFrame:

    def __init__(self, parent, fields, button, options=None):
        self._frame = Frame(parent, padding=3)
        self._field_frame = Frame(self._frame)
        self._option_frame = Frame(self._frame)
        self._button_frame = Frame(self._frame)

        self._fields = {field: self.create_field(field_type) for field, field_type in fields.items()}
        self._option_var = StringVar()
        self._options = []
        if options:
            self._options = [self.create_option(option) for option in options]
            self._option_var.set(options[0])
        self._button = Button(self._button_frame, text=button, command=lambda: self.create_event())

    @property
    def data(self):
        return {field.lower(): convert_value(entry.get()) for field, entry in self._fields.items()}

    @property
    def option(self):
        return self._option_var.get()

    @property
    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def update_frame(self, option):
        pass

    @abstractmethod
    def verify_data(self, data):
        pass

    def create_field(self, field_type):
        entry = None
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
        elif field_type == FieldType.String:
            entry = Entry(self._field_frame, justify='right', width=10)
        return entry

    def create_option(self, label):
        return Radiobutton(self._option_frame, text=label, variable=self._option_var, value=label,
                           command=lambda: self.update_frame(label))

    def create_event(self):
        error_values = self.verify_data(self.data)

        if error_values:
            messagebox.showinfo(message='Could not execute the action {}'.format(self.action),
                                detail='Missing fields:\n{}'.format('\n'.join(error_values)))
        else:
            pub.sendMessage(self.action, **self.data)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)

        self._field_frame.grid(column=0, row=0, sticky=(N, E, S, W), pady=5)
        self._field_frame.columnconfigure(1, weight=1)
        for index, (label, entry) in enumerate(self._fields.items()):
            Label(self._field_frame, text=label).grid(column=0, row=index, sticky=(N, S, W))
            entry.grid(column=1, row=index, sticky=(N, E, S, W))

        if self._options:
            self._option_frame.grid(column=0, row=1, sticky=(N, E, S, W), pady=(0, 5))
            for index, widget in enumerate(self._options):
                self._option_frame.columnconfigure(index, weight=1)
                widget.grid(column=index, row=0)

        self._button_frame.grid(column=0, row=2, sticky=(N, E, S, W), pady=(0, 5))
        self._button_frame.columnconfigure(0, weight=1)
        self._button.grid(column=0, row=0)
        self.update_frame(self._option_var.get())


class BuySellInputFrame(InputFrame):

    def __init__(self, parent):
        fields = {
            'Stock': FieldType.String,
            'Day': FieldType.Date,
            'Amount': FieldType.Integer,
            'Price': FieldType.Float,
            'Fee': FieldType.Float,
            'Tax': FieldType.Float
        }
        super().__init__(parent, fields, 'OK', ['Buy', 'Sell'])
        self._fields['Stock'].state(['readonly'])
        pub.subscribe(self.set_stock, 'select')

    def set_stock(self, symbol):
        self._fields['Stock'].state(['!readonly'])
        self._fields['Stock'].delete(0, 'end')
        self._fields['Stock'].insert(0, symbol)
        self._fields['Stock'].state(['readonly'])

    @property
    def data(self):
        data = super().data
        if self.option == 'Buy':
            data.pop('tax')
        return data

    @property
    def action(self):
        return '{}.{}'.format(self.option.lower(), self.data['stock'])

    def update_frame(self, option):
        if option == 'Buy':
            for widget in self._field_frame.grid_slaves(row=5):
                widget.grid_remove()
        elif option == 'Sell':
            field = 'Tax'
            Label(self._field_frame, text=field).grid(column=0, row=5)
            self._fields[field].grid(column=1, row=5)

    def verify_data(self, data):
        error_values = []
        if not data['stock']:
            error_values.append('Stock')
        if not isinstance(data['day'], datetime):
            error_values.append('Day')
        for field in ['amount', 'price']:
            if data[field] == 0:
                error_values.append(field.capitalize())
        return error_values


class DividendTaxInputFrame(InputFrame):

    def __init__(self, parent):
        fields = {
            'Stock': FieldType.String,
            'Day': FieldType.Date,
            'Dividend': FieldType.Float,
            'Tax': FieldType.Float
        }
        super().__init__(parent, fields, 'OK', ['Dividend', 'Tax'])
        self._fields['Stock'].state(['readonly'])
        pub.subscribe(self.set_stock, 'select')

    def set_stock(self, symbol):
        self._fields['Stock'].state(['!readonly'])
        self._fields['Stock'].delete(0, 'end')
        self._fields['Stock'].insert(0, symbol)
        self._fields['Stock'].state(['readonly'])

    @property
    def data(self):
        data = super().data
        if self.option == 'Tax':
            data.pop('dividend')
        return data

    @property
    def action(self):
        return '{}.{}'.format(self.option.lower(), self.data['stock'])

    def update_frame(self, option):
        if option == 'Tax':
            for widget in self._field_frame.grid_slaves(row=2):
                widget.grid_remove()
        elif option == 'Dividend':
            field = 'Dividend'
            Label(self._field_frame, text=field).grid(column=0, row=2)
            self._fields[field].grid(column=1, row=2)

    def verify_data(self, data):
        error_values = []
        if not data['stock']:
            error_values.append('Stock')
        if not isinstance(data['day'], datetime):
            error_values.append('Day')
        for field in ['tax', 'dividend']:
            if self.option == field.capitalize() and data[field] == 0:
                error_values.append(field.capitalize())
        return error_values


class InputPanel:

    def __init__(self, parent):
        self._frame = Frame(parent, padding=5)

        self._transaction_frame = BuySellInputFrame(self._frame)
        self._operation_frame = DividendTaxInputFrame(self._frame)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
        self._frame.columnconfigure(0, weight=1)

        self._transaction_frame.grid(column=0, row=0, sticky=(N, E, S, W))
        Separator(self._frame, orient=HORIZONTAL).grid(column=0, row=1, sticky=(E, W), pady=10)
        self._operation_frame.grid(column=0, row=2, sticky=(N, E, S, W))
