import json
from abc import ABC, abstractmethod


class StockEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, StockOperation):
            return self.encode_stock_operation(obj)
        elif isinstance(obj, StockInvestment):
            return self.encode_stock_investment(obj)
        elif isinstance(obj, StockPortfolio):
            return self.encode_stock_portfolio(obj)

        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def encode_stock_operation(obj):
        return {
            'type': 'StockOperation',
            'stock': obj.stock,
            'day': obj.day,
            'shares': obj.shares,
            'price': obj.price,
            'fees': obj.fees,
            'symbol': obj.symbol,
        }

    @staticmethod
    def encode_stock_investment(obj):
        return {
            'type': 'StockInvestment',
            'stock': obj.stock,
            'price': obj.price,
            'operations': obj.operations,
        }

    @staticmethod
    def encode_stock_portfolio(obj):
        return {
            'type': 'StockPortfolio',
            'stocks': obj.stocks,
        }


class StockDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'type' not in obj:
            return obj
        if obj['type'] == 'StockOperation':
            return self.parse_stock_operation(obj)
        elif obj['type'] == 'StockInvestment':
            return self.parse_stock_investment(obj)
        elif obj['type'] == 'StockPortfolio':
            return self.parse_stock_portfolio(obj)
        return obj

    @staticmethod
    def parse_stock_operation(obj):
        if obj['symbol'] == 'B':
            return BuyStockOperation(obj['stock'], obj['day'], obj['shares'], obj['price'], obj['fees'])
        elif obj['symbol'] == 'S':
            return SellStockOperation(obj['stock'], obj['day'], obj['shares'], obj['price'], obj['fees'])
        elif obj['symbol'] == 'D':
            return DividendStockOperation(obj['stock'], obj['day'], obj['shares'], obj['price'])
        return obj

    @staticmethod
    def parse_stock_investment(obj):
        return StockInvestment(obj['stock'], obj['price'], obj['operations'])

    @staticmethod
    def parse_stock_portfolio(obj):
        return StockPortfolio(obj['stocks'])


class StockComponent(ABC):
    """
    The StockComponent is an interface for the composite and leaf of the stocks
    """

    def __init__(self):
        """
        Initializer
        """
        pass

    @abstractmethod
    def set_price(self, stock, price):
        """
        Sets the price of a stock

        :param stock: name of the stock
        :param price: current price of the stock
        :return: empty
        """
        pass

    @abstractmethod
    def buy(self, stock, day, shares, price, fees):
        """
        Buy shares of a stock

        :param stock: name of the stock
        :param day: day of the buy operation
        :param shares: number of shares bought
        :param price: price paid per share
        :param fees: fees paid on the operation
        :return: empty
        """
        pass

    @abstractmethod
    def sell(self, stock, day, shares, price, fees):
        """
        Sell shares of a stock

        :param stock: name of the stock
        :param day: day of the buy operation
        :param shares: number of shares bought
        :param price: price paid per share
        :param fees: fees paid on the operation
        :return: empty
        """
        pass

    @abstractmethod
    def gain_dividends(self, stock, day, shares, dividends):
        """
        Gain dividends of a stock

        :param stock: name of the stock
        :param day: day that the dividends were received
        :param shares: number of shares that received dividend
        :param dividends: dividends received per share
        :return: empty
        """
        pass

    @property
    @abstractmethod
    def cost_value(self):
        """
        The current cost value of the stock

        :return: The current cost value of the stock
        """
        pass

    @property
    @abstractmethod
    def market_value(self):
        """
        The current market value of the stock based on the current price set

        :return: The current market value of the stock
        """
        pass

    @property
    @abstractmethod
    def fees(self):
        """
        The total amount of fees paid on the stock

        :return: The total amount of fees paid on the stock
        """
        pass

    @property
    @abstractmethod
    def dividends(self):
        """
        The total amount of dividends received on the stock

        :return: The total amount of dividends received on the stock
        """
        pass


