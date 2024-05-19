from typing import List
from src.application.interface import RepositoryInterface
from src.domain.stock import Portfolio, Stock


class InMemoryRepository(RepositoryInterface):

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    def add_stock(self, stock: Stock) -> None:
        self.portfolio.stocks[stock.symbol] = stock
        
    def get_stocks(self) -> List[Stock]:
        return list(self.portfolio.stocks.values())
