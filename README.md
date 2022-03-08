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
To launch the tools simpy run the command:


- `python mockup.py MEDSEA_MULTIYEAR_PHY_006_004` -> download from WEkEO

- `python mockup.py MEDSEA_MULTIYEAR_PHY_006_004_STHUB` -> download from StorageHub

- `python OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041` -> download from WEkEO
