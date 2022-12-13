#!/usr/bin/env python

import json

from download.contexts.input_ctx import InputContext
from download.contexts.download_ctx import DownloadContext
from download.wekeo import in_hda, hda
from download.storagehubfacility import in_sthub, sthub
from download.src import utils

workingDomain_attrs = ['lonLat', 'time']
workingDomain_attrs_optional = ['depth']


def get_infrastructure(dataset):
    root_dir = utils.get_root_dir()
    json_inf_file = root_dir + '/config/dataset_infrastructures.json'
    with open(json_inf_file) as json_file:
        dataset_infrastructures = json.load(json_file)
    if dataset in dataset_infrastructures:
        infrastructure = dataset_infrastructures[dataset]['infrastructure']
    else:
        raise Exception("Can't find dataset: " + dataset + ' in catalogue')

    return infrastructure


class Daccess:
    def __init__(self, dataset: str, fields: list, output_dir=None, hda_key=""):
        """
        @param dataset: source dataset
        @param fields: fields to download as cf standard name (used to represent a variable)
        @param output_dir: output directory
        @param hda_key: key to access to hda service, leave "" if you want to use D4Science proxy
        """
        self.fields = fields
        self.outDir = output_dir
        self.hdaKey = hda_key

        # select the right strategy in according to the selected dataset
        self.dataset = dataset
        self._infrastructure = get_infrastructure(dataset)

        # select the right input/download interface
        if self._infrastructure == 'WEKEO':
            print("Downloading from WEkEO")
            self.input_ctx = InputContext(in_hda.InHDA())
            self.download_ctx = DownloadContext(hda.HDA(self.hdaKey, self.outDir))
        elif self._infrastructure == 'STHUB':
            print("Downloading from Storage Hub Facility")
            self.input_ctx = InputContext(in_sthub.InStHub())
            self.download_ctx = DownloadContext(sthub.StHub(self.dataset, self.outDir))
        else:
            raise Exception('Infrastructure: ' + self._infrastructure + ' not supported')

    def download(self, working_domain_dict: dict, **kwargs):
        """
        @param working_domain_dict: dict with spatial/time information:
                    lonLat: list of list, the internal list has the format:  [minLon , maxLon, minLat , maxLat]
                    depth: depth range in string format: [minDepth, maxDepth]
                    time: list of two strings that represent a time range: [YYYY-MM-DDThh:mm:ssZ, YYYY-MM-DDThh:mm:ssZ]
        As kwargs:
        @param in_memory: if True, try to download the file directly in memory -> it's not fully supported
        @param rm_file: if True, remove file from disk after load it in memory
        @param max_attempt: maximum number of download attempt in case of errors
        @param return_type: if netCDF4 return a netCDF4.Dataset, if str return the output filename
                                if is str, please disable rm_file and in_memory
        @return: store netCDF file in download directory
            """

        wd_validation(working_domain_dict)
        # creating working_domain class in according to the selected download strategy
        working_domain = self.input_ctx.get_wd(working_domain_dict, self.dataset)
        return self.download_ctx.download(self.dataset, working_domain, self.fields, **kwargs)


def wd_validation(working_domain_dict):
    """
    This function check if workingDomain is valid
    @param working_domain_dict: dict with spatial/time information:
                lonLat: list of list, the internal list has the format:  [minLon , maxLon, minLat , maxLat]
                depth: depth range in string format: [minDepth, maxDepth]
                time: list of two strings that represent a time range: [YYYY-MM-DDThh:mm:ssZ, YYYY-MM-DDThh:mm:ssZ]
    @return: True if workingDomain is valid
    """
    for wd_attr in workingDomain_attrs:
        if wd_attr not in working_domain_dict:
            raise Exception("Can't find " + wd_attr + ' in workingDomain: ' + str(working_domain_dict))
    for wd_attr_opt in workingDomain_attrs_optional:
        if wd_attr_opt not in working_domain_dict:
            print("WARNING: ", wd_attr_opt, ' not found')

    # lonLat check
    lonLat = working_domain_dict['lonLat']
    if len(lonLat) != 4:
        raise Exception("Wrong size for lonLat, please check it: " + str(lonLat))
    elif not float_int_check(lonLat):
        raise Exception("Type error in lonLat")

    # depth check
    if 'depth' in working_domain_dict:
        depth = working_domain_dict['depth']
        if len(depth) != 2:
            raise Exception("Wrong size for depth, please check it: " + str(depth))
        elif not float_int_check(depth):
            print("ERROR lonLat value must be float or int, please check it: ", depth)
            raise Exception("Type error in depth")

    # time check
    time = working_domain_dict['time']
    if len(time) != 2:
        raise Exception("Wrong size for lonLat, please check it: " + str(time))


def float_int_check(elements):
    for x in elements:
        if not isinstance(x, float) and not isinstance(x, int):
            print("ERROR found no float or int type: ", x)
            return False
    return True


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Daccess")
    parse.add_argument('product_id', type=str, help="Product to download")
    parse.add_argument('--fields', nargs='+', type=str, default=list(),
                       help="List of fields as cf standard name to download")
    parse.add_argument('start_time', type=str, help="Start time")
    parse.add_argument('end_time', type=str, help="End time")
    parse.add_argument('time_freq', type=str, help="Time frequency")
    parse.add_argument('lon_lat', type=str, help="Lon - Lat coordinate as [minLon, maxLon, minLat, maxLat]")
    parse.add_argument('depth', type=str, help="Depth")
    parse.add_argument('-o', '--outdir', dest="outdir", type=str, default=None, help="Path of output directory")

    return parse.parse_args()


def main():
    import json
    args = get_args()

    product_id = args.product_id
    fields = args.fields
    time_freq = args.time_freq

    lon_lat = json.loads(args.lon_lat)
    start_time = args.start_time
    end_time = args.end_time
    depth = json.loads(args.depth)
    outdir = args.outdir

    daccess_working_domain = dict()
    daccess_working_domain['time'] = [start_time, end_time]
    daccess_working_domain['depth'] = depth
    daccess_working_domain['lonLat'] = lon_lat
    daccess_working_domain['time_freq'] = time_freq

    dcs = Daccess(product_id, fields, output_dir=outdir)
    dcs.download(daccess_working_domain, rm_file=False)


if __name__ == '__main__':
    main()
