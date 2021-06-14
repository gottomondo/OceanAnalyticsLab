from plot.lib.netcdf import name_dict


def get_depth_string(depth_bnds):
    """
    This function maps the depth level to a default string

    Args:
        depth_bnds (list): list of two values that indicates the depth range of netCDF file

    Returns:
        str: a string that represent a specific layer of depth

    """
    depth_size = depth_bnds[1] - depth_bnds[0]
    if 0 < depth_size <= 3:
        return 'surface'
    if depth_size > 5800:
        return 'basin'
    else:
        return str(int(depth_bnds[0])) + "m - " + str(int(depth_bnds[1])) + "m"


def get_out_name(var, descr, level=None, depth_field=None):
    """

    Args:
        var: variable to plot
        descr (str): additional output file name string passed as argument
        level (int): depth level of var
        depth_field (str): the depth range

    Returns:
        str: the output file name

    """
    out_name = name_dict[var][1] if var in name_dict else var
    if level is not None:
        out_name += "-" + 'd' + str(level)
    elif depth_field is not None:
        out_name += "-" + get_depth_string(depth_field).replace(' ', '')
    out_name += "-" + descr if descr is not None else ""
    out_name += '.png'
    return out_name


def get_map_title(var, level, descr, diff=False, curr=False):
    """
    This functions constructs a default title for the map figure

    Args:
        var: variable to plot
        level (int): depth level of var
        descr (str): additional title description passed as argument
        diff (bool): enable diff title
        curr (bool): enable curr title

    Returns:
        str: the figure title

    """
    if curr:
        title = "Sea currents"
    else:
        title = "Difference " if diff else ''
        title += name_dict[var][0] if var in name_dict else var

    level_title = 'surface' if level is None else 'surface' if 0 <= level < 3 else str(level) + 'm'
    title += ", " + level_title
    title += ", " + descr if descr is not None else ""
    return title


def get_ts_title(var, plot_dates, descr, depth_field, diff=False, clim=False, time_range="", freq=None):
    """
    This functions constructs a default title for the timeseries figure

    Args:
        var (str): variable to plot
        plot_dates (list): dates to plot
        descr (str): additional title description passed as argument
        depth_field (list): the depth range
        diff (bool): enable diff title
        clim (bool): enable climatology title
        time_range (str): the years range  (climatology case)
        freq (str): the plot_date frequency

    Returns:
        str: the figure title

    """
    title = name_dict[var][0] if var in name_dict else var
    if clim:
        title += " climatology timeseries"
    elif diff:
        title += " difference timeseries"
    else:
        title += " timeseries"

    if depth_field is not None:
        title += ", layer " + get_depth_string(depth_field)
    title += ", " + get_date_title(plot_dates, clim, time_range, freq)
    title += ", " + descr if descr is not None else ""
    return title


def get_date_title(plot_dates, clim, time_range="", freq=None):
    """
    This function returns a time range as string with the right data format resolution
    in according to timeseries frequency

    Args:
        plot_dates (list): dates to plot
        clim (bool): if True it activate climatology plot
        time_range (str): the years range  (climatology case)
        freq (str): plot_dates frequency

    Returns:
        str: timeseries time range

    """
    if clim is True:
        out_title = time_range + ", Jan - Dec"
    else:
        if 'Y' in freq:
            out_title = plot_dates[0].strftime("%Y") + " - " + plot_dates[-1].strftime("%Y")
        elif 'M' in freq:
            out_title = plot_dates[0].strftime("%m-%Y") + " - " + plot_dates[-1].strftime("%m-%Y")
        else:
            out_title = plot_dates[0].strftime("%d-%m-%Y") + " - " + plot_dates[-1].strftime("%d-%m-%Y")
    return out_title


def get_times_freq(ncTime, ncVarLongName):
    """
    This function reads three consecutive date read from netCDF file in order to detect the timeseries frequency.

    Args:
        ncTime: the dates read from netCDF file
        ncVarLongName: long name attribute of netCDF var

    Returns:
        string: a pattern that indicates the time frequency

    """
    # Try to read the information from metadata
    if 'annual' in ncVarLongName:
        return 'YS'
    elif 'month' in ncVarLongName:
        return 'MS'
    elif 'day' in ncVarLongName:
        return 'D'
    else:
        # we need to have at least 3 files to understand the frequency
        if len(ncTime) > 3:
            first_date = ncTime[0]
            second_date = ncTime[1]
            third_date = ncTime[2]

            if first_date.year != second_date.year and second_date.year != third_date.year:
                return 'YS'
            elif first_date.month != second_date.month and second_date.month != third_date.month:
                return 'MS'
            else:
                return 'D'
        else:
            raise Exception("Can't understand data frequency due to incomplete metadata and/or few data")
