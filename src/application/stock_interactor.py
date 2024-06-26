from prettytable import PrettyTable
from src.domain.stock import Stock, StockMetrics
from src.application.interface import PersistenceInterface, PresenterInterface, RepositoryInterface


class CreateStockUseCase:

    def __init__(self, repository: RepositoryInterface) -> None:
        self.repository = repository

    def execute(self, symbol: str, name: str, sector: str, current_price: float) -> None:
        stock = Stock(symbol, name, sector, current_price)
        self.repository.add_stock(stock)


class AddStockYearDataUseCase:

    def __init__(self, repository: RepositoryInterface) -> None:
        self.repository = repository

    def execute(self, symbol: str, year: int, market_capitalization: float, earnings_per_share: float,
                closing_price: float, book_value_per_share: float, dividend_per_share: float) -> None:
        metrics = StockMetrics(year, market_capitalization, earnings_per_share, closing_price, book_value_per_share, dividend_per_share)
        self.repository.add_year_data(symbol, metrics)


class CalculateAggregateDataUseCase:

    def __init__(self, repository: RepositoryInterface) -> None:
        self.repository = repository

    def execute(self) -> None:
        for stock in self.repository.get_stocks():
            stock.calculate_aggregation()


class GetStockYearDataUseCase:

    def __init__(self, repository: RepositoryInterface, presenter: PresenterInterface) -> None:
        self.repository = repository
        self.presenter = presenter

    def execute(self, symbol: str) -> None:
        stock = self.repository.get_stock(symbol)
        if stock is None:
            return
        self.presenter.show_year_data(list(stock.year_data.values()))


class GetStockAggregateDataUseCase:

    def __init__(self, repository: RepositoryInterface, presenter: PresenterInterface) -> None:
        self.repository = repository
        self.presenter = presenter

    def execute(self, symbol: str) -> None:
        stock = self.repository.get_stock(symbol)
        if stock is None:
            return
        self.presenter.show_aggregate_data(list(stock.aggregate_data.values()))


class GetStockCurrentDataUseCase:

    def __init__(self, repository: RepositoryInterface, presenter: PresenterInterface) -> None:
        self.repository = repository
        self.presenter = presenter

    def execute(self, symbol: str) -> None:
        stock = self.repository.get_stock(symbol)
        if stock is None:
            return
        self.presenter.show_stock_data(stock)


class SavePortfolioUseCase:

    def __init__(self, repository: RepositoryInterface, persistence: PersistenceInterface) -> None:
        self.repository = repository
        self.persistence = persistence

    def execute(self, filename: str) -> None:
        self.persistence.save_portfolio(filename, self.repository.get_portfolio())


class LoadPortfolioUseCase:

    def __init__(self, repository: RepositoryInterface, persistence: PersistenceInterface) -> None:
        self.repository = repository
        self.persistence = persistence

    def execute(self, filename: str) -> None:
        self.repository.set_portfolio(self.persistence.load_portfolio(filename))
