# Load module
import os
import sys
import shutil

def remove_cache(file_path):
    if os.path.exists(file_path+"c"):
        os.remove(file_path+"c")
    if os.path.exists(file_path+"o"):
        os.remove(file_path+"o")
    index = file_path.rfind("/")
    if index == -1:
        shutil.rmtree("__pycache__")
    else:
        shutil.rmtree(file_path[:index] + "/__pycache__")

class ConfigFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        pass

    def read_variable(self, variable_name):
        # if the requested module is not here at the beginning
        file_path = self.file_path
        if not os.path.exists(file_path):
            open(file_path, "w").close()

        # read the module
        from imp import load_source
        # print(file_path)
        module = load_source("tmp_module", file_path)
        value = module.__dict__.get(variable_name)
        # print(value)

        # remove pyc file and module instance
        remove_cache(file_path)
        del module
        return value

    def write_variable(self, variable_name, value):
        file_path = self.file_path
        try_times = 10 ** 4
        for i in range(try_times):
            if not os.path.exists(file_path + ".lock") : break
        if os.path.exists(file_path + ".lock") :
            raise os.error

        open(file_path+".lock", "a").close()
        f = open(file_path, "write")

        # Module variables, key value mapping
        # dic = {key:value for key,value in module.__dict__.iteritems()}
        from imp import load_source
        module = load_source("tmp_module", file_path)
        dic = module.__dict__

        # Add new variables to the list
        old_variables = dir(module)
        # DELETE print old_variables
        if variable_name not in old_variables:
            old_variables.append(variable_name)

        # Change values
        dic[variable_name] = value

        # Save to file
        for key in old_variables:
            if not key.startswith("__") and not key.startswith("-") :
                if type(dic[key]) == unicode:
                    f.write("%s=u'%s'\n"%(key, unicode(dic[key])))
                elif type(dic[key]) == str:
                    f.write("%s='%s'\n"%(key, str(dic[key])) )
                else :
                    f.write("%s=%s\n"%(key, str(dic[key])) )
        # DELETED print "written"
        f.close()
        os.remove(file_path+".lock")
        del module
        remove_cache(file_path)

    def modify_variable(self):
        pass

def write_variables(module, path, variables):

    try_times = 10 ** 4
    for i in xrange(try_times):
        if not os.path.exists(path + ".lock") : break
    if os.path.exists(path + ".lock") :
        raise os.error

    open(path+".lock", "a").close()
    f = open(path, "write")

    # Module variables, key value mapping
    dic = {key:value for key,value in module.__dict__.iteritems()}

    # Add new variables to the list
    old_variables = dir(module)
    # DELETE print old_variables
    for key, value in variables:
        if key not in old_variables:
            old_variables.append(key)

    # Change values
    for key, value in variables:
        dic[key] = value

    # Save to file
    for key in old_variables:
        if not key.startswith("__") and not key.startswith("-") :
            if type(dic[key]) == unicode:
                f.write("%s=u'%s'\n"%(key, unicode(dic[key])))
            elif type(dic[key]) == str :
                f.write("%s='%s'\n"%(key, str(dic[key])) )
            else :
                f.write("%s=%s\n"%(key, str(dic[key])) )
    # DELETED print "written"
    f.close()
    os.remove(path+".lock")
    if os.path.exists(path+"c"): os.remove(path+"c")

def get_global_config():
    global_config = read_variables("global_config", os.environ["HOME"]+"/.Chern/config.py")
    return global_config

def get_project_config(global_config, project):
    project_path = global_config.projects_path[project]
    project_config = read_variables("project_config", project_path+"/.config/config.py")
    return project_config

def strip_path_string(path_string):
    if path_string.endswith("/"):
        return path_string[:-1]
    else:
        return path_string

# DELETED c = read_variables("configuration", os.environ["HOME"]+"/.Chern/configuration.py")
# DELETED write_variables(c, os.environ["HOME"]+"/.Chern/configuration.py", [("hello", [3124567])])
def debug(*arg):
    for s in arg:
        print(s,)
        print("")
