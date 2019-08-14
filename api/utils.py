import time
from datetime import datetime

from django.utils import timezone


def convert_to_epcoh(tm):
    return int(time.mktime(tm.timetuple()))


def convert_to_timestamp(naive_time):
    dt = datetime.fromtimestamp(int(naive_time))
    return timezone.make_aware(dt, timezone.utc)
