from __future__ import annotations
from datetime import datetime, timedelta


class Time:
    def __init__(self):
        self.default_datetime_string_format = "%Y-%m-%d %H:%M:%S"
        self.datetime = datetime
        self.timedelta = timedelta

    def get_current_timestamp_in_10_digits_format(self) -> int:
        return int(datetime.now().timestamp())

    def convert_timestamp_to_string(self, timestamp: int, format: str="%Y-%m-%d %H:%M:%S") -> str:
        return datetime.fromtimestamp(timestamp).strftime(format)
    
    def convert_string_to_timestamp(self, time_string: str, format: str="%Y-%m-%d %H:%M:%S") -> int:
        return int(datetime.strptime(time_string, format).timestamp())
    
    def get_timestamp_from_datetime_object(self, datetime_object: datetime) -> int:
        return int(datetime_object.timestamp())
    
    def get_datetime_object_from_timestamp(self, timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp)
    
    def convert_datetime_object_to_string(self, datetime_object: datetime, format: str="%Y-%m-%d %H:%M:%S") -> str:
        return datetime_object.strftime(format)