#!/usr/bin/env python

import os
import glob
import shutil

import check_json

wdir = "./indir"


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Mockup method")

    parse.add_argument('dirID', type=str, help="D4Science directory ID")

    return parse.parse_args()


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
    myshfo = storagehubfacilitypython.StorageHubFacility(operation="ItemChildren",
                                                         ItemId=dirID)
    myshfo.main()

    mobj = json.load(open('outFile'))
    complete_list = check_json.get_id(mobj)  # list of (id, name_file) pairs

    # download the first file
    myshfo = storagehubfacilitypython.StorageHubFacility(operation="Download", ItemId=complete_list[0][0],
                                                         localFile=wdir + "/" + complete_list[0][1])
    myshfo.main()


def main():
    args = get_args()
    dirId = args.dirID

    make_indir(dirId)

    # move only the first file in wdir and rename to output.nc
    for file in glob.glob(wdir + "/*.nc"):
        print(file)
        shutil.move(file, "output.nc")
        break


if __name__ == '__main__':
    main()
