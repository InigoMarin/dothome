#!/bin/python

import os
import sys

home = os.environ['HOME']

sys.path.append(os.path.abspath("{}/.local/share/s1n7ax/commons".format(home)))

from execute import execute

execute([['firefox']], False)
execute([['chromium']], False)
execute([['imwheel', '-b', '45']], False)
execute([['setxkbmap', '-option', 'ctrl:nocaps']], False)
execute([['xset', 'r', 'rate', '180', '80']], False)
