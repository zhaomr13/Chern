import os
import shutil
import imp
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/config.py"
def get_current_project():
    global global_config_path
    global_config = utils.get_global_config()
    if "current_project" not in dir(global_config) :
        utils.write_variables(global_config, global_config_path, [("current_project", "/")])
        return "/"
    return global_config.current_project

def get_all_projects():
    global global_config_path
    global_config = utils.get_global_config()
    if "projects_list" not in dir(global_config) :
        utils.write_variables(global_config, global_config_path, [("projects_list", [])])
        return []
    return global_config.projects_list

def get_project_path(command):
    global global_config_path
    global_config = utils.get_global_config()
    return global_config.projects_path[command]


def switch_project(project_name):
    global global_config_path
    global_config = utils.get_global_config()
    utils.write_variables(global_config, global_config_path, [("current_project", project_name)])

def new_project(project_name):

    #def check the forbidden name
    forbidden_names = ["config", "new", "projects", "start"]
    def check_project_failed(project_name, forbidden_names):
        message = "The following project names are forbidden:"
        message += "\n    "
        for name in forbidden_names:
            message += name + ", "
        raise Exception(message)
    if project_name in forbidden_names:
        check_project_failed(project_name, forbidden_names)

    ncpus = int(input("Please input the number of cpus to use for this project: "))

    pwd = os.getcwd()
    if os.path.exists(pwd + "/.config") :
        raise Exception("The folder already has configuration file")

    os.mkdir(pwd + "/.config")
    os.mkdir(pwd + "/Algs")
    os.mkdir(pwd + "/tasks")
    os.mkdir(pwd + "/data")
    os.mkdir(pwd + "/result")

    global_config = utils.get_global_config()
    projects_path = global_config.projects_path if "projects_path" in dir(global_config) else {}
    projects_path[project_name] = pwd
    projects_list = global_config.projects_list if "projects_list" in dir(global_config) else []
    projects_list.append(project_name)
    utils.write_variables(global_config, global_config_path, [("current_project", project_name), ("projects_path", projects_path), ("projects_list", projects_list)])
    # Write information to the config file of the project
    global_config = utils.get_global_config()
    project_config = utils.get_project_config(global_config, project_name)
    utils.write_variables(project_config, pwd + "/.config/config.py", [("ncpus", ncpus)])


def update_configuration():
    if not os.path.exists(global_config_path):
        shutil.copyfile(os.environ["CHENSYSPATH"]+"/config/global_config.py", os.environ["HOME"])

def main(command_list):
    #current_project = get_current_project()
    #projects_list = get_all_projects()

    if len(command_list) == 0 :
        print "Current project is:", get_current_project()
        print "All the projects are:",
        for obj in get_all_projects():
            print obj,
        return

    if command_list[0] == "config":
        update_configuration()
        from subprocess import call
        call("vim " + get_project_path(get_current_project()) + "/.config/config.py", shell = True)
        return

    if not command_list[0] in get_all_projects():
        print "No such a project ", command_list[0], " try to create a new one."
        #try:
        new_project(command_list[0])
        #except Exception as e:
        #    print e

    if command_list[0] in get_all_projects():
        switch_project(command_list[0])
        print "Switch to project", command_list[0]
        return "cd " + get_project_path(command_list[0]) + "\n"

    #except :
    #    print "Can not config new project for some reason"


