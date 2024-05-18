import unittest
import json
from src.domain.stock import Portfolio, Stock, StockAggregate, StockMetrics
from src.infrastructure.json_coder import StockEncoder, decode_stock

class TestEncoders(unittest.TestCase):

    def test_portfolio_encoder(self) -> None:
        portfolio = Portfolio({
            'AAPL': Stock('AAPL', 'Apple', 'Technology', 150.0, {2022: StockMetrics(2022, 4.335, 2.59, 34.20, 5.43, 8.65)}, {2020: StockAggregate(2020, 1.20, 2.40, 4.34, 6.43)}),
            'GOOG': Stock('GOOG', 'Alphabet', 'Technology', 2500.0, {}, {})
        })
        expected_encoded_portfolio = '{"object": "Portfolio", "stocks": {"AAPL": {"object": "Stock", "symbol": "AAPL", "name": "Apple", "sector": "Technology", "current_price": 150.0, "year_data": {"2022": {"object": "StockMetrics", "year": 2022, "market_capitalization": 4.335, "earnings_per_share": 2.59, "closing_price": 34.2, "book_value_per_share": 5.43, "dividend_per_share": 8.65}}, "aggregate_data": {"2020": {"object": "StockAggregate", "year": 2020, "earnings_per_share": 1.2, "pe_ratio": 2.4, "price_per_book_value": 4.34, "dividends_yield": 6.43}}}, "GOOG": {"object": "Stock", "symbol": "GOOG", "name": "Alphabet", "sector": "Technology", "current_price": 2500.0, "year_data": {}, "aggregate_data": {}}}}'
        
        actual_encoded_portfolio = json.dumps(portfolio, cls=StockEncoder)
        self.assertEqual(actual_encoded_portfolio, expected_encoded_portfolio)
        
    def test_stock_encoder(self) -> None:
        stock = Stock('AAPL', 'Apple', 'Technology', 150.0, {2022: StockMetrics(2022, 4.335, 2.59, 34.20, 5.43, 8.65)}, {2020: StockAggregate(2020, 1.20, 2.40, 4.34, 6.43)})
        expected_encoded_stock = '{"object": "Stock", "symbol": "AAPL", "name": "Apple", "sector": "Technology", "current_price": 150.0, "year_data": {"2022": {"object": "StockMetrics", "year": 2022, "market_capitalization": 4.335, "earnings_per_share": 2.59, "closing_price": 34.2, "book_value_per_share": 5.43, "dividend_per_share": 8.65}}, "aggregate_data": {"2020": {"object": "StockAggregate", "year": 2020, "earnings_per_share": 1.2, "pe_ratio": 2.4, "price_per_book_value": 4.34, "dividends_yield": 6.43}}}'

        actual_encoded_stock = json.dumps(stock, cls=StockEncoder)
        self.assertEqual(actual_encoded_stock, expected_encoded_stock)
    
    def test_stock_metrics_encoder(self) -> None:
        stock_metrics = StockMetrics(2022, 4.335, 2.59, 34.20, 5.43, 8.65)
        expected_encoded_stock_metrics = '{"object": "StockMetrics", "year": 2022, "market_capitalization": 4.335, "earnings_per_share": 2.59, "closing_price": 34.2, "book_value_per_share": 5.43, "dividend_per_share": 8.65}'

        actual_encoded_stock_metrics = json.dumps(stock_metrics, cls=StockEncoder)
        self.assertEqual(actual_encoded_stock_metrics, expected_encoded_stock_metrics)

    def test_stock_aggregate_encoder(self) -> None:
        stock_aggregate = StockAggregate(2020, 1.20, 2.40, 4.34, 6.43)
        expected_encoded_stock_aggregate = '{"object": "StockAggregate", "year": 2020, "earnings_per_share": 1.2, "pe_ratio": 2.4, "price_per_book_value": 4.34, "dividends_yield": 6.43}'
        
        actual_encoded_stock_aggregate = json.dumps(stock_aggregate, cls=StockEncoder)
        self.assertEqual(actual_encoded_stock_aggregate, expected_encoded_stock_aggregate)


