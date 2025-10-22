from typing import Dict, Set, Optional, List
from dataclasses import dataclass
from commons.enums import OptionType, Underlying, ExpiryType
from data_storage.models import Quote
from datetime import datetime

"""
OPTIMIZED METADATA STRUCTURE FOR EQUITY, FUTURES & OPTIONS BACKTESTING

Key Design Principles:
1. Fast lookups for intraday time-series data
2. Separate structures for EQ vs Derivatives (cleaner access patterns)
3. Minimal nesting (max 3-4 levels)
4. Support multiple timeframes efficiently
5. Easy to query by strike/expiry for options chains
"""

# ============================================================================
# APPROACH 1: SEPARATED BY INSTRUMENT TYPE (RECOMMENDED)
# ============================================================================

@dataclass
class TimeSeriesKey:
    """Composite key for fast lookups"""
    symbol: str
    timeframe: int  # 1, 5, 15 minutes etc
    
    def __hash__(self):
        return hash((self.symbol, self.timeframe))

class MetaDataV1:
    """
    PROS: 
    - Clear separation between instrument types
    - Fast equity lookups (no option_type filtering needed)
    - Options chain queries are intuitive
    - Less memory overhead (no redundant keys)
    - WEEKLY and MONTHLY expiries separated for easy access
    
    CONS:
    - Need to know instrument type before querying
    """
    
    def __init__(self):
        # Track available trading dates per underlying
        self.available_dates: Dict[str, Set[int]] = {}
        
        # ==================== EQUITY DATA ====================
        # Structure: symbol -> timeframe -> date -> time -> Quote
        # Example: "NIFTY" -> 1 -> 180101 -> 34200 -> Quote
        self.equity_data: Dict[str, Dict[int, Dict[int, Dict[int, Quote]]]] = {}
        
        # ==================== FUTURES DATA ====================
        # Structure: symbol -> expiry -> timeframe -> date -> time -> Quote
        # Example: "NIFTY" -> 180125 -> 1 -> 180101 -> 34200 -> Quote
        self.futures_data: Dict[str, Dict[int, Dict[int, Dict[int, Dict[int, Quote]]]]] = {}
        
        # ==================== OPTIONS DATA (SEPARATED BY EXPIRY TYPE) ====================
        # Structure: underlying -> expiry_type -> expiry -> strike -> option_type -> timeframe -> date -> time -> Quote
        # Example: "NIFTY" -> WEEKLY -> 180125 -> 10500.0 -> CE -> 1 -> 180101 -> 34200 -> Quote
        self.options_data: Dict[str, Dict[ExpiryType, Dict[int, Dict[float, Dict[OptionType, Dict[int, Dict[int, Dict[int, Quote]]]]]]]] = {}
        
        # ==================== OPTIONS CHAIN METADATA ====================
        # Fast lookup: what strikes are available for a given expiry?
        # Structure: underlying -> date -> expiry_type -> expiry -> Set[strikes]
        self.available_strikes: Dict[str, Dict[int, Dict[ExpiryType, Dict[int, Set[float]]]]] = {}
        
        # Fast lookup: what expiries are available on a given date?
        # Structure: underlying -> date -> expiry_type -> List[expiries] (sorted)
        self.available_expiries: Dict[str, Dict[int, Dict[ExpiryType, List[int]]]] = {}
        
        # ==================== EXPIRY TYPE MAPPING ====================
        # Map each expiry date to its type (WEEKLY/MONTHLY)
        # Structure: underlying -> ExpiryType -> expiry_date
        self.expiry_type_map: Dict[str, Dict[ExpiryType, int]] = {}
        
        # ==================== INDICATOR CACHE ====================
        # Store calculated indicators separately to avoid mixing with raw data
        # Structure: indicator_name -> symbol -> timeframe -> date -> time -> value
        self.indicators: Dict[str, Dict[str, Dict[int, Dict[int, Dict[int, float]]]]] = {}


# ============================================================================
# APPROACH 2: UNIFIED WITH OPTIONAL FIELDS (ALTERNATIVE)
# ============================================================================

