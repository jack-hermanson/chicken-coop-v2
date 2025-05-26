from datetime import datetime

import pytz


def utc_to_local(utc_dt: datetime) -> datetime:
    """
    Convert a UTC datetime to a local datetime.
    :param utc_dt: The UTC datetime to convert.
    :return: A local datetime.
    """
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)

    local_tz = pytz.timezone("America/Denver")
    return utc_dt.astimezone(tz=local_tz)
