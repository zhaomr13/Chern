from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

import os
import Chern
from Chern import utils
from Chern.ChernManager import get_manager
from Chern.VData import create_data
from Chern.VAlgorithm import create_algorithm
from Chern.VTask import create_task

manager = get_manager()
c = manager.c
p = manager.p

@register_line_magic
def mkdata(line):
    line = utils.strip_path_string(line)
    if line.startswith("p"):
        line = manager.p.path + line[1:]
        create_data(line)
        new_object = create_object_instance(path)
        del manager.c
        manager.c = new_object
        return

    line = os.getcwd() + "/" + line
    create_data(line)
    new_object = create_object_instance(line)
    del manager.c
    manager.c = new_object
    os.chdir(manager.c.path)
del mkdata

@register_line_magic
def mkalgorithm(line):
    line = utils.strip_path_string(line)
    if line.startswith("p"):
        line = manager.p.path + line[1:]
        create_algorithm(line)
        new_object = create_object_instance(path)
        del manager.c
        manager.c = new_object
        return

    line = os.getcwd() + "/" + line
    create_data(line)
del mkalgorithm

@register_line_magic
def mktask(line):
    line = utils.strip_path_string(line)
    if line.startswith("p"):
        line = manager.p.path + line[1:]
        create_task(line)
        new_object = create_object_instance(line)
        del manager.c
        manager.c = new_object
        return

    line = os.getcwd() + "/" + line
    create_task(line)
    new_object = create_object_instance(line)
    del manager.c
    manager.c = new_object
    os.chdir(manager.c.path)
del mktask


