from typing import Dict, List, Tuple, Set

from commons.enums import ExpiryType, OptionType, Underlying
from commons.models import Candle, Contract
from data_storage.enums import TimeFrames
from data_storage.models import Quote


# class FramesData:
#     def __init__(self):
#         self.quote_data: Dict[int, Dict[int, Dict[OptionType, Dict[str, Dict[TimeFrames, Quote]]]]] = {}


class Indicators:
    def __init__(self):
        # dict[time_frame, dict[option_type, dict[symbol, dict[date, dict[time, sma_value]]]]]
        self.sma: Dict[str, Dict[OptionType, Dict[str, dict[int, Dict[int, float]]]]] = {}


class MetaData:
    def __init__(self):
        self.available_dates: Dict[str, Set[int]] = {}

        # self.available_strikes: Dict[Underlying, Dict[int, Dict[OptionType, Dict[int,Set[int]]]]] = {}

        self.Contracts: Dict[int, Dict[int, Dict[Underlying, Dict[OptionType, Dict[int, Dict[float, Contract]]]]]] = {}
        # self.expiries: Dict[int, Dict[ExpiryType, int]] = {}

        ## date -> option_type -> underlyig -> timeframe -> time -> quote
        self.quote_data: Dict[int, Dict[OptionType, Dict[str, Dict[int, Dict[int, Quote]]]]]

        self.indicators: Indicators = Indicators()


meta_data = MetaData()