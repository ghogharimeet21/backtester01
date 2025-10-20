from commons.enums import Exchange, Underlying
from commons.utils import hms_to_seconds




class Sample_strategy:
    def __init__(self, strategy_json: dict):

        self.id = int(strategy_json["id"])
        self.exchange = Exchange((strategy_json["exchange"]).upper())
        self.underlying = Underlying((strategy_json["underlying"]).upper())
        self.start_date: int = int(strategy_json["start_date"])
        self.end_date: int = int(strategy_json["end_date"])
        self.entry_time: int = (
            hms_to_seconds(strategy_json["entry_time"])
            if isinstance(strategy_json["entry_time"], str)
            else strategy_json["entry_time"]
        )
        self.exit_time: int = (
            hms_to_seconds(strategy_json["exit_time"])
            if isinstance(strategy_json["exit_time"], str)
            else strategy_json["exit_time"]
        )