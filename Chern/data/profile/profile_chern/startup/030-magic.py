from IPython.core.magic import register_line_magic
import os
import subprocess
from Chern.utils import csys
from Chern.utils.pretty import color_print
from Chern.interface.ChernManager import get_manager
from Chern.interface import shell
import click
from click.testing import CliRunner

manager = get_manager()
runner = CliRunner()

#----------
@click.command()
@click.argument("project")
def cd_project(project):
    """ switch project
    """
    shell.cd_project(project)

click_cd_project = cd_project

@register_line_magic
def cd_project(line):
    """ The extended cd function: cd number
    """
    result = runner.invoke(click_cd_project, line.split())
    print(result.output.rstrip("\n"))
del cd_project

@register_line_magic
def cdproject(line):
    """ The extended cd function: cd number
    """
    result = runner.invoke(click_cd_project, line.split())
    print(result.output.rstrip("\n"))
del cdproject

#----------
@click.command()
@click.argument("object")
def cd(object):
    """ Switch directory or object
    """
    shell.cd(object)
click_cd = cd

@register_line_magic
def cd(line):
    """ The extended cd function: cd number
    """
    result = runner.invoke(click_cd, line.split())
    output = result.output.rstrip("\n")
    if output != "":
        print(output)
del cd

@register_line_magic
def mv(line):
    """ Move a object to another object
    """
    shell.mv(line)
del mv

# Copy object
@register_line_magic
def cp(line):
    shell.cp(line)
del cp

@register_line_magic
def rm(line):
    shell.rm(line)
del rm

@register_line_magic
def helpme(line):
    commands = line.split()
    if commands == []:
        manager.c.helpme("")
        return
    commands.append("--help")
    func = globals()["click_" + commands[0]]
    result = runner.invoke(func, commands[1:])
    print(result.output.rstrip("\n"))
del helpme

@click.command()
@click.option("-r/-R", "--show-readme/--hide-readme", default=True, help="Show readme")
@click.option("-p/-P", "--show-predecessors/--hide-predecessors", default=True, help="Show predecessors")
@click.option("-c/-C", "--show-subobjects/--hide-subobjects", default=True, help="Show subobjects")
@click.option("-n/-N", "--show-successors/--hide-successors", default=False, help="Show successors")
@click.option("-t/-T", "--show-status/--hide-status", default=False, help="Show status")
@click.option("-a", "--show-all", is_flag=True, default=False, help="Show all")
def ls(show_readme, show_predecessors, show_subobjects, show_successors, show_status, show_all):
    """ switch project
    """
    if show_all:
        show_readme = True
        show_predecessors = True
        show_subobjects = True
        show_successors = True
        show_status = True
    manager.c.ls(show_readme, show_predecessors, show_subobjects, show_status, show_successors)

click_ls = ls

@register_line_magic
def ls(line):
    """ The extended cd function: cd number
    """
    result = runner.invoke(click_ls, line.split())
    print(result.output.rstrip("\n"))
del ls

@register_line_magic
def ls_projects(line):
    """ The extended cd function: cd number
    """
    manager.ls_projects()
del ls_projects

@register_line_magic
def ll(line):
    shell.ls(line)
del ll

#----------
@click.command()
@click.argument("PATH")
@click.argument("ALIAS")
def add_input(path, alias):
    """ Add input task
    """
    shell.add_input(path, alias)
click_add_input = add_input

@register_line_magic
def add_input(line):
    """
    """
    result = runner.invoke(click_add_input, line.split())
    output = result.output.rstrip("\n")
    if output != "":
        print(output)
del add_input

@register_line_magic
def addinput(line):
    """
    """
    result = runner.invoke(click_add_input, line.split())
    print(result.output.rstrip("\n"))
del addinput

#----------
@click.command()
@click.argument("ALIAS")
def remove_input(alias):
    """ Remove input task
    """
    shell.remove_input(alias)
click_remove_input = remove_input

@register_line_magic
def remove_input(line):
    """
    """
    result = runner.invoke(click_remove_input, line.split())
    output = result.output.rstrip("\n")
    if output != "":
        print(output)
del remove_input

@register_line_magic
def removeinput(line):
    """
    """
    result = runner.invoke(click_remove_input, line.split())
    print(result.output.rstrip("\n"))
del removeinput




def set_algorithm(line):
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task")
        return
    manager.c.set_algorithm(line)
    # git.commit("{}:set algorithm {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(line)))


    # git.commit("{}:add input {} named {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(path), alias))

def add_output(line):
    line = csys.strip_path_string(line)
    # if line.startswith()
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task")
        return
    line = line.split(" ")
    path = os.path.abspath(line[0])
    alias = line[1]
    manager.c.add_output(path, alias)
    # git.commit("{}:add output {} named {}".format(manager.p.relative_path(manager.c.path), manager.p.relative_path(path), alias))

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
    line = csys.strip_path_string(line)
    if manager.c.object_type() != "task":
        print("Can not set the algorithm if you are not a task or a directory")
        return
    line = os.path.abspath(line)
    manager.c.add_algorithm(line)


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
    elif line.startswith("parameter"):
        add_parameter(line.lstrip("parameter").strip())
    elif line.startswith("source"):
        shell.add_source(line.lstrip("source").strip())
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
    elif line.startswith("site"):
        remove_site(line.lstrip("site").strip())
    elif line.startswith("parameter"):
        remove_parameter(line.lstrip("parameter").strip())
    else:
        manager.c.remove(line)
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
    subprocess.call("vim " + chern_config_path+"/config.json", shell=True)
del configuration

@register_line_magic
def submit(line):
    manager.c.submit()
del submit

@register_line_magic
def resubmit(line):
    manager.c.resubmit()
del resubmit

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
def view(line):
    manager.c.view(line)
del view

@register_line_magic
def jobs(line):
    shell.jobs(line)
del jobs

@register_line_magic
def git(line):
    subprocess.call("git {}".format(line), shell=True)
del git

@register_line_magic
def vim(line):
    subprocess.call("vim {}".format(line), shell=True)
    # git.commit("edit file {}".format(line))
del vim

@register_line_magic
def download(line):
    manager.c.download()
del download

@register_line_magic
def bash(line):
    subprocess.call("bash", shell=True)
    # git.commit("edit .".format(line))
del bash

@register_line_magic
def check(line):
    if line == "":
        line = "local"
    manager.c.check(line)
del check
