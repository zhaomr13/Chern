from Chern.kernel.VProject import VProject
from Chern.interface.ChernManager import get_manager
import os

manager = get_manager()
current_project_name = manager.get_current_project()
from Chern.interface.ChernManager import create_object_instance as obj

if current_project_name is not None:
    current_project_path = manager.get_project_path(current_project_name)
    if os.path.exists(current_project_path) is None:
        current_project_name
if current_project_name is None:
    # FIXME may exsit
    # os.mkdir(os.environ["HOME"] +"/.Chern")
    project_name = input("please input the new project name: ")
    manager.new_project(project_name)
    current_project_name = manager.get_current_project()

current_project_path = manager.get_project_path(current_project_name)
manager.p = VProject(current_project_path)
manager.c = manager.p

os.chdir(manager.c.path)


