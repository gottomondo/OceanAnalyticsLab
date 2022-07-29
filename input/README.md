# Input Parameters module

This module take in charge to read the input parameter string, extract the information and store it in a python class object.
It provides also some useful function to perform a (basic) validation on the input string.

In the current implementation, it is mandatory that each method must have associated at least a data source and an output type. 
This requirement implies that data_sources and id_output_type are mandatory attributes for any implemented method.

## Input Parameters string
A method receives always a json like string like the following one:


`{ 'arg1': 'value2', 'arg2': int1, 'arg2': ['v1', 'v2'] }`

It is called json-like because it uses the single quote **'** instead of the double quotes **"**.

Why single quotes?
The use of the single quotes, is a temporary implementation choice due to the fact that WPS (or dataminer?) encapsulates the string sent by the web app between the double quotes.
If we maintain in our string the double quotes, to avoid breaking the string, we should add the escape symbol (\) when a double quote occurs. All these escape symbols would make the string syntax too heavy, making it very difficult to read.

Example:

`"{ \"arg1\": \"value2\", \"arg2\": int1, \"arg2\": [\"v1\", \"v2\"] }"`

Already with this small example it is possible to see how the string is less readable respect the original one 

Then, the use of single quotes allows us to maintain a clear syntax.
Will be the python module in charge to substitute all single quotes with the double ones to convert the json-like string to a json string.

### Input Parameters Type
As seen in the previous section, the input parameters string is basically a json string that uses the single quote instead of the double quotes.
This allows us to use all the types defined in the json standard (see https://www.json.org/json-en.html for more details).

Actually, the input module supports the following types:

- string
- int
- array
- object
- bool

## iparameter.py

The class iparameter.py should be seen as a super class which contains a set of parameters that can be common between all methods: 

- **data_source**
- **id_output_type**
- **id_field**
- **working_domain**
- **start_time**
- **end_time**
- **year**
- **month**

*year and month attributes are used to provide a better user experience when selecting a time range from the web app 

Then, it provides some useful function:

- Convert json-like string to json string filtering all None values
- Validate the type of input parameter
- Validate the syntax of some complex parameter like working domain

The access to the input argument in a method should be always done using this class.

## Specialization

As specified in the previous paragraph, iparameter.py should be considered as a super class which contains all the basic parameter needed by a method.
In general a method should need additional parameters, closely related to the method itself.
For a correct implementation, each method should extend the iparameter class, adding its specific parameter and the related validation.

Example:

```python
from input.iparameters import InputParameters


class OceanClimateIParameter(InputParameters):
    def __init__(self, input_parameters_string: str):
        super().__init__(input_parameters_string)  # read all common parameter
        self._parallel = self._extract_optional_attribute("parallel", False)
    
    def get_parallel_flag(self):
        return self._parallel

    def _validate_ocean_climate_input_parameters(self):
        """
        Validate the typeof each parameter of Ocean Climate method
        Returns: raise an exception if there is an input parameter with a wrong type

        """
        if not isinstance(self._parallel, str):
            self._raise_type_exception("_id_field", "bool")

```
