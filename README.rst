memory_utils
============

|Build Status|

Yeah Memory Issues!!


Memory Issues happens to the best of us.  ``memory_utils`` will give you some simple tools to help you quickly issolate
The cuplrit.  And ideally warn you before you run into issues.

From my experience there is no silver-bullet in dealing with memory issues.  You just have roll up your sleeve and get
dirty with print statements.  In our teams recent fight with a memory issue, we created a utility that we found useful
and we wanted to share.

Install
-------

.. code:: bash

    pip install memory_utils


print_memory
~~~~~~~~~~~~
The workhorse of this package is ``print_memory`` It simply prints out 3 columns of data, the current memory, the delta
since the previous statement and an message that you pass it.  If there is an additional memory used -- the line will
be printed RED and if there is a decrease, the line will be printed GREEN.

It is a very simple approach -- but it really helped us at glance to find out where the issue was,  The output could
look like this::

    RSS                  Delta                Message
    14,393,344           14,393,344          BEFORE BLOAT
    14,397,440           4,096               DURING BLOAT (1)
    14,413,824           16,384              DURING BLOAT (102)
    14,417,920           4,096               DURING BLOAT (211)
    14,438,400           20,480              DURING BLOAT (1002)
    14,442,496           4,096               DURING BLOAT (2034)
    14,462,976           20,480              DURING BLOAT (2056)


memory_watcher and check_memory
~~~~~~~~~~~~~~
We have worker processes that run in containers.  I like to fail hard and early.  So we have two helper functions
that help us with that

``check_memory``
    Will check the current rss memory against the memory_utils set memory limit.  And if it crosses that limit it will
    raise a ``MemoryToBigException``::

        import memory_utils
        memory_utils.set_memory_limit(200 * memory_utils.MEGABTYES)

        .... else where

        memory_utils.check_memory()




Configuration
-------------

``set_verbose``
``set_memory_limit``
``set_out``





Questions / Issues
------------------

Feel free to ping me on twitter: `@tushman`_
or add issues or PRs at https://github.com/jtushman/memory_utils

.. _@tushman: http://twitter.com/tushman

.. |Build Status| image:: https://travis-ci.org/jtushman/proxy_tools.svg?branch=master
    :target: https://travis-ci.org/jtushman/memory_utils
