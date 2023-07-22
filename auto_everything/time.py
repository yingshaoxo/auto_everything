from typing import Any

from datetime import datetime, timedelta
from time import sleep
from multiprocessing import Process


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
    
    def run_a_function_at_a_certain_time(self, the_function: Any, the_time: str, format: str="%Y-%m-%d %H:%M:%S", wait=True) -> Process | None:
        def run_a_function_when_time_arrive():
            target_time = self.convert_datetime_object_to_string(
                    self.get_datetime_object_from_timestamp(
                        self.convert_string_to_timestamp(time_string=the_time, format=format)
                    ), format=format
                )
            while True:
                current_time = self.convert_datetime_object_to_string(self.datetime.now(), format=format)
                print(current_time, target_time)
                if (current_time == target_time):
                    a_process = Process(target=the_function)
                    a_process.start()
                    a_process.join()
                    return None
                sleep(0.1)

        if wait == True:
            run_a_function_when_time_arrive()
            return None
        else:
            new_process = Process(target=run_a_function_when_time_arrive)
            new_process.start()
            return new_process

    def run_a_function_after_x_seconds(self, the_function: Any, seconds: int | float, wait=True) -> Process | None:
        def run_a_function():
            sleep(seconds)
            a_process = Process(target=the_function)
            a_process.start()
            a_process.join()

        if wait == True:
            run_a_function()
            return None
        else:
            new_process = Process(target=run_a_function)
            new_process.start()
            return new_process
    
    def run_a_function_every_x_seconds(self, the_function: Any, seconds: int | float, wait=True) -> Process | None:
        def run_it():
            while True:
                the_function()
                sleep(seconds)

        if wait == True:
            run_it()
            return None
        else:
            new_process = Process(target=run_it)
            new_process.start()
            return new_process