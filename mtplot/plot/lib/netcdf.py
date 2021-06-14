import datetime

import numpy as np

from plot.lib.time import get_date_from_timedelta
from netCDF4 import Dataset

ts_tuple = (1,)
name_dict = {
    # Var name : Title name, File name
    'thetao': ['Potential Temperature', 'potential_temperature'],
    'votemper': ['Potential Temperature', 'potential_temperature'],
    'vosaline': ['Salinity', 'salinity'],
    'sossheig': ['Sea Surface Height', 'ssh'],
    'vodnsity_tmp': ['Sea Water Density', 'density'],
    'so': ['Salinity', 'salinity'],
}


def get_clim_timerange(ncDataset):
    """
    Reading the climatology_bnds var to obtain the time range of climatology

    Args:
        ncDataset(Dataset): netCDF dataset

    Returns:
        string: time range in string format
    """
    ncRefTime = ncDataset.variables['climatology_bnds'].units
    ncClimBnds = ncDataset.variables['climatology_bnds'][:].compressed()
    startClim = get_date_from_timedelta(ncClimBnds[0], ncRefTime)
    endClim = get_date_from_timedelta(ncClimBnds[-1], ncRefTime) - datetime.timedelta(days=1)
    return startClim.strftime("%d-%m-%Y") + " - " + endClim.strftime("%d-%m-%Y")


def get_map_field(nc_variable, depthLevel):
    """
    This function masks all value equal to 0 ( the land in standard plot
    and land + area with no error in diff plot ) if the file isn't masked,
    then extract the selected depth level of variable if more then one is present

    Args:
        nc_variable: input variable
        depthLevel (int): depth level to extract

    Returns:
        ndarray: a matrix ready to be plotted on a map

    """
    nc_var = nc_variable
    if not np.ma.is_masked(nc_var):
        print('Variable not masked, applying mask to 0 values...')
        nc_var[nc_var == 0] = np.ma.masked
    if len(nc_var.shape) == 4:
        out_field = np.squeeze(nc_var[0, depthLevel, :, :])
    else:
        out_field = np.squeeze(nc_var[0, :, :])
    return out_field


def read_dim_var(nc_dataset, lonLat=None, depthLevel=None):
    """
    This function reads the dimensional variables from netcdf dataset.
    Both 2d and 3d variables are supported.
    In case of 2d variables, lon and lat must be converted to matrix.

    Args:
        nc_dataset: input netcdf dataset
        lonLat (list): the coordinates of the map to plot
        depthLevel (int): depth level of var to read

    Returns:
        longitude, latitude, depth, time

    """
    ncVars = nc_dataset.variables

    if 'nav_lon' in ncVars:
        ncLon, ncLonBnds = read_lon_lat(nc_dataset.variables, 'longitude', twod_name='nav_lon')
    elif 'lon' in ncVars:
        ncLon, ncLonBnds = read_lon_lat(nc_dataset.variables, 'longitude', oned_name='lon')
    else:
        raise Exception("No longitude found")

    if 'nav_lat' in ncVars:
        ncLat, LatBnds = read_lon_lat(nc_dataset.variables, 'latitude', twod_name='nav_lat')
    elif 'lat' in ncVars:
        ncLat, LatBnds = read_lon_lat(nc_dataset.variables, 'latitude', oned_name='lat')
    else:
        raise Exception("No latitude found")

    if lonLat is not None:
        ncLonIndex = find_index(ncLonBnds, lonLat[0], lonLat[1])
        ncLonBnds = ncLonBnds[ncLonIndex[0]:ncLonIndex[1], :]
    else:
        ncLonIndex = (0, ncLon.size)
    lonCells = np.zeros(ncLonBnds[:, 0].size)
    lonCells[0:] = ncLonBnds[:, 0]

    if lonLat is not None:
        ncLatIndex = find_index(LatBnds, lonLat[2], lonLat[3])
        LatBnds = LatBnds[ncLatIndex[0]:ncLatIndex[1], :]
    else:
        ncLatIndex = (0, ncLat.size)
    latCells = np.zeros(LatBnds[:, 0].size)
    latCells[0:] = LatBnds[:, 0]

    ncDepth = ncVars['deptht'][:] if 'deptht' in ncVars else ncVars['depth'][:] if 'depth' in ncVars else None
    if ncDepth is not None:
        ncDepth = ncDepth.compressed()[depthLevel]
        ncDepth = round(ncDepth)
    ncTime = ncVars['time_counter'][:] if 'time_counter' in ncVars else ncVars['time']

    if len(lonCells.shape) == 1 and len(latCells.shape) == 1:  # in case lon, lat are array and not matrix
        lonCells, latCells = np.meshgrid(lonCells, latCells)

    return lonCells, latCells, ncLonIndex, ncLatIndex, ncDepth, ncTime,


