#! /usr/bin/env python

import plot.lib.netcdf as nclib
import plot.lib.util as utillib
from netCDF4 import Dataset
from plot.map import template
import numpy as np


def find_diff_mask_level(var1, var2):
    """
    This functions finds the index of points where var1 mask differs from var2 mask

    Args:
        var1: netCDF variable of file1
        var2: netCDF variable of file2

    Returns:
        ndarray: matrix of indexes that indicates the points where the two mask differ
    """
    diff_mask = var1.mask ^ var2.mask
    index_diff_mask = np.where(diff_mask == True)
    if len(index_diff_mask) == 0:
        return None
    if len(index_diff_mask) == 4:
        print("number of different points :", len(index_diff_mask[0]))
        print("coordinate of the firtst different point :", index_diff_mask[0][0], index_diff_mask[1][0],
              index_diff_mask[2][0], index_diff_mask[3][0])
        print("Value of field1: ",
              var1.mask[index_diff_mask[0][0], index_diff_mask[1][0], index_diff_mask[2][0], index_diff_mask[3][0]])
        print("Value of field2: ",
              var2.mask[index_diff_mask[0][0], index_diff_mask[1][0], index_diff_mask[2][0], index_diff_mask[3][0]])
        diff_mask_level = index_diff_mask[1][0]
    elif len(index_diff_mask) == 4:
        print("number of different points :", len(index_diff_mask[0]))
        print("coordinate of the firtst different point :", index_diff_mask[0][0], index_diff_mask[1][0],
              index_diff_mask[2][0])
        print("Value of field1: ",
              var1.mask[index_diff_mask[0][0], index_diff_mask[1][0], index_diff_mask[2][0]])
        print("Value of field2: ",
              var2.mask[index_diff_mask[0][0], index_diff_mask[1][0], index_diff_mask[2][0]])
        diff_mask_level = index_diff_mask[0][0]
    else:
        raise Exception("Dimension different of 4 or 3 not supported")

    return index_diff_mask


def check_dim_var(lonf1, latf1, depf1, timf1,
                  lonf2, latf2, depf2, timf2):
    """
    This function check if dimensional variables are equals, if not it raise an exceptions

    Args:
        lonf1: longitude of first file
        latf1: latitude of first file
        depf1: depth of first file
        timf1: time of first file
        lonf2: longitude of second file
        latf2: latitude of second file
        depf2: depth of second file
        timf2: time of second file

    Returns:
        Raise an exception with an error message if some variables are different

    """
    diff_vars = list()  # list where appen the different variables

    if (lonf1 != lonf2).any():
        diff_vars.append('longitude')
    if (latf1 != latf2).any():
        diff_vars.append('latitude')
    if (depf1 != depf2).any():
        diff_vars.append('depth')
    if (timf1 != timf2).any():
        diff_vars.append('time')

    # build an error message with all different variables
    if len(diff_vars) > 0:
        err_msg = "Variable/s: "
        print("Variable/s: ")
        for v in diff_vars:
            err_msg = err_msg + v + ", "
        err_msg += " are differ"
        raise Exception(err_msg)


def diff_plot(inputFile, inputFile2, var, depthLevel, title, tDescr, lonLat, outFileName, mapLevels, diffMask=False,
              diffForce=False, clbLim=None):
    """
    This function compute the diff for variable computed as: field = inputFile2.variable - inputFile.variable,
    then call the plot function for the new field variable

    Args:
        inputFile: first netCDF file path
        inputFile2: second netCDF file path
        var: variable to plot
        depthLevel: depth level of var
        title: if not None this will be the figure title
        tDescr: figure title extension if title is None
        lonLat: the coordinates of the map to plot
        outFileName: if not None this will be the output file name
        mapLevels: number of color to use in the colorbar
        diffMask (bool): enable plotting mask difference instead of var difference
        diffForce (bool): use this option if ground values are equal to 0 (not masked) and there are some 0 values also in a variable
        clbLim (str): the range limit of colorbar
    """
    ncDataset1 = Dataset(inputFile, mode='r')
    ncDataset2 = Dataset(inputFile2, mode='r')

    ncLon1, ncLat1, ncLonIndex1, ncLatIndex1, ncDepth1, ncTime1 = nclib.read_dim_var(ncDataset1, lonLat, depthLevel)
    ncLon2, ncLat2, ncLonIndex2, ncLatIndex2, ncDepth2, ncTime2 = nclib.read_dim_var(ncDataset2, lonLat, depthLevel)

    # check_dim_var(lonf1, latf1, depf1, timf1,
    #             lonf2, latf2, depf2, timf2)

    if diffMask:
        index_diff_mask = find_diff_mask_level(ncDataset1.variables[var][:], ncDataset2.variables[var][:])
        if index_diff_mask is not None and depthLevel not in index_diff_mask[1]:
            print('\n\nWARNING: In the selected depth level there is no mask difference..\n\n')

    ncVar1, ncVarUnit1 = nclib.read_var(ncDataset1, var, depthLevel, ncLonIndex1, ncLatIndex1)
    ncVar2, ncVarUnit2 = nclib.read_var(ncDataset2, var, depthLevel, ncLonIndex2, ncLatIndex2)

    if ncVarUnit1 is not ncVarUnit2:
        "Can't compare variable with different units"

    ncDataset1.close(), ncDataset2.close()

    ncField1 = nclib.get_map_field(ncVar1, depthLevel)
    ncField2 = nclib.get_map_field(ncVar2, depthLevel)

    if diffForce:
        sentinel_value = 10000
        # using sentinel_value a point that is masked only in a file can be subtract (counting 0)
        ncField1 = np.array(ncField1.filled(fill_value=sentinel_value))
        ncField2 = np.array(ncField2.filled(fill_value=-sentinel_value))

    if diffMask:
        ncField = ncField2.mask.astype(int) - ncField1.mask.astype(int)
    else:
        ncField = ncField2 - ncField1

    if np.ma.max(ncField) == 0 and np.ma.min(ncField) == 0:
        ncField = np.ma.masked_values(ncField, 0)

    if diffForce:
        # now all originally masked values are set to -2*sentinel
        ncField = np.ma.masked_values(ncField, -2 * sentinel_value)  # restore original masked values

        maxDiff = ncField.max()
        minDiff = ncField.min()
        # If masked values or zero values are in inputFile2
        if maxDiff > sentinel_value - sentinel_value / 10:  # this should be never satisfied
            ncField = ncField - sentinel_value
            ncField[ncField == -sentinel_value] = 0
        # If masked values or zero values are in inputFile
        elif minDiff < -sentinel_value + sentinel_value / 10:
            ncField[ncField < -sentinel_value + sentinel_value / 10] += sentinel_value
            ncField[ncField == sentinel_value] = 0

    if title is None:
        if diffMask:
            if tDescr is None:
                tDescr = 'mask diff'
            else:
                tDescr += ', mask diff'
        title = utillib.get_map_title(var, ncDepth1, tDescr, diff=True)
    if outFileName is None:
        outFileName = utillib.get_out_name(var, tDescr, level=depthLevel)

    mapPlot = template.MapPlot(diff=True,
                               cmap='bwr',
                               mapLevels=mapLevels)
    mapPlot.plot(ncLon1, ncLat1, ncField, title, outFileName, lonLat, clbLim=clbLim)
