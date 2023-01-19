def check_working_domain(working_domain: dict):
    """
    This function try to read working domain value, if there's some problem with this value
    an exception will be raised
    @param working_domain: String value that determines the domain within which processing is performed.
                            Contains information on both the horizontal and vertical domains
    """
    print('working_domain found, try to read its value...')

    print("Horizontal domain: ")
    print(get_horizontal_domain(working_domain))

    print("Vertical domain: ")
    print(get_vertical_domain(working_domain))

    print("working domain is correct")


def init_daccess_working_domain(working_domain: dict=None, lonLat=None, depth=None, time=None, freq="m"):
    """Extract spatial/time information from args and save it in a new dict()"""
    daccess_wd = dict()
    daccess_wd['lonLat'] = extract_daccess_lonLat(working_domain) if lonLat is None else lonLat
    daccess_wd['depth'] = extract_daccess_depth(working_domain) if depth is None else depth
    daccess_wd['time'] = None if time is None else time
    daccess_wd['time_freq'] = freq
    return daccess_wd


def extract_daccess_lonLat(working_domain: dict):
    """
    @param working_domain: dict with working domain information
    @return: extract lonLat in the format: [minLon, maxLon, minLat , maxLat]
    """
    horizontal_domain = get_horizontal_domain(working_domain)
    if horizontal_domain is None:
        raise Exception("Horizontal domain is None")
    else:   # take only the first box
        return [horizontal_domain[0][0], horizontal_domain[0][2], horizontal_domain[0][1], horizontal_domain[0][3]]


def extract_daccess_depth(working_domain: dict):
    """
    @param working_domain: dict with working domain information
    @return: extract depth in the format: [min_depth, max_depth]
    """
    vertical_domain = get_vertical_domain(working_domain)
    if vertical_domain is None:
        return None
    else:
        return [vertical_domain[0][0], vertical_domain[0][1]]


def get_mp2_working_domain(working_domain: dict):
    from input import iparameters_validation
    """
    This function convert the new dict working domain in the mapreduce format
    @param working_domain: working domain in the format: { 'box' : [ [lon_min, lat_min, lon_max, lat_max ] ] ,
    'depth_layers' : [[depth_min,depth_max] ] }
    @return: return mp2_working domain as [ DOMAINOFINTEREST, LAYEROFINTEREST ] where:
        DOMAINOFINTEREST: [ list d1, list d2, …. list dn ] - Horizontal domain
                            list_di = [ [ lon_min_i , lon_max_i ] , [ lat_min_i , lat_max_i ] ]
        LAYEROFINTEREST: [ d , [ list y1, list y2, ... , list ym ] ] - Vertical domain
                            list_yj = [ depth_min_j , depth_max_j ]
    """
    domain_of_interest = list()
    layer_of_interest = list()
    horizontal_domain = get_horizontal_domain(working_domain)
    vertical_domain = get_vertical_domain(working_domain)

    for h_domain in horizontal_domain:
        domain_of_interest.append([[h_domain[0], h_domain[2]], [h_domain[1], h_domain[3]]])

    if vertical_domain is not None:
        for v_domain in vertical_domain:
            layer_of_interest.append(v_domain)

    mp2_working_domain = "[ DOMAINOFINTEREST, LAYEROFINTEREST ]"
    mp2_working_domain = mp2_working_domain.replace("DOMAINOFINTEREST", ','.join(str(x) for x in domain_of_interest)).replace("LAYEROFINTEREST", '[ "d", ' + str(layer_of_interest) + ']')
    iparameters_validation.square_bracket_validation(mp2_working_domain)
    return mp2_working_domain


def get_horizontal_domain(working_domain: dict):
    horizontal_domain = working_domain.get('box')
    if horizontal_domain is None or len(horizontal_domain) == 0:
        raise Exception("Horizontal domain is None/Invalid")
    else:
        return horizontal_domain


def get_vertical_domain(working_domain: dict):
    return working_domain.get('depth_layers')
