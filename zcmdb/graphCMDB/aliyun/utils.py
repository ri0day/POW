# -*- coding: UTF-8 -*-
"""
    aliyun.utils
    ~~~~~~~~~~~
"""
from __future__ import print_function
import time
from functools import wraps


# because aliyun API only return at most 100 records every request,
# so we have to create a decorator of recursive function.
def scan_page(func):
    """Fetch all data from aliyun API."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        num = 1
        size = 50
        total = []
        while True:
            ret = func(page_num=num, page_size=size, *args, **kwargs)
            total.extend(ret)
            if len(ret) < size:
                return total
            num += 1

    return wrapped


def print_star_stop(func):
    @wraps(func)
    def wrapped(*arg, **kwargs):
        print("%s start." % func.__name__)
        start = time.time()
        ret = func(*arg, **kwargs)
        elapsed = (time.time() - start) * 1000.0
        print("%s end." % func.__name__)
        print("elapsed: %0.3f ms" % elapsed)
        print("------------------")
        return ret

    return wrapped
