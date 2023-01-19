#!/usr/bin/env python

import traceback

from input.iparameters import InputParameters
from log.logmng import LogMng
from tools import utils
from modules import modules_factory

DOWNLOAD_DIR = "indir"  # where download/read data
DATASET_FREQ = "m"
MOCK_DIR = "mockups/mock_ocean_climate"


def get_args():
    import argparse

    parse = argparse.ArgumentParser(description="Ocean Climate Mockup method")
    parse.add_argument('input_parameters', type=str, help="JSON-like string (use ' instead of \")")

    return parse.parse_args()


def init_input_parameters(input_arguments):
    input_parameters_json_like = input_arguments.input_parameters
    input_parameters_class = InputParameters(input_parameters_json_like)
    return input_parameters_class


def main(args=None):
    json_log = LogMng()
    try:
        if args is None:
            args = get_args()
        input_parameters: InputParameters = init_input_parameters(input_arguments=args)
        json_log.set_input_parameters(input_parameters.get_input_parameters())
    except Exception as e:
        json_log.handle_exc(traceback.format_exc(), str(e), 1)
        exit(1)

    root_dir = utils.get_root_dir()
    input_dir = root_dir + '/' + DOWNLOAD_DIR
    outdir = root_dir  # sequential and master mode

    factory = modules_factory.ModulesFactory(input_parameters=input_parameters, json_log=json_log)

    # ------------ Download ------------ #
    download = factory.get_module("retrieve_file")
    outfile: list = download.exec(input_dir, DATASET_FREQ)

    # ------------ Execution ------------ #
    prod_exec = factory.get_module("prod_ocean_climate")
    prod_exec.exec(outfile)

    # ------------ Plot ------------ #
    # plot_mod = factory.get_module("plot")
    # plot_mod.exec()

    # ------------ Close ------------ #
    json_log.set_done(outdir=outdir)


if __name__ == '__main__':
    main()
