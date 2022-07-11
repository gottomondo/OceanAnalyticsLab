from download.interface.iinput import InputStrategy


class InStHub(InputStrategy):
    def __init__(self):
        super().__init__()

    # lonLat information is not necessary
    def get_lon_lat(self, working_domain, product_id):
        """
        @param working_domain: dict with lonLat information:
                    lonLat: list of list, the internal list has the format:  [minLon , maxLon, minLat , maxLat]
        @return: a lonLat represent as a list of float with the template:
                    [minLon , maxLon, minLat , maxLat]
        """
        return working_domain['lonLat']

    # depth information is not necessary
    def get_depth(self, working_domain, product_id):
        # some product id doesn't have the depth attributes
        depth = working_domain.get('depth', None)
        return depth

    def get_time(self, working_domain):
        """
        Check if the time range refers to the same month, then return the date with the pattern YYYYMM
        @param working_domain: dict with time information:
                time: date in string format: [YYYYMM]
        @return a list of date with pattern YYYYMM
        """
        if 'time' not in working_domain:
            raise Exception("Can't read time from workingDomain")
        time = working_domain['time']
        time_freq = working_domain.get('time_freq', 'm')

        # extract time as YYYYMM
        start_time = time[0]
        end_time = time[1]

        time_list = self.generate_time_list(start_time, end_time, time_freq)
        # check if only one month has been requested
        # if start_time != end_time:
        #     raise Exception("time error, check the time range: " + start_time + " - " + end_time)

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
