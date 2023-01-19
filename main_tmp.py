#!/usr/bin/env python

from mockups import ocean_climate

download_dir = "indir"  # where download/read data


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Mockup method")
    parse.add_argument('input_parameters', type=str, help="JSON-like string (use ' instead of \")")
    parse.add_argument('-o', '--ocean_climate', action="store_true", help="Enable Ocean Climate mockup execution")

    return parse.parse_args()


def main():
    args = get_args()
    input_parameters = args.input_parameters
    ocean_climate_flag = args.ocean_climate

    if ocean_climate_flag:
        ocean_climate.main(args)
    else:
        raise Exception("ERROR Please select a valid mockup, use python mockup.py -h to see available arguments")




if __name__ == '__main__':
    main()
