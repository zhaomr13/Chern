# Load module
import os
import sys

def read_variables(module_name, path):
    from imp import load_source
    module = load_source(module_name, path)
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
    for key, value in variables:
        if key not in old_variables:
            old_variables.append(key)

    # Change values
    for key, value in variables:
        dic[key] = value

    # Save to file
    print old_variables
    for key in old_variables:
        if not key.startswith("__") and not key.startswith("-") :
            if type(dic[key]) == str :
                f.write("%s='%s'\n"%(key, str(dic[key])) )
            else :
                f.write("%s=%s\n"%(key, str(dic[key])) )
    f.close()
    os.remove(path+".lock")


#c = read_variables("configuration", os.environ["HOME"]+"/.Chern/configuration.py")
#write_variables(c, os.environ["HOME"]+"/.Chern/configuration.py", [("hello", [3124567])])
