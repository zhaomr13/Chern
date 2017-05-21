from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

import os
import Chern

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
del cdp
