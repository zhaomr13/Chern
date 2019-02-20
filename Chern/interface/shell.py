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
from Chern.kernel.ChernCommunicator import ChernCommunicator

import time

manager = get_manager()
cherndb = ChernDatabase.instance()
cherncc = ChernCommunicator.instance()

def cd_project(line):
    manager.switch_project(line)
    os.chdir(manager.c.path)

def shell_cd_project(line):
    cd_project(line)
    print(manager.c.path)

def cd(line):
    """
    Change the directory.
    The standalone Chern.cd command is protected.
    """
    line = line.rstrip("\n")
    if line.isdigit():
        index = int(line)
        sub_objects = manager.c.sub_objects()
        successors = manager.c.successors()
        predecessors = manager.c.predecessors()
        total = len(sub_objects)
        if index < total:
            sub_objects.sort(key=lambda x:(x.object_type(), x.path))
            cd(manager.c.relative_path(sub_objects[index].path))
            return
        index -= total
        total = len(predecessors)
        if index < total:
            cd(manager.c.relative_path(predecessors[index].path))
            return
        index -= total
        total = len(successors)
        if index < total:
            cd(manager.c.relative_path(successors[index].path))
            return
        else:
            color_print("Out of index", "remind")
            return
    else:
        # cd can be used to change directory using absolute path
        line = utils.special_path_string(line)
        if line.startswith("@/") or line == "@":
            line = csys.project_path() + line.strip("@")
        else:
            line = os.path.abspath(line)

        # Check available
        if os.path.relpath(line, csys.project_path()).startswith(".."):
            print("Can not go to a place not in the project")
            return
        if not os.path.exists(line):
            print("Directory not exists")
            return
        manager.switch_current_object(line)
        os.chdir(manager.c.path)

def mv(source, destination):
    """
    Move or rename file. Will keep the link relationship.
    mv SOURCE DEST
    or
    mv SOURCE DIRECTORY
    BECAREFULL!!
    mv SOURCE1 SOURCE2 SOURCE3 ... DIRECTORY is not supported
    use loop instead
    """
    if destination.startswith("@/") or destination == "@":
        destination = os.path.normpath(csys.project_path() + destination.strip("@"))
    else:
        destination = os.path.abspath(destination)
    if os.path.exists(destination):
        destination += "/" + source
    if source.startswith("@/") or source == "@":
        source = os.path.normpath(csys.project_path() +destination.strip("@"))
    else:
        source = os.path.abspath(source)

    VObject(source).move_to(destination)

def cp(source, destination):
    """
    Move or rename file. Will keep the link relationship.
    mv SOURCE DEST
    or
    mv SOURCE DIRECTORY
    BECAREFULL!!
    mv SOURCE1 SOURCE2 SOURCE3 ... DIRECTORY is not supported
    use loop instead
    """
    if manager.c.object_type() == "task":
        manager.c.cp(source, destination)
        return

    if destination.startswith("@/") or destination == "@":
        destination = os.path.normpath(manager.p.path + destination.strip("@"))
    else:
        destination = os.path.abspath(destination)

    if os.path.exists(destination):
        destination += "/" + os.path.basename(source)

    if source.startswith("@/") or source == "@":
        source = os.path.normpath(manager.p.path+destination.strip("@"))
    else:
        source = os.path.abspath(source)

    VObject(source).copy_to(destination)

def ls(line):
    """
    The function ls should not be defined here
    """
    manager.current_object().ls()

def short_ls(line):
    """
    The function ls should not be defined here
    """
    manager.c.short_ls()

def mkalgorithm(obj, use_template=False):
    """ Create a new algorithm """
    line = csys.refine_path(obj, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create algorithm here")
        return
    create_algorithm(line, use_template)

def mktask(line):
    """ Create a new task """
    line = csys.refine_path(line, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create task here")
        return
    create_task(line)

def mkdir(line):
    """ Create a new directory """
    line = csys.refine_path(line, cherndb.project_path())
    parent_path = os.path.abspath(line+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "directory" and object_type != "project":
        print("Not allowed to create directory here")
        return
    create_directory(line)

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
    consult_id = time.time()
    if manager.c.object_type() == "task" or manager.c.object_type() == "algorithm":
        if manager.c.object_type() == "task":
            status = manager.c.status(consult_id)
        else:
            status = manager.c.status(consult_id)
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
        status = create_object_instance(obj.path).status(consult_id)
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

def remove_input(alias):
    if manager.c.object_type() != "task":
        print("Unable to call remove_input if you are not in a task.")
        return
    manager.c.remove_input(alias)

def add_host(host, url):
    cherncc.add_host(host, url)

def hosts():
    hosts = cherncc.hosts()
    urls = cherncc.urls()
    print("{0:<20}{1:20}".format("HOSTS", "STATUS"))
    for host in hosts:
        status = cherncc.host_status(host)
        color_tag = {"ok":"ok", "unconnected":"warning"}[status]
        print("{0:<20}{1:20}".format(host, colorize(status, color_tag)))