class TestDecoders(unittest.TestCase):

    def test_portfolio_decoder(self) -> None:
        encoded_portfolio = '{"object": "Portfolio", "stocks": {"AAPL": {"object": "Stock", "symbol": "AAPL", "name": "Apple", "sector": "Technology", "current_price": 150.0, "year_data": {"2022": {"object": "StockMetrics", "year": 2022, "market_capitalization": 4.335, "earnings_per_share": 2.59, "closing_price": 34.2, "book_value_per_share": 5.43, "dividend_per_share": 8.65}}, "aggregate_data": {"2020": {"object": "StockAggregate", "year": 2020, "earnings_per_share": 1.2, "pe_ratio": 2.4, "price_per_book_value": 4.34, "dividends_yield": 6.43}}}, "GOOG": {"object": "Stock", "symbol": "GOOG", "name": "Alphabet Inc.", "sector": "Technology", "current_price": 2500.0, "year_data": {}, "aggregate_data": {}}}}'
        expected_portfolio = Portfolio({
            'AAPL': Stock('AAPL', 'Apple', 'Technology', 150.0, {2022: StockMetrics(2022, 4.335, 2.59, 34.20, 5.43, 8.65)}, {2020: StockAggregate(2020, 1.20, 2.40, 4.34, 6.43)}),
            'GOOG': Stock('GOOG', 'Alphabet Inc.', 'Technology', 2500.0, {}, {})
        })

        decoded_portfolio = json.loads(encoded_portfolio, object_hook=decode_stock)
        self.assertEqual(decoded_portfolio, expected_portfolio)

    def test_stock_decoder(self) -> None:
        encoded_stock = '{"object": "Stock", "symbol": "AAPL", "name": "Apple", "sector": "Technology", "current_price": 150.0, "year_data": {"2022": {"object": "StockMetrics", "year": 2022, "market_capitalization": 4.335, "earnings_per_share": 2.59, "closing_price": 34.2, "book_value_per_share": 5.43, "dividend_per_share": 8.65}}, "aggregate_data": {"2020": {"object": "StockAggregate", "year": 2020, "earnings_per_share": 1.2, "pe_ratio": 2.4, "price_per_book_value": 4.34, "dividends_yield": 6.43}}}'
        expected_stock = Stock('AAPL', 'Apple', 'Technology', 150.0, {2022: StockMetrics(2022, 4.335, 2.59, 34.20, 5.43, 8.65)}, {2020: StockAggregate(2020, 1.20, 2.40, 4.34, 6.43)})

        decoded_stock = json.loads(encoded_stock, object_hook=decode_stock)
        self.assertEqual(decoded_stock, expected_stock)

    def test_stock_metrics_decoder(self) -> None:
        encoded_stock_metrics = '{"object": "StockMetrics", "year": 2022, "market_capitalization": 4.335, "earnings_per_share": 2.59, "closing_price": 34.2, "book_value_per_share": 5.43, "dividend_per_share": 8.65}'
        expected_encoded_stock_metrics = StockMetrics(2022, 4.335, 2.59, 34.20, 5.43, 8.65)

        decoded_stock_metrics = json.loads(encoded_stock_metrics, object_hook=decode_stock)
        self.assertEqual(decoded_stock_metrics, expected_encoded_stock_metrics)

    def test_stock_aggregate_decoder(self) -> None:
        encoded_stock_aggregate = '{"object": "StockAggregate", "year": 2020, "earnings_per_share": 1.2, "pe_ratio": 2.4, "price_per_book_value": 4.34, "dividends_yield": 6.43}'
        expected_stock_aggregate = StockAggregate(2020, 1.20, 2.40, 4.34, 6.43)

        decoded_stock_aggregate = json.loads(encoded_stock_aggregate, object_hook=decode_stock)
        self.assertEqual(decoded_stock_aggregate, expected_stock_aggregate)

if __name__ == '__main__':
    unittest.main()
