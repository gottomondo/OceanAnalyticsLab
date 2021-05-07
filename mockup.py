#!/usr/bin/env python

import glob
import shutil
import sys
import time
import datetime
from tools import json_builder
from dateutil.tz import tzutc
from download import daccess

wdir = "./indir"


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Mockup method")

    parse.add_argument('dataset', type=str, help="Source dataset to download")

    return parse.parse_args()


def main():
    main_start_time = time.time()
    args = get_args()
    exec_log = json_builder.get_exec_log()

    # ------------ parameter declaration ------------ #
    # direct declaration of parameters, you should able to extract these information from input_parameters
    dataset = args.dataset
    fields = ['sea_water_potential_temperature']
    daccess_working_domain = dict()
    daccess_working_domain['time'] = ['1987-01-01T00:00:00', '1987-01-31T00:00:00']
    daccess_working_domain['depth'] = [10, 100]
    daccess_working_domain['lonLat'] = [-1.99, 1, 34, 37]

    # ------------ file download ------------ #
    print("START MakeInDir")
    exec_log.add_message("Start Download files")
    try:
        start_dl_time = time.time()
        dcs = daccess.Daccess(dataset, fields)
        dcs.download(daccess_working_domain)
    except Exception as e:
        print(e, file=sys.stderr)
        err_log = json_builder.LogError(-1, str(e))
        error_exit(err_log, exec_log)
    exec_log.add_message("Complete Download files", time.time() - start_dl_time)

    # move only the first file in wdir and rename to output.nc
    for file in glob.glob(wdir + "/*.nc"):
        print(file)
        shutil.copy(file, "output.nc")
        break

    # Save info in json file
    exec_log.add_message("Total time: " + " %s seconds " % (time.time() - main_start_time))
    err_log = json_builder.LogError(0, "Execution Done")
    end_time = get_iso_timestamp()
    json_builder.write_json(error=err_log.__dict__,
                            exec_info=exec_log.__dict__['messages'],
                            end_time=end_time)


def error_exit(err_log, exec_log):
    """
    This function is called if there's an error occurs, it write in log_err the code error with
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
