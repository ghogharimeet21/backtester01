import logging
import os
from datetime import datetime, timedelta

from data_storage.storage import MetaData




logger = logging.getLogger(__name__)

















def get_date_span(
        start_date,
        end_date,
        format,
):
    
    start = datetime.strptime(str(start_date), format)
    end = datetime.strptime(str(end_date), format)

    date_span = []

    while start <= end:
        date = int(start.strftime(format))

        date_span.append(date)


        start += timedelta(days=1)
    
    return date_span



def adjust_exppiries(meta_data: MetaData):
    ...

