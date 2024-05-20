from typing import Dict, List
from prettytable import PrettyTable
from src.application.interface import PresenterInterface
from src.domain.stock import Stock, StockAggregate, StockMetrics
from src.interface.view import ViewInterface


class Presenter(PresenterInterface):

    def __init__(self, view: ViewInterface) -> None:
        self.view = view

    def show_year_data(self, year_data: List[StockMetrics]) -> None:
        header = ['Year', 'Market Cap.', 'EPS', 'Closing Price', 'P/E Ratio', 'BV / Share', 'Price / BV', 'Dividend', 'Dividend Yield']
        rows = [self._get_year_data(data) for data in sorted(year_data, key=lambda x: x.year, reverse=True)]
        self.view.show_tabular_data(header, rows)

    def show_aggregate_data(self, aggregate_data: List[StockAggregate]) -> None:
        header = ['Year', 'EPS', 'P/E Ratio', 'Price / BV', 'Multiplier', 'Dividend Yield']
        rows =[self._get_aggregate_data(data) for data in sorted(aggregate_data, key=lambda x: x.year, reverse=True)]
        self.view.show_tabular_data(header, rows)

    def show_stock_data(self, stock: Stock) -> None:
        print(stock.year_data[2023].to_dict())
        print(stock.aggregate_data[2023].to_dict())
        print()

    def _get_year_data(self, year_data: StockMetrics) -> List[str]:
        return [
            f'{year_data.year}',
            f'{year_data.market_capitalization:.3f}' if year_data.market_capitalization is not None else '-',
            f'{year_data.earnings_per_share:.2f}',
            f'{year_data.closing_price:.2f}',
            f'{year_data.pe_ratio:.2f}' if year_data.pe_ratio is not None else '-',
            f'{year_data.book_value_per_share:.2f}' if year_data.book_value_per_share is not None else '-',
            f'{year_data.price_per_book_value:.2f}' if year_data.price_per_book_value is not None else '-',
            f'{year_data.dividend_per_share:.2f}',
            f'{year_data.dividend_yield:.2%}',
        ]

    def _get_aggregate_data(self, aggregate_data: StockAggregate) -> List[str]:
        return [
            f'{aggregate_data.year}',
            f'{aggregate_data.earnings_per_share:.2f}' if aggregate_data.earnings_per_share is not None else '-',
            f'{aggregate_data.pe_ratio:.2f}' if aggregate_data.pe_ratio is not None else '-',
            f'{aggregate_data.price_per_book_value:.2f}' if aggregate_data.price_per_book_value is not None else '-',
            f'{aggregate_data.multiplier:.2f}',
            f'{aggregate_data.dividend_yield:.2%}',
        ]
    