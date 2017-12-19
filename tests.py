# -*- coding: utf-8 -*-
"""
    tests.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    memory_utils tests.

    :copyright: (c) 2014 by Jonathan Tushman
    :license: MIT, see LICENSE for more details.
"""
import sys
import nose
from nose.tools import eq_
import memory_utils
from six import StringIO
from six.moves import range


def test_print_memory():

    out = StringIO()
    memory_utils.set_out(out)

    leak = []
    memory_utils.print_memory("BEFORE BLOAT")
    for _ in range(100 * 100):
        leak.append(LONGISH_STRING)
        memory_utils.print_memory("DURING BLOAT")

    memory_utils.print_memory("AFTER BLOAT")

    assert "4,096" in out.getvalue() or "8,192" in out.getvalue()


def test_memory_watch():

    out = StringIO()
    memory_utils.set_out(out)
    memory_utils.set_verbose(True)

    leak = []
    for _ in memory_utils.memory_watcher(range(100 * 100)):
        leak.append(LONGISH_STRING)

    assert "4,096" in out.getvalue()




LONGISH_STRING = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sapien velit, elementum a justo vel, rutrum finibus mauris. Donec elementum tellus ex, a mollis diam ultricies eget. Nulla consequat augue quis urna maximus, ut dapibus nibh dapibus. Ut fringilla ligula ac maximus suscipit. Mauris dapibus leo purus, non pulvinar massa volutpat sodales. Integer finibus urna vel risus molestie, eu elementum quam euismod. Ut elit neque, blandit vel pharetra eu, rhoncus ac lectus. Morbi pulvinar at diam non molestie.

Quisque ornare, libero interdum mollis interdum, lectus odio faucibus arcu, id facilisis metus odio et tellus. Suspendisse iaculis a enim posuere pharetra. Proin vel est sit amet lectus feugiat posuere ac et ex. Curabitur pretium diam at orci tincidunt eleifend. Mauris orci dui, mollis nec urna id, consequat ullamcorper est. Fusce at diam viverra odio ullamcorper lobortis. In eget ante mauris. Morbi quis sodales est. Aliquam sagittis porttitor porttitor. Proin tincidunt finibus facilisis. Mauris sodales eget sem sed tristique. Aliquam erat volutpat. Nulla maximus et eros non rutrum.

Mauris mattis felis fermentum augue auctor, sed sollicitudin nunc tristique. Nullam a urna pretium, mollis mi nec, congue lectus. Proin ornare sollicitudin ante ac congue. Quisque tempus ante a nunc tempor, vitae faucibus turpis tempus. Proin non dignissim est. Etiam facilisis turpis eu sagittis ullamcorper. Nunc vulputate est quis pretium gravida. Nunc orci sapien, aliquet non luctus at, porttitor non sapien. Vivamus semper vitae nulla quis fringilla. Etiam malesuada leo a suscipit congue. Donec egestas dapibus nisi, et porttitor est lacinia in. Vivamus libero velit, dignissim vel porta ac, ultricies a nisl. Curabitur pharetra aliquam nisl, a ullamcorper nunc tristique at. Sed sodales eros eu dictum bibendum. Vivamus sit amet dictum dui.

Nam porta, ipsum quis faucibus imperdiet, velit dolor mollis nisi, non vehicula ex metus feugiat purus. Sed at elementum leo, dignissim blandit ipsum. Mauris eget lacus semper arcu tempor egestas. Etiam non sapien vitae sem euismod maximus. Pellentesque ante lacus, consectetur ac odio sit amet, auctor tristique justo. Fusce fringilla rhoncus sapien, non aliquet diam elementum eu. Maecenas in interdum diam. Fusce aliquam, est in dignissim commodo, lorem quam sagittis eros, pharetra malesuada quam mi vitae felis.

Donec finibus ultricies sapien vel volutpat. Curabitur egestas rutrum posuere. Duis ut sem quis arcu fringilla molestie. Sed nulla tellus, placerat id egestas ut, consequat nec erat. Nulla scelerisque ut risus non accumsan. Nam ac mi ante. Vivamus mollis dolor ac dictum sagittis. Nam ut nunc non velit hendrerit semper in nec eros.
"""