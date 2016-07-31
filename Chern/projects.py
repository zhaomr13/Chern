import os
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/configuration.py"
def show_project():
    global global_config_path
    config = utils.read_variables("configuation", global_config_path)
    if "current_project" not in dir(config) :
        utils.write_variables(config, global_config_path, [("current_project", "/")])
        return "/"
    return config.current_project

def get_all_projects():
    global global_config_path
    config = utils.read_variables("configuation", global_config_path)
    if "projects_list" not in dir(config) :
        utils.write_variables(config, global_config_path, [("projects_list", [])])
        return []
    return config.projects_list



def switch_project(project_name):
    global global_config_path
    config = utils.read_variables("configuation", global_config_path)
    utils.write_variables(config, global_config_path, [("current_project", project_name)])

def new_project(project_name):
    pwd = os.getcwd()
    if os.path.exists(pwd + "/.config") :
        print "Cannot init"
        raise os.error
        return
    os.mkdir(pwd + "/.config")
    global global_config_path
    config = utils.read_variables("configuation", global_config_path)
    projects_path = config.projects_path if "projects_path" in dir(config) else{}
    projects_path[project_name] = pwd
    utils.write_variables(config, global_config_path, [("current_project", project_name), ("projects_path", projects_path)])


def main(command):
    current_project = show_project()
    project_list = get_all_projects()

    if command == None :
        print "Current project is:", current_project
        print "All the projects are:"
        for obj in project_list:
            print obj
        return

    if command in project_list:
        switch_project(command)
        print "Switch to project", command
        return "cd " + get_project_path(command)

    #try :
    new_project(command)
    #except :
    #    print "Can not config new project for some reason"


