import datetime
import re
import dateutil.parser as parser


def extract_date_from_text(text):
    """

    Args:
        text (str): A text string that contains a date

    Returns:
        datetime: the date expressed in the text

    """
    match_date = re.search(r'\d{4}-\d{2}-\d{2}', text)
    if match_date is None:
        match_date = re.search(r'\d{2}-\d{2}-\d{4}', text)

    if match_date is None:
        raise Exception("Can't find date in: ", text)

    match_time = re.search(r'\d{2}:\d{2}:\d{2}', text)

    str_date = match_date.group() + ' ' + match_time.group()
    return parser.parse(str_date)


def get_date_from_timedelta(td, RefTimeUnits):
    """
    This functions converts a timedelta object into hours or minutes in according to RefTimeUnits

    Args:
        td (str): timedelta
        RefTimeUnits (str): string with netCDF time reference

    Returns:
        datetime: the timedelta expressed in hours or minutes

    """
    if 'hour' in RefTimeUnits:
        delta = datetime.timedelta(hours=int(td))
    elif 'minute' in RefTimeUnits:
        delta = datetime.timedelta(minutes=int(td))
    elif 'second' in RefTimeUnits:
        delta = datetime.timedelta(seconds=int(td))
    else:
        raise Exception("Unknown netCDF reference Time")
    refDate = extract_date_from_text(RefTimeUnits)

    return refDate + delta
