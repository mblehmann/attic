from typing import Protocol


class ViewInterface(Protocol):

    def show_tabular_data(self) -> None:
        ...

    def show_dict_data(self) -> None:
        ...