class MetaDataV2:
    """
    PROS:
    - Single query path for all instruments
    - Flexible for mixed strategies
    - Easier to add new instrument types
    
    CONS:
    - More memory usage (many None values)
    - Slower filtering (need to check option_type)
    - Complex nested structure
    """
    
    def __init__(self):
        self.available_dates: Dict[str, Set[int]] = {}
        
        # ==================== UNIFIED DATA STRUCTURE ====================
        # Structure: date -> timeframe -> underlying -> option_type -> identifier -> time -> Quote
        # identifier = symbol for EQ, expiry for FUT, "strike_optiontype" for options
        self.quote_data: Dict[int, Dict[int, Dict[str, Dict[OptionType, Dict[str, Dict[int, Quote]]]]]] = {}
        
        # Helper indices for fast queries
        self.option_chain_index: Dict[str, Dict[int, Dict[int, Set[float]]]] = {}  # underlying -> date -> expiry -> strikes
        self.indicators: Dict[str, Dict[str, Dict[int, Dict[int, Dict[int, float]]]]] = {}


# ============================================================================
# APPROACH 3: HYBRID WITH TIME-SERIES OPTIMIZATION (BEST FOR LARGE DATA)
# ============================================================================

class MetaDataV3:
    """
    PROS:
    - Optimized for time-series access (most common in backtesting)
    - Pre-sorted data for fast iteration
    - Separate hot vs cold data paths
    
    BEST FOR: Large datasets, high-frequency strategies
    """
    
    def __init__(self):
        self.available_dates: Dict[str, Set[int]] = {}
        
        # ==================== TIME-FIRST STRUCTURE ====================
        # Primary access pattern: iterate through time -> query instruments
        # Structure: date -> time -> timeframe -> instrument_key -> Quote
        self.time_series: Dict[int, Dict[int, Dict[int, Dict[str, Quote]]]] = {}
        
        # ==================== INSTRUMENT LOOKUP TABLES ====================
        # For specific instrument queries (less frequent)
        self.equity_lookup: Dict[str, Dict[int, Dict[int, List[int]]]] = {}  # symbol -> timeframe -> date -> [times]
        self.futures_lookup: Dict[str, Dict[int, Dict[int, Dict[int, List[int]]]]] = {}  # symbol -> expiry -> timeframe -> date -> [times]
        self.options_lookup: Dict[str, Dict[int, Dict[float, Dict[OptionType, Dict[int, Dict[int, List[int]]]]]]] = {}
        
        # ==================== OPTIONS CHAIN ====================
        self.option_chains: Dict[str, Dict[int, Dict[int, Dict[float, Dict[OptionType, Quote]]]]] = {}  # underlying -> date -> expiry -> strike -> type -> Quote
        
        self.indicators: Dict[str, Dict[str, Dict[int, Dict[int, Dict[int, float]]]]] = {}


# ============================================================================
# EXPIRY TYPE DETECTION UTILITIES
# ============================================================================

def detect_expiry_type(expiry_date: int, underlying: str = "NIFTY") -> ExpiryType:
    """
    Detect if an expiry is WEEKLY or MONTHLY based on date
    
    Logic for NIFTY/BANKNIFTY:
    - MONTHLY: Last Thursday of the month
    - WEEKLY: Any other Thursday
    
    Args:
        expiry_date: Date in YYMMDD format (e.g., 180125 for Jan 25, 2018)
        underlying: "NIFTY" or "BANKNIFTY"
    
    Returns:
        ExpiryType.WEEKLY or ExpiryType.MONTHLY
    """
    from calendar import monthrange
    
    # Parse date
    date_str = str(expiry_date)
    year = int("20" + date_str[:2])
    month = int(date_str[2:4])
    day = int(date_str[4:6])
    
    date_obj = datetime(year, month, day)
    
    # Get last day of the month
    last_day = monthrange(year, month)[1]
    
    # Find last Thursday of the month
    last_thursday = None
    for d in range(last_day, 0, -1):
        check_date = datetime(year, month, d)
        if check_date.weekday() == 3:  # Thursday = 3
            last_thursday = d
            break
    
    # If expiry is on last Thursday, it's MONTHLY
    if day == last_thursday:
        return ExpiryType.MONTHLY
    else:
        return ExpiryType.WEEKLY


