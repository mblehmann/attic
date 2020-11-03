from abc import abstractmethod


# provides aggregated information of all stock investments
class StockPortfolio:

    def __init__(self):
        self._stocks = {}

    def add_stock(self, name):
        self._stocks[name] = StockInvestment(name)

    def buy(self, name, day, shares, price, fees):
        self._stocks[name].buy(day, shares, price, fees)


# provides information regarding a single stock
class StockInvestment:

    def __init__(self, name):
        self._name = name
        self._operations = []

    @property
    def shares(self):
        return sum([o.shares if o.type_ == 'b' else -o.shares for o in self._operations])

    @property
    def average_price(self):
        return None

    @property
    def fees(self):
        return None

    @property
    def total_value(self):
        return None

    def add_price(self, day, price):
        pass

    def buy(self, day, shares, price, fees):
        self._operations.append(StockOperation(day, shares, price, fees))


class StockOperation:

    def __init__(self, stock, day, shares, price, fees):
        self._stock = stock
        self._day = day
        self._shares = shares
        self._price = price
        self._fees = fees

    def __repr__(self):
        return '{} {} {} {}'.format(self._stock, self._shares, self._price, self._day)

    @property
    @abstractmethod
    def is_buy(self):
        pass

    @property
    def total_value(self):
        return self._shares * self._price + self._fees


class BuyStockOperation(StockOperation):

    def __init__(self, stock, day, shares, price, fees):
        super().__init__(stock, day, shares, price, fees)

    def __repr__(self):
        return '{} {}'.format('B', super().__repr__())

    def is_buy(self):
        return True


class SellStockOperation(StockOperation):

    def __init__(self, stock, day, shares, price, fees):
        super().__init__(stock, day, shares, price, fees)

    def __repr__(self):
        return '{} {}'.format('S', super().__repr__())

    def is_buy(self):
        return False


if __name__ == '__main__':
    # p = StockPortfolio()
    # p.add_stock('Erste Group')
    # p.buy('Erste Group', '20.04.1988', 200, 17.20, 1.20)
    # print(p._stocks['Erste Group']._operations[0].total_value)
    # print(p._stocks['Erste Group'].shares)

    b = BuyStockOperation('Erste Group', '20.04.1988', 200, 17.20, 2.50)
    print(b, b.total_value)
    s = SellStockOperation('Erste Group', '20.04.1988', 200, 17.20, 2.50)
    print(s, s.total_value)
