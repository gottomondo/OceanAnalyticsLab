# Mockup SSI method

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


2. Generate the WEkEO api key using the command (NOT IMPLEMENTED:

` python wekeo_api_key.py wekeo_username wekeo_password`

then put your key in hdaKey param [daccess.py](./download/daccess.py)

##### Attention: by default the system use bluecloud proxy to request the token to access to hda, if you put your hda key the proxy will be disabled

3. (Optional) you can change dirID in  [daccess.py](./download/daccess.py) if you want
to download your dataset from StorageHub


### Run the algorithm
The SSI method supports three different output types:ssi_percentile, ssi_percentile_min (default), ssi_fixed 
And produces the following output:
-**SSIoutput.nc**: calculated SSI grid data in NetCDF format
-**SSImaps.png**: map plots  of the calculated SSI grid data
-**SSIseries.png**: timeseries plot of the total SSI grid data area 


To launch the tools simply run the command:

- `python SSI.py "{ 'data_source': ['C3S_ERA5_MEDSEA_1979_2020_STHUB'], 'working_domain': { 'box': [[-6, 36.0, 32.0, 44.0]] }, 'start_time': '1990-01-01', 'end_time': '2019-12-31' }"`-> download from StorageHub 

or

- `python SSI.py "{ 'id_output_type': 'ssi_percentile_min', 'data_source': ['C3S_ERA5_MEDSEA_1979_2020_STHUB'], 'working_domain': { 'box': [[-6, 36.0, 32.0, 44.0]] }, 'start_time': '1990-01-01', 'end_time': '2019-12-31', 'title': 'Annual_SSI_Med_Sea_1990_2020' , 'time_stepsize' : 1, 'time_stepunit': 'Years', 'threshold_perc': 'P98', 'threshold_value' : 15.0  }"` -> download from StorageHub
