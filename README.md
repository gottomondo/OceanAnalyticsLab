# Mockup method

This is a simple tools to deploy a working method on D4Science.
In this method the first  prototype version of *daccess* module is released.
With this module it is possible to download netCDF files from WEkEO and StorageHub.

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

3. (Optional) you can change dirID in  [daccess.py](./download/daccess.py) if you want
to download your dataset from StorageHub


### Run the algorithm
The mockup method supports two different output type:

- **mockup_download**: download a netCDF file and produce a plot (with some data source)
- **mockup_input_read**: print the input parameters send as input
- 
To launch the tools simply run the command:


- `python mockup.py "{ 'id_output_type': 'mockup_download', 'id_field': 'sea_water_potential_temperature', 'data_source': ['MEDSEA_MULTIYEAR_PHY_006_004'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1987-01', 'end_time': '1987-01' }"` -> download from WEkEO

- `python mockup.py "{ 'id_output_type': 'mockup_download', 'id_field': 'sea_water_potential_temperature', 'data_source': ['MEDSEA_MULTIYEAR_PHY_006_004_STHUB'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1987-01', 'end_time': '1987-01' }"` -> download from StorageHub

- `python mockup.py "{ 'id_output_type': 'mockup_download', 'id_field': 'mass_concentration_of_chlorophyll_a_in_sea_water', 'data_source': ['OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041'], 'working_domain': {'box': [[-6,30.15625,36.28125,45.96875]], 'depth_layers': [[1.472102,5334.648]]}, 'start_time': '2020-07', 'end_time': '2020-07'}"` -> download from WEkEO

- `python mockup.py "{ 'id_output_type': 'mockup_download', 'id_field': 'wind_speed', 'data_source': ['C3S_ERA5_MEDSEA_1979_2020_STHUB'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1979-01-01', 'end_time': '2021-01-31' }"` -> download from StorageHub (plot is not produced)

or

- `python mockup.py "{ 'id_output_type': 'mockup_input_read', 'id_field': 'sea_water_potential_temperature', 'data_source': ['MEDSEA_MULTIYEAR_PHY_006_004'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1987-01', 'end_time': '1987-01' }"` -> download from WEkEO

- `python mockup.py "{ 'id_output_type': 'mockup_input_read', 'id_field': 'sea_water_potential_temperature', 'data_source': ['MEDSEA_MULTIYEAR_PHY_006_004_STHUB'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1987-01', 'end_time': '1987-01' }"` -> download from StorageHub

- `python mockup.py "{ 'id_output_type': 'mockup_input_read', 'id_field': 'mass_concentration_of_chlorophyll_a_in_sea_water', 'data_source': ['OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041'], 'working_domain': {'box': [[-6,30.15625,36.28125,45.96875]], 'depth_layers': [[1.472102,5334.648]]}, 'start_time': '2020-07', 'end_time': '2020-07'}"` -> download from WEkEO

- `python mockup.py "{ 'id_output_type': 'mockup_input_read', 'id_field': 'wind_speed', 'data_source': ['C3S_ERA5_MEDSEA_1979_2020_STHUB'], 'working_domain': { 'box': [[-6, 30.15625, 36.28125, 45.96875]], 'depth_layers': [[1.472102, 5334.648]] }, 'start_time': '1979-01-01', 'end_time': '2021-01-31' }"` -> download from StorageHub (plot is not produced)
