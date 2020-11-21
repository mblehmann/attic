import unittest
from decimal import *

from stocks.stock import StockPortfolio


class TestStock(unittest.TestCase):

    def test_something(self):
        # current price as of 20.11.2020
        stock_data = {
            'BG.VI': [('29.10.2020', 50, 31.34, 2.50), (37.88, 1894.00, 324.50, 20.68)],
            'CAI.VI': [('29.10.2020', 60, 23.45, 2.50), (28.65, 1719.00, 309.50, 21.96)],
            'EBS.VI': [('29.10.2020', 200, 17.20, 2.50), (23.44, 4688.00, 1245.50, 36.18)],
            'LNG.VI': [('29.10.2020', 20, 59.70, 2.50), (71.10, 1422.00, 225.50, 18.85)],
            'OMV.VI': [('29.10.2020', 150, 19.85, 2.50), (28.18, 4227.00, 1247.00, 41.85)],
            'RBI.VI': [('29.10.2020', 230, 12.02, 2.50), (15.68, 3606.40, 839.30, 30.33)],
            'SPI.VI': [('29.10.2020', 220, 12.86, 2.50), (15.68, 3449.60, 617.90, 21.82)],
            'UQA.VI': [('29.10.2020', 600, 4.73, 2.50), (6.19, 3714.00, 873.50, 30.75)],
            'VIG.VI': [('29.10.2020', 160, 17.20, 2.50), (19.52, 3123.20, 368.70, 13.39)]
        }

        total_cost, total_fee, total_value, total_profit, total_percentage = (21769.30, 22.50, 27843.20, 6051.40, 27.77)
        sp = StockPortfolio()

        for stock, (buy, current) in stock_data.items():
            with self.subTest(stock):
                day, shares, price, fees = buy
                sp.add_stock(stock)
                sp.buy(stock, day, shares, price, fees)

                cur_price, expected_value, expected_profit, expected_percentage = current
                sp.set_price(stock, cur_price)

                si = sp.get_stock(stock)
                self.assertEqual(si.stock, stock)
                self.assertEqual(len(si.operations), 1)
                self.assertAlmostEqual(si.price, Decimal(cur_price), 2)
                self.assertAlmostEqual(si.market_value, Decimal(expected_value), 2)
                self.assertAlmostEqual(si.current_profit, Decimal(expected_profit), 2)
                self.assertAlmostEqual(si.current_profit_percentage, Decimal(expected_percentage), 2)

        self.assertAlmostEqual(sp.cost_value, Decimal(total_cost + total_fee), 2)
        self.assertAlmostEqual(sp.fees, Decimal(total_fee), 2)
        self.assertAlmostEqual(sp.market_value, Decimal(total_value), 2)
        self.assertAlmostEqual(sp.current_profit, Decimal(total_profit), 2)
        self.assertAlmostEqual(sp.current_profit_percentage, Decimal(total_percentage), 2)


if __name__ == '__main__':
    unittest.main()
