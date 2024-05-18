import json
from src.application.interface import RepositoryInterface
from src.domain.stock import Portfolio
from src.infrastructure.json_coder import StockEncoder, decode_stock


class JSONRepository(RepositoryInterface):

    def save_portfolio(self, filename: str, portfolio: Portfolio) -> None:
        with open(filename, 'w') as json_file:
            json.dump(portfolio, json_file, cls=StockEncoder, indent=4)

    def load_portfolio(self, filename: str) -> Portfolio:
        with open(filename) as json_file:
            return json.load(json_file, object_hook=decode_stock)
