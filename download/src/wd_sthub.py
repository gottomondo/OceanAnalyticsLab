from download.src.working_domain import WorkingDomain
from download.src import time_utils


class WorkingDomainStHub(WorkingDomain):
    def get_time(self):
        # time_list_raw is a pandas.DataTimeIndex: An immutable container for datetimes -> to convert in str
        # with the appropriate format
        time_list_raw = time_utils.generate_time_list(self.get_start_time(), self.get_end_time(), self.get_time_freq())
        time_list = [
            self.get_formatted_date(time.year, str(time.month).zfill(2), str(time.day).zfill(2), self.get_time_freq())
            for time in time_list_raw
        ]

        return time_list

    def get_formatted_date(self, year, month, day, time_freq):
        if time_freq == "y":
            date_formatted = "{}".format(year)
        elif time_freq == "m":
            date_formatted = "{}{}".format(year, month)
        elif time_freq == "d":
            date_formatted = "{}{}{}".format(year, month, day)
        else:
            raise Exception("Time resolution {} unknown".format(time_freq))

        return date_formatted
