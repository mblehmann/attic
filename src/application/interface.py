from typing import Protocol

from src.domain.stock import Portfolio


class RepositoryInterface(Protocol):

    def save_portfolio(self, filename: str, portfolio: Portfolio) -> None:
        ...

    def load_portfolio(self, filename: str) -> Portfolio:
        ...
