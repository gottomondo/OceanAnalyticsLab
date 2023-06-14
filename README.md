# Mockup method

This is a simple tools to deploy a working method on D4Science.
In this method are included some extra modules (which are still in development):

- **download module**: With this module it is possible to download netCDF files from WEkEO and StorageHub.
- **log manager**: With this module it is possible to store some execution info, error info and to provide always the expected output files to WPS protoc also in case of errors
- **input manager**: With this module it is possible to manage the input parameters string


## Instruction

### Preparation

To run this tools locally, follow this steps:

1. run  [get_variables.sh](./get_globalvariables.sh) passing as 
argument the user token (you can find it when log into D4Science):

`./get_variables.sh $TOKEN`

A file named **globalvariables.csv** will be created and used to download the file correctly.
##### Attention: do not upload this file when upload the method, it will be created at runtime by dataminer itself


2. Generate the WEkEO api key using the command:

` python wekeo_api_key.py wekeo_username wekeo_password`

then put your key in hdaKey param [daccess.py](./download/daccess.py)

##### Attention: by default the system use bluecloud proxy to request the token to access to hda, if you put your hda key the proxy will be disabled


3. Setup Virtualenv

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Run the algorithm
This repo contains three different mockups:

- **Ocean Climate Mockup**
- **Storm Severity Index Mockup**
- **Ocean Pattern Mockup**

It is present a unique main which give the possibility to choose wich mockup to exec.

*Be sure that the **indir** directory is not present before starting the tool*

Here the info about mockup execution:

```bash
python mockup.py -h
storagehubpythonfacility/command init
usage: mockup.py [-h] [-o] [-s] [-p] input_parameters

Mockup method

positional arguments:
  input_parameters     JSON-like string (use ' instead of ")

options:
  -h, --help           show this help message and exit
  -o, --ocean_climate  Enable Ocean Climate mockup execution
  -s, --ssi            Enable SSI mockup execution
  -p, --ocean_pattern  Enable Ocean Pattern mockup execution
```

Then with the option arguments -o, -s, -p it is possible to choose a specific mockup.
TO notice that the mockups don't exec some real computation. It depends on the specific mockup, but in general they performs
only a download of the requested files and then simply copy some mockup outputs.

Here some instruction to exec the three mockups:

- Ocean Climate: `python mockup.py "{ 'id_output_type': 'mockup_download', 'id_field': 'sea_water_potential_temperature', 'data_source': ['MEDSEA_MULTIYEAR_PHY_006_004_STHUB'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1987-01', 'end_time': '1987-01' }" -o`

- Storm Severity Index: `python mockup.py "{ 'id_output_type': 'mockup_download', 'id_field': 'mass_concentration_of_chlorophyll_a_in_sea_water', 'data_source': ['OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041'], 'working_domain': {'box': [[-6,30.15625,36.28125,45.96875]], 'depth_layers': [[1.472102,5334.648]]}, 'start_time': '2020-07', 'end_time': '2020-07'}" -s`

- Ocean Pattern: `python mockup.py "{ 'id_output_type':'FIT_PRED', 'id_field':'sea_water_potential_temperature', 'k':6, 'working_domain': {'box': [[-5, 31, 36, 45]], 'depth_layers': [[10,300]]}, 'start_time': '1987-01', 'end_time': '1987-12', 'data_source': ['MEDSEA_MULTIYEAR_PHY_006_004_STHUB'] }" -p`
