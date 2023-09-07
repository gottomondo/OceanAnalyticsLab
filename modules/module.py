#!/usr/bin/env python

"""
Module interface definition

With a module it is indicated small part of a complex workflow which includes some actions of a specific domains.
A module should be in charge only of a one and well-defined part of the workflow, with a general interface.

Here a list of functionalities of the module:

- All the module have access to the same parameters of the workflow
- A standard way to exec safely the core of the module in a try-catch statement, using the log modules to store
    execution info and error log in a standard way (see log readme for more details)
- All the modules must be used in the same way, because only the exec function is exposed externally
"""


import traceback
from abc import ABC, abstractmethod
from input.iparameters import InputParameters
from log.logmng import LogMng


class Module(ABC):
    def __init__(self, json_log: LogMng = None, error_code=1,
                 input_parameters: InputParameters = None):
        self._json_log = json_log
        self._input_parameters = input_parameters
        self._error_code = error_code

    def exec(self, *args, **kwargs):
        """
        THe only function exposed externally. This is the function which starts the module execution
        Returns: It depends on the specific implementation
        """
        try:
            self._pre_exec()
            result = self._exec_impl(*args, **kwargs)
            self._post_exec()
            return result
        except Exception as e:
            self._json_log.handle_exc(traceback.format_exc(), str(e), self._error_code)
            exit(self._error_code)

    def _pre_exec(self):
        """An action executed always before the core of the module to store the start info in the json log"""
        self._json_log.phase_start(self.__class__.__name__)

    def _post_exec(self):
        """An action executed at the end of the core of the module to store the end info in the json log"""
        self._json_log.phase_done(self.__class__.__name__)

    @abstractmethod
    def _exec_impl(self, *args, **kwargs):
        """
        The Core of the module.
        It contains the core of the module which represent the real execution of the module itself.
        It is executed after _pre_exec and before _post_exec inside a try-catch
        """
        pass