def find_index(Bnds, Min, Max):
    """
    This function finds the min and max index in the array if the
    selected domain is lower than netCDF domain.
    If the desired domain is greater than netCDF domain, all domain
    will be selected

    Args:
        Bnds (list): netCDF domain
        Min (int): min value desired
        Max (int): max value desired

    Returns:
        int: the index of the min and max

    """
    import sys

    iMin = 0
    if Min < Bnds[0, 0]:
        print('WARNING : Lon min chosen is out of range, the lowest value supported will be selected...".',
              file=sys.stderr)
    if Min > Bnds[0, 0]:
        iMin = 0
        for i in range(0, Bnds[:, 0].size):
            # print Bnds[i,0],Min,Bnds[i,1]
            if Bnds[i, 0] <= Min < Bnds[i, 1]:
                iMin = i
                break
    if Max > Bnds[-1, 1]:
        iMax = Bnds.shape[0]
        print('WARNING : Lat min chosen is out of range, the highest value supported will be selected...".',
              file=sys.stderr)
    else:
        for i in range(iMin, Bnds[:, 0].size):
            if Bnds[i, 0] < Max <= Bnds[i, 1]:
                iMax = i + 1
                break
    return iMin, iMax


def read_lon_lat(ncVars, stdName, oned_name=None, twod_name=None):
    """
    This functions reads from netCDF variable the lon and lat variables.
    It supports both 1d and 2d cases

    Args:
        ncVars: netCDF variables
        stdName (str): var standard name
        oned_name: 1-dim name
        twod_name: 2-dim name

    Returns:
        ndarray: the extracted var from ncVars with the boundaries

    """
    import numpy
    import sys
    if oned_name is not None:
        if ncVars[oned_name].standard_name == stdName:
            MyDatasetDim = ncVars[oned_name]
            if 'bounds' in MyDatasetDim.ncattrs():
                MyDatasetDimBnds = ncVars[ncVars[oned_name].bounds]
            else:
                MyDatasetDimBnds = dim_bnds(MyDatasetDim)
                print('WARNING : auto-generating ' + stdName + ' boundaries', file=sys.stderr)
            print("INFO reading " + stdName, file=sys.stderr)
            return MyDatasetDim, MyDatasetDimBnds
        else:
            return None
    elif twod_name is not None:
        if ncVars[twod_name].standard_name == stdName:
            if twod_name.find("lat") >= 0:
                MyDatasetDim = ncVars[twod_name][:, 0]
            elif twod_name.find("lon") >= 0:
                for myx in range(ncVars[twod_name].shape[0]):
                    MyDatasetDim = ncVars[twod_name][myx, :]
                    if numpy.count_nonzero(MyDatasetDim) == ncVars[twod_name].shape[1]:
                        break
            MyDatasetDimBnds = dim_bnds(MyDatasetDim)
            print('WARNING : auto-generating ' + stdName + ' boundaries', file=sys.stderr)
            return MyDatasetDim, MyDatasetDimBnds


def dim_bnds(Dim):
    import numpy
    DimDelta = Dim[1] - Dim[0]
    Bnds = numpy.zeros((Dim[:].size, 2))
    Bnds[:, 0] = Dim[:] - DimDelta / 2
    Bnds[0:Bnds[:, 0].size - 1, 1] = Bnds[1:Bnds[:, 0].size, 0]
    Bnds[-1, 1] = Dim[-1] + DimDelta / 2
    return Bnds


def read_var(ncDataset, varName, depthLevel, ncLonIndex, ncLatIndex):
    """
    This function reads a variable from a netcdf dataset with its unit measure.
    Only the domain indicated by ncLonIndex and ncLatIndex will be extracted

    Args:
        ncDataset: input netcdf dataset
        varName (str): variable to be read
        depthLevel (int): depth level of var to read
        ncLonIndex (list): indexes of min and max value of interval to extract
        ncLatIndex (list): indexes of min and max value of interval to extract

    Returns:
        the netCDF variable with its unit measure

    """
    nc_var = ncDataset.variables[varName]

    if ncDataset.variables[varName].ndim == 4:
        tmp_var = nc_var[:, depthLevel, ncLatIndex[0]:ncLatIndex[1], ncLonIndex[0]:ncLonIndex[1]]
    else:
        tmp_var = nc_var[:, ncLatIndex[0]:ncLatIndex[1], ncLonIndex[0]:ncLonIndex[1]]

    try:
        mp_var_unit = nc_var.units
    except:
        mp_var_unit = None
    return tmp_var, mp_var_unit


def get_ts_field(nc_variable):
    """
    This function removes unnecessary dimensions

    Args:
        nc_variable: netCDF variable

    Returns:
        ndarray: a variable without unnecessary array dimensions

    """
    nc_var = nc_variable
    out_field = np.squeeze(nc_var)
    return out_field


def read_time_var(nc_dataset):
    """
    This functions extracts the date variable from nc_dataset if present and convert it
    to a datetime object using the time units attribute

    Args:
        nc_dataset (Dataset): netCDF dataset

    Returns:
        datetime: the netCDF time variable if it is presents

    """
    nc_vars = nc_dataset.variables
    timf = list()

    temp_timf = nc_vars['time'][:] if 'time' in nc_vars else None
    RefTimeUnits = nc_vars['time'].units if 'time' in nc_vars else None

    for t in temp_timf:
        timf.append(get_date_from_timedelta(t, RefTimeUnits))

    return timf


def get_plot_type(inputFile):
    ncDataset = Dataset(inputFile, mode='r')
    ncVars = ncDataset.variables
    if 'lat' in ncVars:
        ncLat = ncVars['lat']
    elif 'nav_lat' in ncVars:
        ncLat = ncVars['nav_lat']
    else:
        raise Exception("Can't find latitude in input file")

    ts = ncLat.shape == ts_tuple
    map = not ts
    return ts, map
