#!/usr/bin/env python

import os
import glob
import shutil
import sys
import check_json
import time
import datetime
from tools import json_builder
from dateutil.tz import tzutc

wdir = "./indir"


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Mockup method")

    parse.add_argument('dirID', type=str, help="D4Science directory ID")

    return parse.parse_args()


def filter_list(list_file, output_type):
    """
    This function filters the input list and return a new list with the files that have
    the type of files desired
    @param list_file: list containing (id, file_name) pairs
    @param output_type: file type you want to download from list_file
    @return: list that contains only files of desired type
    """

    llist = list()
    for file in list_file:
        if output_type in file[1]:
            llist.append(file)
            break  # remove if you want to download all files

    return llist


def make_indir(dirID):
    """
    This function downloads the first file founded in directory with id = dirID
    @dirID: D4Science directory ID from which download a file
    """
    import json
    import storagehubfacilitypython

    if os.path.isdir(wdir):
        print(wdir + ' already exists, please remove it')
        return

    os.mkdir("indir")
    # GET CONTENT OF input_datasets/test_med_rea16 or input_datasets/appo
    print("START ItemChildren")
    try:
        myshfo = storagehubfacilitypython.StorageHubFacility(operation="ItemChildren", ItemId=dirID)
        myshfo.main()
    except Exception as e:
        print(e, file=sys.stderr)
        raise Exception('Download error')

    mobj = json.load(open('outFile'))
    complete_list = check_json.get_id(mobj)  # list of (id, name_file) pairs
    filtered_list = filter_list(complete_list, '.nc')

    # download
    for x in filtered_list:
        myshfo = storagehubfacilitypython.StorageHubFacility(operation="Download", ItemId=x[0],
                                                             localFile=wdir + "/" + x[1])
        myshfo.main()


def main():
    main_start_time = time.time()
    args = get_args()
    dirId = args.dirID
    exec_log = json_builder.get_exec_log()

    # ------------ file download ------------ #
    print("START MakeInDir")
    exec_log.add_message("Start Download files")
    try:
        start_dl_time = time.time()
        make_indir(dirId)
    except Exception as e:
        print(e, file=sys.stderr)
        err_log = json_builder.LogError(-1, str(e))
        error_exit(err_log, exec_log)
    exec_log.add_message("Complete Download files", time.time() - start_dl_time)

    # move only the first file in wdir and rename to output.nc
    for file in glob.glob(wdir + "/*.nc"):
        print(file)
        shutil.move(file, "output.nc")
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
