#! /usr/bin/env python

from netCDF4 import Dataset

import mtplot.lib.netcdf as nclib
import mtplot.lib.util as utillib
from mtplot.src.timeseries import template


def diff_plot(inputFile1, inputFile2, var, title, tDescr, xTicksMax, outFileName, freq, yLim=None):
    """
    This function compute the diff for variable computed as: field = inputFile2.variable - inputFile1.variable,
    then call the src function for the new field variable

    Args:
        inputFile1: first netCDF file path
        inputFile2: second netCDF file path
        var: variable to src
        title: if not None this will be the figure title
        tDescr: figure title extension if title is None
        xTicksMax: number of thick on x axis
        outFileName: if not None this will be the output file name
        freq: data frequency ( monthly, annual, ...)

    """

    ncDataset1 = Dataset(inputFile1, mode='r')
    ncDataset2 = Dataset(inputFile2, mode='r')

    ncTime = nclib.read_time_var(ncDataset1)
    depthBnds = ncDataset1.variables['depth_bnds'][:].compressed if 'depth_bnds' in ncDataset1.variables else None
    ncVar1 = ncDataset1.variables[var][:]
    ncVar2 = ncDataset2.variables[var][:]
    ncVarUnits = ncDataset1.variables[var].units
    ncVarLongName = ncDataset1.variables[var].long_name.lower() if hasattr(ncDataset1.variables[var], 'long_name') else None

    ncDataset1.close()
    ncDataset2.close()

    varField1 = nclib.get_ts_field(ncVar1)
    varField2 = nclib.get_ts_field(ncVar2)
    varField = varField2 - varField1
    depthField = nclib.get_ts_field(depthBnds) if depthBnds is not None else None

    if freq is None:
        freq = utillib.get_times_freq(ncTime, ncVarLongName)
    timeSeriesPlot = template.TimeSeriesPlot(ncTime, xTicksMax, freq, diff=True, yLabel=ncVarUnits, yLim=yLim)
    plotDates = timeSeriesPlot.get_plot_dates()

    # Applying default title if not passed as arg
    if title is None:
        title = utillib.get_ts_title(var, plotDates, tDescr, depthField, diff=True, freq=freq)

    # Applying default output file name if not passed as arg
    if outFileName is None:
        outFileName = utillib.get_out_name(var, tDescr, depth_field=depthField)

    timeSeriesPlot.plot(varField, title, outFileName)
