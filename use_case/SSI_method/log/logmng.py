import sys

from log.exec_info import ExecInfo
from log.status_info import LogError
from log.other_info import OtherInfo
from tools import time_utils
from tools import utils


class LogMng:
    def __init__(self, input_parameters_dict: dict = None):
        self.input = input_parameters_dict
        self.exec_info = ExecInfo()
        self.other = OtherInfo()
        self.error_log = LogError()
        self.end_time = None
        self.worker_logs = None

    def set_input_parameters(self, input_parameters):
        self.input = input_parameters

    def phase_start(self, input_phase: str):
        self.exec_info.start_event(input_phase)

    def phase_done(self, input_phase: str, input_run_time=None, idle_time=None):
        self.exec_info.done_event(input_phase, input_run_time, idle_time)

    def get_exec_log(self):
        return self.exec_info

    def set_done(self, outdir=None):
        self.error_log.set_no_error()
        self.exec_info.done_event("Main")
        self.set_end_time()

        self.write_json(outdir)

    def set_poutkey(self, poutkey):
        self.other.set_poutkey(poutkey)

    def set_worker_logs(self, worker_logs):
        self.worker_logs = worker_logs

    def set_end_time(self):
        self.end_time = time_utils.get_iso_timestamp()

    def write_json(self, outdir=None):
        """
        This function writes in a json file the two classes exec_log and log_error
        @param outdir: a list of dicts to insert in a json file
        """
        import json
        import os

        if outdir is None:
            outdir = utils.get_root_dir()

        if not os.path.exists(outdir):
            raise Exception("Path " + outdir + " not exists")

        json_log = dict()
        for jsonDict in self.__dict__:
            if self.__getattribute__(jsonDict) is None:
                continue
            dict_attribute = self.__getattribute__(jsonDict)
            if isinstance(dict_attribute, ExecInfo):
                dict_attribute = dict_attribute.get_exec_log()
            if isinstance(dict_attribute, LogError):
                dict_attribute = dict_attribute.get_error_log()
            if isinstance(dict_attribute, OtherInfo):
                dict_attribute = dict_attribute.__dict__

            json_log[jsonDict] = dict_attribute
        json.dump(json_log, open(outdir + "/output.json", "w"), indent=4)

    def handle_exc(self, traceback_exc: str, exc_msg: str, err_code: int):
        """
        This function is called if there's an error occurs, it writes in log_err the code error with
        a relative message, then copy some mock files in order to avoid bluecloud to terminate with error
        """
        import shutil

        complete_exception = traceback_exc + '\n' + exc_msg
        print(complete_exception, file=sys.stderr)

        self.set_end_time()
        self.error_log = LogError(err_code, complete_exception)

        # wps method will always look for the output files, also if execution has failed
        # provide mock output files allow us to be able to return a correct log file
        shutil.copy("./mock/SSIoutput.nc", "SSIoutput.nc")
        shutil.copy("./mock/SSImaps.png", "SSImaps.png")
        shutil.copy("./mock/SSItimeseries.png", "SSItimeseries.png")

        self.write_json()
