from typing import Dict, List, Tuple, Set

from commons.enums import ExpiryType, OptionType, Underlying
from commons.models import Candle, Contract
from data_storage.enums import TimeFrames
from data_storage.metadata_manupulator.Indicator_engine.models import (
    Sma
)
from data_storage.models import Quote


# class FramesData:
#     def __init__(self):
#         self.quote_data: Dict[int, Dict[int, Dict[OptionType, Dict[str, Dict[TimeFrames, Quote]]]]] = {}


class Indicators:
    def __init__(self):
        # time_frame -> date -> time -> option_type -> underlying -> symbol -> sma_value
        self.sma: Dict[int, Dict[int, Dict[int, Dict[OptionType, Dict[str, Dict[str, Sma]]]]]]


class MetaData:
    def __init__(self):
        self.available_dates: Dict[str, Dict[OptionType, Set[int]]] = {}

        # self.available_strikes: Dict[Underlying, Dict[int, Dict[OptionType, Dict[int,Set[int]]]]] = {}

        # date -> time -> Underlying -> OptionType -> expiry -> strike : Contract
        self.contracts: Dict[int, Dict[int, Dict[Underlying, Dict[OptionType, Dict[int, Dict[float, Contract]]]]]] = {}
        # self.expiries: Dict[int, Dict[ExpiryType, int]] = {}

        ## date -> option_type -> underlyig -> symbol -> timeframe -> time -> quote
        self.quote_data: Dict[int, Dict[OptionType, Dict[str, Dict[str, Dict[int, Dict[int, Quote]]]]]] = {}

        ## time_frame -> date -> time -> option_type -> underlying -> symbol -> quote
        self.quote_data: Dict[int, Dict[int, Dict[int, Dict[OptionType, Dict[str, Dict[str, Quote]]]]]]

        self.indicators: Indicators = Indicators()


meta_data: MetaData = MetaData()