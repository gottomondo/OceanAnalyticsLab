class LogError:
    def __init__(self, code=-1, message="Error"):
        self._error_log = dict()

        self._error_log['code'] = code
        self._error_log['message'] = message

    def get_error_log(self):
        return self._error_log

    def set_no_error(self):
        self._error_log['code'] = 0
        self._error_log['message'] = "Execution Done"
