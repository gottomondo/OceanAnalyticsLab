#!/usr/bin/env python
from copy import deepcopy
import json


def get_json_input_parameters(input_parameters_json_like):
    input_parameters_json_format = input_parameters_json_like.replace("'", '"')
    try:
        input_parameters = json.loads(input_parameters_json_format)  # try to read the string as a Json
    except:
        raise Exception("Can't parse input parameters as json string")
    return input_parameters


def clean_raw_param_name(str_to_clean):  # remove the first _ character from a string if it is present
    string_cleaned = str_to_clean.replace('"_', '"')
    return string_cleaned


def get_black_list():
    black_list = list()
    attribute_to_avoid_list = ['_input_parameters_dict']
    for attribute_to_avoid in attribute_to_avoid_list:
        black_list.append(attribute_to_avoid)
    return black_list


def remove_param_in_back_list(input_dict: dict):
    dict_without_blacklist = deepcopy(input_dict)
    black_list = get_black_list()

    for param_to_remove in black_list:
        if param_to_remove in input_dict:
            dict_without_blacklist.pop(param_to_remove)
        else:
            print("Can't remove parameter: {}, it doesn't exists in input_dict".format(param_to_remove))

    return dict_without_blacklist


def remove_none_value(input_dict: dict):
    dict_without_none = deepcopy(input_dict)
    for key, value in input_dict.items():
        if value is None:
            del dict_without_none[key]

    return dict_without_none


def clean_dict(input_dict):
    dict_to_clean = deepcopy(input_dict)
    dict_to_convert_with_none = remove_param_in_back_list(dict_to_clean)
    dict_to_convert = remove_none_value(dict_to_convert_with_none)
    return dict_to_convert


def dict_to_json_str(input_dict: dict):
    json_string = json.dumps(input_dict)
    json_str = clean_raw_param_name(json_string)  # raw param name starts with _
    return json_str


def dict_to_json_like_str(json_str: str):
    json_like_str = json_str.replace('"', "'")
    return json_like_str


class InputParameters:
    def __init__(self, input_parameters_string: str):
        self._input_parameters_dict: dict = get_json_input_parameters(input_parameters_string)
        # A method must have at least 1 data source and 1 output type
        self._id_output_type: str = self._extract_mandatory_attribute('id_output_type')
        self._data_source: list = self._extract_mandatory_attribute('data_source')

        self._working_domain: dict = self._extract_optional_attribute('working_domain')
        self._id_field: str = self._extract_optional_attribute('id_field')
        self._year: str = self._extract_optional_attribute('year')
        self._month: int = self._extract_optional_attribute('month')
        self._start_time: str = self._extract_start_time_from_input_parameters()
        self._end_time: str = self._extract_end_time_from_input_parameters()

        self._validate_wd()
        self._validate_input_parameters()

    def _validate_wd(self):
        if self._working_domain is not None:
            from input import working_domain as wd
            wd.check_working_domain(self._working_domain)

    def _extract_mandatory_attribute(self, name_attribute: str):
        value = self._input_parameters_dict.get(name_attribute, None)
        if value is None:
            raise Exception('Mandatory attribute "' + name_attribute + '" not found in input parameter')
        else:
            return value

    def _extract_optional_attribute(self, name_attribute: str, default=None):
        return self._input_parameters_dict.get(name_attribute, default)

    def _extract_start_time_from_input_parameters(self):
        if self._year is None:
            start_time = self._extract_mandatory_attribute('start_time')
        else:
            start_time = self._input_parameters_dict.get('year')  # is it the case to set 01 as month?
        return start_time

    def _extract_end_time_from_input_parameters(self):
        if self._year is None:
            end_time = self._extract_mandatory_attribute('end_time')
        else:
            end_time = self._input_parameters_dict.get('year')  # is it the case to set 12 as month?
        return end_time

    def get_input_parameters(self):
        return self._input_parameters_dict

    def get_output_type(self):
        return self._id_output_type

    def get_id_field(self):
        return self._id_field

    def get_data_source(self):
        return self._data_source[0]  # the algorithm use always one data source

    def get_working_domain(self):
        return self._working_domain

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_month(self):
        return self._month

    def get_start_end_time_and_month(self):
        return self._start_time, self._end_time, self._month

    def get_time_domain_as_str(self):
        time_domain_str = self._start_time + '_' + self._end_time
        if self._month is not None:
            time_domain_str += '_' + str(self._month).zfill(2)
        return time_domain_str

    def update_month(self, new_month):
        self._month = new_month

    def update_start_time(self, new_start_time):
        self._start_time = new_start_time

    def update_end_time(self, new_end_time):
        self._end_time = new_end_time

    def to_json_str(self):
        dict_to_convert_full = self.__dict__

        dict_to_convert = clean_dict(dict_to_convert_full)  # remove element in black list or elements equal to None
        json_str = dict_to_json_str(dict_to_convert)

        return json_str

    def to_json_like_str(self):
        """
        Create the input_parameters string starting from the class attributes
        Returns: the input_parameters string in json-like format

        """
        json_str = self.to_json_str()
        json_like_str = dict_to_json_like_str(json_str)
        return json_like_str

    def _validate_input_parameters(self):
        """
        Validate the typeof each parameter
        Returns: raise an exception if there is an input parameter with a wrong type

        """
        if not isinstance(self._id_output_type, str):
            self._raise_type_exception("data_source", "list")
        if not isinstance(self._data_source, list):
            self._raise_type_exception("data_source", "list")

        if self._working_domain is not None and not isinstance(self._working_domain, dict):
            self._raise_type_exception("working_domain", "dict")
        if self._id_field is not None and not isinstance(self._id_field, str):
            self._raise_type_exception("_id_field", "str")
        if self._year is not None and not isinstance(self._year, str):
            self._raise_type_exception("_year", "str")
        if self._start_time is not None and not isinstance(self._start_time, str):
            self._raise_type_exception("_start_time", "str")
        if self._end_time is not None and not isinstance(self._end_time, str):
            self._raise_type_exception("_end_time", "str")
        if self._month is not None and not isinstance(self._month, int):
            self._raise_type_exception("month", "int")

    def _raise_type_exception(self, name_var, type_name):
        raise Exception("ERROR Input object: {} is not {}".format(name_var, type_name))
