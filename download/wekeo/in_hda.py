from download.interface.iinput import InputStrategy
from download.wekeo import dataset_access as db
import copy


def binary_search(elements, value, mode: int):
    """
    @param elements: list where to search
    @param value: value used to find the sets
    @param mode: if 0 -> select the biggest value in elements that is contained by x_des,
                 if 1 -> select the minimum value in elements that contains x_des
    @return: if mode == 0: the biggest value in elements that is contained within x_des,
             if mode == 1: the minimum value in elements that contains x_des
    """
    half_index = int(len(elements) / 2)

    if len(elements) == 2:
        if mode == 0:
            return elements[0]
        else:
            return elements[1]

    if elements[half_index] == value:
        return elements[half_index]
    # if mode == 1 the bigger element from left list is excluded.
    elif value < elements[half_index]:
        return binary_search(elements[0: half_index + 1], value, mode)
    else:
        return binary_search(elements[half_index:len(elements)], value, mode)


class InHDA(InputStrategy):
    def __init__(self):
        super().__init__()
        self.dataset = db.Dataset()

    def get_depth(self, working_domain, product_id):
        """
        @param product_id: source dataset
        @param working_domain: dict with depth information:
                    depth: depth range in string format: [minDepth, maxDepth]
        @return: depth range in string format: [minDepth, maxDepth]
        """
        depth_dataset = self.dataset.get_depth(product_id)
        if depth_dataset is None:
            print("Dataset: ", product_id, " doesn't have depth attribute")
            return None
        depth = copy.deepcopy(working_domain['depth'])
        depth_dataset.sort()

        if depth[0] > min(depth_dataset):
            depth[0] = str(binary_search(depth_dataset, depth[0], 0))
        else:
            depth[0] = str(depth[0])

        depth[1] = str(binary_search(depth_dataset, depth[1], 1))

        if depth is None:
            raise Exception("Can't extract vertical domain from wd: " + str(working_domain))
        return depth

    # time information from daccess is already correct
    def get_time(self, working_domain):
        if 'time' not in working_domain:
            raise Exception("Can't read time from workingDomain")
        return working_domain['time']

    def get_lon_lat(self, working_domain, product_id):
        """
        @param product_id: source dataset
        @param working_domain: dict with lonLat information:
                    lonLat: list of list, the internal list has the format:  [[minLon , maxLon], [minLat , maxLat]]
        @return: a lonLat represent as a list of float with the template:
                    [minLon, minLat, maxLon, maxLat]
        """
        if 'lonLat' not in working_domain:
            raise Exception("Can't read lonLat from workingDomain")

        lonLat_tmp = working_domain['lonLat']
        lonLat = [lonLat_tmp[0], lonLat_tmp[2], lonLat_tmp[1], lonLat_tmp[3]]

        lon_dataset = self.dataset.get_lon(product_id)
        if lonLat[0] > min(lon_dataset):
            lonLat[0] = binary_search(lon_dataset, lonLat[0], 0)
        lonLat[2] = binary_search(lon_dataset, lonLat[2], 1)

        lat_dataset = self.dataset.get_lat(product_id)
        if lonLat[1] > min(lon_dataset):
            lonLat[1] = binary_search(lat_dataset, lonLat[1], 0)
        lonLat[3] = binary_search(lat_dataset, lonLat[3], 1)

        if lonLat is None:
            raise Exception("Can't extract horizontal domain from wd: " + str(working_domain))
        return lonLat

    def get_formatted_date(self, year, month, day, time_freq):
        if time_freq == "y":
            date_formatted = "{}".format(year)
        elif time_freq == "m":
            date_formatted = "{}-{}".format(year, month)
        elif time_freq == "d":
            date_formatted = "{}-{}-{}".format(year, month, day)
        else:
            raise Exception("Time resolution {} unknown".format(time_freq))

        return date_formatted
