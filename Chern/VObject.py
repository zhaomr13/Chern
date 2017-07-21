import os
from Chern import utils
from Chern.utils import debug
from subprocess import call

class VObject(object):
    """
    Virtual class of the objects, including VData, VAlgorithm, VData and VDirectory
    """
    def __init__(self, path):
        """
        Initialize the project the only **information** of a object instance
        is its path, the other things are all stored in the disk.
        FIXME
        The created time of the directory should also be stored.
        The created time should be used for check available of the instance
        """
        self.path = utils.strip_path_string(path)
        self.created_time = None

    def __str__(self):
        """
        Define the behavior of print(vobject)
        """
        return self.path

    def __repr__(self):
        """
        Define the behavior of print(vobject)
        """
        return self.path

    def relative_path(self, path):
        """
        Return a path relative to the path of this object
        """
        return os.path.relpath(path, self.path)

    def is_modified(self):
        """
        Return whether this object object is modified.
        Check should be done before every use.
        """
        pass

    def object_type(self, path=None):
        """
        Return the type of the object under a specific path.
        If path is left blank, return the type of the object itself.
        """
        if path is None:
            path = self.path
        debug(path)
        # simply read object_type in .config.py
        if not os.path.exists(path+"/.config.py"):
                return None
        config_file = utils.ConfigFile(path + "/.config.py")
        return config_file.read_variable("object_type")

    def ls(self):
        """
        FIXME
        Print the subdirectory of the object
        I recommend to print also the README
        and the parameters|inputs|outputs ...
        And it's better to give a number to the listed
        object and therefore, command like cd 1
        can be used
        """
        debug("Running ls")
        print(self.readme())
        sub_objects = self.sub_objects()
        print(sub_objects)
        sub_objects.sort(key=lambda x:(x.object_type(),x.path))
        for sub_object in sub_objects:
            print("{0:>10} {1:>20}".format(sub_object.object_type(), self.relative_path(sub_object.path)))

    def add_arc_from(self, path):
        """
        Add an link from the path object to this object
        """
        config_file = utils.ConfigFile(path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        succ_str.append(self.path)
        config_file.write_variable("successors", succ_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("predecessors")
        pred_str.append(self.path)
        config_file.write_variable("predecessors", pred_str)

    def remove_arc_from(self, path):
        """
        FIXME
        Remove link from the path
        Just copied from "remove_arc_from"
        """
        config_file = utils.ConfigFile(path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        succ_str.remove(self.path)
        config_file.write_variable("successors", succ_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("predecessors")
        pred_str.remove(self.path)
        config_file.write_variable("predecessors", pred_str)

    def add_arc_to(self, path):
        """
        FIXME
        Add a link from this object to the path object
        """
        config_file = utils.ConfigFile(path+"/.config.py")
        pred_str = config_file.read_variable("predecessors")
        pred_str.append(self.path)
        config_file.write_variable("predecessors", pred_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        succ_str.append(self.path)
        config_file.write_variable("successors", succ_str)

    def remove_path_to(self, path):
        """
        FIXME
        remove the path to the path
        """
        config_file = utils.ConfigFile(path+"/.config.py")
        pred_str = config_file.read_variable("predecessors")
        pred_str.remove(self.path)
        config_file.write_variable("predecessors", pred_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        succ_str.remove(self.path)
        config_file.write_variable("successors", succ_str)

    def get_successors(self):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        if succ_str is None:
            return []
        successors = []
        for path in succ_str:
            successors.append(path)
        return successors

    def get_predecessors(self):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("predecessors")
        if pred_str is None:
            return []
        predecessors = []
        for path in pred_str:
            predecessors.append(path)
        return predecessors

    def cp(self, new_path):
        """
        FIXME
        """
        queue = self.sub_objects_recursively()
        for obj in queue:
            new_object = VObject(new_path +"/"+ self.relative_path(obj.path))

    def path_to_alias(self, path):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        path_to_alias = config_file.read_variable("path_to_alias")
        return path_to_alias[path]

    def alias_to_path(self, path):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        alias_to_path = config_file.read_variable("alias_to_path")
        return path_to_alias[path]

    def remove_alias(self, alias):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        alias_to_path = config_file.read_variable("alias_to_path")
        path_to_alias = config_file.read_variable("path_to_alias")
        path = alias_to_path[alias]
        path_to_alias.pop(path)
        alias_to_path.pop(alias)
        config_file.write_variable("alias_to_path", alias_to_path)
        config_file.write_variable("path_to_alias", path_to_alias)



    def set_alias(self, path, alias):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        path_to_alias = config_file.read_variable("path_to_alias")
        alias_to_path = config_file.read_variable("alias_to_path")
        path_to_alias[path] = alias
        alias_to_path[alias] = path
        config_file.write_variable("path_to_alias", path_to_alias)
        config_file.write_variable("alias_to_path", alias_to_path)



    def mv(self, new_path):
        """
        FIXME
        mv to another path
        """
        queue = self.sub_objects_recursively()
        for obj in queue:
            new_object = VObject(new_path +"/"+ self.relative_path(obj.path))
            for pred_object in obj.get_predecessors():
                if self.relative_path(pred_object.path).startwith(".."):
                    new_object.add_in_arc(pred_object.path)
                    alias1 = obj.path_to_alias(pred_object.path)
                    alias2 = pred_object.path_to_alias(obj.path)
                    new_object.set_alias(alias1, pred_object.path)
                    pred_object.set_alias(alias2, new_object.path)
                else:
                # if in the same tree
                    relative_path = self.relative_path(pred_object.path)
                    new_object.add_in_arc(new_path+"/"+relative_path)
                    alias1 = obj.path_to_alias(pred_obj.path)
                    alias2 = pred_obj.path_to_alias(obj.path)
                    new_object.set_alias(alias1, new_path+"/"+relative_path)
                    VObject(new_path+"/"+relative_path).set_alias(alias2, new_object.path)
            for succ_object in obj.get_successors():
                if self.relative_path(succ_object.path).startwith(".."):
                    new_object.add_out_arc(succ_object.path)
                    alias1 = obj.path_to_alias(succ_object.path)
                    alias2 = succ_object.path_to_alias(obj.path)
                    new_object.set_alias(alias1, succ_object.path)
                    succ_object.set_alias(alias2, new_object.path)

        self.remove()
        pass

    def remove(self):
        """
        Remove this object.
        The important this is to unalias
        """
        queue = self.sub_objects_recursively()
        for obj in queue:
            for pred_object in obj.get_predecessors():
                if self.relative_path(pred_object.path).startwith(".."):
                    obj.remove_in_arc(pred_object.path)
            for pred_object in obj.get_successors():
                if self.relative_path(pred_object.path).startwith(".."):
                    obj.remove_out_arc(succ_object.path)

    def sub_objects(self):
        """
        return a list of the sub_objects
        """
        sub_directories = os.listdir(self.path)
        sub_object_list = []
        print(sub_directories)
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                object_type = self.object_type(self.path+"/"+item)
                debug(object_type)
                if object_type is None:
                    continue
                sub_object_list.append(VObject(self.path+"/"+item))
        return sub_object_list

    def sub_objects_recursively(self):
        """
        Return a list of all the sub_objects
        """
        queue = [self]
        index = 0
        while index < len(queue):
            top_object = queue[index]
            queue += top_object.sub_objects()
            index += 1
        return queue

    def edit_readme(self):
        """
        FIXME
        need more editor support

        """
        call("vim {0}".format(self.path+"/.README.md"), shell=True)

    def readme(self):
        """
        FIXME
        Get the README String.
        I'd like it to support more
        """
        debug(self.path)
        with open(self.path+"/.README.md") as f:
            return f.read()

    def __getitem__(self, index):
        """
        FIXME
        This method should be written to realize the function like
        a.b.c
        """
        pass