def get_weekly_expiry(date: int, underlying: str = "NIFTY") -> Optional[int]:
    """
    Get the current week's expiry for a given date
    
    Args:
        date: Current date in YYMMDD format
        underlying: "NIFTY" or "BANKNIFTY"
    
    Returns:
        Expiry date in YYMMDD format or None
    """
    from datetime import timedelta
    
    date_str = str(date)
    year = int("20" + date_str[:2])
    month = int(date_str[2:4])
    day = int(date_str[4:6])
    
    current_date = datetime(year, month, day)
    
    # Find next Thursday (NIFTY/BANKNIFTY weekly expiry)
    days_ahead = 3 - current_date.weekday()  # Thursday = 3
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    
    expiry_date = current_date + timedelta(days=days_ahead)
    
    return int(expiry_date.strftime("%y%m%d"))


def get_monthly_expiry(date: int, underlying: str = "NIFTY") -> Optional[int]:
    """
    Get the current month's expiry (last Thursday) for a given date
    
    Args:
        date: Current date in YYMMDD format
        underlying: "NIFTY" or "BANKNIFTY"
    
    Returns:
        Monthly expiry date in YYMMDD format or None
    """
    from calendar import monthrange
    
    date_str = str(date)
    year = int("20" + date_str[:2])
    month = int(date_str[2:4])
    
    # Get last day of the month
    last_day = monthrange(year, month)[1]
    
    # Find last Thursday of the month
    for d in range(last_day, 0, -1):
        check_date = datetime(year, month, d)
        if check_date.weekday() == 3:  # Thursday = 3
            return int(check_date.strftime("%y%m%d"))
    
    return None


def populate_expiry_type_map(meta: MetaDataV1, underlying: str = "NIFTY"):
    """
    Scan all loaded expiries and classify them as WEEKLY or MONTHLY
    
    Call this after loading all data but before backtesting
    """
    if underlying not in meta.expiry_type_map:
        meta.expiry_type_map[underlying] = {}
    
    # Collect all unique expiries from options_data
    all_expiries = set()
    
    if underlying in meta.options_data:
        for expiry_type in meta.options_data[underlying].values():
            for expiry in expiry_type.keys():
                all_expiries.add(expiry)
    
    # Classify each expiry
    for expiry in all_expiries:
        expiry_type = detect_expiry_type(expiry, underlying)
        meta.expiry_type_map[underlying][expiry] = expiry_type


# ============================================================================
# USAGE EXAMPLES WITH EXPIRY SEPARATION
# ============================================================================

def example_usage_v1():
    """How to use MetaDataV1 with WEEKLY/MONTHLY expiry separation"""
    meta = MetaDataV1()
    
    # === LOADING DATA WITH EXPIRY TYPE ===
    underlying = "NIFTY"
    expiry = 180125  # Jan 25, 2018
    strike = 10500.0
    opt_type = OptionType.CE
    date = 180101
    time = 34200
    
    # Detect expiry type
    expiry_type = detect_expiry_type(expiry, underlying)
    print(f"Expiry {expiry} is {expiry_type}")  # Will print WEEKLY or MONTHLY
    
    # Initialize nested structure
    if underlying not in meta.options_data:
        meta.options_data[underlying] = {}
    if expiry_type not in meta.options_data[underlying]:
        meta.options_data[underlying][expiry_type] = {}
    if expiry not in meta.options_data[underlying][expiry_type]:
        meta.options_data[underlying][expiry_type][expiry] = {}
    if strike not in meta.options_data[underlying][expiry_type][expiry]:
        meta.options_data[underlying][expiry_type][expiry][strike] = {}
    if opt_type not in meta.options_data[underlying][expiry_type][expiry][strike]:
        meta.options_data[underlying][expiry_type][expiry][strike][opt_type] = {}
    if 1 not in meta.options_data[underlying][expiry_type][expiry][strike][opt_type]:
        meta.options_data[underlying][expiry_type][expiry][strike][opt_type][1] = {}
    if date not in meta.options_data[underlying][expiry_type][expiry][strike][opt_type][1]:
        meta.options_data[underlying][expiry_type][expiry][strike][opt_type][1][date] = {}
    
    meta.options_data[underlying][expiry_type][expiry][strike][opt_type][1][date][time] = Quote(...)
    
    # Update metadata
    if underlying not in meta.available_strikes:
        meta.available_strikes[underlying] = {}
    if date not in meta.available_strikes[underlying]:
        meta.available_strikes[underlying][date] = {}
    if expiry_type not in meta.available_strikes[underlying][date]:
        meta.available_strikes[underlying][date][expiry_type] = {}
    if expiry not in meta.available_strikes[underlying][date][expiry_type]:
        meta.available_strikes[underlying][date][expiry_type][expiry] = set()
    
    meta.available_strikes[underlying][date][expiry_type][expiry].add(strike)
    
    # === QUERYING DATA ===
    
    # Get WEEKLY option quote
    quote = meta.options_data["NIFTY"][ExpiryType.WEEKLY][expiry][strike][OptionType.CE][1][date][time]
    
    # Get MONTHLY option quote
    monthly_expiry = get_monthly_expiry(date)
    quote = meta.options_data["NIFTY"][ExpiryType.MONTHLY][monthly_expiry][strike][OptionType.CE][1][date][time]
    
    # Get all WEEKLY expiries on a date
    weekly_expiries = meta.available_expiries["NIFTY"][date][ExpiryType.WEEKLY]
    
    # Get all MONTHLY expiries on a date
    monthly_expiries = meta.available_expiries["NIFTY"][date][ExpiryType.MONTHLY]
    
    # Get all strikes for WEEKLY expiry
    weekly_strikes = meta.available_strikes["NIFTY"][date][ExpiryType.WEEKLY][expiry]
    
    # === STRATEGY EXAMPLE: Trade only WEEKLY expiries ===
    if ExpiryType.WEEKLY in meta.options_data["NIFTY"]:
        for expiry in meta.options_data["NIFTY"][ExpiryType.WEEKLY]:
            for strike in meta.options_data["NIFTY"][ExpiryType.WEEKLY][expiry]:
                ce_quote = meta.options_data["NIFTY"][ExpiryType.WEEKLY][expiry][strike][OptionType.CE][1][date][time]
                # Your strategy logic
    
    # === STRATEGY EXAMPLE: Trade only MONTHLY expiries ===
    if ExpiryType.MONTHLY in meta.options_data["NIFTY"]:
        for expiry in meta.options_data["NIFTY"][ExpiryType.MONTHLY]:
            for strike in meta.options_data["NIFTY"][ExpiryType.MONTHLY][expiry]:
                ce_quote = meta.options_data["NIFTY"][ExpiryType.MONTHLY][expiry][strike][OptionType.CE][1][date][time]
                # Your strategy logic


