import unittest

from src.domain.stock import Stock, StockMetrics


class TestStock(unittest.TestCase):
    
    def setUp(self) -> None:
        self.metrics = {
            2020: StockMetrics(year=2020, market_capitalization=3.897, earnings_per_share=2.08, closing_price=37.48, book_value_per_share=12.64, dividend_per_share=1.00),
            2019: StockMetrics(year=2019, market_capitalization=3.993, earnings_per_share=1.27, closing_price=38.40, book_value_per_share=12.05, dividend_per_share=0.50),
            2018: StockMetrics(year=2018, market_capitalization=4.172, earnings_per_share=2.20, closing_price=40.12, book_value_per_share=13.02, dividend_per_share=1.55),
            2017: StockMetrics(year=2017, market_capitalization=4.896, earnings_per_share=2.58, closing_price=47.09, book_value_per_share=12.77, dividend_per_share=1.55),
            2016: StockMetrics(year=2016, market_capitalization=4.960, earnings_per_share=2.69, closing_price=47.70, book_value_per_share=13.00, dividend_per_share=1.50),
            2010: StockMetrics(year=2010, market_capitalization=3.577, earnings_per_share=1.74, closing_price=19.77, book_value_per_share=7.34, dividend_per_share=0.85),
            2009: StockMetrics(year=2009, market_capitalization=2.107, earnings_per_share=0.96, closing_price=21.10, book_value_per_share=6.14, dividend_per_share=0.50),
            2008: StockMetrics(year=2008, market_capitalization=0.944, earnings_per_share=1.37, closing_price=6.63, book_value_per_share=5.30, dividend_per_share=0.55)
        }
        self.stock = Stock(symbol="ANDR", name="Andritz", sector="Technology", year_data=self.metrics, aggregate_data={}, current_price=54.25)

    def test_pe_ratio(self) -> None:
        self.assertAlmostEqual(18.02, self.metrics[2020].pe_ratio, 2)
        self.assertAlmostEqual(30.24, self.metrics[2019].pe_ratio, 2)
        self.assertAlmostEqual(18.24, self.metrics[2018].pe_ratio, 2)

    def test_price_per_book_value(self) -> None:
        self.assertAlmostEqual(2.97, self.metrics[2020].price_per_book_value, 2)
        self.assertAlmostEqual(3.19, self.metrics[2019].price_per_book_value, 2)
        self.assertAlmostEqual(3.08, self.metrics[2018].price_per_book_value, 2)

    def test_dividend_yield(self) -> None:
        self.assertAlmostEqual(2.67, self.metrics[2020].dividend_yield, 2)
        self.assertAlmostEqual(1.30, self.metrics[2019].dividend_yield, 2)
        self.assertAlmostEqual(3.86, self.metrics[2018].dividend_yield, 2)

    def test_aggregation(self) -> None:
        aggregation = self.stock.create_aggregation(2020)
        self.assertEqual(2020, aggregation.year)
        self.assertAlmostEqual(1.85, aggregation.earnings_per_share, 2)
        self.assertAlmostEqual(20.26, aggregation.pe_ratio, 2)
        self.assertAlmostEqual(3.08, aggregation.price_per_book_value, 2)
        self.assertAlmostEqual(2.85, aggregation.dividend_yield, 2)
        self.assertAlmostEqual(62.36, aggregation.multiplier, 2)

    def test_calculate_aggregation(self):
        self.stock.calculate_aggregation()
        self.assertIn(2016, self.stock.aggregate_data)
        self.assertIn(2017, self.stock.aggregate_data)
        self.assertIn(2018, self.stock.aggregate_data)
        self.assertIn(2019, self.stock.aggregate_data)
        self.assertIn(2020, self.stock.aggregate_data)

    def test_growth(self):
        self.stock.calculate_aggregation()
        self.assertAlmostEqual(36.36, self.stock.growth, 2)

if __name__ == '__main__':
    unittest.main()
