import os
import shutil
import time
import subprocess
import Chern
import uuid
import filecmp
from Chern.utils import csys
from Chern.utils import metadata
from Chern.utils.pretty import colorize
from Chern.utils.utils import color_print
from Chern.kernel.ChernDaemon import status as daemon_status
from Chern.kernel.ChernDatabase import ChernDatabase

cherndb = ChernDatabase.instance()

class VObject(object):
    """ Virtual class of the objects, including VData, VAlgorithm and VDirectory
    """

    def __init__(self, path):
        """ Initialize a instance of the object.
        All the infomation is directly read from and write to the disk.
        parameter ``path'' is allowed to be a string begin with empty characters.
        """
        self.path = csys.strip_path_string(path)
        self.config_file = metadata.ConfigFile(self.path+"/.chern/config.json")


    def __str__(self):
        """ Define the behavior of print(vobject)
        """
        return self.invariant_path()

    def __repr__(self):
        """ Define the behavior of print(vobject)
        """
        return self.invariant_path()

    def invariant_path(self):
        """ The path relative to the project root.
        It is invariant when the project is moved.
        """
        project_path = csys.project_path()
        path = os.path.relpath(self.path, project_path)
        return path

    def relative_path(self, path):
        """ Return a path relative to the path of this object
        """
        return os.path.relpath(path, self.path)

    def object_type(self):
        """ Return the type of the object under a specific path.
        If path is left blank, return the type of the object itself.
        If the object does not exists, return ""
        """
        return self.config_file.read_variable("object_type", "")

    def is_zombie(self):
        return self.object_type() == ""

    def color_tag(self, status):
        if status == "built" or status == "done" or status == "finished":
            color_tag = "success"
        elif status == "failed" or status == "unfinished":
            color_tag = "warning"
        elif status == "running":
            color_tag = "running"
        else:
            color_tag = "normal"
        return color_tag

    def ls(self, show_readme=True, show_predecessors=True, show_sub_objects=True, show_status=False, show_successors=False):
        """ Print the subdirectory of the object
        I recommend to print also the README
        and the parameters|inputs|outputs ...
        """
        if not cherndb.is_docker_started():
            color_print("!!Warning: docker not started", color="warning")
        if daemon_status() != "started":
            color_print("!!Warning: runner not started, the status is {}".format(daemon_status()), color="warning")

        if show_readme:
            print(colorize("README:", "comment"))
            print(colorize(self.readme(), "comment"))

        sub_objects = self.sub_objects()
        sub_objects.sort(key=lambda x:(x.object_type(),x.path))
        if sub_objects and show_sub_objects:
            print(colorize(">>>> Subobjects:", "title0"))

        if show_sub_objects:
            for index, sub_object in enumerate(sub_objects):
                sub_path = self.relative_path(sub_object.path)
                if show_status:
                    status = Chern.interface.ChernManager.create_object_instance(sub_object.path).status()
                    color_tag = self.color_tag(status)
                    print("{2} {0:<12} {1:>20} ({3})".format("("+sub_object.object_type()+")", sub_path, "[{}]".format(index), colorize(status, color_tag)))
                else:
                    print("{2} {0:<12} {1:>20}".format("("+sub_object.object_type()+")", sub_path, "[{}]".format(index)))

        total = len(sub_objects)
        predecessors = self.predecessors()
        if predecessors and show_predecessors:
            print(colorize("o--> Predecessors:", "title0"))
            for index, pred_object in enumerate(predecessors):
                alias = self.path_to_alias(pred_object.invariant_path())
                order = "[{}]".format(total+index)
                pred_path = pred_object.invariant_path()
                obj_type = "("+pred_object.object_type()+")"
                print("{2} {0:<12} {3:>10}: @/{1:<20}".format(obj_type, pred_path, order, alias))

        total += len(predecessors)
        successors = self.successors()
        if successors and show_successors:
            print(colorize("-->o Successors:", "title0"))
            for index, succ_object in enumerate(successors):
                alias = self.path_to_alias(succ_object.invariant_path())
                order = "[{}]".format(total+index)
                succ_path = succ_object.invariant_path()
                obj_type = "("+succ_object.object_type()+")"
                print("{2} {0:<12} {3:>10}: @/{1:<20}".format(obj_type, succ_path, order, alias))


    def add_arc_from(self, obj):
        """ Add an link from the object contains in `path' to this object.
        FIXME: it directly operate the config_file of other object rather operate through.
        """
        succ_str = obj.config_file.read_variable("successors", [])
        succ_str.append(self.invariant_path())
        obj.config_file.write_variable("successors", succ_str)

        pred_str = self.config_file.read_variable("predecessors", [])
        pred_str.append(obj.invariant_path())
        self.config_file.write_variable("predecessors", pred_str)

    def remove_arc_from(self, obj, single=False):
        """
        Remove link from the path
        """
        if not single:
            config_file = obj.config_file
            succ_str = config_file.read_variable("successors", [])
            succ_str.remove(self.invariant_path())
            config_file.write_variable("successors", succ_str)

        pred_str = self.config_file.read_variable("predecessors", [])
        pred_str.remove(obj.invariant_path())
        self.config_file.write_variable("predecessors", pred_str)

    def add_arc_to(self, obj):
        """
        FIXME
        Add a link from this object to the path object
        """
        pred_str = obj.config_file.read_variable("predecessors", [])
        pred_str.append(self.invariant_path())
        obj.config_file.write_variable("predecessors", pred_str)

        succ_str = self.config_file.read_variable("successors", [])
        succ_str.append(obj.invariant_path())
        config_file.write_variable("successors", succ_str)

    def remove_arc_to(self, obj, single=False):
        """
        remove the path to the path
        """
        if not single:
            config_file = obj.config_file
            pred_str = config_file.read_variable("predecessors", [])
            pred_str.remove(self.invariant_path())
            config_file.write_variable("predecessors", pred_str)

        succ_str = self.config_file.read_variable("successors", [])
        succ_str.remove(obj.invariant_path())
        self.config_file.write_variable("successors", succ_str)

    def successors(self):
        """
        The successors of the current object
        """
        succ_str = self.config_file.read_variable("successors", [])
        successors = []
        project_path = csys.project_path()
        for path in succ_str:
            successors.append(VObject(project_path+"/"+path))
        return successors

    def predecessors(self):
        pred_str = self.config_file.read_variable("predecessors", [])
        predecessors = []
        project_path = csys.project_path()
        for path in pred_str:
            predecessors.append(VObject(project_path+"/"+path))
        return predecessors

    def has_successor(self, obj):
        succ_str = self.config_file.read_variable("successors", [])
        return obj.invariant_path() in succ_str

    def has_predecessor(self, obj):
        pred_str = self.config_file.read_variable("predecessors", [])
        return obj.invariant_path() in pred_str

    def doctor(self):
        queue = self.sub_objects_recursively()
        for obj in queue:
            if obj.object_type() != "task" and obj.object_type() != "algorithm":
                continue

            for pred_object in obj.predecessors():
                if pred_object.is_zombie() or not pred_object.has_successor(obj):
                    print("The predecessor \n\t {} \n\t does not exists or do not \
has a link to object {}".format(pred_object, obj) )
                    choice = input("Would you like to remove the input or the algorithm? [Y/N]")
                    if choice == "Y":
                        obj.remove_arc_from(pred_object, single=True)
                        obj.remove_alias(obj.path_to_alias(pred_object.path))
                        obj.impress()

            for succ_object in obj.successors():
                if succ_object.is_zombie() or not succ_object.has_predecessor(obj):
                    print("The succecessor \n\t {} \n\t does not exists or do not \
has a link to object {}".format(succ_object, obj) )
                    choice = input("Would you like to remove the output? [Y/N]")
                    if choice == "Y":
                        obj.remove_arc_to(succ_object, single=True)

            for pred_object in obj.predecessors():
                if obj.path_to_alias(pred_object.invariant_path()) == "" and pred_object.object_type() != "algorithm":
                    print("The input {} of {} does not have alias, it will be removed".format(pred_object, obj))
                    choice = input("Would you like to remove the input or the algorithm? [Y/N]")
                    if choice == "Y":
                        obj.remove_arc_from(pred_object)
                        obj.impress()


            alias_to_path = obj.config_file.read_variable("alias_to_path", {})
            path_to_alias = obj.config_file.read_variable("path_to_alias", {})
            for path in path_to_alias.keys():
                project_path = csys.project_path()
                pred_obj = VObject(project_path+"/"+path)
                if not obj.has_predecessor(pred_obj):
                    print("There seems being a zombie alias to {} in {}".format(pred_obj, obj))
                    choice = input("Would you like to remove it?[Y/N]")
                    if choice == "Y":
                        obj.remove_alias(obj.path_to_alias(path))



    def copy_to(self, new_path):
        """ Copy the current objects and its containings to a new path.
        """
        queue = self.sub_objects_recursively()

        # Make sure the related objects are all impressed
        for obj in queue:
            if obj.object_type() != "task" and obj.object_type() != "algorithm":
                continue
            if not obj.is_impressed_fast():
                obj.impress()
        shutil.copytree(self.path, new_path)

        for obj in queue:
            # Calculate the absolute path of the new directory
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            new_object.clean_flow()
            new_object.clean_impressions()

        for obj in queue:
            # Calculate the absolute path of the new directory
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            for pred_object in obj.predecessors():
                # if in the outside directory
                if self.relative_path(pred_object.path).startswith(".."):
                    """
                    Do nothing
                    new_object.add_arc_from(pred_object.path)
                    alias1 = obj.path_to_alias(pred_object.path)
                    alias2 = pred_object.path_to_alias(obj.path)
                    new_object.set_alias(alias1, pred_object.invariant_path())
                    pred_object.remove_alias(alias2)
                    pred_object.set_alias(alias2, new_object.invariant_path())
                    """
                else:
                # if in the same tree
                    relative_path = self.relative_path(pred_object.path)
                    new_object.add_arc_from(VObject(new_path+"/"+relative_path))
                    alias1 = obj.path_to_alias(pred_object.invariant_path())
                    norm_path = os.path.normpath(new_path +"/"+ relative_path)
                    new_object.set_alias(alias1, VObject(norm_path).invariant_path())

            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    """
                    Do nothing
                    new_object.add_arc_to(succ_object.path)
                    alias1 = obj.path_to_alias(succ_object.path)
                    alias2 = succ_object.path_to_alias(obj.path)
                    new_object.set_alias(alias1, succ_object.invariant_path())
                    succ_object.remove_alias(alias2)
                    succ_object.set_alias(alias2, new_object.invariant_path())
                    """

        # Deal with the impression
        for obj in queue:
            # Calculate the absolute path of the new directory
            if obj.object_type() == "directory":
                norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
                continue
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            new_object.impress()

    def path_to_alias(self, path):
        path_to_alias = self.config_file.read_variable("path_to_alias", {})
        return path_to_alias.get(path, "")

    def alias_to_path(self, alias):
        alias_to_path = self.config_file.read_variable("alias_to_path", {})
        return alias_to_path.get(alias, "")

    def has_alias(self, alias):
        alias_to_path = self.config_file.read_variable("alias_to_path", {})
        return alias in alias_to_path.keys()

    def remove_alias(self, alias):
        if alias == "":
            return
        alias_to_path = self.config_file.read_variable("alias_to_path", {})
        path_to_alias = self.config_file.read_variable("path_to_alias", {})
        path = alias_to_path[alias]
        path_to_alias.pop(path)
        alias_to_path.pop(alias)
        self.config_file.write_variable("alias_to_path", alias_to_path)
        self.config_file.write_variable("path_to_alias", path_to_alias)

    def set_alias(self, alias, path):
        if alias == "":
            return
        path_to_alias = self.config_file.read_variable("path_to_alias", {})
        alias_to_path = self.config_file.read_variable("alias_to_path", {})
        path_to_alias[path] = alias
        alias_to_path[alias] = path
        self.config_file.write_variable("path_to_alias", path_to_alias)
        self.config_file.write_variable("alias_to_path", alias_to_path)

    def clean_impressions(self):
        self.config_file.write_variable("impressions", [])
        self.config_file.write_variable("impression", "")
        self.config_file.write_variable("output_md5s", {})
        self.config_file.write_variable("output_md5", "")

    def clean_flow(self):
        """
        Clean all the alias, predecessors and successors
        """
        self.config_file.write_variable("alias_to_path", {})
        self.config_file.write_variable("path_to_alias", {})
        self.config_file.write_variable("predecessors", [])
        self.config_file.write_variable("successors", [])

    def move_to(self, new_path):
        """ mv to another path
        """
        queue = self.sub_objects_recursively()

        # Make sure the related objects are all impressed
        for obj in queue:
            if obj.object_type() != "task" and obj.object_type() != "algorithm":
                continue
            if not obj.is_impressed_fast():
                obj.impress()
        shutil.copytree(self.path, new_path)

        for obj in queue:
            # Calculate the absolute path of the new directory
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            new_object.clean_flow()

        for obj in queue:
            # Calculate the absolute path of the new directory
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            for pred_object in obj.predecessors():
                # if in the outside directory
                if self.relative_path(pred_object.path).startswith(".."):
                    new_object.add_arc_from(pred_object)
                    alias = obj.path_to_alias(pred_object.invariant_path())
                    new_object.set_alias(alias, pred_object.invariant_path())
                else:
                # if in the same tree
                    relative_path = self.relative_path(pred_object.path)
                    new_object.add_arc_from(VObject(new_path+"/"+relative_path) )
                    alias1 = obj.path_to_alias(pred_object.invariant_path())
                    alias2 = pred_object.path_to_alias(obj.invariant_path())
                    norm_path = os.path.normpath(new_path +"/"+ relative_path)
                    new_object.set_alias(alias1, VObject(norm_path).invariant_path())
                    VObject(norm_path).set_alias(alias2, new_object.invariant_path())

            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    new_object.add_arc_to(succ_object.path)
                    alias = obj.path_to_alias(succ_object.invariant_path())
                    succ_object.remove_alias(alias)
                    succ_object.set_alias(alias, new_object.invariant_path())

        for obj in queue:
            for pred_object in obj.predecessors():
                if self.relative_path(pred_object.path).startswith(".."):
                    obj.remove_arc_from(pred_object)

            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object)

        # Deal with the impression
        for obj in queue:
            # Calculate the absolute path of the new directory
            if obj.object_type() == "directory":
                continue
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)

        if self.object_type() == "directory":
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))

        shutil.rmtree(self.path)

    def add(self, src, dst):
        if not os.path.exists(src):
            return
        csys.copy(src, self.path+"/"+dst)

    def rm(self):
        """
        Remove this object.
        The important this is to unalias
        """
        queue = self.sub_objects_recursively()
        for obj in queue:
            for pred_object in obj.predecessors():
                if self.relative_path(pred_object.path).startswith(".."):
                    obj.remove_arc_from(pred_object)
                    alias = pred_object.path_to_alias(pred_object.path)
                    pred_object.remove_alias(alias)

            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object)
                    alias = succ_object.path_to_alias(succ_object.path)
                    succ_object.remove_alias(alias)

        shutil.rmtree(self.path)

    def sub_objects(self):
        """ return a list of the sub_objects
        """
        sub_directories = os.listdir(self.path)
        sub_object_list = []
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                obj = VObject(self.path+"/"+item)
                if obj.is_zombie():
                    continue
                sub_object_list.append(obj)
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

    def is_impressed_fast(self):
        # return self.is_impressed()
        # config_file = utils.ConfigFile(os.environ["HOME"] + "/.Chern/git-cache")
        consult_table = cherndb.impression_consult_table
        # config_file.read_variable("impression_consult_table", {})
        last_consult_time, is_impressed = consult_table.get(self.path, (-1,-1))
        now = time.time()
        if now - last_consult_time < 1:
            return is_impressed
        modification_time = csys.dir_mtime( cherndb.project_path() )
        if modification_time < last_consult_time:
            return is_impressed
        is_impressed = self.is_impressed()
        consult_table[self.path] = (time.time(), is_impressed)
        # config_file.write_variable("impression_consult_table", consult_table)
        return is_impressed

    def impression_file_list(self, impression = ""):
        if impression != "":
            config_file = metadata.ConfigFile(self.path+"/.chern/impressions/{}/config.json".format(impression))
            return config_file.read_variable("tree")
        file_list = []
        for dirpath, dirnames, filenames in csys.walk(self.path):
            if "README.md" in filenames:
                filenames.remove("README.md")
            file_list.append([dirpath, dirnames, filenames])

        return file_list

    def pred_impressions(self, impression = ""):
        if impression != "":
            config_file = metadata.ConfigFile(self.path+"/.chern/impressions/{}/config.json".format(impression))
            return config_file.read_variable("dependencies")
        dependencies = []
        for pred in self.predecessors():
            dependencies.append(pred.impression())
        return sorted(dependencies)

    def is_impressed(self, is_global=False):
        """ Judge whether the file is impressed
        """
        # Check whether there is an impression already
        impression = self.impression()
        if self.impression() == "":
            return False

        for pred in self.predecessors():
            if not pred.is_impressed_fast():
                return False

        file_list = self.impression_file_list()
        if file_list != self.impression_file_list(impression):
            return False
        if self.pred_impressions() != self.pred_impressions(impression):
            return False

        for dirpath, dirnames, filenames in file_list:
            for f in filenames:
                if not filecmp.cmp(self.path+"/{}/{}".format(dirpath, f),
                               self.path+"/.chern/impressions/{}/contents/{}/{}".format(impression, dirpath, f)):
                    return False
        return True

    def impress(self):
        """ Create an impression.
        The impressions are store in a directory .chern/impressions/[uuid]
        It is organized as following:
            [uuid]
            |------ contents
            |------ config.json
        In the config.json, the tree of the contents as well as the dependencies are stored.
        The object_type is also saved in the json file.
        The tree and the dependencies are sorted via name.
        """
        object_type = self.object_type()
        if object_type != "task" and object_type != "algorithm":
            return
        if self.is_impressed_fast():
            print("Already impressed.")
            return
        for pred in self.predecessors():
            if not pred.is_impressed_fast():
                pred.impress()

        # self.config_file.write_variable("pred_impression", pred_impression)
        impression = uuid.uuid4().hex
        self.config_file.write_variable("impression", impression)
        impressions = self.config_file.read_variable("impressions", [])
        impressions.append(impression)
        self.config_file.write_variable("impressions", impressions)

        # Create an impression directory and
        file_list = self.impression_file_list()
        csys.mkdir(self.path+"/.chern/impressions/{}/contents".format(impression))
        for dirpath, dirnames, filenames in file_list:
            for f in filenames:
                csys.copy(self.path+"/{}/{}".format(dirpath, f),
                          self.path+"/.chern/impressions/{}/contents/{}/{}".format(impression, dirpath, f))

        # Write tree and dependencies to the configuration file
        dependencies = self.pred_impressions()
        config_file = metadata.ConfigFile(self.path+"/.chern/impressions/{}/config.json".format(impression))
        config_file.write_variable("tree", file_list)
        config_file.write_variable("dependencies", dependencies)

        # Write the basic metadata to the configuration file
        object_type = {"task":"container", "algorithm":"image"}.get(object_type)
        config_file.write_variable("object_type", object_type)
        config_file.write_variable("impressions", impressions)

        path_to_alias = self.config_file.read_variable("path_to_alias", {})
        impression_to_alias = {}
        for path, alias in path_to_alias.items():
            impression = VObject(csys.project_path() + "/" + path).impression()
            impression_to_alias[impression] = alias
        config_file.write_variable("impression_to_alias", impression_to_alias)

    def impression(self):
        impression = self.config_file.read_variable("impression", "")
        return impression

    def readme(self):
        """
        FIXME
        Get the README String.
        I'd like it to support more
        """
        with open(self.path+"/README.md") as f:
            return f.read().strip("\n")
