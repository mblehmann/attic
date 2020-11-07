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

    def __init__(self, stock):
        self._stock = stock
        self._operations = []
        self._buy = StockAggregation()
        self._sell = StockAggregation()
        self._dividends = []

    def __repr__(self):
        return '\n'.join([self.summary(), self.operations_str()])

    def summary(self):
        return '{} {} {:.2f} {:,.2f}'.format(self._stock, self.shares, self.average_price, self.current_money_invested)

    def gains(self):
        profit = 'Profit: {:,.2f} ({:.2f}%)'.format(self.profit, self.profit_percentage)
        realization = 'Realization: {:,.2f}'.format(self.realizations)
        dividend = 'Dividend: {:,.2f}'.format(self.dividends)
        return '\n'.join([profit, realization, dividend])

    def operations_str(self):
        return '\n'.join([o.__repr__() for o in self._operations])

    def dividends_str(self):
        return '\n'.join([div.__repr__() for div in self._dividends])

    @property
    def shares(self):
        return self._buy.shares - self._sell.shares

    @property
    def current_money_invested(self):
        return self._buy.value - self._sell.value

    @property
    def average_price(self):
        return self.current_money_invested / self.shares

    @property
    def fees(self):
        return self._buy.fees + self._sell.fees

    @property
    def dividends(self):
        return sum([div.value for div in self._dividends])

    @property
    def realizations(self):
        bought_value = self._sell.shares * self._buy.average_price
        sold_value = self._sell.shares * self._sell.average_price
        return sold_value - bought_value

    @property
    def profit(self):
        return self.realizations + self.dividends

    @property
    def profit_percentage(self):
        return self.profit / self.current_money_invested

    def buy(self, day, shares, price, fees):
        buy_operation = BuyStockOperation(self._stock, day, shares, price, fees)
        self._operations.append(buy_operation)
        self._buy.add_shares(buy_operation)

    def sell(self, day, shares, price, fees):
        sell_operation = SellStockOperation(self._stock, day, shares, price, fees)
        self._operations.append(sell_operation)
        self._sell.add_shares(sell_operation)

    def gain_dividends(self, day, dividends):
        self._dividends.append(Dividends(self._stock, day, self.shares, dividends))

    def market_value(self, price):
        return self.shares * price

    def market_profit(self, price):
        return self.market_value(price) - self.current_money_invested

    def market_profit_percentage(self, price):
        return self.market_profit(price) / self.current_money_invested

    def market_str(self, price):
        money = 'Money invested: {:,.2f}'.format(self.current_money_invested)
        market_value = 'Market value: {:,.2f}'.format(self.market_value(price))
        profit = 'Profit: {:,.2f} ({:.2f}%)'.format(self.market_profit(price),
                                                    self.market_profit_percentage(price) * 100)
        return '\n'.join([money, market_value, profit])


class StockAggregation:

    def __init__(self):
        self._shares = 0
        self._value = 0
        self._fees = 0

    @property
    def shares(self):
        return self._shares

    @property
    def value(self):
        return self._value

    @property
    def fees(self):
        return self._fees

    @property
    def average_price(self):
        if self.value:
            return self.shares / self.value
        else:
            return 0

    def add_shares(self, operation):
        self._shares += operation.shares
        self._value += operation.total_value
        self._fees += operation.fees

    def remove_shares(self, operation):
        self._shares -= operation.shares
        self._value -= operation.total_value
        self._fees -= operation.fees


class Dividends:

    def __init__(self, stock, day, shares, dividends):
        self._stock = stock
        self._day = day
        self._shares = shares
        self._dividends = dividends
        self._value = shares * dividends

    def __repr__(self):
        return '{} {} {:,.2f} {}'.format(self._stock, self._shares, self._dividends, self._day)

    @property
    def value(self):
        return self._value


class StockOperation:

    def __init__(self, stock, day, shares, price, fees):
        self._stock = stock
        self._day = day
        self._shares = shares
        self._price = price
        self._fees = fees

    def __repr__(self):
        return '{} {} {:.2f} {}'.format(self._stock, self._shares, self._price, self._day)

    @property
    @abstractmethod
    def is_buy(self):
        pass

    @property
    def total_value(self):
        return self._shares * self._price + self._fees

    @property
    def shares(self):
        return self._shares

    @property
    def fees(self):
        return self._fees


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
    b = BuyStockOperation('Erste Group', '20.04.1988', 200, 17.20, 2.50)
    print(b, b.total_value)
    s = SellStockOperation('Erste Group', '20.04.1988', 200, 17.20, 2.50)
    print(s, s.total_value)

    stock_data = {
        'BAWAG': ('29.10.2020', 50, 31.34, 2.50, 32.10),
        'CA IMMO': ('29.10.2020', 60, 23.45, 2.50, 25.25),
        'ERSTE GROUP': ('29.10.2020', 200, 17.20, 2.50, 17.98),
        'LENZING': ('29.10.2020', 20, 59.70, 2.50, 65.20),
        'OMV': ('29.10.2020', 150, 19.85, 2.50, 21.02),
        'RAIFFEISEN': ('29.10.2020', 230, 12.02, 2.50, 12.82),
        'S IMMO': ('29.10.2020', 220, 12.86, 2.50, 13.68),
        'UNIQA': ('29.10.2020', 600, 4.73, 2.50, 5.02),
        'VIENNA': ('29.10.2020', 160, 17.20, 2.50, 17.46)
    }

    for st, data in stock_data.items():
        investment = StockInvestment(st)
        d, sh, bp, f, cp = data
        investment.buy(d, sh, bp, f)
        print(investment)
        print(investment.market_str(cp))
        print()
