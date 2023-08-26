import datetime


def convert_datetime_utc_to_local(datetime_utc: datetime.datetime) -> datetime.datetime:
    # utc_datetime = datetime.datetime.fromisoformat(datetime_utc_str)

    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    local_time = datetime_utc.astimezone(local_timezone)

    local_time_final = datetime_utc + datetime.timedelta(seconds=local_timezone.utcoffset(local_time).seconds)

    return local_time_final
