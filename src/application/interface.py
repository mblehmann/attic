from typing import List, Optional, Protocol

from src.domain.stock import Portfolio, Stock, StockMetrics


class PersistenceInterface(Protocol):

    def save_portfolio(self, filename: str, portfolio: Portfolio) -> None:
        ...

    def load_portfolio(self, filename: str) -> Portfolio:
        ...


class RepositoryInterface(Protocol):

    def add_stock(self, stock: Stock) -> None:
        ...

    def add_year_data(self, symbol: str, metrics: StockMetrics) -> None:
        ...

    def get_stocks(self) -> List[Stock]:
        ...

    def get_stock(self, symbol: str) -> Optional[Stock]:
        ...

    def get_portfolio(self) -> Portfolio:
        ...

    def set_portfolio(self, portfolio: Portfolio) -> None:
        ...
