from Chern.VProject import VProject
from Chern.ChernManager import get_manager
import os

manager = get_manager()
current_project_name = manager.get_current_project()
if current_project_name != "/":
    current_project_path = manager.get_project_path(current_project_name)

if current_project_name != "/":
    manager.p = VProject(current_project_path)
    manager.c = manager.p

os.chdir(manager.c.path)


