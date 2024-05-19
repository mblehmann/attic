from typing import List, Protocol

from src.domain.stock import Portfolio, Stock


class PersistenceInterface(Protocol):

    def save_portfolio(self, filename: str, portfolio: Portfolio) -> None:
        ...

    def load_portfolio(self, filename: str) -> Portfolio:
        ...


class RepositoryInterface(Protocol):

    def add_stock(self, stock: Stock) -> None:
        ...

    def get_stocks(self) -> List[Stock]:
        ...
