#!/usr/bin/env python

from mockups import ocean_climate
from mockups import ssi
from mockups import ocean_pattern
import base64

download_dir = "indir"  # where download/read data


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Mockup method")
    parse.add_argument('input_parameters', type=str, help="JSON-like string (use ' instead of \")")
    parse.add_argument('-o', '--ocean_climate', action="store_true", help="Enable Ocean Climate mockup execution")
    parse.add_argument('-s', '--ssi', action="store_true", help="Enable SSI mockup execution")
    parse.add_argument('-p', '--ocean_pattern', action="store_true", help="Enable Ocean Pattern mockup execution")

    return parse.parse_args()


def main():
    args = get_args()
    args.input_parameters = base64.b64decode(args.input_parameters).decode("utf-8")

    ocean_climate_flag = args.ocean_climate
    ssi_flag = args.ssi
    ocean_pattern_flag = args.ocean_pattern

    if ocean_climate_flag:
        ocean_climate.main(args)
    elif ssi_flag:
        ssi.main(args)
    elif ocean_pattern_flag:
        ocean_pattern.main(args)
    else:
        raise Exception("ERROR Please select a valid mockup, use python mockup.py -h to see available arguments")


if __name__ == '__main__':
    main()
