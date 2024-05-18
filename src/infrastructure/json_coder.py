import json
from typing import Any, Dict

from src.domain.stock import Portfolio, Stock, StockAggregate, StockMetrics


class StockEncoder(json.JSONEncoder):
    def default(self, object: Any) -> Any:
        if isinstance(object, Portfolio):
            return {
                'object': 'Portfolio',
                'stocks': object.stocks
            }
        elif isinstance(object, Stock):
            return {
                'object': 'Stock',
                'symbol': object.symbol,
                'name': object.name,
                'sector': object.sector,
                'current_price': object.current_price,
                'year_data': object.year_data,
                'aggregate_data': object.aggregate_data
            }
        elif isinstance(object, StockMetrics):
            return {
                'object': 'StockMetrics',
                'year': object.year,
                'market_capitalization': object.market_capitalization,
                'earnings_per_share': object.earnings_per_share,
                'closing_price': object.closing_price,
                'book_value_per_share': object.book_value_per_share,
                'dividend_per_share': object.dividend_per_share,
            }
        elif isinstance(object, StockAggregate):
            return {
                'object': 'StockAggregate',
                'year': object.year,
                'earnings_per_share': object.earnings_per_share,
                'pe_ratio': object.pe_ratio,
                'price_per_book_value': object.price_per_book_value,
                'dividends_yield': object.dividends_yield,
            }
        else:
            return super().default(object)
        

def decode_stock(object: Dict) -> Portfolio:
    if "object" in object:
        if object['object'] == 'Portfolio':
            stocks = object['stocks']
            return Portfolio(stocks)
        elif object['object'] == 'Stock':
            return Stock(object['symbol'], object['name'], object['sector'], object['current_price'], {int(year): data for year, data in object['year_data'].items()}, {int(year): data for year, data in object['aggregate_data'].items()})
        elif object['object'] == 'StockMetrics':
            return StockMetrics(object['year'], object['market_capitalization'], object['earnings_per_share'], object['closing_price'], object['book_value_per_share'], object['dividend_per_share'])
        elif object['object'] == 'StockAggregate':
            return StockAggregate(object['year'], object['earnings_per_share'], object['pe_ratio'], object['price_per_book_value'], object['dividends_yield'])
    return object
