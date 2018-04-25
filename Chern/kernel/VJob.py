import os
from Chern.utils import utils
from Chern.utils import csys

class VJob(object):
    """ Virtual class of the objects, including VVolume, VImage, VContainer
    """

    def __init__(self, path):
        """ Initialize the project the only **information** of a object instance
        """
        self.path = csys.strip_path_string(path)
        self.config_file = metadata.ConfigFile(self.path+"/.chern/config.json")

    def __str__(self):
        """ Define the behavior of print(vobject)
        """
        return self.path

    def __repr__(self):
        """ Define the behavior of print(vobject)
        """
        return self.path

    def relative_path(self, path):
        """ Return a path relative to the path of this object
        """
        return os.path.relpath(path, self.path)

    def job_type(self, path=None):
        """ Return the type of the object under a specific path.
        If path is left blank, return the type of the object itself.
        """
        if path is None:
            path = self.path
        # simply read object_type in .chern/config.json
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        return config_file.read_variable("job_type")


    def error(self):
        if os.path.exists(self.path+"/error"):
            f = open(self.path+"/error")
            error = f.read()
            f.close()
            return error
        else:
            return ""

    def append_error(self, message):
        with open(self.path+"/error", "w") as f:
            f.write(message)
            f.write("\n")


    def add_arc_from(self, path):
        """ Add an link from the path object to this object
        """
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        succ_str = config_file.read_variable("successors")
        if succ_str is None:
            succ_str = []
        succ_str.append(self.path)
        config_file.write_variable("successors", succ_str)

        pred_str = self.config_file.read_variable("predecessors")
        if pred_str is None:
            pred_str = []
        pred_str.append(path)
        self.config_file.write_variable("predecessors", pred_str)

    def remove_arc_from(self, path):
        """ FIXME
        Remove link from the path
        Just copied from "remove_arc_from"
        """
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        succ_str = config_file.read_variable("successors")
        succ_str.remove(self.path)
        config_file.write_variable("successors", succ_str)
        config_file = metadata.ConfigFile(self.path+"/.chern/config.json")
        pred_str = config_file.read_variable("predecessors")
        pred_str.remove(path)
        config_file.write_variable("predecessors", pred_str)

    def add_arc_to(self, path):
        """ FIXME:
        Add a link from this object to the path object
        """
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        pred_str = config_file.read_variable("predecessors")
        if pred_str is None:
            pred_str = []
        pred_str.append(self.path)
        config_file.write_variable("predecessors", pred_str)
        config_file = metadata.ConfigFile(self.path+"/.chern/config.json")
        succ_str = config_file.read_variable("successors")
        if succ_str is None:
            succ_str = []
        succ_str.append(path)
        config_file.write_variable("successors", succ_str)

    def remove_arc_to(self, path):
        """ FIXME remove the path to the path
        """
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        pred_str = config_file.read_variable("predecessors")
        pred_str.remove(self.path)
        config_file.write_variable("predecessors", pred_str)
        config_file = metadata.ConfigFile(self.path+"/.chern/config.json")
        succ_str = config_file.read_variable("successors")
        succ_str.remove(path)
        config_file.write_variable("successors", succ_str)

    def successors(self):
        """ The successors of the current object
        """
        succ_str = self.config_file.read_variable("successors")
        if succ_str is None:
            return []
        successors = []
        for path in succ_str:
            successors.append(VJob(path))
        return successors

    def predecessors(self):
        """ Predecessors
        """
        pred_str = self.config_file.read_variable("pred_impression")
        if pred_str is None:
            return []
        predecessors = []
        for path in pred_str:
            predecessors.append(VJob(utils.storage_path()+"/"+path))
        return predecessors

    def impression_to_alias(self, path):
        """
        """
        impression_to_alias = self.config_file.read_variable("impression_to_alias", {})
        return impression_to_alias.get(path, "")

    def alias_to_path(self, alias):
        alias_to_path = self.config_file.read_variable("alias_to_path")
        return alias_to_path[alias]

    def remove_alias(self, alias):
        if alias == "":
            return
        alias_to_path = self.config_file.read_variable("alias_to_path")
        path_to_alias = self.config_file.read_variable("path_to_alias")
        path = alias_to_path[alias]
        path_to_alias.pop(path)
        alias_to_path.pop(alias)
        self.config_file.write_variable("alias_to_path", alias_to_path)
        self.config_file.write_variable("path_to_alias", path_to_alias)

    def set_alias(self, alias, path):
        if alias == "":
            return
        path_to_alias = self.config_file.read_variable("path_to_alias")
        alias_to_path = self.config_file.read_variable("alias_to_path")
        if path_to_alias is None:
            path_to_alias = {}
        if alias_to_path is None:
            alias_to_path = {}
        path_to_alias[path] = alias
        alias_to_path[alias] = path
        self.config_file.write_variable("path_to_alias", path_to_alias)
        self.config_file.write_variable("alias_to_path", alias_to_path)
