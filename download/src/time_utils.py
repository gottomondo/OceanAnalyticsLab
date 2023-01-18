def generate_time_list(start_time, end_time, time_freq):
    import pandas

    from datetime import date

    time_list = list()

    start_year = int(start_time[0:4])
    end_year = int(end_time[0:4])
    # default value to handle all supported frequencies
    start_month = 1
    end_month = 12
    start_day = 1
    end_day = 31

    if time_freq == "y":
        pass  # the default parameters are okay
    elif time_freq == "m":
        start_month = extract_month(start_time)
        end_month = extract_month(end_time)
        end_day = get_number_day_in_month(end_year, end_month)
    elif time_freq == "d":
        start_month = extract_month(start_time)
        end_month = extract_month(end_time)
        start_day = extract_day(start_time)
        end_day = get_number_day_in_month(end_year, end_month)
    else:
        raise Exception("Time resolution {} unknown".format(time_freq))

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    pandas_time_list = pandas.date_range(start_date, end_date, freq=time_freq)
    for time in pandas_time_list:
        # year = time.year
        # month = str(time.month).zfill(2)
        # day = str(time.day).zfill(2)
        time_list.append(time)
    return time_list


def extract_month(input_date):
    if isinstance(input_date, str):
        if len(input_date) == 6 or len(input_date) == 7:     # case date format is YYYYMM or YYYY-MM
            month = int(input_date[-2:])
        else:
            raise Exception(f"ERROR Can't extract month from date: {input_date}")
    else:
        raise Exception("Can't extract month from data type: {}", type(input_date))

    return month


def extract_day(input_date):
    if isinstance(input_date, str):
        day = int(input_date[8:10])
    else:
        raise Exception("Can't extract day from data type: {}", type(input_date))

    return day


def get_number_day_in_month(year, month):
    from calendar import monthrange
    return monthrange(year, month)[1]  # to get the correct last day of end_month
