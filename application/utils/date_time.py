from datetime import datetime

import pytz


def utc_to_local(utc_dt: datetime) -> datetime:
    """
    Convert a UTC datetime to a local datetime.
    :param utc_dt: The UTC datetime to convert.
    :return: A local datetime.
    """
    local_tz = pytz.timezone("America/Denver")
    return utc_dt.astimezone(local_tz)
