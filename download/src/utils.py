import time
import os


def get_field(type_file):
    """
    @param type_file: String that represent the file type
    @return: return the field associated to the input_file as cf standard name
    """
    import json
    root_dir = get_root_dir()
    with open(root_dir + '/config/filename.json') as json_file:
        filename = json.load(json_file)
    field = None
    for type_file_tmp, fields_tmp in filename.items():
        if type_file == type_file_tmp:
            field = fields_tmp
            break
    if field is None:
        raise Exception("Can't assign a type file for type_file: " + str(type_file))
    return field


def get_type_file(field):
    """
    @param field: cf standard name used to represent a variable
    @return: return the type file associated to field indicated
    """
    import json
    root_dir = get_root_dir()
    with open(root_dir + '/config/filename.json') as json_file:
        filename = json.load(json_file)

    type_file = None
    for type_file_tmp, fields_tmp in filename.items():
        if field in fields_tmp:
            type_file = type_file_tmp
            break
    if type_file is None:
        raise Exception("Can't assign an output type file for field: " + str(field))
    return type_file


def init_dl_dir(outdir=None):
    """
    If not exists, create the download dir
    @return: the path of default download directory
    """

    if outdir is None:
        root_dir = get_root_dir()
        outdir = root_dir + '../indir'
    # create new dir called 'indir' in the parent directory of daccess module
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    return outdir


def get_gcube_token(globalVariablesFile):
    gcubeToken = None
    envs = os.environ

    if os.path.exists(globalVariablesFile):
        print(f"Reading gcube_token from {globalVariablesFile}")
        with open(globalVariablesFile) as fp:
            for line in fp:
                if line.find("gcube_token") != -1:
                    tk = line[14:]
                    gcubeToken = tk.replace('"', '').strip()
                    # print("Found gcube_token")
                    break
    elif 'GCUBE_TOKEN' in envs:  # when a method is executed in the dataminer
        print(f"Reading gcube_token from 'GCUBE_TOKEN' variables")
        gcubeToken = os.environ.get('GCUBE_TOKEN')
    else:
        raise Exception('Error gcube_token not found!')

    if gcubeToken is None:
        raise Exception("Some error occurs when try to read gcube_token!")

    return gcubeToken


def show_dl_percentage(dl, start, total_length):
    if total_length is not None:  # no content length header
        done = int(50 * dl / total_length)
        try:
            print("\r[%s%s]  %8.2f Mbps" % ('=' * done, ' ' * (50 - done),
                                            (dl / (time.process_time() - start)) / (1024 * 1024)), end='',
                  flush=True)
        except:
            pass
    else:
        if dl % 1024 == 0:
            try:
                print("[%8.2f] MB downloaded, %8.2f kbps" \
                      % (dl / (1024 * 1024), (dl / (time.process_time() - start)) / 1024))
            except:
                pass


def get_root_dir(base_dir=None) -> str:
    """
    @return: absolute path of root dir where there's seastat.py script
    """
    if base_dir is not None:
        root_dir = base_dir
    else:
        root_dir = os.path.dirname(__file__).split('download')[0] + '/download'
    return root_dir


workingDomain_attrs = ['lonLat', 'time']
workingDomain_attrs_optional = ['depth']


def wd_dict_validation(working_domain_dict):
    """
    This function check if workingDomain is valid
    @param working_domain_dict: dict with spatial/time information:
                lonLat: list of list, the internal list has the format:  [minLon , maxLon, minLat , maxLat]
                depth: depth range in string format: [minDepth, maxDepth]
                time: list of two strings that represent a time range: [YYYY-MM-DDThh:mm:ssZ, YYYY-MM-DDThh:mm:ssZ]
    @return: True if workingDomain is valid
    """
    for wd_attr in workingDomain_attrs:
        if wd_attr not in working_domain_dict:
            raise Exception("Can't find " + wd_attr + ' in workingDomain: ' + str(working_domain_dict))
    for wd_attr_opt in workingDomain_attrs_optional:
        if wd_attr_opt not in working_domain_dict:
            print("WARNING: ", wd_attr_opt, ' not found')

    # lonLat check
    lonLat = working_domain_dict['lonLat']
    if len(lonLat) != 4:
        raise Exception("Wrong size for lonLat, please check it: " + str(lonLat))
    elif not float_int_check(lonLat):
        raise Exception("Type error in lonLat")

    # depth check
    if 'depth' in working_domain_dict:
        depth = working_domain_dict['depth']
        if len(depth) != 2:
            raise Exception("Wrong size for depth, please check it: " + str(depth))
        elif not float_int_check(depth):
            print("ERROR lonLat value must be float or int, please check it: ", depth)
            raise Exception("Type error in depth")

    # time check
    time = working_domain_dict['time']
    if len(time) != 2:
        raise Exception("Wrong size for lonLat, please check it: " + str(time))


def float_int_check(elements):
    for x in elements:
        if not isinstance(x, float) and not isinstance(x, int):
            print("ERROR found no float or int type: ", x)
            return False
    return True
