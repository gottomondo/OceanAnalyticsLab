from abc import ABC, abstractmethod
from download.src import working_domain


class InputStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete Strategies.
    """

    @abstractmethod
    def get_wd(self, working_domain_dict, product_id):
        pass

    @abstractmethod
    def get_lon_lat(self, working_domain_dict, product_id):
        pass

    @abstractmethod
    def get_depth(self, working_domain_dict, product_id):
        pass

    @abstractmethod
    def get_time_range(self, working_domain_dict):
        pass

    def _get_time_freq(self, working_domain_dict):
        return working_domain_dict['time_freq']
