import input.working_domain


def revert_string_template(string_template):
    from download.src import utils
    from download.src import time_utils as tu

    ID_PRODUCT, type_file, YYYYMM, depth_tmp, lonLat_tmp = string_template.split('%')

    fields = utils.get_field(type_file)

    time_range = tu.get_month_range(YYYYMM=YYYYMM)

    depth = [float(i) for i in depth_tmp.split('&')]

    lonLat_tmp = [float(i) for i in lonLat_tmp.split('&')]
    lonLat = [lonLat_tmp[0], lonLat_tmp[1], lonLat_tmp[2], lonLat_tmp[3]]

    daccess_wd = input.working_domain.init_daccess_working_domain(lonLat=lonLat, depth=depth, time=time_range)

    print('ID_PRODUCT', ID_PRODUCT)
    print('fields', fields)
    print(daccess_wd)

    return ID_PRODUCT, fields, daccess_wd


def get_date(string_template):
    ID_PRODUCT, type_file, YYYYMM, depth_tmp, lonLat_tmp = string_template.split('%')
    return YYYYMM


def get_outfile_template(dataset, daccess_wd, fields):
    from download.src import utils
    # [minLon, maxLon, minLat , maxLat]
    lonLat = daccess_wd['lonLat']
    depth = daccess_wd['depth']
    time = daccess_wd['time']

    template_prefix = 'DACCESS://'
    outfile_templates = list()

    type_files = list()
    for field in fields:
        type_file = utils.get_type_file(field)
        if type_file not in type_files:
            type_files.append(type_file)

    ID_PRODUCT = dataset
    YYYYMM = time[0][0:4] + time[0][5:7]
    for type_file in type_files:
        outfile_templates.append(template_prefix + ID_PRODUCT + '%' + type_file + '%' + YYYYMM + '%' + '&'.join(
            map(str, depth)) + '%' + '&'.join(map(str, lonLat)))
    return outfile_templates
