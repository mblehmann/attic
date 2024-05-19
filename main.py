import sys

sys.path.append('/Users/matheus/projects/attic')

from src.application.stock_interactor import AddStockYearDataUseCase, CalculateAggregateDataUseCase, CreateStockUseCase, GetStockAggregateDataUseCase, GetStockCurrentDataUseCase, GetStockYearDataUseCase, LoadPortfolioUseCase, SavePortfolioUseCase
from src.domain.stock import Portfolio
from src.infrastructure.cli import StockCmd
from src.infrastructure.controller_cli import CliController
from src.infrastructure.persistence import JSONPersistence
from src.infrastructure.repository import InMemoryRepository


if __name__ == '__main__':
    repository = InMemoryRepository(Portfolio())
    persistence = JSONPersistence()
    create_stock_use_case = CreateStockUseCase(repository)
    add_stock_year_data_use_case = AddStockYearDataUseCase(repository)
    calculate_aggregate_data_use_case = CalculateAggregateDataUseCase(repository)
    get_stock_year_data_use_case = GetStockYearDataUseCase(repository)
    get_stock_aggregate_data_use_case = GetStockAggregateDataUseCase(repository)
    get_stock_current_data_use_case = GetStockCurrentDataUseCase(repository)
    save_portfolio_use_case = SavePortfolioUseCase(repository, persistence)
    load_portfolio_use_case = LoadPortfolioUseCase(repository, persistence)
    controller = CliController(create_stock_use_case, add_stock_year_data_use_case, calculate_aggregate_data_use_case, get_stock_year_data_use_case,
                               get_stock_aggregate_data_use_case, get_stock_current_data_use_case, save_portfolio_use_case, load_portfolio_use_case)
    cli = StockCmd(controller)
    cli.cmdloop()
    