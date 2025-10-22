import os
from typing import Dict, List
from commons.enums import OptionType
from commons.models import Contract
# from data_storage.enums import TimeFrames
from data_storage.models import Quote
from data_storage.storage import meta_data
import pandas as pd

from data_storage.utils import get_date_span

from commons.enums import Underlying




def load_data_from_dataset():

    cwd = os.getcwd()

    config_dict: Dict[str: List[int]] = {}

    data_store_config_file = os.path.join(cwd, "data_storage", "load.csv")

    load_df = pd.read_csv(data_store_config_file)

    for i in range(len(load_df)):
        conf_row = load_df.iloc[i]
        underlying = conf_row["underlying"]
        start_date = int(conf_row["start_date"])
        end_date = int(conf_row["end_date"])

        if underlying not in config_dict:
            config_dict[underlying] = []
        
        config_dict[underlying] = get_date_span(start_date, end_date, "%y%m%d")

        

    dataset_path = os.path.join(cwd, "feather_dataset")

    available_underlying = os.listdir(dataset_path)

    for underlying in available_underlying:
        if underlying.__contains__("."):
            continue

        if underlying not in config_dict:
            continue

        load_dates = config_dict[underlying]
        
        underlying_path = os.path.join(dataset_path, underlying)

        available_contract_type = os.listdir(underlying_path)
        
        if underlying not in meta_data.available_dates:
            meta_data.available_dates[underlying] = set()

        for underlying_type in ["nifty_eq", "nifty_pe", "nifty_ce", "nifty_fut"]:

            print(f"loading {underlying_type}")

            if underlying_type == "nifty_fut":
                # temp condition
                continue


            stock_type = (
                OptionType.EQ if underlying_type == f"{underlying}_eq" else
                OptionType.CE if underlying_type == f"{underlying}_ce" else
                OptionType.PE if underlying_type == f"{underlying}_pe" else
                OptionType.FUT if underlying_type == f"{underlying}_fut" else
                None
            )

            if not stock_type:
                print("skipping new Contract type in none")
                continue

            all_files_path = os.path.join(underlying_path, underlying_type)

            all_files = os.listdir(all_files_path)

            for file_name in all_files:
                file_date = int(file_name.replace(".feather", "").split("_")[-1])
                
                if file_date not in load_dates:
                    continue

                file_path = os.path.join(all_files_path, file_name)

                df = pd.read_feather(file_path)

                df.fillna(0, inplace=True)

                if file_date not in meta_data.quote_data:
                    meta_data.quote_data[file_date] = {}

                for i in range(len(df)):
                    row = df.iloc[i]
                    date = int(row["date"])
                    time = int(row["time"])
                    try:
                        symbol = str(row["tradingsymbol"])
                    except KeyError:
                        symbol = str(row["symbol"])

                    strike = int(row["strike"]) if "strike" in df.columns else None
                    expiry = int(row["expiry"]) if "expiry" in df.columns else None
                    
                    open = float(row["open"])
                    high = float(row["high"])
                    low = float(row["low"])
                    close = float(row["close"])

                    volume = int(row["volume"]) if "volume" in df.columns else 0
                    oi = int(row["oi"]) if "oi" in df.columns else 0
                    coi = float(row["coi"]) if "coi" in df.columns else 0
                    

                    meta_data.available_dates[underlying].add(date)

                    contract = Contract(
                        symbol,
                        stock_type,
                        expiry,
                        strike
                    )

                    quote = Quote(
                        contract,
                        symbol,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        oi,
                        coi,
                    )

                    if stock_type not in meta_data.quote_data[file_date]:
                        meta_data.quote_data[file_date][stock_type] = {}
                    if underlying not in meta_data.quote_data[file_date][stock_type]:
                        meta_data.quote_data[file_date][stock_type][underlying] = {}
                    if symbol not in meta_data.quote_data[file_date][stock_type][underlying]:
                        meta_data.quote_data[file_date][stock_type][underlying][symbol] = {}
                    if 1 not in meta_data.quote_data[file_date][stock_type][underlying][symbol]:
                        meta_data.quote_data[file_date][stock_type][underlying][symbol][1] = {}
                    if time not in meta_data.quote_data[file_date][stock_type][underlying][symbol][1]:
                        meta_data.quote_data[file_date][stock_type][underlying][symbol][1][time] = quote
                    

                    if (expiry is not None) and (strike is None):
                        # Futute contract
                        ...
                    

                    if (strike is not None) and (expiry is not None):
                        # Options contracts


                        ...
                
                    
                    

                    





