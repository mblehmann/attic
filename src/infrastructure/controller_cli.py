import os
from src.application.stock_interactor import AddStockYearDataUseCase, CalculateAggregateDataUseCase, CreateStockUseCase, GetStockAggregateDataUseCase, GetStockCurrentDataUseCase, GetStockYearDataUseCase, LoadPortfolioUseCase, SavePortfolioUseCase


class CliController:

    def __init__(self,
                 create_stock_use_case: CreateStockUseCase,
                 add_stock_year_data_use_case: AddStockYearDataUseCase,
                 calculate_aggregate_data_use_case: CalculateAggregateDataUseCase,
                 get_stock_year_data_use_case: GetStockYearDataUseCase,
                 get_stock_aggregate_data_use_case: GetStockAggregateDataUseCase,
                 get_stock_current_data_use_case: GetStockCurrentDataUseCase,
                 save_portfolio_use_case: SavePortfolioUseCase,
                 load_portfolio_use_case: LoadPortfolioUseCase) -> None:
        self.create_stock_use_case = create_stock_use_case
        self.add_stock_year_data_use_case = add_stock_year_data_use_case
        self.calculate_aggregate_data_use_case = calculate_aggregate_data_use_case
        self.get_stock_year_data_use_case = get_stock_year_data_use_case
        self.get_stock_aggregate_data_use_case = get_stock_aggregate_data_use_case
        self.get_stock_current_data_use_case = get_stock_current_data_use_case
        self.save_portfolio_use_case = save_portfolio_use_case
        self.load_portfolio_use_case = load_portfolio_use_case
        self.filename = None

    def create_stock(self) -> None:
        symbol = input('Symbol: ')
        name = input('Name: ')
        sector = input('Sector: ')
        current_price = float(input('Current Price: '))
        self.create_stock_use_case.execute(symbol, name, sector, current_price)

    def add_stock_year_data(self) -> None:
        symbol = input('Symbol: ')
        year = int(input('Year: '))
        try:
            market_capitalization = float(input('Market Capitalization (B): '))
        except ValueError:
            market_capitalization = None
        earnings_per_share = float(input('Earnings per Share: '))
        closing_price = float(input('Closing Price: '))
        try:
            book_value_per_share = float(input('Book Value per Share: '))
        except ValueError:
            book_value_per_share = None
        dividend_per_share = float(input('Dividends per Share: '))
        self.add_stock_year_data_use_case.execute(symbol, year, market_capitalization, earnings_per_share, closing_price, book_value_per_share, dividend_per_share)
        self.save_portfolio()

    def calculate_aggregate(self) -> None:
        self.calculate_aggregate_data_use_case.execute()

    def get_stock_year_data(self) -> None:
        symbol = input('Symbol: ')
        self.get_stock_year_data_use_case.execute(symbol)

    def get_stock_aggregate_data(self) -> None:
        symbol = input('Symbol: ')
        self.get_stock_aggregate_data_use_case.execute(symbol)

    def get_stock_current_data(self) -> None:
        symbol = input('Symbol: ')
        self.get_stock_current_data_use_case.execute(symbol)

    def save_portfolio(self) -> None:
        if self.filename is None:
            self.filename = input('Filename: ')
            self.filename = os.path.join('data', self.filename)
        self.save_portfolio_use_case.execute(self.filename)

    def load_portfolio(self) -> None:
        if self.filename is None:
            self.filename = input('Filename: ')
            self.filename = os.path.join('data', self.filename)
        self.load_portfolio_use_case.execute(self.filename)
