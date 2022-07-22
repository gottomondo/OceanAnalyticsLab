#!/usr/bin/env python

import netCDF4
import traceback

from input.iparameters import InputParameters
from input import working_domain as wd
from log.logmng import LogMng
from download import daccess
from mtplot import ncplot
from tools import time_utils
from tools import fields_mng

wdir = "./indir"


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="SSI method")
    parse.add_argument('input_parameters', type=str, help="JSON-like string (use ' instead of \")")

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


def get_time_frequency(dataset):
    time_freq = "y" if dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB" else "m"
    return time_freq


def get_return_type(dataset):
    return_type = "str" if dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB" else "netCDF4"
    return return_type


def init_input_parametersSSI(input_arguments):
    input_parameters_json_like = input_arguments.input_parameters
    input_parameters_class = InputParameters(input_parameters_json_like)
    return input_parameters_class


def prepare_input_parametersSSI(input_arguments):
    #Data Source
    try:
        if input_parameters.get_data_source() != "C3S_ERA5_MEDSEA_1979_2020_STHUB":
            raise Exception("Only data source C3S_ERA5_MEDSEA_1979_2020_STHUB is currently available")
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
    
    #Output type
    try:
        if input_parameters.get_output_type() is None:
            input_parameters.update_output_type('ssi_percentile_min') #default (NOW MANDATORY!!!)
        elif input_parameters.get_output_type not in {'ssi_percentile', 'ssi_percentile_min', 'ssi_fixed'}::
            raise Exception("Output type '{}' unknown".format(input_parameters.get_output_type()))
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    
        

    #Title
    try:
        if input_parameters.get_title() is None:
            input_parameters.update_get_title('SSI_output') #default
        title = input_parameters.get_title()
        forbidden_chars = ' "*\\/\'|?:<>'
        for x in title:
            if x in forbidden_chars:
                raise Exception("Title can not contain %s" % (forbidden_chars)")
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)          
                                
                                
    #Start time & End time (MANDATORY)
    starttime = date.fromisoformat(input_parameters.get_start_time())
    endtime = date.fromisoformat(input_parameters.get_end_time())                             
    try:
        if enddate < startdate:
            raise Exception("Illegal End time: End time must be after Start time")
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    

    #Stepsize Time                            
                                
                                if args.time_stepsize > 0 and args.time_stepsize < 11:
        stepsize = args.time_stepsize
    else:
        raise Exception('Íllegal stepsize')

    allowed_stepunits = {'None':1, 'Days':2, 'Months':3, 'Years':4}
    if args.time_stepunit in allowed_stepunits:
        stepunit=allowed_stepunits[args.time_stepunit]
    else:
        raise Exception('Íllegal stepunit')

    valid_workdomain = daccess_working_domain['lonLat']   
    args.workdomain = eval(args.workdomain)
    if len(args.workdomain)==4 :
        workdomain= args.workdomain
        if args.workdomain[0] < valid_workdomain[0] or args.workdomain[1] > valid_workdomain[1] or args.workdomain[2] < valid_workdomain[2] or args.workdomain[3] > valid_workdomain[3] :
            raise Exception('Íllegal workdomain')

    if args.threshold_perc in {'P90', 'P95', 'P98', 'P99'} :
        windspeed_threshold_percentile= args.threshold_perc
    else:
        raise Exception('Illegal percentile')

    if args.threshold_value > 0:
        windspeed_threshold_value = args.threshold_value
 





def summarize_input_parametersSSI(input_parameters: InputParametersSSI):
    print("\n\nInput arguments\n")
    print("Data Source:", input_parameters.get_data_source())
    #print("Id Field:", input_parameters.get_id_field())
    print("Output Type:", input_parameters.get_output_type())
    print("Title:", input_parameters.get_title())   
    print("Start Time:", input_parameters.get_start_time())
    print("End Time:", input_parameters.get_end_time())
    print("Working Domain:", input_parameters.get_working_domain()) 
    print("Stepsize Time:", input_parameters.get_time_stepsize())
    print("Stepunit Time:", input_parameters.get_time_stepunit())
    print("Windspeed threshold percentile:", input_parameters.get_threshold_perc())
    print("Windspeed threshold value (m/s):", input_parameters.get_threshold_value())
    

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

    #Validate and prepare SSI calculation input
    
    #Summarize SSI calculation input
    
    #Download dataset
    
    #Start calculation
    
    
    
    output_type = input_parametersSSI.get_output_type()

    try:

        if output_type == "mockup_download":

            mockup_download(input_parametersSSI, json_log)
        elif output_type == "mockup_input_read":
            mockup_input_read(input_parameters)
        else:
            raise Exception("Output type '{}' unknown".format(output_type))
    except Exception as e:  # create mock output file and finalize json log file
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)


def mockup_download(input_parameters: InputParameters, json_log: LogMng):
    # read all necessary info from input_parameters
    dataset = input_parameters.get_data_source()
    working_domain = input_parameters.get_working_domain()
    id_field = input_parameters.get_id_field()

    # ------------ file download ------------ #
    nc_dataset = download(working_domain, dataset, id_field, json_log, input_parameters)
    if dataset != "C3S_ERA5_MEDSEA_1979_2020_STHUB":  # unable to plot this data source
        # move download file in root dir and rename in output.nc
        nc_output = netCDF4.Dataset('output.nc', mode='w')
        clone_nc_dataset(nc_source=nc_dataset[0], nc_dest=nc_output)
        nc_output.close()
        # ------------ plot ------------ #
        var_to_plot = fields_mng.get_output_var(id_field)
        plot_args = ["output.nc", var_to_plot, '--title=' + ','.join(id_field), '--o=output']
        ncplot.main(plot_args)
    # Save info in json file
    json_log.set_done()


def download(working_domain, dataset, id_field, json_log: LogMng, input_parameters: InputParameters):
    print("START MakeInDir")
    json_log.phase_start("download")  # will create an item download_start in exec section of json file
    nc_dataset = None
    try:
        start_time, end_time, month = input_parameters.get_start_end_time_and_month()
        return_type = get_return_type(dataset)
        time_freq = get_time_frequency(dataset)

        # convert parameters in daccess format
        daccess_working_domain = wd.init_daccess_working_domain(working_domain)  # convert format of working domain
        fields = fields_mng.get_cf_standard_name(id_field)
        times = time_utils.get_time_range_wd(start_time, end_time, month)
        if dataset == "C3S_ERA5_MEDSEA_1979_2020_STHUB":    # download the timerange file
            times = [times[0]]  # it's sufficient to match with one of the timerange dates in the file to download
        dcs = daccess.Daccess(dataset, fields, time_freq=time_freq)
        for time in times:
            daccess_working_domain['time'] = time
            nc_dataset = dcs.download(daccess_working_domain, return_type=return_type, rm_file=False)
    except Exception as e:
        error_code = 3
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)

    # string here must be equals to phase start
    json_log.phase_done("download")  # it will create an item download_end in exec section reporting running time
    if nc_dataset is None:
        raise Exception("An error occurs while downloading file")
    return nc_dataset


if __name__ == '__main__':
    main()
