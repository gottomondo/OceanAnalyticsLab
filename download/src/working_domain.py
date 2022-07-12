from abc import ABC, abstractmethod


class WorkingDomain(ABC):
    def __init__(self, lon_lat: list, depth: list, time_range: list, time_freq: str):
        self._lon_lat = lon_lat  # [min_lon , max_lon, min_lat , max_lat]
        self._depth = depth  # [min_depth, max_depth]
        self._time_range = time_range  # [start_time, end_time]

        if time_freq not in ['y', 'm', 'd']:
            raise ValueError(f"Frequency time unknown: {time_freq}, please select one from [y, m, d]")
        else:
            self._time_freq = time_freq

    def get_lon_lat(self):
        return self._lon_lat

    def get_depth(self):
        return self._depth

    def get_time_range(self):
        return self.get_time_range()

    def get_time_freq(self):
        return self._time_freq

    def get_start_time(self):
        return self._time_range[0]

    def get_end_time(self):
        return self._time_range[1]

    @abstractmethod
    def get_time(self):
        pass

    @abstractmethod
    def get_formatted_date(self, year, month, day, time_freq):
        pass
