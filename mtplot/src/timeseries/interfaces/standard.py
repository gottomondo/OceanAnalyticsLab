#! /usr/bin/env python

from netCDF4 import Dataset

import mtplot.lib.netcdf as nclib
import mtplot.lib.util as utillib
from mtplot.src.timeseries import template


def standard_plot(inputFile, var, title, tDescr, xTicksMax, outFileName, freq, lr=False, yLim=None, subtitle=None):
    """
    This function reads from file the variable indicated, then call the function
    in order to generate a standard timeseries src

    Args:
        yLim:
        inputFile: netCDF file path
        var: variable to src
        title: if not None this will be the figure title
        tDescr: figure title extension if title is None
        xTicksMax: number of thick on x axis
        outFileName: if not None this will be the output file name
        freq: data frequency ( monthly, annual, ...)
        lr: Enable Linear Regression on timeseries src

    """

    ncDataset = Dataset(inputFile, mode='r')

    ncTime = nclib.read_time_var(ncDataset)
    ncDepthBnds = ncDataset.variables['depth_bnds'][:].compressed() if 'depth_bnds' in ncDataset.variables else None
    ncVar = ncDataset.variables[var][:].compressed()
    ncVarUnits = ncDataset.variables[var].units
    ncVarLongName = ncDataset.variables[var].long_name.lower() if hasattr(ncDataset.variables[var], 'long_name') else None

    ncDataset.close()

    varField = nclib.get_ts_field(ncVar)
    depthField = nclib.get_ts_field(ncDepthBnds) if ncDepthBnds is not None else None

    if freq is None:
        freq = utillib.get_times_freq(ncTime, ncVarLongName)
    timeSeriesPlot = template.TimeSeriesPlot(ncTime, xTicksMax, freq, yLabel=ncVarUnits, yLim=yLim)
    plotDates = timeSeriesPlot.get_plot_dates()

    # Applying default title if not passed as arg
    if title is None:
        title = utillib.get_ts_title(var, plotDates, tDescr, depthField, freq=freq)

    # Applying default output file name if not passed as arg
    if outFileName is None:
        outFileName = utillib.get_out_name(var, tDescr, depth_field=depthField)

    timeSeriesPlot.plot(varField, title, outFileName, linearRegression=lr, subtitle=subtitle)