class StockPortfolio(StockComponent):
    """
    The StockPortfolio is the composite of the stocks
    """

    def __init__(self, stocks=None):
        """
        Creates the mapping that will be used to hold StockInvestment based on the stock name. The stocks should be only
        used when restoring data from json

        :param stocks: the stocks portfolio
        """
        super().__init__()
        self._stocks = stocks if stocks is not None else {}

    @property
    def stocks(self):
        """
        Return all the portfolio

        :return: Return the portfolio
        """
        return self._stocks

    def add_stock(self, stock):
        """
        Adds a new stock to the portfolio. Creates a new leaf to represent the stock

        :param stock: The added stock
        :return: empty
        """
        self._stocks[stock] = StockInvestment(stock)

    def set_price(self, stock, price):
        """
        Sets the price of a stock. Forwards the call to the stock leaf

        :param stock: name of the stock
        :param price: current price of the stock
        :return: empty
        """
        self._stocks[stock].set_price(stock, price)

    def buy(self, stock, day, shares, price, fees):
        """
        Buy shares of a stock. Forwards the call to the stock leaf

        :param stock: name of the stock
        :param day: day of the buy operation
        :param shares: number of shares bought
        :param price: price paid per share
        :param fees: fees paid on the operation
        :return: empty
        """
        self._stocks[stock].buy(stock, day, shares, price, fees)

    def sell(self, stock, day, shares, price, fees):
        """
        Sell shares of a stock. Forwards the call to the stock leaf

        :param stock: name of the stock
        :param day: day of the buy operation
        :param shares: number of shares bought
        :param price: price paid per share
        :param fees: fees paid on the operation
        :return: empty
        """
        self._stocks[stock].sell(stock, day, shares, price, fees)

    def gain_dividends(self, stock, day, shares, dividends):
        """
        Gain dividends of a stock. Forwards the call to the stock leaf

        :param stock: name of the stock
        :param day: day that the dividends were received
        :param shares: number of shares that received dividend
        :param dividends: dividends received per share
        :return: empty
        """
        self._stocks[stock].gain_dividends(stock, day, shares, dividends)

    @property
    def cost_value(self):
        """
        The current cost value of the portfolio. Aggregates the cost value of all stocks

        :return: The current cost value of the portfolio
        """
        return sum([stock.cost_value for stock in self._stocks.values()])

    @property
    def market_value(self):
        """
        The current market value of the portfolio based on the current price set for each stock. Aggregates the market
        value of all stocks

        :return: The current market value of the portfolio
        """
        return sum([stock.market_value for stock in self._stocks.values()])

    @property
    def fees(self):
        """
        The total amount of fees paid on the portfolio. Aggregates the fees paid of all stocks

        :return: The total amount of fees paid on the portfolio
        """
        return sum([stock.fees for stock in self._stocks.values()])

    @property
    def dividends(self):
        """
        The total amount of dividends received on the portfolio. Aggregates the dividends received of all stocks

        :return: The total amount of dividends received on the portfolio
        """
        return sum([stock.dividends for stock in self._stocks.values()])


class StockInvestment(StockComponent):
    """
    The StockInvestment is the leaf of the stocks
    """

    def __init__(self, stock, price=0, operations=None):
        """
        Initializes the name os the stock, the price, and the operations. The price and operations should only be used
        when restoring data from json

        :param stock: name of the stock
        :param price: price of the stock, defaults to 0
        :param operations: operations done related to the stock, defaults to empty
        """
        super().__init__()
        self._stock = stock
        self._price = price
        self._operations = operations if operations is not None else []

    @property
    def stock(self):
        """
        The name of the stock

        :return: The name of the stock
        """
        return self._stock

    @property
    def price(self):
        """
        The current price of the stock

        :return: The current price of the stock
        """
        return self._price

    @property
    def operations(self):
        """
        All the operations related to the stock

        :return: All the operations related to the stock
        """
        return self._operations

    def set_price(self, stock, price):
        """
        Sets the price of the stock

        :param stock: name of the stock
        :param price: current price of the stock
        :return: empty
        """
        self._price = price

    def buy(self, stock, day, shares, price, fees):
        """
        Buy shares of the stock

        :param stock: name of the stock
        :param day: day of the buy operation
        :param shares: number of shares bought
        :param price: price paid per share
        :param fees: fees paid on the operation
        :return: empty
        """
        self._operations.append(BuyStockOperation(stock, day, shares, price, fees))

    def sell(self, stock, day, shares, price, fees):
        """
        Sell shares of the stock

        :param stock: name of the stock
        :param day: day of the buy operation
        :param shares: number of shares bought
        :param price: price paid per share
        :param fees: fees paid on the operation
        :return: empty
        """
        self._operations.append(SellStockOperation(stock, day, shares, price, fees))

    def gain_dividends(self, stock, day, shares, dividends):
        """
        Gain dividends of the stock

        :param stock: name of the stock
        :param day: day that the dividends were received
        :param shares: number of shares that received dividend
        :param dividends: dividends received per share
        :return: empty
        """
        self._operations.append(DividendStockOperation(stock, day, shares, dividends))

    @property
    def cost_value(self):
        """
        The current cost value of the stock. The cost value is defined by the current money invested on the stock

        :return: The current cost value of the stock
        """
        return self.shares * self.average_buy_price

    @property
    def market_value(self):
        """
        The current market value of the stock based on the current price of the stock

        :return: The current market value of the stock
        """
        return self.shares * self._price

    @property
    def fees(self):
        """
        The total amount of fees paid on the stock. Aggregates the fees of all operations

        :return: The total amount of fees paid on the stock
        """
        return sum([operation.fees for operation in self._operations])

    @property
    def dividends(self):
        """
        The total amount of dividends received on the stock

        :return: The total amount of dividends received on the stock
        """
        return sum([operation.value for operation in self.dividend_operations])

    @property
    def shares(self):
        """
        The current number of shares of the stock. Subtracts the number of shares sold from the ones bought

        :return: The current number of shares of the stock
        """
        return sum([operation.shares for operation in self.buy_operations]) - sum(
            [operation.shares for operation in self.sell_operations])

    @property
    def average_buy_price(self):
        """
        The average buy price of the shares. Divides the total amount of cost from the buy operations by the total
        amount of shares bought

        :return: The average buy price of the shares
        """
        return sum([operation.value for operation in self.buy_operations]) / sum(
            [operation.shares for operation in self.buy_operations])

    @property
    def buy_operations(self):
        """
        All the buy operations

        :return: All the buy operations
        """
        return [operation for operation in self._operations if isinstance(operation, BuyStockOperation)]

    @property
    def sell_operations(self):
        """
        All the sell operations

        :return: All the sell operations
        """
        return [operation for operation in self._operations if isinstance(operation, SellStockOperation)]

    @property
    def dividend_operations(self):
        """
        All the dividend operations

        :return: All the dividend operations
        """
        return [operation for operation in self._operations if isinstance(operation, DividendStockOperation)]


