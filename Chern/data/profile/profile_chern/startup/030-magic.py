from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

import os
import Chern
import shutil
from Chern import utils
from Chern.interface.ChernManager import get_manager
from Chern.interface import shell
from Chern.kernel.VObject import VObject
from Chern.utils.utils import debug
import subprocess

manager = get_manager()

@register_line_magic
def mkp(line):
    "make a new project"
    return manager.new_project(line)
del mkp

@register_line_magic
def cd(line):
    """ The extended cd function: cd number
    """
    if line.isdigit():
        index = int(line)
        sub_objects = manager.c.sub_objects()
        successors = manager.c.successors()
        predecessors = manager.c.predecessors()
        total = len(sub_objects)
        if index < total:
            sub_objects.sort(key=lambda x:(x.object_type(), x.path))
            shell.cd(manager.c.relative_path(sub_objects[index].path))
            return
        index -= total
        total = len(predecessors)
        if index < total:
            shell.cd(manager.c.relative_path(predecessors[index].path))
            return
        index -= total
        total = len(successors)
        if index < total:
            shell.cd(manager.c.relative_path(successors[index].path))
            return
        else:
            print("Out out index")
            return
    else:
        shell.cd(line, inloop=False)
del cd

# How to get a line magic
# old_mv = ip.magics_manager.magics["line"]["mv"]
@register_line_magic
def mv(line):
    """ Move a object to another object
    """
    shell.mv(line, inloop=False)
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
    shell.rm(line)
del rm

@register_line_magic
def helpme(line):
    manager.c.helpme(line)
del helpme

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

def remove_site(line):
    pass

def add_parameter(line):
    if manager.c.object_type() != "task" and manager.c.object_type() != "directory":
        print("Can not add parameter if you are not a task or a directory")
        return
    line = line.split(" ")
    if len(line) != 2:
        print("Add paramter require 2 arguments.")
        return
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

def remove_output(line):
    pass

def remove_parameter(line):
    if manager.c.object_type() != "task":
        print("Can not remove parameter if you are not a task")
        return
    manager.c.remove_parameter(line)

@register_line_magic
def define(line):
    line = line.strip()
    if line.startswith("algorithm"):
        set_algorithm(line.lstrip("algorithm").strip())
    elif line.startswith(""):
        pass

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
    else:
        line = line.split(" ")
        manager.c.add(line[0], line[1])
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
    chern_config_path = os.environ["HOME"]
    subprocess.call("vim " + chern_config_path+"/config.py", shell=True)
del configuration

@register_line_magic
def submit(line):
    manager.c.submit()
del submit

@register_line_magic
def stdout(line):
    print(manager.c.stdout())
del stdout

@register_line_magic
def stderr(line):
    print(manager.c.stderr())
del stderr

@register_line_magic
def kill(line):
    print(manager.c.kill())
del kill

@register_line_magic
def resubmit(line):
    manager.c.resubmit()
del resubmit

@register_line_magic
def impress(line):
    manager.c.impress()
del impress

@register_line_magic
def git(line):
    subprocess.call("git {}".format(line), shell=True)
del git

@register_line_magic
def vim(line):
    subprocess.call("vim {}".format(line), shell=True)
    git.commit("edit file {}".format(line))
del vim

@register_line_magic
def download(line):
    manager.c.download()
del download

@register_line_magic
def bash(line):
    subprocess.call("bash", shell=True)
    git.commit("edit .".format(line))
del bash

@register_line_magic
def check(line):
    if line == "":
        line = "local"
    manager.c.check(line)
del check
