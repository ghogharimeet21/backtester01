from commons.enums import OptionType


class Candle:
    def __init__(
            self, 
            open = None, 
            high = None, 
            low = None, 
            close = None,
            volume = None,
            oi = None,
            coi = None,
    ):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.oi = oi
        self.coi = coi
    
    def __str__(self):
        return(
            f"open={self.open}, high={self.high}, low={self.low}, close={self.close}\
            volume={self.volume}, oi={self.oi}, coi={self.coi}"
        )
    
    def avg_ohlc(self):
        return (self.open + self.high + self.low + self.close) / 4






class Contract:
    def __init__(self, trading_symbol: str = None, option_type: OptionType = None, expiry: int = None, strike: float = None):
        self.trading_symbol = trading_symbol
        self.option_type = option_type
        self.expiry = expiry
        self.strike = strike







