#!/usr/bin/env python
import traceback
from datetime import date
from input.iparameters import InputParameters
from input import working_domain as wd
from log.logmng import LogMng

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

    def update_title(self, new_title):
        self._title = new_title
    
    def get_time_stepsize(self):
        return self._time_stepsize

    def update_time_stepsize(self, new_time_stepsize):
        self._time_stepsize = new_time_stepsize
    
    def get_time_stepunit(self):
        return self._time_stepunit

    def update_time_stepunit(self, new_time_stepunit):
        self._time_stepunit = new_time_stepunit
    
    def get_threshold_perc(self):
        return self._threshold_perc

    def update_threshold_perc(self, new_threshold_perc):
        self._threshold_perc = new_threshold_perc
    
    def get_threshold_value(self):
        return self._threshold_value

    def update_threshold_value(self, new_threshold_value):
        self._threshold_value = new_threshold_value
    
    def _validate_input_SSIparameters(self):
        """
        Validate the typeof each parameter
        Returns: raise an exception if there is an input parameter with a wrong type

        """
        #super()._validate_input_parameters()
        
        if self._title is not None and not isinstance(self._title, str):
            self._raise_type_exception("_title", "str")
        if self._time_stepsize is not None and not isinstance(self._time_stepsize, int):
            self._raise_type_exception("_time_stepsize", "int")
        if self._time_stepunit is not None and not isinstance(self._time_stepunit, str):
            self._raise_type_exception("_time_stepunit", "str")
        if self._threshold_perc is not None and not isinstance(self._threshold_perc, str):
            self._raise_type_exception("self._threshold_perc", "str")
        if self._threshold_value is not None and not isinstance(self._threshold_value, float):
            self._raise_type_exception("self._threshold_value", "float")


def init_input_parametersSSI(input_arguments):
    input_parameters_json_like = input_arguments.input_parameters
    input_parametersSSI_instance = InputParametersSSI(input_parameters_json_like)
    return input_parametersSSI_instance


def validate_input_parametersSSI(input_parameters: InputParametersSSI, json_log: LogMng):

    #Data Source (MANDATORY)
    try:
        if input_parameters.get_data_source() is None:
            raise Exception("No data source specified (mandatory input)")
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
    
    try:
        if input_parameters.get_data_source() != "C3S_ERA5_MEDSEA_1979_2020_STHUB":
            raise Exception("Only data source C3S_ERA5_MEDSEA_1979_2020_STHUB is currently available")
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
    
    #Output type
    try:
        if input_parameters.get_output_type() is None:
            input_parameters.update_output_type('ssi_percentile_min') #default (NOW MANDATORY!!!)
        elif input_parameters.get_output_type() not in {'ssi_percentile', 'ssi_percentile_min', 'ssi_fixed'}:
            raise Exception("Output type '{}' unknown".format(input_parameters.get_output_type()))
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    
        
    #Title
    try:
        if input_parameters.get_title() is None:
            input_parameters.update_title('SSI') #default
        title = input_parameters.get_title()
        forbidden_chars = ' "*\\/\'|?:<>'
        for x in title:
            if x in forbidden_chars:
                raise Exception("Title can not contain %s" % (forbidden_chars))
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)          
                                                               
    #Start time & End time (MANDATORY)
    try:
        if input_parameters.get_start_time() is None:
            raise Exception("No start time specified (mandatory input)")
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
    
    try:
        if input_parameters.get_end_time() is None:
            raise Exception("No end time specified (mandatory input)")
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
    
    starttime = date.fromisoformat(input_parameters.get_start_time())
    endtime = date.fromisoformat(input_parameters.get_end_time())                             
    try:
        if endtime < starttime:
            raise Exception("Illegal end time: End time must be after start time")
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    
        
    #Workdomain = boundingbox (MANDATORY)
    try:
        if input_parameters.get_working_domain() is None:
            raise Exception("No working domain specified (mandatory input)")
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)
    
    workdomain= wd.get_horizontal_domain(input_parameters.get_working_domain())[0]
    try:
        if workdomain[0] > workdomain[1] or workdomain[2] > workdomain[3] :
            raise Exception('Íllegal workdomain (lat/long coordinates horizontal box)')
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    
        
    #Stepsize Time
    if input_parameters.get_time_stepsize() is None:
        input_parameters.update_time_stepsize(1) #default
    stepsize=input_parameters.get_time_stepsize()
    try:
        if stepsize < 1 and stepsize >10:
            raise Exception('Íllegal stepsize (allowed 1 till 10)')
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    

    #Stepsize Unit 
    if input_parameters.get_time_stepunit() is None:
        input_parameters.update_time_stepunit('Years') #default
    allowed_stepunits = {'None':1, 'Days':2, 'Months':3, 'Years':4}
    stepunitstr=input_parameters.get_time_stepunit()
    try:
        if stepunitstr in allowed_stepunits:
            stepunit=allowed_stepunits[stepunitstr]
        else:
            raise Exception('Íllegal stepunit (allowed: None, Days, Months, Years)')
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code) 

    #Windspeed threshold percentile
    if input_parameters.get_threshold_perc() is None:
        input_parameters.update_threshold_perc('P98') #default    
    windspeed_threshold_percentile= input_parameters.get_threshold_perc()
    try:
        if windspeed_threshold_percentile not in {'P90', 'P95', 'P98', 'P99'} :
            raise Exception('Illegal percentile (allowed: P90, P95, P98, P99)')
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code) 

    #Windspeed threshold value    
    if input_parameters.get_threshold_value() is None:
        input_parameters.update_threshold_value(15.0) #default    
    windspeed_threshold_value = input_parameters.get_threshold_value()
    try:
        if windspeed_threshold_value <= 0:
            raise Exception('Illegal value, must be greater than 0')
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code) 

    #Summarize input
    summarize_input_parametersSSI(input_parameters)

    
    
    
def summarize_input_parametersSSI(input_parameters: InputParametersSSI):
    print("\n\nInput arguments SSI method\n")
    inputfile = "indir/" + (input_parameters.get_data_source()).replace("_STHUB", "_WIND.nc")
    pvaluesfile = "indir/" + (input_parameters.get_data_source()).replace("_STHUB", "_WIND_P90959899.nc")
    print("Data Source (inputfile)\t\t:", inputfile)
    print("Data Source (pvaluesfile)\t:", pvaluesfile)
    print("Output Type\t\t\t:", input_parameters.get_output_type())
    print("Title\t\t\t\t:", input_parameters.get_title())   
    print("Start Time\t\t\t:", input_parameters.get_start_time())
    print("End Time\t\t\t:", input_parameters.get_end_time())
    print("Working Domain\t\t\t:", wd.get_horizontal_domain(input_parameters.get_working_domain())[0])
    print("Stepsize Time\t\t\t:", input_parameters.get_time_stepsize())
    print("Stepunit Time\t\t\t:", input_parameters.get_time_stepunit())
    print("Windspeed threshold percentile\t:", input_parameters.get_threshold_perc())
    print("Windspeed threshold value (m/s)\t:", input_parameters.get_threshold_value())
    print("\n\n")

    
