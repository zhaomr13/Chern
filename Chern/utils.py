# Load module
import os
import sys

def read_variables(module_name, path):
    # if the requested module is not here at the beginning
    if not os.path.exists(path): open(path, "w").close()

    # read the module
    from imp import load_source
    module = load_source(module_name, path)

    # remove pyc file
    if os.path.exists(path+"c"): os.remove(path+"c")

    return module


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
            if type(dic[key]) == str :
                f.write("%s='%s'\n"%(key, str(dic[key])) )
            else :
                f.write("%s=%s\n"%(key, str(dic[key])) )
    # DELETED print "written"
    f.close()
    os.remove(path+".lock")
    if os.path.exists(path+"c"): os.remove(path+"c")

# DELETED c = read_variables("configuration", os.environ["HOME"]+"/.Chern/configuration.py")
# DELETED write_variables(c, os.environ["HOME"]+"/.Chern/configuration.py", [("hello", [3124567])])
