from commons.enums import OptionType








class Contract:
    def __init__(
            self,
            symbol: str = None,
            option_type: OptionType = None,
            expiry: int = None,
            strike: float = None
    ):
        self.symbol = symbol
        self.option_type = option_type
        self.expiry = expiry
        self.strike = strike




class Quote:
    def __init__(
        self,
        contract: Contract = None,
        symbol: str = None,
        open: float = None,
        high: float = None,
        low: float = None,
        close: float = None,
        volume: float = None,
        oi: float = None,
        coi: float = None
    ):
        self.contract = contract
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.oi = oi
        self.coi = coi