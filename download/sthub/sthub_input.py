from download.interface.iinput import InputStrategy
from download.sthub.sthub_wd import WorkingDomainStHub


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

    def get_time_range(self, working_domain):
        if 'time' not in working_domain:
            raise Exception("Can't read time from workingDomain")
        return working_domain['time']

    def get_wd(self, working_domain_dict, product_id):
        """
                    @param product_id: product to download
                    @param working_domain_dict: dict with spatial/time information:
                        lonLat: list of list, the internal list has the format:  [[minLon , maxLon], [minLat , maxLat]]
                        depth: depth range in string format: [minDepth, maxDepth]
                        time: list of two strings that represent a time range: [YYYY-MM-DDThh:mm:ssZ, YYYY-MM-DDThh:mm:ssZ]
                        """
        lon_lat = self.get_lon_lat(working_domain_dict, product_id)
        depth = self.get_depth(working_domain_dict, product_id)
        time_range = self.get_time_range(working_domain_dict)
        time_freq = self._get_time_freq(working_domain_dict)
        return WorkingDomainStHub(lon_lat, depth, time_range, time_freq)
