from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

import os
import Chern

@register_line_magic
def mkdata(line):
    Chern.mkdata(line, inloop=False)
del mkdata

@register_line_magic
def mkalgorithm(line):
    Chern.mkalgorithm(line, inloop=False)
del mkalgorithm

@register_line_magic
def mktask(line):
    Chern.mktask(line, inloop=False)
del mktask

@register_line_magic
def mkdir(line):
    Chern.mkdir(line, inloop=False)
del mkdir


