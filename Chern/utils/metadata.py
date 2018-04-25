class ConfigFile(object):
    """ ConfigFile class, it contains the metadata.
    ConfigFile(somefile.py) can define a config file,
    where you can read and write python variables
    """
    def __init__(self, file_path):
        """ Initialize the class use a path
        Create a file if it is not initially exists
        """
        self.file_path = file_path

    def read_variable(self, variable_name, default=None):
        """ Get the content of some variable
        """
        file_path = self.file_path
        if not os.path.exists(file_path):
            return default
        # read the module
        from imp import load_source
        module = load_source("tmp_module_{0}".format(uuid.uuid4().hex), file_path)
        value = module.__dict__.get(variable_name, default)

        # remove pyc file and module instance
        remove_cache(file_path)
        del module
        return value

    def write_variable(self, variable_name, value):
        file_path = self.file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            open(file_path, "w").close()
        try_times = 10 ** 4
        for i in range(try_times):
            if not os.path.exists(file_path + ".lock"):
                break
        if os.path.exists(file_path + ".lock"):
            raise os.error

        open(file_path+".lock", "a").close()

        # Module variables, key value mapping
        from imp import load_source
        module = load_source("tmp_module_{0}".format(uuid.uuid4().hex), file_path)
        dic = module.__dict__

        # Add new variables to the list
        old_variables = dir(module)
        # DELETE print old_variables
        if variable_name not in old_variables:
            old_variables.append(variable_name)

        f = open(file_path, "w")
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
