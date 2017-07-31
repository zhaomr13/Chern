import os
import Chern
from Chern.VObject import VObject
from Chern import utils
from Chern.utils import debug
from Chern.ChernManager import get_manager
import shutil
from Chern.VTask import create_task
from Chern.VAlgorithm import create_algorithm
from Chern.VData import create_data
from Chern.VDirectory import create_directory

manager = get_manager()

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
    Chern.git.add(destination)
    VObject(source).mv(destination)
    shutil.rmtree(source)
    Chern.git.rm(source)
    Chern.git.commit("mv {} to {}".format(manager.p.relative_path(source), manager.p.relative_path(destination)))

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

def mkdata(line, inloop=True):
    line = utils.special_path_string(line)
    if line.startswith("p/") or line == "p":
        line = manager.p.path + line.strip("p")
    else:
        line = os.path.abspath(line)
    create_data(line, inloop)
    manager.switch_current_object(line)
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)
    Chern.git.add(line)
    Chern.git.commit("Create data at {}".format(manager.p.relative_path(line)))

def mkalgorithm(line, inloop=True):
    line = utils.special_path_string(line)
    if line.startswith("p/") or line == "p":
        line = manager.p.path + line.strip("p")
    else:
        line = os.path.abspath(line)
    create_algorithm(line, inloop)
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)
    Chern.git.add(line)
    Chern.git.commit("Create algorithm at {}".format(manager.p.relative_path(line)))

def mktask(line, inloop=True):
    line = utils.special_path_string(line)
    if line.startswith("p/") or line == "p":
        line = manager.p.path + line.strip("p")
    else:
        line = os.path.abspath(line)
    create_task(line, inloop)
    manager.switch_current_object(line)
    manager.c.set_update_time()
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)
    Chern.git.add(line)
    Chern.git.commit("Create task at {}".format(manager.p.relative_path(line)))

def mkdir(line, inloop=True):
    line = utils.special_path_string(line)
    if line.startswith("p/") or line == "p":
        line = manager.p.path + line.strip("p")
    else:
        line = os.path.abspath(line)
    create_directory(line, inloop)
    manager.switch_current_object(line)
    manager.c.set_update_time()
    if not inloop:
        manager.switch_current_object(line)
        os.chdir(manager.c.path)
    Chern.git.add(line)
    Chern.git.commit("Create directory at {}".format(manager.p.relative_path(line)))
