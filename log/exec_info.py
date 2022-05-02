import time
from datetime import datetime

classname_keylog_dict = {
    "Main": "main",
    "Plot": "plot",
    "MasterExecution": "parallel",
    "Prod": "mapreduce",
    "Download": "download",
    "Workflow": "xml",
}

classname_msg_dict = {
    "Main": "Ocean Climate",
    "Plot": "Plot phase",
    "MasterExecution": "Parallel phase",
    "Prod": "Map reduce",
    "Download": "Download file",
    "Workflow": "Workflow building",
}


def get_log_message(msg):
    """
    This function prints to stdout the message passed as argument with a timestamp as prefix
    @param msg: Message to be printed
    """
    date_now = datetime.now()
    log_message = "[" + date_now.strftime("%m/%d/%Y, %H:%M:%S") + "]   -   " + msg
    print(log_message, flush=True)
    return log_message


class ExecInfo:
    def __init__(self):
        self._exec_log = dict()
        self._time_log = dict()

        self.start_event("Main")

    def get_exec_log(self):
        return self._exec_log

    def build_message(self, msg_dsc, run_time=None):
        if run_time is not None:
            message = msg_dsc + ",  time needed: " + " %s seconds " % run_time
        else:
            message = msg_dsc
        log_message = get_log_message(message)

        return log_message

    def get_atomic_key(self, input_phase: str):
        atomic_key = classname_keylog_dict.get(input_phase, None)
        if atomic_key is None:
            print("WARNING Phase unknown, the key will be the phase name itself")
            atomic_key = input_phase

        return atomic_key

    def start_event(self, input_phase: str):
        now = time.time()
        atomic_key = self.get_atomic_key(input_phase)
        key = atomic_key + '_start'

        msg_descr = "Start " + classname_msg_dict.get(input_phase, input_phase)
        log_message = self.build_message(msg_descr)

        self._time_log[key] = now
        self._exec_log[key] = log_message

    def done_event(self, input_phase: str, input_run_time=None, idle_time=None):
        now = time.time()
        atomic_key = self.get_atomic_key(input_phase)
        start_key = atomic_key + '_start'
        done_key = atomic_key + '_end'

        if input_run_time is not None:
            run_time = input_run_time
        elif idle_time is not None:
            start_time = self._time_log[start_key]
            run_time = now - start_time - idle_time
        else:
            start_time = self._time_log[start_key]
            run_time = now - start_time

        msg_descr = "End " + classname_msg_dict.get(input_phase, input_phase)
        log_message = self.build_message(msg_descr, run_time=run_time)
        self._time_log[done_key] = now
        self._exec_log[done_key] = log_message
