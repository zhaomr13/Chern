import os
import imp
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/config.py"
def get_current_project():
    global global_config_path
    global_config = utils.read_variables("config", global_config_path)
    print "global_config is : ", dir(global_config)
    if "current_project" not in dir(global_config) :
        utils.write_variables(global_config, global_config_path, [("current_project", "/")])
        return "/"
    return global_config.current_project

def get_all_projects():
    global global_config_path
    global_config = utils.read_variables("config", global_config_path)
    print "get all projects :" , dir(global_config)
    if "projects_list" not in dir(global_config) :
        utils.write_variables(global_config, global_config_path, [("projects_list", [])])
        return []
    return global_config.projects_list

def get_project_path(command):
    global global_config_path
    global_config = utils.read_variables("config", global_config_path)
    print dir(global_config)
    return global_config.projects_path[command]


def switch_project(project_name):
    global global_config_path
    global_config = utils.read_variables("config", global_config_path)
    utils.write_variables(global_config, global_config_path, [("current_project", project_name)])

def new_project(project_name):
    pwd = os.getcwd()
    if os.path.exists(pwd + "/.config") :
        print "Cannot init"
        raise os.error
        return
    os.mkdir(pwd + "/.config")

    # print "Start ========================================="
    # Write information to global config file
    global global_config_path
    global_config = utils.read_variables("global_config", global_config_path)
    projects_path = global_config.projects_path if "projects_path" in dir(global_config) else {}
    projects_path[project_name] = pwd
    projects_list = global_config.projects_list if "projects_list" in dir(global_config) else []
    projects_list.append(project_name)
    utils.write_variables(global_config, global_config_path, [("current_project", project_name), ("projects_path", projects_path), ("projects_list", projects_list)])

    # Write information to the config file of the project
    config = utils.read_variables("config", pwd + "/.config/config.py")
    utils.write_variables(config, pwd + "/.config/config.py", [("ncpus", 1)])



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
        from subprocess import call
        call("vim " + get_project_path(get_current_project()) + "/.config/config.py", shell = True)
        return


    if not command_list[0] in get_all_projects():
        print "No such a project ", command_list[0], " create a new one."
        new_project(command_list[0])

    if command_list[0] in get_all_projects():
        switch_project(command_list[0])
        print "Switch to project", command_list[0]
        return "cd " + get_project_path(command_list[0]) + "\n"

    #except :
    #    print "Can not config new project for some reason"


