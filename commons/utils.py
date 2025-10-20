from datetime import datetime











def is_weekend(date_str) -> bool:
    date_obj = datetime.strptime(str(date_str), "%y%m%d").date()
    if (date_obj.weekday() == 5) or (date_obj.weekday() == 6):
        return True
    return False

    
def hms_to_seconds(time_str: str) -> int:
    hours, minutes, seconds = map(int, time_str.split(':'))
    if hours > 24:
        raise ValueError(f"in {time_str} hour={hours} is not valid please enter less then 24")
    if minutes > 59:
        raise ValueError(f"in {time_str} minute={minutes} is not valid please enter less then 60")
    if seconds > 59:
        raise ValueError(f"in {time_str} seconds={seconds} is not valid please enter less then 60")
    return (hours * 3600) + minutes * 60 + seconds


def seconds_to_hms(seconds: int) -> str:
    if seconds > 86399:
        raise ValueError(f"{seconds} is not valid please enter less then 86399")
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"




