from typing import Dict
from prettytable import PrettyTable
from src.application.interface import PresenterInterface
from src.domain.stock import Stock, StockAggregate, StockMetrics
from src.interface.view import ViewInterface


class Presenter(PresenterInterface):

    def __init__(self, view: ViewInterface) -> None:
        self.view = view

    def show_year_data(self, year_data: Dict[int, StockMetrics]) -> None:
        header = list(list(year_data.values())[0].to_dict().keys())
        rows = [list(data.to_dict().values()) for data in sorted(year_data.values(), key=lambda x: x.year, reverse=True)]
        self.view.show_tabular_data(header, rows)

    def show_aggregate_data(self, aggregate_data: Dict[int, StockAggregate]) -> None:
        header = list(list(aggregate_data.values())[0].to_dict().keys())
        rows = [list(data.to_dict().values()) for data in sorted(aggregate_data.values(), key=lambda x: x.year, reverse=True)]
        self.view.show_tabular_data(header, rows)

    def show_stock_data(self, stock: Stock) -> None:
        print(stock.year_data[2023].to_dict())
        print(stock.aggregate_data[2023].to_dict())
        print()

    