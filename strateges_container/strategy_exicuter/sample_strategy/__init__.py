from strateges_container.strategy_exicuter.sample_strategy.models import Sample_strategy

from data_storage.storage import meta_data












def start_exicution(requast_model: Sample_strategy):

    for date in meta_data.quote_data:
        for option_type in meta_data.quote_data[date]:
            for underlying in meta_data.quote_data[date][option_type]:
                for symbol in meta_data.quote_data[date][option_type][underlying]:
                    for time_frame in meta_data.quote_data[date][option_type][underlying][symbol]:
                        for time, quote in meta_data.quote_data[date][option_type][underlying][symbol][time_frame].items():
                            print(
                                f"date={date}, option_type={option_type}, underlying={underlying}\
                                    symbol={symbol}, time_frame={time_frame}\
                                        time={time}, quote={quote}"
                            )
    ...