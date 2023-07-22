from auto_everything.time import Time
time_ = Time()


def test_time():
    now = time_.get_current_timestamp_in_10_digits_format()
    print(now)

    now_string = time_.convert_timestamp_to_string(now)
    print(now_string)

    now2 = time_.convert_string_to_timestamp(now_string)
    print(now2)

    assert now == now2
    
    now_datetime = time_.get_datetime_object_from_timestamp(now2)
    yesterday_datetime = (now_datetime - time_.timedelta(days=1))
    yesterday_string = time_.convert_datetime_object_to_string(yesterday_datetime)
    print(yesterday_string)


def test_run_function():
    def ok():
        print("no")
    time_.run_a_function_after_x_seconds(ok, 5)