def example_usage_v3():
    """How to use MetaDataV3 (BEST for time-series iteration)"""
    meta = MetaDataV3()
    
    # === BACKTESTING LOOP (Most efficient) ===
    date = 180101
    for time in sorted(meta.time_series[date].keys()):
        timeframe = 1
        
        # Get all instruments at this timestamp
        all_quotes = meta.time_series[date][time][timeframe]
        
        # Access specific instruments
        nifty_spot = all_quotes.get("NIFTY_EQ")
        nifty_fut = all_quotes.get("NIFTY_FUT_180125")
        nifty_ce = all_quotes.get("NIFTY_OPT_180125_10500_CE")
        
        # Your strategy logic here
        # ...


# ============================================================================
# RECOMMENDATION
# ============================================================================

"""
FOR YOUR PROJECT, I RECOMMEND: **MetaDataV1** (Separated by instrument type)

WHY?
1. ✅ Clear separation matches your domain (EQ, FUT, CE, PE are fundamentally different)
2. ✅ Easier to implement strategy-specific logic (most strategies focus on one type)
3. ✅ Better performance for option chain queries (common in options strategies)
4. ✅ Less memory waste (no None values for unused fields)
5. ✅ Simpler to understand and maintain

MIGRATION PATH from your current structure:
- Your current: date -> option_type -> symbol -> timeframe -> time -> Quote
- New V1: Flip to symbol/underlying first for better access patterns
- Add separate equity_data, futures_data, options_data dictionaries

WHEN TO USE V3 (Time-first):
- If you're doing high-frequency strategies
- If you need to process multiple instruments simultaneously at each timestamp
- If dataset is very large (>10GB in memory)
"""

# ============================================================================
# HELPER FUNCTIONS FOR V1
# ============================================================================

