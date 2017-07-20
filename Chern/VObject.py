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
        succ_str.append(self.path)
        config_file.write_variable("successors", succ_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("")
        pred_str.append(self.path)
        config_file.write_variable("pre")

    def add_arc_to(self, path):
        """
        FIXME
        Add a link from this object to the path object
        """
        config_file = utils.ConfigFile(path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        succ_str.append(self.path)
        config_file.write_variable("successors", succ_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("")
        pred_str.append(self.path)
        config_file.write_variable("pre")

    def remove_path_to(self, path):
        """
        FIXME
        remove the path to the path
        """
        config_file = utils.ConfigFile(path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        succ_str.append(self.path)
        config_file.write_variable("successors", succ_str)
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("")
        pred_str.append(self.path)
        config_file.write_variable("pre")



    def get_successors():
        config_file = utils.ConfigFile(self.path+"/.config.py")
        succ_str = config_file.read_variable("successors")
        successors = []
        for path in succ_str:
            successors.append(path)
        return successors

    def get_predecessors():
        config_file = utils.ConfigFile(self.path+"/.config.py")
        pred_str = config_file.read_variable("predecessors")
        predecessors = []
        for path in pred_str:
            predecessors.append(path)
        return predecessors

    def cp(self, new_path):
        """
        FIXME
        """
        queue = self.sub_objects_respectively()
        for obj in queue:
            new_project = VObject(new_path +"/"+ self.relative_path(obj.path))
            for arc in arc.in_arcs():
                if arc not in queue: new_project.add_from(arc)
                else:
                    new_project.add_from(path+relative_arc path)

    def mv(self, new_path):
        """
        FIXME
        mv to another path
        """
        self.cp(new_path)
        self.remove()
        pass

    def remove(self):
        """
        queue
        remove_from
        remove_to
        """
        pass


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
        This method should be written to realize the function of
        """
        pass
