#!/usr/bin/env python

import sys
import time
import datetime
import netCDF4
from tools import json_builder
from dateutil.tz import tzutc
from download import daccess
from mtplot import ncplot

wdir = "./indir"


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Mockup method")

    parse.add_argument('dataset', type=str, help="Source dataset to download")

    return parse.parse_args()


def clone_nc_dataset(nc_source, nc_dest):
    nc_dest.setncatts(nc_source.__dict__)

    for name, dimension in nc_source.dimensions.items():
        nc_dest.createDimension(
            name, (len(dimension) if not dimension.isunlimited() else None))

    # create all necessary variables in dailyFile
    for name, variable in nc_source.variables.items():
        nc_dest.createVariable(name, variable.datatype, variable.dimensions)
        # copy variable attributes all at once via dictionary
        nc_dest[name].setncatts(nc_source[name].__dict__)
        nc_dest[name][:] = nc_source[name][:]


def get_fields(dataset):
    if dataset == "OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041":
        return ['mass_concentration_of_chlorophyll_a_in_sea_water']
    elif dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":
        return ['wind_speed']
    else:
        return ['sea_water_potential_temperature']


def get_time_frequency(dataset):
    if dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":
        time_freq = "y"
    else:
        time_freq = "m"

    return time_freq


def get_return_type(dataset):
    if dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":
        return_type = "str"
    else:
        return_type = "netCDF4"

    return return_type


def main():
    main_start_time = time.time()
    args = get_args()
    exec_log = json_builder.get_exec_log()

    # ------------ parameter declaration ------------ #
    # direct declaration of parameters, you should able to extract these information from input_parameters
    dataset = args.dataset
    fields = get_fields(dataset)
    var_to_plot = get_var_to_plot(dataset)
    daccess_working_domain = get_daccess_working_domain(dataset)
    time_freq = get_time_frequency(dataset)
    return_type = get_return_type(dataset)

    # ------------ file download ------------ #
    nc_dataset = download(daccess_working_domain, dataset, exec_log, fields, time_freq, return_type)

    # move download file in root dir and rename in output.nc
    if return_type == "netCDF4":
        nc_output = netCDF4.Dataset('output.nc', mode='w')
        clone_nc_dataset(nc_source=nc_dataset[0], nc_dest=nc_output)
        nc_output.close()

    # ------------ plot ------------ #
    if dataset != "C3S_ERA5_MEDSEA_1979_2020_STHUB":    # unable to plot this datasource as is original
        plot_args = ["output.nc", var_to_plot, '--title=' + ','.join(fields), '--o=output']
        ncplot.main(plot_args)

    # Save info in json file
    exec_log.add_message("Total time: " + " %s seconds " % (time.time() - main_start_time))
    err_log = json_builder.LogError(0, "Execution Done")
    end_time = get_iso_timestamp()
    json_builder.write_json(error=err_log.__dict__, exec_info=exec_log.__dict__['messages'], end_time=end_time)


def download(daccess_working_domain, dataset, exec_log, fields, time_freq, return_type):
    print("START MakeInDir")
    exec_log.add_message("Start Download files")
    nc_dataset = None
    start_dl_time = time.time()
    try:
        dcs = daccess.Daccess(dataset, fields, time_freq=time_freq, return_type=return_type)
        nc_dataset = dcs.download(daccess_working_domain)
    except Exception as e:
        print(e, file=sys.stderr)
        err_log = json_builder.LogError(-1, str(e))
        error_exit(err_log, exec_log)
    exec_log.add_message("Complete Download files", time.time() - start_dl_time)
    if nc_dataset is None:
        raise Exception("An error occurs while downloading file")
    return nc_dataset


def get_var_to_plot(dataset):
    if dataset == "MEDSEA_MULTIYEAR_PHY_006_004_STHUB":
        var_to_plot = "thetao"
    elif dataset == "MEDSEA_MULTIYEAR_PHY_006_004":
        var_to_plot = "thetao"
    elif dataset == "OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041":
        var_to_plot = "CHL"  # to check
    elif dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":
        var_to_plot = 'ssi'
    else:
        raise Exception("Dataset unknown: " + dataset)
    return var_to_plot


def get_daccess_working_domain(dataset):
    daccess_working_domain = dict()
    daccess_working_domain['time'] = get_time_wd(dataset)
    daccess_working_domain['depth'] = [10, 100]
    daccess_working_domain['lonLat'] = [-6, 36.5, 30, 46]
    return daccess_working_domain


def get_time_wd(dataset):
    if dataset == "MEDSEA_MULTIYEAR_PHY_006_004_STHUB":
        time_wd = ['1987-01-01T00:00:00', '1987-02-31T00:00:00']
    elif dataset == "MEDSEA_MULTIYEAR_PHY_006_004":
        time_wd = ['2000-01-01T00:00:00', '2000-01-31T00:00:00']
    elif dataset == "OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041":
        time_wd = ['2020-07-01T00:00:00', '2020-07-31T00:00:00']
    elif dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":
        # must be present a match between the date indicated in the
        # time range and the date in the filename to download
        time_wd = ['1979-01-01T00:00:00', '2021-01-31T00:00:00']

    return time_wd


def error_exit(err_log, exec_log):
    """
    This function is called if there's an error occurs, it writes in log_err the code error with
    a relative message, then copy some mock files in order to avoid bluecloud to terminate with error
    """
    # shutil.copy("./mock/output.nc", "output.nc")
    # shutil.copy("./mock/output.png", "output.png")
    end_time = get_iso_timestamp()
    json_builder.write_json(error=err_log.__dict__,
                            exec_info=exec_log.__dict__['messages'],
                            end_time=end_time)
    exit(0)


def get_iso_timestamp():
    isots = datetime.datetime.now(tz=tzutc()).replace(microsecond=0).isoformat()
    return isots


if __name__ == '__main__':
    main()
