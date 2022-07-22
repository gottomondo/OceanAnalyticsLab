#!/usr/bin/env python
from input.iparameters import InputParameters


class InputParametersSSI(InputParameters):
    def __init__(self, input_parameters_string: str):
        super().__init__(input_parameters_string)
        
        self._title: str = self._extract_optional_attribute('title')
        self._time_stepsize: int = self._extract_optional_attribute('time_stepsize')
        self._time_stepunit: str = self._extract_optional_attribute('time_stepunit')
        self._threshold_perc: str = self._extract_optional_attribute('threshold_perc')
        self._threshold_value: float = self._extract_optional_attribute('threshold_value')
            
        self._validate_input_SSIparameters()
        
    
    def get_title(self):
        return self._title

    def get_time_stepsize(self):
        return self._time_stepsize

    def get_time_stepunit(self):
        return self._time_stepunit

    def get_threshold_perc(self):
        return self._threshold_perc

    def get__threshold_value(self):
        return self._threshold_value

    def _validate_input_SSIparameters(self):
        """
        Validate the typeof each parameter
        Returns: raise an exception if there is an input parameter with a wrong type

        """
        #super()._validate_input_parameters()
        
        if self._title is not None and not isinstance(self._title, str):
            self._raise_type_exception("_title", "str")
        if self._time_stepsize is not None and not isinstance(sself._time_stepsize, int):
            self._raise_type_exception("_time_stepsize", "int")
        if self._time_stepunit is not None and not isinstance(self._time_stepunit, str):
            self._raise_type_exception("_time_stepunit", "str")
        if self.self._threshold_perc is not None and not isinstance(self._threshold_perc, str):
            self._raise_type_exception("self._threshold_perc", "str")
        if self._threshold_value is not None and not isinstance(self._threshold_value, float):
            self._raise_type_exception("self._threshold_value", "float")


