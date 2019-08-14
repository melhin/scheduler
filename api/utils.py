import time


def convert_to_epcoh(tm):
    return int(time.mktime(tm.timetuple()))
