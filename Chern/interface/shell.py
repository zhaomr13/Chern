import os
import Chern
from Chern.utils import git
from Chern.utils import csys
from Chern.kernel.VObject import VObject
from Chern.utils import utils
from Chern.utils.utils import debug
from Chern.interface.ChernManager import get_manager
import shutil
from Chern.kernel.VTask import create_task
from Chern.kernel.VAlgorithm import create_algorithm
from Chern.kernel.VDirectory import create_directory
from Chern.kernel.ChernDatabase import ChernDatabase

manager = get_manager()
cherndb = ChernDatabase.instance()

def cd(line, inloop=True):
    """
    Change the directory.
    The standalone Chern.cd command is protected.
    """
    if line.startswith("project"):
        if inloop:
            print("cd to a project in the script is not allowed")
            return
        debug(line)
        line = utils.strip_path_string(line.lstrip("project"))
        debug(line)
        manager.switch_project(line)
        os.chdir(manager.c.path)
        manager.p = manager.c
        return

    # cd can be used to change directory using absolute path
    line = utils.special_path_string(line)
    if line.startswith("p/") or line == "p":
        line = manager.p.path + line.strip("p")
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

    shutil.copytree(source, destination)
    VObject(source).mv(destination)
    shutil.rmtree(source)

def cp(line):
    line = line.split(" ")
    old_object = line[0]
    destination = line[1]
    if os.path.exists(destination):
        destination += old_object
    os.copy(old_object, destination)
    VObject(old_object).cp(destination)

def ls(line):
    """
    The function ls should not be defined here
    """
    pass

def mkalgorithm(line, inloop=True):
    """ Create a new algorithm """
    line = csys.special_path_string(line)
    line = csys.refine_path(line, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create algorithm here")
        return
    create_algorithm(line, inloop)
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)

def mktask(line, inloop=True):
    """ Create a new task """
    line = csys.special_path_string(line)
    line = csys.refine_path(line, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create task here")
        return
    create_task(line, inloop)
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)

def mkdir(line, inloop=True):
    line = utils.special_path_string(line)
    if line.startswith("p/") or line == "p":
        line = manager.p.path + line.strip("p")
    else:
        line = os.path.abspath(line)
    create_directory(line, inloop)
    manager.switch_current_object(line)
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)

def rm(line):
    line = os.path.abspath(line)
    VObject(line).rm()
