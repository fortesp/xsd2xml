import random
import string
import time


def get_date(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def get_mixed_string(length):
    return get_string(string.ascii_uppercase + string.digits, length)


def get_digits(length):
    return get_string(string.digits, length)


def get_string(population, length):
    return ''.join(random.choices(population, k=length))
