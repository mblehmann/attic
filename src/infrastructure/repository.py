from typing import List, Optional
from src.application.interface import RepositoryInterface
from src.domain.stock import Portfolio, Stock, StockMetrics


class InMemoryRepository(RepositoryInterface):

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def add_stock(self, stock: Stock) -> None:
        self.portfolio.stocks[stock.symbol] = stock
        
    def add_year_data(self, symbol: str, metrics: StockMetrics) -> None:
        stock = self.get_stock(symbol)
        if stock is not None:
            stock.year_data[metrics.year] = metrics

    def get_stocks(self) -> List[Stock]:
        return list(self.portfolio.stocks.values())

    def get_stock(self, symbol: str) -> Optional[Stock]:
        return self.portfolio.stocks.get(symbol, None)

    def get_portfolio(self) -> Portfolio:
        return self.portfolio

    def set_portfolio(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio
