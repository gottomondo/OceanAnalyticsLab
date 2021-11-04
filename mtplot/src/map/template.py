#! /usr/bin/env python

import math
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np


def get_fig_size(lonLat):
    area = 60
    a = lonLat[1] - lonLat[0]
    b = lonLat[3] - lonLat[2]
    if a > b:
        b += b * 0.1  # consider colorbar and title for y-axis
        y = math.sqrt((80 * b) / a)
        x = area / y
    else:
        a += a * 0.1  # consider colorbar and title for y-axis
        x = math.sqrt((80 * a) / b)
        y = area / x
    return x, y


class MapPlot:
    def __init__(self,
                 mapLevels=None,
                 xStep=None,
                 yStep=None,
                 round_factor=None,
                 cmap=None,
                 diff=False,
                 curr=False,
                 grid=None,
                 qScale=None,
                 qWidth=None):  # it defines the precision of diff src     -> Define the precision of diff src
        self.mapLevels = mapLevels  # it defines the precision of src          -> Define the precision of src
        self.xStep = 10 if xStep is None else xStep  # x coordinates step grid
        self.yStep = 5 if yStep is None else yStep  # y coordinates step grid
        self.round_factor = 4 if round_factor is None else round_factor  # it defines the precision of diff src     -> Define the precision of diff src
        self.cmap = 'viridis' if cmap is None else cmap
        self.diff = diff
        self.curr = curr
        self.grid = grid
        if self.curr:
            self.qScale = qScale
            self.qWidth = qWidth

        if self.diff and self.curr:
            raise Exception("It is not possible to simultaneously activate diff and curr")

    def get_locators(self, lonLat):
        if self.grid is None:
            x1Loc = int(math.floor(lonLat[0] / self.xStep)) * self.xStep
            x2Loc = int(math.ceil(lonLat[1] / self.xStep)) * self.xStep
            y1Loc = int(math.floor(lonLat[2] / self.yStep)) * self.yStep
            y2Loc = int(math.ceil(lonLat[3] / self.yStep)) * self.yStep
            xLocators = np.arange(x1Loc, x2Loc, self.xStep)
            yLocators = np.arange(y1Loc, y2Loc, self.yStep)
        else:

            xStep = int((lonLat[1] - lonLat[0]) / self.grid)
            yStep = int((lonLat[3] - lonLat[2]) / self.grid)
            xLocators = np.arange(lonLat[0], lonLat[1], xStep)
            yLocators = np.arange(lonLat[2], lonLat[3], yStep)

        return xLocators.tolist(), yLocators.tolist()

    def get_contourf_levels(self, minp, maxp, clbLim=None):
        """
        This function defines how many values src on the map.
        The higher the number of levels the more accurate the map will be
        and the longer the computation time will be. It computes a value range that
        differ in case of differ src ( in this case the src is centered to 0 ).
        Change round_factor and contourf_round_factor to increase or decrease the map precision

        Args:
            minp: left end of the range
            maxp: right end of the range
            clbLim (str): the range limit of colorbar

        Returns:
            ndarray: an array with values in the range [minp, maxp] in standard case,
                in case of diff src it return a range [-cbarLim, cbarLim], cbarLim = max(|minp|, |maxp|)

        """

        if clbLim is not None:
            import json
            clbLim = json.loads(clbLim)
            minp = clbLim[0]
            maxp = clbLim[1]

        if self.diff:
            # Plot diff map case
            if minp == 0 and maxp == 0:
                # default colorbar range if all values are zero
                minp -= 1
                maxp += 1
                step = 2
            else:
                step = int(self.mapLevels / 2)

            if abs(minp) >= abs(maxp):
                cbarLim = minp
            else:
                cbarLim = maxp

            contourfLevelLeft = np.linspace(-abs(cbarLim), 0, step, endpoint=True)
            contourfLevelRight = np.linspace(0, abs(cbarLim), step, endpoint=True)

            contourfLevel = np.unique(np.concatenate((contourfLevelLeft, contourfLevelRight)))
        else:
            # Plot standard map case
            x = self.mapLevels
            contourfLevel = np.round(np.linspace(minp, maxp, int(x), endpoint=True), self.round_factor)
        return contourfLevel

    def plot(self, lon, lat, wrk, title, out_name, lonLat, curr_u=None, curr_v=None, clbLim=None):
        """
        Plotting function

        Args:
            lon: longitude of wrk
            lat: latitude of wrk
            wrk: variable to src
            title: src title
            out_name: name of outfile
            lonLat: longitude and latitude of the figure
            curr_u: u component of current
            curr_v: v component of current
            clbLim (str): the range limit of colorbar

        Returns:
            file: save a png map src

        """
        figSize = get_fig_size(lonLat)
        # Initialize Plot
        fig = plt.figure(figsize=figSize, dpi=500)
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        ax.set_extent(lonLat, crs=ccrs.PlateCarree())
        ax.coastlines(resolution='10m', color='black', linewidth=1)
        minWrkValue = np.ma.min(wrk)
        maxWrkValue = np.ma.max(wrk)

        # Map create
        contourfLevel = self.get_contourf_levels(minWrkValue, maxWrkValue, clbLim)
        cmap = plt.get_cmap(self.cmap)
        if self.curr:
            cs = plt.contourf(lon, lat, wrk, levels=contourfLevel, transform=ccrs.PlateCarree(), cmap=cmap, vmax=0.6)
        else:
            cs = plt.contourf(lon, lat, wrk, levels=contourfLevel, transform=ccrs.PlateCarree(), cmap=cmap)
        norm = matplotlib.colors.Normalize(vmin=cs.cvalues.min(), vmax=cs.cvalues.max())
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cs.cmap)
        sm.set_array(wrk)
        cbar = fig.colorbar(sm, orientation="horizontal", aspect=30, fraction=0.05)

        try:
            minValue = round(minWrkValue, self.round_factor)
        except Exception as e:
            print("Warning:", e)
            minValue = 0
        try:
            maxValue = round(maxWrkValue, self.round_factor)
        except Exception as e:
            print("Warning:", e)
            maxValue = 0
        cbar.set_label(
            "min: " + np.format_float_positional(minValue) + ", max: " + np.format_float_positional(maxValue),
            fontsize=12)

        plt.title(title, fontsize=24, y=1.1)
        ax.add_feature(cfeature.LAND)
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=1, color='grey', alpha=0.5,
                          linestyle='--')

        gl.xlabels_top = False
        gl.ylabels_left = True
        gl.ylabels_right = False
        gl.xlines = True
        xlocator, ylocator = self.get_locators(lonLat)
        gl.xlocator = mticker.FixedLocator(xlocator)
        gl.ylocator = mticker.FixedLocator(ylocator)
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        if self.curr:
            ax.coastlines('50m')

            Q = ax.quiver(lon, lat, curr_u, curr_v,
                          scale=self.qScale,
                          width=self.qWidth,
                          minlength=0.1,
                          # headwidth=3,
                          # headlength=3,
                          # headaxislength=2,
                          transform=ccrs.PlateCarree())
            plt.quiverkey(Q, X=-0.05, Y=0, U=0.1,
                          label='0.1 m/s', labelpos='W')

        # plt.subplots_adjust(bottom=0, right=0.9, top=0.1, left=0.09)

        plt.savefig(out_name)
        plt.close()
