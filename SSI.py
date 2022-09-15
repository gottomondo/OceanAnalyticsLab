#!/usr/bin/env python

import netCDF4
import traceback
from datetime import date

from SSI.SSI_iparameters import InputParametersSSI
from SSI.SSI_iparameters import init_input_parametersSSI
from SSI.SSI_iparameters import validate_input_parametersSSI
from SSI.SSI_calculation import calculateSSI
from input.iparameters import InputParameters
from input import working_domain as wd
from log.logmng import LogMng
from download import daccess
from mtplot import ncplot
from tools import time_utils
from tools import fields_mng
from input import working_domain as wd



def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="SSI method")
    parse.add_argument('input_parameters', type=str, help="JSON-like string (use ' instead of \")")

    return parse.parse_args()


def main():
    json_log = LogMng()

    try:
        args = get_args()
        input_parametersSSI: InputParametersSSI = init_input_parametersSSI(input_arguments=args)
        json_log.set_input_parameters(input_parametersSSI.get_input_parameters())  # save input args info in json log
    except Exception as e:  # create SSI output file and finalize json log file
        error_code = 1
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
                                                  

    try:                     
                    
        #Download data source into running environment (if needed) - currently files in sthub. 
        data_download(input_parametersSSI, json_log)
        
        #Prepare SSI calculation input
        validate_input_parametersSSI(input_parametersSSI, json_log)
                                
        #Calculation and store output results
        calculateSSI(input_parametersSSI, json_log)  
        
        # Save info in json file
        json_log.set_done()
                                
    except Exception as e:  # create SSI output file and finalize json log file
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
                                
                                
def data_download(input_parameters: InputParameters, json_log: LogMng):
    # read all necessary info from input_parameters
    dataset = input_parameters.get_data_source()
    working_domain = input_parameters.get_working_domain()
    input_parameters.update_id_field('wind_speed')
    id_field = input_parameters.get_id_field()

    # ------------ file download ------------ #
    nc_dataset = download(working_domain, dataset, id_field, json_log, input_parameters)

                               


def download(working_domain, dataset, id_field, json_log: LogMng, input_parameters: InputParameters):
    print("START MakeInDir")
    json_log.phase_start("Download SSI input data")  # will create an item download_start in exec section of json file
    nc_dataset = None
    try:
        start_time, end_time, month = input_parameters.get_start_end_time_and_month()
        #return_type = get_return_type(dataset)
        #time_freq = get_time_frequency(dataset)

        # convert parameters in daccess format
        daccess_working_domain = wd.init_daccess_working_domain(working_domain)  # convert format of working domain
        fields = fields_mng.get_cf_standard_name(id_field)
        times = time_utils.get_time_range_wd(start_time, end_time, month)
        if dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":    # download the timerange file
            times = [times[0]]  # it's sufficient to match with one of the timerange dates in the file to download
        dcs = daccess.Daccess(dataset, fields, time_freq="y")
        for time in times:
            daccess_working_domain['time'] = time
            nc_dataset = dcs.download(daccess_working_domain, return_type="str", rm_file=False)
    except Exception as e:
        error_code = 3
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)

    # string here must be equals to phase start
    json_log.phase_done("Download SSI input data")  # it will create an item download_end in exec section reporting running time
    if nc_dataset is None:
        raise Exception("An error occurs while downloading file")
    return nc_dataset


if __name__ == '__main__':
    main()
