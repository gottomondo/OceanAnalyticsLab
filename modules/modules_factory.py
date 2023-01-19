from input.iparameters import InputParameters
from modules import retrieve_file, prod_ocean_climate, plot
from log.logmng import LogMng


class ModulesFactory:
    def __init__(self, json_log: LogMng, input_parameters: InputParameters):
        self._json_log = json_log
        self._input_parameters = input_parameters

    def get_module(self, phase_name: str):
        if phase_name == "plot":
            error_code = 5
            phase = plot.Plot(input_parameters=self._input_parameters,
                              json_log=self._json_log,
                              error_code=error_code)
        elif phase_name == "prod":
            error_code = 4
            phase = prod_ocean_climate.OceanClimateMockup(input_parameters=self._input_parameters,
                                                          json_log=self._json_log,
                                                          error_code=error_code)
        elif phase_name == "retrieve_file":
            error_code = 7
            phase = retrieve_file.Download(input_parameters=self._input_parameters,
                                           json_log=self._json_log,
                                           error_code=error_code)
        else:
            raise Exception("ERROR: Selected phase is unknown: " + phase_name)

        return phase
