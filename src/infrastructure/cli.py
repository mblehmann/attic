import cmd
from src.infrastructure.controller_cli import CliController


class StockCmd(cmd.Cmd):
    prompt = 'stock> '

    def __init__(self, controller: CliController):
        super().__init__()
        self.controller = controller

    def do_create_stock(self, _: str) -> None:
        """create_stock: Creates a new stock"""
        self.controller.create_stock()

    def do_add_stock_year_data(self, _: str) -> None:
        """add_stock_year_data: Adds stock year data"""
        self.controller.add_stock_year_data()

    def do_calculate_aggregate(self, _: str) -> None:
        """calculate_aggregate: Calculates the aggregate for all stocks"""
        self.controller.calculate_aggregate()

    def do_get_stock_year_data(self, _: str) -> None:
        """get_stock_year_data: Gets year data of a stock"""
        self.controller.get_stock_year_data()

    def do_get_stock_aggregate_data(self, _: str) -> None:
        """get_stock_aggregate_data: Gets aggregate data of a stock"""
        self.controller.get_stock_aggregate_data()

    def do_get_stock_current_data(self, _: str) -> None:
        """get_stock_current_data: Gets current data of a stock"""
        self.controller.get_stock_current_data()

    def do_save(self, _: str) -> None:
        """save: Saves portfolio"""
        self.controller.save_portfolio()

    def do_load(self, _: str) -> None:
        """load: Loads portfolio"""
        self.controller.load_portfolio()

    def do_quit(self, _: str) -> bool:
        """quit: Quits the program"""
        return True
