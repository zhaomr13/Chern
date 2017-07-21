"""
Created by Mingrui Zhao @ 2017
define some classes and functions used throughout the project
"""
# Load module
import os
import shutil

def strip_path_string(path_string):
    """
    Remove the "/" in the end of the string
    and the " " in the begin and the end of the string.
    replace the "." in the string to "/"
    """
    path_string = path_string.strip(" ")
    path_string = path_string.rstrip("/")
    return path_string

def colorize(string, color):
    """
    Make the string have color
    """
    if color == "debug":
        return "\033[31m" + string + "\033[m"
    return string

def debug(*arg):
    """
    Print debug string
    """
    print(colorize("debug >> ", "debug"), end="")
    for s in arg:
        print(colorize(s.__str__(), "debug"), end=" ")
    print("*")

def remove_cache(file_path):
    """
    Remove the python cache file *.pyc *.pyo *.__pycache
    file_path = somewhere/somename.py
            or  somename.py
    """
    file_path = strip_path_string(file_path)
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
    """
    ConfigFile class
    ConfigFile(somefile.py) can define a config file,
    where you can read and write python variables
    """
    def __init__(self, file_path):
        """
        Initialize the class use a path
        Create a file if it is not initially exists
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            open(file_path, "w").close()

    def read_variable(self, variable_name):
        """
        Get the content of some variable
        """
        # read the module
        from imp import load_source
        # print(file_path)
        file_path = self.file_path
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
            if not os.path.exists(file_path + ".lock"):
                break
        if os.path.exists(file_path + ".lock"):
            raise os.error

        open(file_path+".lock", "a").close()
        debug("write to", file_path)
        f = open(file_path, "w")

        # Module variables, key value mapping
        # dic = {key:value for key,value in module.__dict__.iteritems()}
        from imp import load_source
        module = load_source("tmp_module_{0}".format(file_path), file_path)
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
            if not key.startswith("__") and not key.startswith("-"):
                if type(dic[key]) == str:
                    f.write("%s=u'%s'\n"%(key, str(dic[key])))
                elif type(dic[key]) == str:
                    f.write("%s='%s'\n"%(key, str(dic[key])))
                else:
                    f.write("%s=%s\n"%(key, str(dic[key])))
        # DELETED print "written"
        f.close()
        os.remove(file_path+".lock")
        del module
        remove_cache(file_path)

    def modify_variable(self):
        """
        Might be used in the future
        FIXME
        """
        pass
