"""
    memory_utils/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Collection of utilities to help with memory leaks and monitoring


    :copyright: (c) 2014 by Jonathan Tushman 2014.
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import psutil
from six import print_
from six.moves import range
from colorama import Fore, Style

KILOBYTE = KILOBYTES = 1024
MEGABYTE = MEGABYTES = 1024 * KILOBYTES
GIGABYTE = GIGABYTES = 1024 * MEGABYTES
TERABYTE = TERABYTES = 1024 * GIGABYTES
PETABYTE = PETABYTES = 1024 * TERABYTES


# Note we treat this module like a singleton -- hence these following globals
# There are helper methods to adjust these

_MEMORY_LIMIT = 200 * MEGABYTES

_OUT = sys.stdout

_previous_memory = None

_verbose = False


class MemoryTooBigException(Exception):

    """ The system crosses a set memory limit
    """
    pass


def memory():
    """ returns the rss (Resident Set Size) memory of the current process.

        The *resident set size* is the portion of a process's memory that is held in RAM.
        The rest of the memory exists in swap of the file system.

        We care primarily about rss -- for once you bypass that -- bad things start to happen

        returns int (rss in btyes)

    """
    p = psutil.Process(os.getpid())
    memory_info = p.memory_info()
    return memory_info.rss


def formatted_memory():
    """ Returns :func:`memory` as a human readable string
    """
    return sizeof_fmt(memory())


def sizeof_fmt(num):
    """ "Human-readable" string of memory.  Input memory in bytes
    """
    if num == 0:
        return '0'
    if num < 0:
        negative = True
    else:
        negative = False

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if abs(num) < 1024.0:
            if negative:
                return "-%3.1f %s" % (num, x)
            else:
                return "%3.1f %s" % (num, x)
        num = abs(num) / 1024.0


def print_memory(message=''):
    """ Useful method (I will be the judge of what I think is useful) for helping find memory leaks
        prints current process memory usage, and the delta since the last print statement

        if its a gain in memory it will print RED
        if its a decrease in memeory is will print in GREEN
    """
    global _previous_memory

    current_rss = memory()

    if _previous_memory is None:
        echo('{:<20s} {:20s} {}'.format('RSS', 'Delta', 'Message'))
        delta = current_rss
    else:
        delta = current_rss - _previous_memory

    if delta > 0:
        echo(Fore.RED + '{:<20,d} {:<20,d}{}'.format(current_rss, delta, message) + Style.RESET_ALL)
    elif delta < 0:
        echo(Fore.GREEN + '{:<20,d} {:<20,d}{}'.format(current_rss, delta, message) + Style.RESET_ALL)
    else:
        if _verbose:
            echo('{:<20,d} {:<20,d}{}'.format(current_rss, delta, message) + Style.RESET_ALL)

    _previous_memory = current_rss


def set_memory_limit(new_memory_limit):
    """ By default I have set the memory limit at 200 MB

        Use this method to change the default.

        Note: for all methods that deal with this limit -- you can also override it at
        the function level as well
    """
    global _MEMORY_LIMIT
    _MEMORY_LIMIT = new_memory_limit


def set_verbose(bool):
    """ By default :func:`print_memory` will only print statements that move the memory
        and :func:`memory_watcher` will not print its memory useage
        If you want additional verbosity set this to true::

            import memory_utils
            memory_utils.set_verbose(True)
    """
    global _verbose
    _verbose = bool


def set_out(io_stream):
    """ By default we will print to standard out.  Feel free to override here like so::

        import memory_utils
        from StringIO import StringIO

        out = StringIO()
        memory_utils.set_out(out)

    """
    global _OUT
    _OUT = io_stream


def echo(string):
    print_(string, file=_OUT)


def check_memory(limit=None):
    """ Check the current process memory against a set limit
        if greater then limit then raise :class:`MemoryToBigException`
    """
    if limit is None:
        limit = _MEMORY_LIMIT

    current_rss = memory()

    if current_rss > limit:
        raise MemoryTooBigException("{} > {}".format(sizeof_fmt(current_rss), sizeof_fmt(limit)))


def memory_watcher(it, limit=None):
    """ Use this to wrap loops that you are concerned that might have memory issues
        In general this should be a concern in scheduled or background jobs

        Usage::

            for account in memory_watcher(Account.objects):
                account.do_something_memory_intensive()
                account.save()

        if logging is turned on -- you will get memory info printed out for each iteration

        if memory crosses limit -- it will raise a :class:`MemoryToBigException`
    """

    if limit is None:
        limit = _MEMORY_LIMIT

    counter = 0
    for value in it:
        counter += 1
        if _verbose:
            print_memory("[{}] {}".format(counter, value))
        check_memory(limit)
        yield value
