#! /usr/bin/env python

import numpy as np

import plot.lib.netcdf as nclib
import plot.lib.util as utillib
from netCDF4 import Dataset
from plot.map import template


def get_current_component(ncVar, depthLevel, qd):
    """
    This functions get a curr component from netCDF file and remove from it
    the unnecessary dimensions and set some points to nan in according to qd value.
    In this way there won't be too many quivers to plot in the map

    Args:
        ncVar: current component
        depthLevel: depth level of ncVar
        qd: the distance in terms of 'ncVar matrix points' between the quivers

    Returns:
        ndarray: a sparse matrix from ncVar
    """
    x = nclib.get_map_field(ncVar, depthLevel)
    x = np.array(x.filled(fill_value=np.nan))
    x = get_sparse_matrix(x, qd)  # reduce values in matrix
    return x


def get_sparse_matrix(m, qd):
    """
    This functions sets to nan all value in the matrix where i or j are not multiple of qd

    Args:
        m: matrix i x j
        qd: the distance in terms of 'ncVar matrix points' between the quivers

    Returns:
        ndarray: a sparse m matrix

    """
    for i in range(0, m.shape[0]):
        for j in range(0, m.shape[1]):
            if i % qd != 0:
                m[i][j] = np.nan
            elif j % qd == 0:
                continue
            else:
                m[i][j] = np.nan
    return m


def get_current(cur_u, cur_v):
    """
    This function computes the current module from its u and v component as: curr = sqrt(u^2 + v^2)

    Args:
        cur_u: u curr component
        cur_v: v corr component

    Returns:
        ndarray: current module

    """
    currents = np.ma.empty_like(cur_u)

    for t in range(0, cur_u.shape[0]):
        for d in range(0, cur_u.shape[1]):
            currents[t, d, ...] = np.ma.sqrt(
                np.ma.power(cur_u[t, d, ...], 2) +
                np.ma.power(cur_v[t, d, ...], 2))
    return currents


def currents_plot(inputFile, inputFile2, var, var2, depthLevel, title,
                  tDescr, lonLat, outFileName, mapLevels, qd, grid, qScale, qWidth, clbLim=None):
    """
    This function setting up the current variable to plot

    Args:
        inputFile: netCDF file path
        inputFile2: second netCDF file path
        var: u current component
        var2: v current component
        depthLevel (int): depth level of var
        title (str): if not None this will be the figure title
        tDescr (str): figure title extension if title is None
        lonLat (list): the coordinates of the map to plot
        outFileName (str): if not None this will be the output file name
        mapLevels (int): number of color to use in the colorbar
        qd (int): the distance in terms of var matrix points between the quivers
        grid (int): grid dimension of map meridians and parallels
        qScale (int): the longer the value the lower the quivers are
        qWidth (int): the quivers width
        clbLim (str): the range limit of colorbar

    """
    ncDataset = Dataset(inputFile, mode='r')
    if inputFile2 is not None:
        ncDataset2 = Dataset(inputFile2, mode='r')
    else:
        ncDataset2 = ncDataset

    ncLon, ncLat, ncLonIndex, ncLatIndex, ncDepth, ncTime = nclib.read_dim_var(ncDataset, lonLat, depthLevel)
    ncVar1, ncVarUnit1 = nclib.read_var(ncDataset, var, depthLevel, ncLonIndex, ncLatIndex)
    ncVar2, ncVarUnit2 = nclib.read_var(ncDataset2, var2, depthLevel, ncLonIndex, ncLatIndex)

    currents = get_current(ncVar1, ncVar2)
    currents = nclib.get_map_field(currents, depthLevel)
    u = get_current_component(ncVar1, depthLevel, qd)
    v = get_current_component(ncVar2, depthLevel, qd)
    ncDataset.close()

    if title is None:
        title = utillib.get_map_title(var, ncDepth, tDescr, curr=True)
    if outFileName is None:
        outFileName = utillib.get_out_name(var, tDescr, level=depthLevel)

    mapPlot = template.MapPlot(curr=True,
                               grid=grid,
                               mapLevels=mapLevels,
                               qScale=qScale,
                               qWidth=qWidth,
                               cmap='Blues')
    mapPlot.plot(ncLon, ncLat, currents, title, outFileName, lonLat, curr_u=u, curr_v=v, clbLim=clbLim)
