from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

import os
import Chern
import shutil
from Chern import utils
from Chern.utils import git
from Chern.ChernManager import get_manager
from Chern.VObject import VObject
from Chern.utils import debug
import subprocess

manager = get_manager()
c = manager.c
p = manager.p

@register_line_magic
def mkp(line):
    "make a new project"
    return manager.new_project(line)
del mkp

@register_line_magic
def cd(line):
    # The extended cd function: cd number
    if line.isdigit():
        index = int(line)
        sub_objects = manager.c.sub_objects()
        successors = manager.c.get_successors()
        predecessors = manager.c.get_predecessors()
        total = len(sub_objects)
        if index < total:
            sub_objects.sort(key=lambda x:(x.object_type(), x.path))
            Chern.cd(manager.c.relative_path(sub_objects[index].path))
            return
        index -= total
        total = len(predecessors)
        if index < total:
            Chern.cd(manager.c.relative_path(predecessors[index].path))
            return
        index -= total
        total = len(successors)
        if index < total:
            Chern.cd(manager.c.relative_path(successors[index].path))
            return
        else:
            print("Out out index")
            return
    else:
    # The normal cd function
        Chern.cd(line, inloop=False)
del cd

# How to get a line magic
# old_mv = ip.magics_manager.magics["line"]["mv"]
@register_line_magic
def mv(line):
    """
    Move a object to another object
    """
    Chern.mv(line, inloop=False)
del mv

# Copy object
@register_line_magic
def cp(line):
    line = line.split(" ")
    old_object = line[0]
    destination = line[1]
    if os.path.exists(destination):
        destination += old_object
    os.copy(old_object, destination)
    VObject(old_object).cp(destination)
del cp

@register_line_magic
def rm(line):
    line = os.path.abspath(line)
    VObject(line).rm()
    shutil.rmtree(line)
    git.rm(line)
    git.commit("rm {}".format(manager.p.relative_path(line)))
del rm

@register_line_magic
def ls(line):
    if line == "projects":
        manager.ls_projects()
        return
    manager.c.ls()
del ls

def set_algorithm(line):
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task")
        return
    manager.c.set_algorithm(line)
    git.commit("{}:set algorithm {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(line)))

def add_rawdata(line):
    line = utils.strip_path_string(line)
    if manager.c.object_type() != "data":
        print("You can only add raw data if you are a data.")
        return
    line = line.split(" ")
    path = os.path.abspath(line[0])
    site = line[1]
    manager.c.add_rawdata(path, site)
    git.commit("{}:add raw data {} on site {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(path), site))

def add_input(line):
    line = utils.strip_path_string(line)
    # if line.startswith()
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task")
        return
    line = line.split(" ")
    path = os.path.abspath(line[0])
    alias = line[1]
    manager.c.add_input(path, alias)
    git.commit("{}:add input {} named {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(path), alias))

def add_output(line):
    line = utils.strip_path_string(line)
    # if line.startswith()
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task")
        return
    line = line.split(" ")
    path = os.path.abspath(line[0])
    alias = line[1]
    manager.c.add_output(path, alias)
    git.commit("{}:add output {} named {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(path), alias))

def add_parameter(line):
    if manager.c.object_type() != "task" and manager.c.object_type() != "directory":
        print("Can not add parameter if you are not a task or a directory")
        return
    line = line.split(" ")
    manager.c.add_parameter(line[0], line[1])

def add_algorithm(line):
    line = utils.strip_path_string(line)
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task or a directory")
        return
    line = os.path.abspath(line)
    manager.c.add_algorithm(line)

def remove_input(line):
    pass

def remove_parameter(line):
    if manager.c.object_type() != "task":
        print("Can not remove parameter if you are not a task")
        return
    manager.c.remove_parameter(line)

@register_line_magic
def add(line):
    line = line.strip()
    if line.startswith("input"):
        add_input(line.lstrip("input").strip())
    elif line.startswith("output"):
        add_output(line.lstrip("output").strip())
    elif line.startswith("algorithm"):
        add_algorithm(line.lstrip("algorithm").strip())
    elif line.startswith("site"):
        add_site(line.lstrip("site").strip())
    elif line.startswith("parameter"):
        add_parameter(line.lstrip("parameter").strip())
del add

@register_line_magic
def remove(line):
    line = line.strip()
    if line.startswith("input"):
        remove_input(line.lstrip("input").strip())
    elif line.startswith("output"):
        remove_output(line.lstrip("output").strip())
    elif line.startswith("algorithm"):
        remove_algorithm(line.lstrip("algorithm").strip())
    elif line.startswith("site"):
        remove_site(line.lstrip("site").strip())
    elif line.startswith("parameter"):
        remove_parameter(line.lstrip("parameter").strip())
del remove

@register_line_magic
def readme(line):
    if line == "edit":
        manager.c.edit_readme()
    else:
        print(manager.c.readme())
del readme

@register_line_magic
def configuration(line):
    subprocess.call("vim /home/zhaomr/.Chern/config.py", shell=True)
del configuration

@register_line_magic
def submit(line):
    if manager.c.object_type() != "task":
        print("A job can not run if it is not a task")
        return
    manager.c.submit()
del submit

from datetime import datetime
from time import time

@register_line_magic
def git(line):
    subprocess.call("git {}".format(line), shell=True)
del git

@register_line_magic
def vim(line):
    subprocesss.call("vim {}".format(line), shell=True)
    git.commit("edit file {}".format(line))
del vim

@register_line_magic
def bash(line):
    subprocess.call("bash", shell=True)
    git.commit("edit .".format(line))
del bash
