from abc import abstractmethod, ABC
from uuid import uuid4


class Transaction(ABC):

    def __init__(self, day):
        self._day = day
        self._transaction = None
        self._id = uuid4()

    @property
    def id(self):
        return str(self._id)

    @property
    @abstractmethod
    def data(self):
        return {
            'id': self.id,
            'transaction': self._transaction,
            'day': self._day,
            'total_cost': self.total_cost,
        }

    @property
    @abstractmethod
    def total_cost(self):
        pass


class ShareTransaction(Transaction, ABC):

    def __init__(self, day, amount, price, fee):
        super().__init__(day)
        self._amount = int(amount)
        self._price = float(price)
        self._fee = float(fee)

    @property
    def data(self):
        return super().data | {
            'amount': self._amount,
            'price': self._price,
            'value': self.value,
            'fee': self._fee,
        }

    @property
    def value(self):
        return self._amount * self._price

    @property
    def amount(self):
        return self._amount

    @property
    def fee(self):
        return self._fee


class BuyTransaction(ShareTransaction):

    def __init__(self, day, amount, price, fee, **kwargs):
        super().__init__(day, amount, price, fee)
        self._transaction = kwargs.get('transaction', 'Buy')

    @property
    def total_cost(self):
        return self.value + self._fee


class SellTransaction(ShareTransaction):

    def __init__(self, day, amount, price, fee, tax, buy_price, **kwargs):
        super().__init__(day, amount, price, fee)
        self._transaction = kwargs.get('transaction', 'Sell')
        self._tax = float(tax)
        self._buy_price = float(buy_price)

    @property
    def data(self):
        return super().data | {'tax': self._tax, 'buy_price': self._buy_price}

    @property
    def total_cost(self):
        return self.value - (self._fee + self._tax)

    @property
    def tax(self):
        return self._tax

    @property
    def gain(self):
        return (self._price - self._buy_price) * self._amount


class StockTransaction(Transaction, ABC):

    def __init__(self, day, tax):
        super().__init__(day)
        self._tax = float(tax)

    @property
    def data(self):
        return super().data | {'tax': self._tax}

    @property
    def tax(self):
        return self._tax


class DividendTransaction(StockTransaction):

    def __init__(self, day, dividend, tax, **kwargs):
        super().__init__(day, tax)
        self._transaction = kwargs.get('transaction', 'Dividend')
        self._dividend = float(dividend)

    @property
    def data(self):
        return super().data | {'dividend': self._dividend}

    @property
    def total_cost(self):
        return self._dividend

    @property
    def dividend(self):
        return self._dividend


class TaxTransaction(StockTransaction):

    def __init__(self, day, value, **kwargs):
        super().__init__(day, value)
        self._transaction = kwargs.get('transaction', 'Tax')

    @property
    def total_cost(self):
        return self._tax
