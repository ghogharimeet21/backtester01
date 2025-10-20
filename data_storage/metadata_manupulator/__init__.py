from typing import Dict, List
from datetime import datetime, timedelta
from data_storage.enums import TimeFrames
from data_storage.models import Quote
from data_storage.storage import meta_data
import logging



logger = logging.getLogger(__name__)






def resample_data(
        strategy_underlying: str,
        strategy_time_frame: TimeFrames,
        strategy_start_date: int,
        startegy_end_date: int,
        market_start_time: int,
        market_end_time: int,
):
    start_date = datetime.strptime(str(strategy_start_date), "%y%m%d")
    end_date = datetime.strptime(str(startegy_end_date), "%y%m%d")

    last_available_date = min([datetime.strptime(str(date), "%y%m%d") for date in meta_data.available_dates[strategy_underlying]])

    your_date = int(start_date.strftime("%y%m%d"))

    start_date -= timedelta(days=2)

    if (
        int(start_date.strftime("%y%m%d"))
        not in
        meta_data.available_dates[strategy_underlying]
    ):
        while int(start_date.strftime("%y%m%d")) not in meta_data.available_dates[strategy_underlying]:
            if start_date < last_available_date:
                start_date += timedelta(days=1)
            elif start_date > last_available_date:
                start_date -= timedelta(days=1)
            elif start_date == last_available_date:
                break
        logger.info(f"start_date adjusted {your_date} to {start_date.strftime("%y%m%d")} to add indicators properly")
    
    if (
        int(end_date.strftime("%y%m%d"))
        not in 
        meta_data.available_dates[strategy_underlying]
    ):
        while int(end_date.strftime("%y%m%d")) not in meta_data.available_dates[strategy_underlying]:
            if end_date < last_available_date:
                end_date += timedelta(days=1)
            elif end_date > last_available_date:
                end_date -= timedelta(days=1)
            elif end_date == last_available_date:
                break
        logger.info(f"end_date adjusted {your_date} to {end_date.strftime("%y%m%d")} to add indicators properly")
    


    while start_date <= end_date:
        resampled: Dict[int, Quote] = {}
        current_date = int(start_date.strftime("%y%m%d"))

        if current_date not in meta_data.available_dates[strategy_underlying]:
            start_date += timedelta(days=1)
            continue

        if (
            strategy_time_frame not in meta_data.quote_data
        )










        start_date += timedelta(days=1)







def add_indicator():



    ...