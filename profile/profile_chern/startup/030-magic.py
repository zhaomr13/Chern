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
def lmagic_hello(line):
    "my line magic"
    return line

@register_cell_magic
def cmagic(line, cell):
    "my cell magic"
    return line, cell

@register_line_cell_magic
def lcmagic(line, cell=None):
    "Magic that works both as %lcmagic and as %%lcmagic"
    if cell is None:
        print("Called as line magic")
        return line
    else:
        print("Called as cell magic")
        return line, cell

# In an interactive session, we need to delete these to avoid
# name conflicts for automagic to work on line magics.
# del lmagic, lcmagic

@register_line_magic
def c(line):
    return manager.c
del c

@register_line_magic
def p(line):
    return manager.p
del p

@register_line_magic
def mkp(line):
    "make a new project"
    return Chern.projects.new_project(line)
del mkp

@register_line_magic
def lsp(line):
    "list all the projects"
    projects_list = Chern.projects.get_all_projects()
    for project_name in projects_list:
        print(project_name)
del lsp

@register_line_magic
def cdp(line):
    "change to project"
    os.chdir(Chern.projects.get_project_path(line))
    print(type(line))
    projects.switch_project(line)
del cdp

@register_line_magic
def cd(line):
    # cd can be used to change project
    line = utils.strip_path_string(line)
    if line.startswith("projects"):
        manager.switch_project()
        os.chdir(manager.c.path)
        return

    # cd can be used to change directory using absolute path
    if line.startswith("p"):
        line = manager.p.path + line[1:]
        new_object = manager.create_object_instance()
        del manager.c
        manager.c = new_object
        return


    line = os.getcwd() + "/" + line
    if os.path.relpath(line, manager.p.path).startswith(".."):
        print("Can not go to a place not in the project")
        return
    new_object = manager.create_object_instance(line)
    del manager.c
    manager.c = new_object
    print(c.readme())
    os.chdir(manager.c.path)
del cd

old_ls = ip.magics_manager.magics["line"]["ls"]

@register_line_magic
def ls(line):
    if line == "projects":
        manager.ls_projects()
        return
    # old_ls()
    manager.c.ls()
del ls
# ip.magic("alias_magic ls lsp")

@register_line_magic
def set_algorithm(line):
    if manager.c.get_type() != "task":
        print("Can not set the algorithm if you are not a task")
        return
    manager.c.set_algorithm(line)
