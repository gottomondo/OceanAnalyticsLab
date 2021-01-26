# Mockup method

This is a simple tools to deploy a working method on D4Science.
This method simply download a netCDF file from D4science workspace and return it as output.nc


## Instruction

To launch the tools simpy run the command:

`python mockup.py $dirID`

where **dirID** is the id of the d4science directory from which you want to download the file.
You can find the id simply by right-clicking on a directory in the workspace and selecting **info**


#### Note
To run this tools locally, it is sufficient to run  [get_variables.sh](./get_globalvariables.sh) passing as 
argument the user token (you can find it when log into D4Science):

`./get_variables.sh $TOKEN`

A file named **globalvariables.csv** will be created and used to download the file correctly.
##### Attention: do not upload this file when upload the method, it will be created at runtime by dataminer itself
