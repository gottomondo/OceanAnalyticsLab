from abc import ABC, abstractmethod


class InputStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete Strategies.
    """
    def __init__(self):
        self.lonLat = None
        self.depth = None
        self.time = None
        self.time_freq = None

    def get_wd(self, working_domain, product_id):
        """
        @param product_id: product to download
        @param working_domain: dict with spatial/time information:
                lonLat: list of list, the internal list has the format:  [[minLon , maxLon], [minLat , maxLat]]
                depth: depth range in string format: [minDepth, maxDepth]
                time: list of two strings that represent a time range: [YYYY-MM-DDThh:mm:ssZ, YYYY-MM-DDThh:mm:ssZ]
        """
        self.lonLat = self.get_lon_lat(working_domain, product_id)
        self.depth = self.get_depth(working_domain, product_id)
        self.time = self.get_time(working_domain)
        return self.__dict__

    @abstractmethod
    def get_lon_lat(self, working_domain, product_id):
        pass

    @abstractmethod
    def get_depth(self, working_domain, product_id):
        pass

    @abstractmethod
    def get_time(self, working_domain):
        pass

    def generate_time_list(self, start_time, end_time, time_freq):
        import pandas

        from datetime import date

        time_list = list()

        start_year = int(start_time[0:4])
        end_year = int(end_time[0:4])
        start_month = 1
        end_month = 12
        start_day = 1
        end_day = 31

        if time_freq == "y":
            pass  # the default parameters are okay
        elif time_freq == "m":
            start_month = self.extract_month(start_time)
            end_month = self.extract_month(end_time)
            end_day = self.get_number_day_in_month(end_year, end_month)
        elif time_freq == "d":
            start_month = self.extract_month(start_time)
            end_month = self.extract_month(end_time)
            start_day = self.extract_day(start_time)
            end_day = self.get_number_day_in_month(end_year, end_month)
        else:
            raise Exception("Time resolution {} unknown".format(time_freq))

        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)

        pandas_time_list = pandas.date_range(start_date, end_date, freq=time_freq)
        for time in pandas_time_list:
            year = time.year
            month = str(time.month).zfill(2)
            day = str(time.day).zfill(2)

            date_formatted = self.get_formatted_date(year, month, day, time_freq)
            time_list.append(date_formatted)
        return time_list

    def extract_month(self, input_date):
        if isinstance(input_date, str):
            month = int(input_date[5:7])
        else:
            raise Exception("Can't extract month from data type: {}", type(input_date))

        return month

    def extract_day(self, input_date):
        if isinstance(input_date, str):
            day = int(input_date[8:10])
        else:
            raise Exception("Can't extract day from data type: {}", type(input_date))

        return day

    def get_number_day_in_month(self, year, month):
        from calendar import monthrange
        return monthrange(year, month)[1]  # to get the correct last day of end_month

    @abstractmethod
    def get_formatted_date(self, year, month, day, time_freq):
        pass
