from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class StockMetrics:
    year: int
    market_capitalization: float
    earnings_per_share: float
    closing_price: float
    book_value_per_share: Optional[float]
    dividend_per_share: float

    @property
    def pe_ratio(self) -> Optional[float]:
        if self.earnings_per_share > 0:
            return self.closing_price / self.earnings_per_share
        return None

    @property
    def price_per_book_value(self) -> Optional[float]:
        if self.book_value_per_share:
            return self.closing_price / self.book_value_per_share
        return None
    
    @property
    def dividend_yield(self) -> float:
        return self.dividend_per_share / self.closing_price
    

@dataclass
class StockAggregate:
    year: int
    earnings_per_share: float
    pe_ratio: Optional[float]
    growth: float
    price_per_book_value: Optional[float]
    dividend_yield: float

    @property
    def multiplier(self) -> Optional[float]:
        if self.pe_ratio is not None and self.price_per_book_value is not None:
            return self.pe_ratio * self.price_per_book_value
        return None


@dataclass
class Stock:
    symbol: str
    name: str
    sector: str
    current_price: float
    year_data: Dict[int, StockMetrics] = field(default_factory=dict)
    aggregate_data: Dict[int, StockAggregate] = field(default_factory=dict)

    def calculate_aggregation(self) -> None:
        for year in self.year_data.keys():
            aggregate = self.create_aggregation(year)
            self.aggregate_data[year] = aggregate
        self.calculate_growth()

    def create_aggregation(self, year: int) -> StockAggregate:
        period = self.get_period(year, 3)
        earnings_per_share = self.average([metric.earnings_per_share for metric in period])
        pe_ratio = period[0].closing_price / earnings_per_share if earnings_per_share > 0 else None
        price_per_book_value = self.average([metric.price_per_book_value for metric in period if metric.price_per_book_value is not None])        
        period = self.get_period(year, 5)
        dividends_yield = self.average([metric.dividend_yield for metric in period])
        return StockAggregate(year, earnings_per_share, pe_ratio, None, price_per_book_value, dividends_yield)

    def calculate_growth(self) -> None:
        for year, aggregate in self.aggregate_data.items():
            compare_year = self.get_compare_year(year)
            if self._is_eps_valid(aggregate.earnings_per_share) and self._is_eps_valid(self.aggregate_data[compare_year].earnings_per_share):
                aggregate.growth = aggregate.earnings_per_share / self.aggregate_data[compare_year].earnings_per_share - 1

    def average(self, values: List[float]) -> Optional[float]:
        if len(values) == 0:
            return None
        return sum(values) / len(values)
    
    def get_period(self, year: int, duration: int) -> List[StockMetrics]:
        period = [value for value in range(year, year-duration, -1)]
        return [metric for ye, metric in self.year_data.items() if ye in period]

    def get_compare_year(self, year: int) -> int:
        compare_year = year - 10
        while compare_year not in self.aggregate_data:
            compare_year += 1
        return compare_year
    
    def _is_eps_valid(self, earning_per_share: Optional[float]) -> bool:
        return earning_per_share is not None and earning_per_share > 0

@dataclass
class Portfolio:
    stocks: Dict[str, Stock] = field(default_factory=dict)
