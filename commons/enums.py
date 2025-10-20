import enum


class Underlying(enum.Enum):
    NIFTY = "NIFTY_50"
    BANKNIFTY = "BANKNIFTY"


class Exchange(enum.Enum):
    NSE = "NSE"
    BSE = "BSE"
    MCX = "MCX"


class OrderType(enum.Enum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"


class StategyOrderStatus(enum.Enum):
    NO_ORDERS_RUNNING = "NO_ORDERS_RUNNING"
    RUNNING_ORDER = "RUNNING_ORDER"



class PositionType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"



class OptionType(enum.Enum):
    EQ = "EQ"
    CE = "CE"
    PE = "PE"
    FUT = "FUT"



class ExpiryType(enum.Enum):
    WEEKLY = "WEEKLY"
    NEXT_WEEKLY = "NEXT_WEEKLY"
    MONTHLY = "MONTHLY"
    ALL = "ALL"