class DataAccessor:
    """Helper class to simplify MetaDataV1 access"""
    
    def __init__(self, meta: MetaDataV1):
        self.meta = meta
    
    def get_equity_quote(self, symbol: str, date: int, time: int, timeframe: int = 1) -> Optional[Quote]:
        """Safe equity quote getter with None handling"""
        try:
            return self.meta.equity_data[symbol][timeframe][date][time]
        except KeyError:
            return None
    
    def get_option_quote(self, underlying: str, expiry: int, strike: float, 
                        option_type: OptionType, date: int, time: int, 
                        timeframe: int = 1, expiry_type: ExpiryType = None) -> Optional[Quote]:
        """
        Safe option quote getter
        
        Args:
            expiry_type: If None, will auto-detect from expiry_type_map
        """
        # Auto-detect expiry type if not provided
        if expiry_type is None:
            if underlying in self.meta.expiry_type_map and expiry in self.meta.expiry_type_map[underlying]:
                expiry_type = self.meta.expiry_type_map[underlying][expiry]
            else:
                # Fallback to detection
                expiry_type = detect_expiry_type(expiry, underlying)
        
        try:
            return self.meta.options_data[underlying][expiry_type][expiry][strike][option_type][timeframe][date][time]
        except KeyError:
            return None
    
    def get_option_chain(self, underlying: str, expiry: int, date: int, time: int, 
                        timeframe: int = 1, expiry_type: ExpiryType = None) -> Dict[float, Dict[OptionType, Quote]]:
        """
        Get entire option chain for a given expiry at specific time
        
        Args:
            expiry_type: WEEKLY or MONTHLY. If None, will auto-detect
        """
        chain = {}
        
        # Auto-detect expiry type if not provided
        if expiry_type is None:
            if underlying in self.meta.expiry_type_map and expiry in self.meta.expiry_type_map[underlying]:
                expiry_type = self.meta.expiry_type_map[underlying][expiry]
            else:
                expiry_type = detect_expiry_type(expiry, underlying)
        
        if underlying not in self.meta.options_data:
            return chain
        
        if expiry_type not in self.meta.options_data[underlying]:
            return chain
        
        if expiry not in self.meta.options_data[underlying][expiry_type]:
            return chain
        
        for strike in self.meta.options_data[underlying][expiry_type][expiry]:
            chain[strike] = {}
            for opt_type in [OptionType.CE, OptionType.PE]:
                try:
                    quote = self.meta.options_data[underlying][expiry_type][expiry][strike][opt_type][timeframe][date][time]
                    chain[strike][opt_type] = quote
                except KeyError:
                    continue
        
        return chain
    
    def get_atm_strike(self, underlying: str, spot_price: float, date: int, 
                    expiry: int, expiry_type: ExpiryType = None) -> Optional[float]:
        """
        Find closest ATM strike
        
        Args:
            expiry_type: If None, will auto-detect
        """
        # Auto-detect expiry type if not provided
        if expiry_type is None:
            if underlying in self.meta.expiry_type_map and expiry in self.meta.expiry_type_map[underlying]:
                expiry_type = self.meta.expiry_type_map[underlying][expiry]
            else:
                expiry_type = detect_expiry_type(expiry, underlying)
        
        if (underlying not in self.meta.available_strikes or 
            date not in self.meta.available_strikes[underlying] or
            expiry_type not in self.meta.available_strikes[underlying][date] or
            expiry not in self.meta.available_strikes[underlying][date][expiry_type]):
            return None
        
        strikes = list(self.meta.available_strikes[underlying][date][expiry_type][expiry])
        if not strikes:
            return None
        
        return min(strikes, key=lambda x: abs(x - spot_price))
    
    def get_all_weekly_expiries(self, underlying: str, date: int) -> List[int]:
        """Get all WEEKLY expiries available on a date"""
        if (underlying not in self.meta.available_expiries or
            date not in self.meta.available_expiries[underlying] or
            ExpiryType.WEEKLY not in self.meta.available_expiries[underlying][date]):
            return []
        return self.meta.available_expiries[underlying][date][ExpiryType.WEEKLY]
    
    def get_all_monthly_expiries(self, underlying: str, date: int) -> List[int]:
        """Get all MONTHLY expiries available on a date"""
        if (underlying not in self.meta.available_expiries or
            date not in self.meta.available_expiries[underlying] or
            ExpiryType.MONTHLY not in self.meta.available_expiries[underlying][date]):
            return []
        return self.meta.available_expiries[underlying][date][ExpiryType.MONTHLY]
    
    def get_current_weekly_expiry(self, underlying: str, date: int) -> Optional[int]:
        """Get the current week's expiry for a given date"""
        return get_weekly_expiry(date, underlying)
    
    def get_current_monthly_expiry(self, underlying: str, date: int) -> Optional[int]:
        """Get the current month's expiry for a given date"""
        return get_monthly_expiry(date, underlying)