import os
from Chern.utils import git
from Chern.utils import csys
from Chern.kernel.VObject import VObject
from Chern.utils import utils
from Chern.utils.utils import debug
from Chern.interface.ChernManager import get_manager
from Chern.interface.ChernManager import create_object_instance
import shutil
from Chern.kernel.VTask import create_task
from Chern.kernel.VAlgorithm import create_algorithm
from Chern.kernel.VDirectory import create_directory
from Chern.kernel.ChernDatabase import ChernDatabase
from Chern.utils.pretty import color_print
from Chern.utils.pretty import colorize

manager = get_manager()
cherndb = ChernDatabase.instance()

def cd_project(line):
    manager.switch_project(line)
    os.chdir(manager.c.path)
    manager.p = manager.c


def cd(line, inloop=True):
    """
    Change the directory.
    The standalone Chern.cd command is protected.
    """
    if line.isdigit():
        index = int(object)
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
            color_print("Out of index", "remind")
            return
    else:
        # cd can be used to change directory using absolute path
        line = utils.special_path_string(line)
        if line.startswith("@/") or line == "@":
            line = manager.p.path + line.strip("@")
        else:
            line = os.path.abspath(line)

        # Check available
        if os.path.relpath(line, manager.p.path).startswith(".."):
            print("Can not go to a place not in the project")
            return
        if not os.path.exists(line):
            print("Directory not exists")
            return
        manager.switch_current_object(line)
        os.chdir(manager.c.path)

def mv(line, inloop=True):
    """
    Move or rename file. Will keep the link relationship.
    mv SOURCE DEST
    or
    mv SOURCE DIRECTORY
    BECAREFULL!!
    mv SOURCE1 SOURCE2 SOURCE3 ... DIRECTORY is not supported
    use loop instead
    """
    line = line.split(" ")
    # Deal with the situation that command is not mv a b
    if len(line) != 2:
        print("Please lookup the USAGE of mv")
        return
    source = utils.special_path_string(line[0])
    destination = utils.special_path_string(line[1])
    if destination.startswith("p/") or destination == "p":
        destination = os.path.normpath(manager.p.path + destination.strip("p"))
    else:
        destination = os.path.abspath(destination)
    if os.path.exists(destination):
        destination += "/" + source
    if source.startswith("p/") or source == "p":
        source = os.path.normpath(manager.p.path+destination.strip("p"))
    else:
        source = os.path.abspath(source)

    VObject(source).mv(destination)

def cp(line, inloop=True):
    """
    Move or rename file. Will keep the link relationship.
    mv SOURCE DEST
    or
    mv SOURCE DIRECTORY
    BECAREFULL!!
    mv SOURCE1 SOURCE2 SOURCE3 ... DIRECTORY is not supported
    use loop instead
    """
    line = line.split(" ")
    # Deal with the situation that command is not mv a b
    if len(line) != 2:
        print("Please lookup the USAGE of cp")
        return
    source = utils.special_path_string(line[0])
    destination = utils.special_path_string(line[1])
    if destination.startswith("p/") or destination == "p":
        destination = os.path.normpath(manager.p.path + destination.strip("p"))
    else:
        destination = os.path.abspath(destination)
    if os.path.exists(destination):
        destination += "/" + source
    if source.startswith("p/") or source == "p":
        source = os.path.normpath(manager.p.path+destination.strip("p"))
    else:
        source = os.path.abspath(source)

    VObject(source).cp(destination)

def ls(line):
    """
    The function ls should not be defined here
    """
    manager.c.ls()

def mkalgorithm(obj, use_template=False):
    """ Create a new algorithm """
    line = csys.refine_path(obj, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create algorithm here")
        return
    create_algorithm(line, use_template)

def mktask(line, inloop=True):
    """ Create a new task """
    line = csys.refine_path(line, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create task here")
        return
    create_task(line, inloop)

def mkdir(line, inloop=True):
    """ Create a new directory """
    line = csys.refine_path(line, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create directory here")
        return
    create_directory(line, inloop)

def rm(line):
    line = os.path.abspath(line)
    VObject(line).rm()

def add_source(line):
    # line = os.path.abspath(line)
    manager.c.add_source(line)

def jobs(line):
    object_type = manager.c.object_type()
    if object_type != "algorithm" and object_type != "task":
        print("Not able to found job")
        return
    manager.c.jobs()

def status():
    if manager.c.object_type() == "task" or manager.c.object_type == "algorithm":
        status = manager.c.status()
        if status == "built" or status == "done":
            color_tag = "success"
        elif status == "failed":
            color_tag = "warning"
        elif status == "running":
            color_tag = "running"
        else:
            color_tag = "normal"
        color_print(status, color_tag)

    sub_objects = manager.c.sub_objects()
    sub_objects.sort(key=lambda x:(x.object_type(),x.path))
    for obj in sub_objects:
        status = create_object_instance(obj.path).status()
        if status == "built" or status == "done" or status == "finished":
            color_tag = "success"
        elif status == "failed" or status == "unfinished":
            color_tag = "warning"
        elif status == "running":
            color_tag = "running"
        else:
            color_tag = "normal"

        print("{1:<20} {0:<20} ".format(colorize(status, color_tag), manager.c.relative_path(obj.path)) )

def add_input(path, alias):
    if manager.c.object_type() != "task":
        print("Unable to call add_input if you are not in a task.")
        return
    manager.c.add_input(path, alias)

