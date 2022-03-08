#! /usr/bin/env python

from netCDF4 import Dataset

import mtplot.lib.netcdf as nclib
import mtplot.lib.util as utillib
from mtplot.src.timeseries import template


def climatology_plot(inputFile, var, title, tDescr, xTicksMax, outFileName, yLim=None, subtitle=None):
    """
    This function reads from file the variable indicated, then call the function
    in order to generate a climatology timeseries src, where on x axis there are
    only the month name as label

    Args:
        inputFile: netCDF file path
        var: variable to src
        title: if not None this will be the figure title
        tDescr: figure title extension if title is None
        xTicksMax: number of thick on x axis
        outFileName: if not None this will be the output file name

    """

    ncDataset = Dataset(inputFile, mode='r')

    ncTime = None
    timeRange = nclib.get_clim_timerange(ncDataset)
    ncVar = ncDataset.variables[var][:]
    ncVarUnits = ncDataset.variables[var].units
    ncDepthBnds = ncDataset.variables['depth_bnds'][:] if 'depth_bnds' in ncDataset.variables else None

    ncDataset.close()

    varField = nclib.get_ts_field(ncVar)
    depthField = nclib.get_ts_field(ncDepthBnds) if ncDepthBnds is not None else None

    timeSeriesPlot = template.TimeSeriesPlot(ncTime, xTicksMax, freq=None, yLabel=ncVarUnits, yLim=yLim)
    plotDates = timeSeriesPlot.get_plot_dates()

    # Applying default title if not passed as arg
    if title is None:
        title = utillib.get_ts_title(var, plotDates, tDescr, depthField, clim=True, time_range=timeRange)

    # Applying default output file name if not passed as arg
    if outFileName is None:
        outFileName = utillib.get_out_name(var, tDescr, depth_field=depthField)

    timeSeriesPlot.plot(varField, title, outFileName, subtitle=subtitle)
