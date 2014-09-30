memory_utils
============

|Build Status|

Yeah Memory Issues!!


Memory Issues happen to the best of us.  ``memory_utils`` will give you simple tools to quickly isolate the
cuplrit, and ideally, warn you before you run into issues.

From my experience, there is no silver-bullet in dealing with memory issues.  You just have to roll up your sleeve and get
dirty with print statements.  In our team's recent fight with a memory issue, we created memory_utils and we wanted to 
share.

``memory_utils`` deals primarily with RSS memory (Resident Set Size).  The most important memory concept to understand 
when dealing with memory constrained systems: RSS, the resident set size, is the portion of a process's memory that 
is held in RAM. The rest of the memory exists in the swap of the file system.

Install
-------

.. code:: bash

    pip install memory_utils


Usage
-----

print_memory
~~~~~~~~~~~~
The workhorse of this package is ``print_memory`` It simply prints out 3 columns of data: the current memory, the 
delta since the previous statement and an message that you pass it.  If there is additional memory used -- 
the line will be printed RED and if there is a decrease, the line will be printed GREEN.

It is a very simple approach, but it really helped us  find out where the issue was, at glance.  The output could
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We have worker processes that run in containers.  I like to fail hard and early.  So we have two helper functions
that help us with that

``check_memory``
^^^^^^^^^^^^^^^

    Will check the current rss memory against the memory_utils set memory limit.  And if it crosses that limit it will
    raise a ``MemoryTooBigException``

.. code:: python

    pip install memory_utils

    import memory_utils
    memory_utils.set_memory_limit(200 * memory_utils.MEGABYTES)

    # .... else where

    memory_utils.check_memory()


``memory_watcher``
^^^^^^^^^^^^^^^^^^

    Often you will want to do your ``check_memory`` at a _safe_ place.  Also memory leaks often happen within a loop.
    We created ``memory_watcher`` with those concepts in mind
    
    .. code:: python

        for account in memory_watcher(Account.objects):
            account.do_something_memory_intensive()
            account.save()

    This will call ``check_memory`` before each iteration


Configuration
~~~~~~~~~~~~~
``set_verbose``
^^^^^^^^^^^^^^^
    By default ``print_memory`` will only print statements that move the memory
    and ``memory_watcher`` will not print its memory usage.
    If you want additional verbosity set this to true
        
    .. code:: python

        import memory_utils
        memory_utils.set_verbose(True)

``set_memory_limit``
^^^^^^^^^^^^^^^^^^^^
    By default, the memory limit at 200 MB.

    Use this method to change the default.

    This setting is used in ``print_memory`` and ``memory_watcher``

    Note: you can also override this limit at the function level as well
    
    .. code:: python

        import memory_utils
        memory_utils.set_memory_limit(500 * memory_utils.MEGABYTES)

``set_out``
^^^^^^^^^^^

    By default, we will print to standard out.  Feel free to override here like so
    
    .. code:: python

        import memory_utils
        from StringIO import StringIO

        out = StringIO()
        memory_utils.set_out(out)


Questions / Issues
------------------

Feel free to ping me on twitter: `@tushman`_
or add issues or PRs at https://github.com/jtushman/memory_utils

.. _@tushman: http://twitter.com/tushman

.. |Build Status| image:: https://travis-ci.org/jtushman/proxy_tools.svg?branch=master
    :target: https://travis-ci.org/jtushman/memory_utils
