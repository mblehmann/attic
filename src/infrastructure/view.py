from typing import List
from prettytable import PrettyTable
from src.interface.view import ViewInterface


class CliView(ViewInterface):

    def show_tabular_data(self, header: List[str], rows: List[List[str]]) -> None:
        table = PrettyTable()
        table.field_names = header
        for row in rows:
            table.add_row(row)
        print(table)
        print()

    def show_dict_data(self) -> None:
        ...
