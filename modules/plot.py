import calendar

from modules.module import Module
from tools import fields_mng
from mtplot import ncplot


def build_plot_subtitle(working_domain, start_time, end_time, month):
    layer_title = 'layer: ' + '-'.join(str(round(depth, 2)) for depth in working_domain['depth_layers'][0]) + ' m'
    box_title = 'box: ' + str(working_domain['box'][0])
    time_title = start_time

    if end_time != start_time:
        time_title += ' - ' + end_time
    if month is not None:
        month_name = calendar.month_name[month]
        time_title += ' ' + month_name

    plot_subtitle = time_title + ', ' + box_title + ', ' + layer_title
    return plot_subtitle


def get_region_to_plot(data_source):
    med24_plot_region = "[-18.125, 36.3, 30, 46]"
    glo_plot_region = "[-180, 179.9167, -80, 90]"

    if 'GLOBAL' in data_source:
        region_to_plot = glo_plot_region
    else:
        region_to_plot = med24_plot_region
    return region_to_plot


def build_plot_title(id_field, id_output_type):
    cf_std_name = id_field.replace('_', ' ')

    name_output_type = id_output_type.replace('_', ' ')

    plot_title = cf_std_name + ', ' + name_output_type
    return plot_title


def get_plot_grid(data_source):
    if 'GLOBAL' in data_source:
        grid_size = 20
    else:
        grid_size = 5
    return grid_size


class Plot(Module):

    def _exec_impl(self):
        data_source = self._input_parameters.get_data_source()
        id_field = self._input_parameters.get_id_field()
        id_output_type = self._input_parameters.get_output_type()
        working_domain = self._input_parameters.get_working_domain()
        start_time, end_time, month = self._input_parameters.get_start_end_time_and_month()

        region_to_plot = get_region_to_plot(data_source)
        var_to_plot = fields_mng.get_output_var(id_field)
        plot_title = build_plot_title(id_field, id_output_type)
        plot_subtitle = build_plot_subtitle(working_domain, start_time, end_time, month)
        plot_grid = get_plot_grid(data_source)
        plot_args = ["output.nc", var_to_plot, '--title=' + plot_title,
                     '--subtitle=' + plot_subtitle, '--lonLat=' + region_to_plot, '--o=output',
                     '--grid=' + str(plot_grid)]
        if 'clim' in id_output_type:
            plot_args.append('--clim')
        ncplot.main(plot_args)
