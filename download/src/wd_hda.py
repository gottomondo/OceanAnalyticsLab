from download.src.working_domain import WorkingDomain
from download.src import time_utils


def fix_date(time_list, time_freq):
    from datetime import date
    # In hda service, the value of the variable with low frequency of time_freq is important
    # example: if time_freq=y -> start_month=1 end_mont=12, start_day=1, end_day=3?

    start_time: date = time_list[0]
    end_time: date = time_list[-1]

    start_month = 1
    start_day = 1

    if time_freq == "y":
        end_month = 12
        end_day = time_utils.get_number_day_in_month(end_time.year, end_month)
        start_time = start_time.replace(month=start_month, day=start_day)
        end_time = end_time.replace(month=end_month, day=end_day)
    elif time_freq == "m":
        end_day = time_utils.get_number_day_in_month(end_time.year, end_time.month)
        start_time = start_time.replace(day=start_day)
        end_time = end_time.replace(day=end_day)
    elif time_freq == "d":
        pass    # nothing to change in both dates
    else:
        raise Exception("Time resolution {} unknown".format(time_freq))

    return [start_time, end_time]


class WorkingDomainHda(WorkingDomain):
    def get_time(self):
        # enable this to download split files from hda
        # time_list_raw is a pandas.DataTimeIndex: An immutable container for datetimes -> to convert in str
        # with the appropriate format
        time_list_raw = time_utils.generate_time_list(self.get_start_time(), self.get_end_time(), self.get_time_freq())
        time_list_boundary_fixed = fix_date(time_list_raw, self.get_time_freq())
        time_list = [
            self.get_formatted_date(time.year, str(time.month).zfill(2), str(time.day).zfill(2), self.get_time_freq())
            for time in time_list_boundary_fixed
        ]

        return [time_list[0], time_list[-1]]

    def get_formatted_date(self, year, month, day, time_freq):
        date_formatted = "{}-{}-{}".format(year, month, day)

        return date_formatted