class StockOperation(ABC):
    """
    Base abstract class for stock operations
    """

    def __init__(self, stock, day, shares, price, fees):
        """
        Initializes the stock operation

        :param stock: name of the stock
        :param day: day of the operation
        :param shares: number of shares
        :param price: price per share
        :param fees: fees of the operation
        """
        self._stock = stock
        self._day = day
        self._shares = shares
        self._price = price
        self._fees = fees
        self._symbol = None

    def __repr__(self):
        """
        The string representation of the operation
        Format is:
         <symbol> <stock> <shares> <price> <day> <value>

        :return: The string representation of the operation
        """
        return '{} {} {} {:.2f} {} {:.2f}'.format(self._symbol, self._stock, self._shares, self._price, self._day,
                                                  self.value)

    @property
    def stock(self):
        """
        The name of the stock

        :return: The name of the stock
        """
        return self._stock

    @property
    def day(self):
        """
        The day of the operation

        :return: The day of the operation
        """
        return self._day

    @property
    def shares(self):
        """
        The number of shares of the operation

        :return: The number of shares of the operation
        """
        return self._shares

    @property
    def price(self):
        """
        The price per share

        :return: The price per share
        """
        return self._price

    @property
    def fees(self):
        """
        The fees of the operation

        :return: The fees of the operation
        """
        return self._fees

    @property
    def symbol(self):
        """
        The operation symbol. It is overridden when inheriting

        :return: The operation symbol
        """
        return self._symbol

    @property
    def value(self):
        """
        The total value of the operation. It is calculated multiplying the number of shares by the price and adding the
        fees

        :return: The total value of the operation
        """
        return self._shares * self._price + self._fees


class BuyStockOperation(StockOperation):
    """
    Buy stock operation
    """

    def __init__(self, stock, day, shares, price, fees):
        """
        Initialize the parent fields and define the buy symbol as B

        :param stock: name of the stock
        :param day: day of the operation
        :param shares: number of shares
        :param price: price per share
        :param fees: fees of the operation
        """
        super().__init__(stock, day, shares, price, fees)
        self._symbol = 'B'


class SellStockOperation(StockOperation):
    """
    Sell stock operation
    """

    def __init__(self, stock, day, shares, price, fees):
        """
        Initialize the parent fields and define the sell symbol as S

        :param stock: name of the stock
        :param day: day of the operation
        :param shares: number of shares
        :param price: price per share
        :param fees: fees of the operation
        """
        super().__init__(stock, day, shares, price, fees)
        self._symbol = 'S'


class DividendStockOperation(StockOperation):
    """
    Dividend stock operation
    """

    def __init__(self, stock, day, shares, price):
        """
        Initialize the parent fields and define the dividend symbol as D

        :param stock: name of the stock
        :param day: day of the operation
        :param shares: number of shares
        :param price: price per share
        """
        super().__init__(stock, day, shares, price, 0)
        self._symbol = 'D'


if __name__ == '__main__':

    b = BuyStockOperation('Erste Group', '20.04.1988', 200, 17.20, 2.50)
    print(b)
    print(StockEncoder().encode(b))
    print(StockDecoder().decode(StockEncoder().encode(b)))

    s = SellStockOperation('Erste Group', '20.04.1988', 200, 17.20, 2.50)
    print(s)
    print(StockEncoder().encode(s))
    print(StockDecoder().decode(StockEncoder().encode(s)))

    si = StockInvestment('BAWAG')
    si.buy('BAWAG', '29.10.2020', 50, 31.34, 2.50)
    si.set_price('BAWAG', 32.10)
    print(si.stock)
    print(si.price)
    print(si.operations)
    print(si)
    print(StockEncoder().encode(si))
    a = StockDecoder().decode(StockEncoder().encode(si))
    print(a.stock)
    print(a.price)
    print(a.operations)

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

    p = StockPortfolio()

    for st, data in stock_data.items():
        p.add_stock(st)
        d, sh, bp, f, cp = data
        p.buy(st, d, sh, bp, f)
        p.set_price(st, cp)

    print(p.cost_value)
    print(p.market_value)
    print(p.fees)
    print(p.dividends)

    print(json.dumps(p, cls=StockEncoder))
    pa = StockDecoder().decode(StockEncoder().encode(p))

    print(pa.cost_value)
    print(pa.market_value)
    print(pa.fees)
    print(pa.dividends)
