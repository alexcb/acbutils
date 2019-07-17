import time
import calendar

default_fmt = '%Y-%m-%dT%H:%M:%SZ'

def utc_timestamp_to_str(x, fmt=default_fmt):
    return time.strftime(fmt, time.gmtime(x))

def str_to_utc_timestamp(s, fmt=default_fmt):
    x = time.strptime(s, fmt)
    return calendar.timegm(x)

