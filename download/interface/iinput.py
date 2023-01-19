from abc import ABC, abstractmethod
from download.interface.iworking_domain import WorkingDomain


class InputStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete Strategies.
    """

    @abstractmethod
    def get_wd(self, working_domain_dict, product_id) -> WorkingDomain:
        pass

    @abstractmethod
    def get_lon_lat(self, working_domain_dict, product_id):
        pass

    @abstractmethod
    def get_depth(self, working_domain_dict, product_id):
        pass

    def get_time_range(self, working_domain_dict):
        if 'time' not in working_domain_dict:
            raise Exception("Can't read time from workingDomain")
        time_to_return = list()
        for time in working_domain_dict['time']:
            if "T" in time:
                yyyy_mm_dd = time.split("T")[0]     # format YYYY-MM-DDThh:mm:ss
                time_to_return.append(yyyy_mm_dd)
            else:
                time_to_return.append(time)
        return time_to_return

    def _get_time_freq(self, working_domain_dict):
        return working_domain_dict['time_freq']
