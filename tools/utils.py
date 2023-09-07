import os
import re


def sort_llist(id_output_type, llist):
    # find a substring is present in a list of strings
    if any('DACCESS' in string for string in llist) and 'climatology' not in id_output_type:
        sort_key = daccess_sort
    elif any('DACCESS' in string for string in llist) and 'climatology' in id_output_type:
        sort_key = daccess_sort_month
    elif 'climatology' in id_output_type:
        sort_key = month_sort
    else:
        sort_key = key_value_sort
    return sorted(llist, key=sort_key)


def daccess_sort(date_string):
    date_string = get_daccess_date(date_string)
    return int(date_string)


def daccess_sort_month(date_string):
    date_string = get_daccess_date(date_string)
    return int(date_string[4:6])


def get_daccess_date(daccess_str):
    from input import string_template
    file_template = daccess_str.split(',')[1]
    file_template = file_template.strip('DACCESS://')
    date_string = string_template.get_date(file_template)
    return date_string


def month_sort(date_string):
    match_date = re.search(r'(\d{8})|(\d{6})', date_string)
    if match_date is not None:
        date_string = match_date.group()
    else:
        print("WARNING Can't find data with the format YYYYMMDD or YYYYMM in: " + date_string)
        return 0

    return int(date_string[4:6])


def key_value_sort(date_string):
    match_date = re.search(r'(\d{8})|(\d{6})', date_string)
    if match_date is not None:
        date_string = match_date.group()
    else:
        print("WARNING Can't find data with the format YYYYMMDD or YYYYMM in: " + date_string)
        return 0

    return int(date_string)


def get_root_dir(base_dir=None) -> str:
    """
    @return: absolute path of root dir where there's seastat.py script
    """
    if base_dir is not None:
        root_dir = base_dir
    else:
        root_dir = os.path.dirname(__file__).split('tools')[0]
    return root_dir
