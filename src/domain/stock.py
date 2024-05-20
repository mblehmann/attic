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
    pe_ratio: float
    price_per_book_value: Optional[float]
    dividend_yield: float

    @property
    def multiplier(self) -> float:
        return self.pe_ratio * self.price_per_book_value


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

    def create_aggregation(self, year: int) -> StockAggregate:
        period = self.get_period(year, 3)
        earnings_per_share = self.average([metric.earnings_per_share for metric in period])
        pe_ratio = period[0].closing_price / earnings_per_share if earnings_per_share > 0 else None
        price_per_book_value = self.average([metric.price_per_book_value for metric in period if metric.price_per_book_value is not None])        
        period = self.get_period(year, 5)
        dividends_yield = self.average([metric.dividend_yield for metric in period])
        return StockAggregate(year, earnings_per_share, pe_ratio, price_per_book_value, dividends_yield)

    def average(self, values: List[float]) -> Optional[float]:
        if len(values) == 0:
            return None
        return sum(values) / len(values)
    
    def get_period(self, year: int, duration: int) -> List[StockMetrics]:
        period = [value for value in range(year, year-duration, -1)]
        return [metric for ye, metric in self.year_data.items() if ye in period]

    @property
    def growth(self) -> Optional[float]:
        end_year = max(self.aggregate_data.keys())
        begin_year = end_year - 10
        while begin_year not in self.aggregate_data:
            begin_year += 1
        if self._is_earning_per_share_valid(self.aggregate_data[end_year].earnings_per_share) and self._is_earning_per_share_valid(self.aggregate_data[begin_year].earnings_per_share):
            return (self.aggregate_data[end_year].earnings_per_share / self.aggregate_data[begin_year].earnings_per_share - 1)
        return None
    
    def _is_earning_per_share_valid(self, earning_per_share: Optional[float]) -> bool:
        return earning_per_share is not None and earning_per_share > 0

@dataclass
class Portfolio:
    stocks: Dict[str, Stock] = field(default_factory=dict)
