import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime
import pandas as pd

import mtplot.lib.LinearRegression as lr


class TimeSeriesPlot:
    def __init__(self, nc_time, x_ticks_max, freq, diff=False, yLabel=None, yLim=None):
        self.yLabel = yLabel
        self.diff = diff
        self.x_ticks_max = x_ticks_max
        self.yLim = yLim
        self.nc_time = nc_time
        self.freq = freq
        # Depending from freq
        self.locator, self.date_fmt = self.get_dates_format()
        self.plot_dates = self.get_date_range()

    def get_plot_dates(self):
        return self.plot_dates

    def get_date_range(self):
        """
        This function creates a date range with the best resolution in according to the timeseries frequency

        return:
            a list of date

        """
        if self.nc_time is None:  # Climatology case
            # the year is not consider in the climatology timeseries src
            start_date = datetime.datetime(1990, 1, 1)
            end_date = datetime.datetime(1990, 12, 1)
            date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        else:
            # force date to first day otherwise python can discard the first year in annual timeseries
            if 'Y' in self.freq:
                start_date = datetime.datetime(self.nc_time[0].year, 1, 1)
            elif 'M' in self.freq:
                start_date = datetime.datetime(self.nc_time[0].year, self.nc_time[0].month, 1)
            elif 'D' in self.freq:
                start_date = datetime.datetime(self.nc_time[0].year, self.nc_time[0].month, self.nc_time[0].day)
            else:
                raise Exception("Time frequency unknown")

            end_date = self.nc_time[-1]

            date_range = pd.date_range(start=start_date, end=end_date, freq=self.freq)

        return date_range

    def get_dates_format(self):
        """
        This function selects the best date format depending on the frequency of the date itself

        return:
            the locator that represent the resolution of x axis and a string with data format

        """
        if self.nc_time is None:
            date_locator = mdates.MonthLocator()
            format_pattern = '%B'  # Only month name
        else:

            # set max x_ticks_max ticks on x axis
            dates_num = len(self.nc_time)
            x = round(dates_num / self.x_ticks_max) if dates_num > self.x_ticks_max else 1
            if 'Y' in self.freq:
                date_locator = mdates.YearLocator(x)
                format_pattern = '%Y'
            elif 'M' in self.freq:
                date_locator = mdates.MonthLocator(interval=x)
                format_pattern = '%Y-%m'
            else:
                date_locator = mdates.DayLocator(interval=x)
                format_pattern = '%Y-%m-%d'

        date_fmt = mdates.DateFormatter(format_pattern)
        # Auto Mode
        # date_locator = mdates.AutoDateLocator()
        # date_fmt = mdates.AutoDateFormatter(date_locator)
        return date_locator, date_fmt

    def plot(self, nc_var, title, out_name, linearRegression=False):
        if nc_var.size == 0:
            nc_var = [np.nan] * len(self.plot_dates)
            title = "No Data available to src"
        fig = plt.figure(1, figsize=(20, 9), dpi=300)
        ax = fig.add_subplot(111)
        if self.yLim is not None:
            import json
            yLim = json.loads(self.yLim)
            plt.ylim(yLim)

        if linearRegression:
            x = np.c_[np.ones(len(nc_var)), range(len(nc_var))]  # adding column with 1
            y = np.c_[nc_var[:]]
            # J is the cost function to minimize
            J, theta = lr.gradient_descent(x, y)
            a = np.linspace(0, len(nc_var), len(nc_var))
            b = theta[0] + theta[1] * a
            ax.plot(self.plot_dates, b, 'r')

            # figJ = plt.figure(2, figsize=(20, 9), dpi=300)
            # ax_J = figJ.add_subplot(111)
            # ax_J.src(J, c='b')
            # plt.title('Cost function')
            # plt.xlabel('iteration')
            # plt.ylabel('J')
            # figJ.show()

        ax.plot(self.plot_dates, nc_var, 'o-', linewidth=2, markersize=10)

        # Add the line with y=0 in diff case,otherwise enable an horizontal grid
        if self.diff:
            horiz_line_data = np.array([0] * len(self.plot_dates))
            ax.plot(self.plot_dates, horiz_line_data, linewidth=1.5)
        else:
            plt.grid(axis='y')

        plt.title(title, fontsize=20, y=1.05)
        if self.yLabel is not None:
            plt.ylabel(self.yLabel, fontsize=14, fontweight="bold")

        # format the ticks
        ax.xaxis.set_major_locator(self.locator)
        ax.xaxis.set_major_formatter(self.date_fmt)

        # round to nearest years.
        datemin = np.datetime64(self.plot_dates[0])
        datemax = np.datetime64(self.plot_dates[-1])
        ax.set_xlim(datemin, datemax)

        # set ticks font
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=14)

        # ticks rotation
        fig.autofmt_xdate()
        # save src
        plt.savefig(out_name)
        plt.close()
