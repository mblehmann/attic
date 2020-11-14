import unittest


class TestStock(unittest.TestCase):

    def test_something(self):
        stock_data = {
            'BAWAG': ('29.10.2020', 50, 31.34, 2.50, 32.10),
            'CA IMMO': ('29.10.2020', 60, 23.45, 2.50, 25.25),
            'ERSTE GROUP': ('29.10.2020', 200, 17.20, 2.50, 17.98),
            'LENZING': ('29.10.2020', 20, 59.70, 2.50, 65.20),
            'OMV': ('29.10.2020', 150, 19.85, 2.50, 21.02),
            'RAIFFEISEN': ('29.10.2020', 230, 12.02, 2.50, 12.82),
            'S IMMO': ('29.10.2020', 220, 12.86, 2.50, 13.68),
            'UNIQA': ('29.10.2020', 600, 4.73, 2.50, 5.02),
            'VIENNA': ('29.10.2020', 160, 17.20, 2.50, 17.46)
        }
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
