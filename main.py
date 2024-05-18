import sys
sys.path.append('/Users/matheus/projects/attic')

from src.application.stock_interactor import AddStockYearDataUseCase, CalculateAggregateDataUseCase, CreateStockUseCase, GetStockYearDataUseCase, ListStocksUseCase, LoadPortfolioUseCase, SavePortfolioUseCase
from src.domain.stock import Portfolio
from src.infrastructure.cli import StockCmd
from src.infrastructure.controller_cli import CliController
from src.infrastructure.repository import JSONRepository


if __name__ == '__main__':
    portfolio = Portfolio()
    repository = JSONRepository()
    create_stock_use_case = CreateStockUseCase(portfolio)
    add_stock_year_data_use_case = AddStockYearDataUseCase(portfolio)
    calculate_aggregate_data_use_case = CalculateAggregateDataUseCase(portfolio)
    list_stocks_use_case = ListStocksUseCase(portfolio)
    get_stock_year_data_use_case = GetStockYearDataUseCase(portfolio)
    save_portfolio_use_case = SavePortfolioUseCase(portfolio, repository)
    load_portfolio_use_case = LoadPortfolioUseCase(portfolio, repository)
    controller = CliController(create_stock_use_case, add_stock_year_data_use_case, calculate_aggregate_data_use_case, list_stocks_use_case,
                               get_stock_year_data_use_case, save_portfolio_use_case, load_portfolio_use_case)
    cli = StockCmd(controller)
    cli.cmdloop()
    