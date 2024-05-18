from prettytable import PrettyTable
from src.domain.stock import Portfolio, Stock, StockMetrics
from src.application.interface import RepositoryInterface


class CreateStockUseCase:

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def execute(self, symbol: str, name: str, sector: str, current_price: float) -> None:
        stock = Stock(symbol, name, sector, current_price)
        self.portfolio.stocks[symbol] = stock


class AddStockYearDataUseCase:

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def execute(self, symbol: str, year: int, market_capitalization: float, earnings_per_share: float,
                closing_price: float, book_value_per_share: float, dividend_per_share: float) -> None:
        stock = self.portfolio.stocks[symbol]
        metrics = StockMetrics(year, market_capitalization, earnings_per_share, closing_price, book_value_per_share, dividend_per_share)
        stock.year_data[year] = metrics


class CalculateAggregateDataUseCase:

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def execute(self) -> None:
        for stock in self.portfolio.stocks.values():
            stock.calculate_aggregation()


class ListStocksUseCase:

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def execute(self) -> None:
        for stock in self.portfolio.stocks.keys():
            print(stock)


class GetStockYearDataUseCase:

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def execute(self, symbol: str) -> None:
        stock = self.portfolio.stocks[symbol]
        table = PrettyTable()
        for data in sorted(stock.year_data.values(), key=lambda x: x.year, reverse=True):
            table.field_names = list(data.to_dict().keys())
            table.add_row(list(data.to_dict().values()))
        print(table)
        print()


class SavePortfolioUseCase:

    def __init__(self, portfolio: Portfolio, repository: RepositoryInterface) -> None:
        self.portfolio = portfolio
        self.repository = repository

    def execute(self, filename: str) -> None:
        self.repository.save_portfolio(filename, self.portfolio)


class LoadPortfolioUseCase:

    def __init__(self, portfolio: Portfolio, repository: RepositoryInterface) -> None:
        self.portfolio = portfolio
        self.repository = repository

    def execute(self, filename: str) -> None:
        self.portfolio.stocks = self.repository.load_portfolio(filename).stocks
