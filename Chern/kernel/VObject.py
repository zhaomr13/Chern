import os
import shutil
import time
from Chern.utils import utils
from Chern.utils import csys
from Chern.utils.utils import debug
from Chern.utils import metadata
from Chern.utils.pretty import colorize
from Chern.utils.utils import color_print
from Chern.kernel.ChernDaemon import status as daemon_status
from subprocess import call
import subprocess
import Chern
from Chern.utils import git
from Chern.kernel.ChernDatabase import ChernDatabase
import uuid

cherndb = ChernDatabase.instance()

class VObject(object):
    """ Virtual class of the objects, including VData, VAlgorithm, VData and VDirectory
    """

    def __init__(self, path):
        """ Initialize a instance of the object.
        All the infomation is directly read from and write to the disk.
        """
        self.path = utils.strip_path_string(path)
        self.created_time = time.time()
        self.config_file = metadata.ConfigFile(self.path+"/.chern/config.json")

    def invariant_path(self):
        """ The path relative to the project root.
        It is invariant when the project is moved.
        """
        project_path = cherndb.project_path()
        path = os.path.relpath(self.path, project_path)
        return path

    def __str__(self):
        """ Define the behavior of print(vobject)
        """
        return self.invariant_path()

    def __repr__(self):
        """ Define the behavior of print(vobject)
        """
        return self.invariant_path()

    def is_git_committed(self, is_global=False):
        """ Whether the object is recorded by git.
        FIXME: the is_global flag maybe useless.
        """
        if is_global:
            ps = subprocess.Popen("git status", shell=True, stdout=subprocess.PIPE)
        else:
            ps = subprocess.Popen("git status -- {0}".format(self.path), shell=True, stdout=subprocess.PIPE)
        ps.wait()
        output = ps.stdout.read()
        return output.decode().find("nothing to commit") != -1

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

    def short_ls(self):
        """ Print the subdirectory of the object
        I recommend to print also the README
        and the parameters|inputs|outputs ...
        """
        if not cherndb.is_docker_started():
            color_print("!!Warning: docker not started", color="warning")
        if daemon_status() != "started":
            color_print("!!Warning: runner not started, the status is {}".format(daemon_status()), color="warning")
        sub_objects = self.sub_objects()
        sub_objects.sort(key=lambda x:(x.object_type(),x.path))
        if sub_objects:
            print(colorize(">>>> Subobjects:", "title0"))
        for index, sub_object in enumerate(sub_objects):
            sub_path = self.relative_path(sub_object.path)
            print("{2} {0:<12} {1:>20}".format("("+sub_object.object_type()+")", sub_path, "[{}]".format(index)))
        total = len(sub_objects)
        predecessors = self.predecessors()
        if predecessors:
            print(colorize("o--> Predecessors:", "title0"))
        for index, pred_object in enumerate(predecessors):
            alias = self.path_to_alias(pred_object.invariant_path())
            order = "[{}]".format(total+index)
            pred_path = pred_object.invariant_path()
            obj_type = "("+pred_object.object_type()+")"
            print("{2} {0:<12} {3:>10}: {1:<20}".format(obj_type, pred_path, order, alias))
        total += len(predecessors)
        successors = self.successors()
        if successors:
            print(colorize("-->o Successors:", "title0"))
        for index, succ_object in enumerate(successors):
            alias = self.path_to_alias(succ_object.invariant_path())
            order = "[{}]".format(total+index)
            succ_path = succ_object.invariant_path()
            obj_type = "("+succ_object.object_type()+")"
            print("{2} {0:<12} {3:>10}: {1:<20}".format(obj_type, succ_path, order, alias))

    def is_zombine(self):
        return self.object_type() == ""

    def check_arcs(self):
        predecessors = self.precesessors()
        for obj in predecessors:
            if obj.is_zombine() or not obj.has_successor(self):
                self.remove_arc_from(obj, single=True)
                self.remove_alias(self.path_to_alias(obj.path))
        for obj in successors:
            if obj.is_zombine() or not obj.has_predecessor(self):
                self.remove_arc_to(obj, single=True)

    def add_arc_from(self, path):
        """ Add an link from the object contains in `path' to this object.
        FIXME: it directly operate the config_file of other object rather operate through.
        """
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        succ_str = config_file.read_variable("successors", [])
        succ_str.append(self.invariant_path())
        config_file.write_variable("successors", succ_str)
        print("!!!!!", path, succ_str)

        pred_str = self.config_file.read_variable("predecessors", [])
        pred_str.append(VObject(path).invariant_path())
        self.config_file.write_variable("predecessors", pred_str)

    def remove_arc_from(self, obj, single=False):
        """
        Remove link from the path
        """
        if not single:
            print(obj)
            config_file = obj.config_file
            succ_str = config_file.read_variable("successors", [])
            print(succ_str)
            print(self.invariant_path())
            succ_str.remove(self.invariant_path())
            config_file.write_variable("successors", succ_str)

        pred_str = self.config_file.read_variable("predecessors", [])
        pred_str.remove(obj.invariant_path())
        self.config_file.write_variable("predecessors", pred_str)

    def add_arc_to(self, path):
        """
        FIXME
        Add a link from this object to the path object
        """
        config_file = metadata.ConfigFile(path+"/.chern/config.json")
        pred_str = config_file.read_variable("predecessors")
        if pred_str is None:
            pred_str = []
        pred_str.append(self.invariant_path())
        config_file.write_variable("predecessors", pred_str)
        config_file = metadata.ConfigFile(self.path+"/.chern/config.json")
        succ_str = config_file.read_variable("successors")
        if succ_str is None:
            succ_str = []
        succ_str.append(VObject(path).invariant_path())
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
        project_path = cherndb.project_path()
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
                if pred_object.is_zombine() or not pred_object.has_successor(obj):
                    print("The predecessor \n\t {} \n\t does not exists or do not \
has a link to object {}".format(pred_object, obj) )
                    choice = input("Would you like to remove the input or the algorithm? [Y/N]")
                    if choice == "Y":
                        obj.remove_arc_from(pred_object, single=True)
                        obj.remove_alias(obj.path_to_alias(pred_object.path))
                        obj.impress()

            for succ_object in obj.successors():
                if succ_object.is_zombine() or not succ_object.has_predecessor(obj):
                    print("The succecessor \n\t {} \n\t does not exists or do not \
has a link to object {}".format(succ_object, obj) )
                    choice = input("Would you like to remove the output? [Y/N]")
                    if choice == "Y":
                        obj.remove_arc_to(succ_object, single=True)
                        message = obj.latest_commit_message()
                        # git.add(obj.path)
                        # git.commit("{}/remove output arc".format(message))

            for pred_object in obj.predecessors():
                if obj.path_to_alias(pred_object.invariant_path()) == "" and pred_object.object_type() != "algorithm":
                    print("The input {} of {} does not have alias, it will be removed".format(pred_object, obj))
                    choice = input("Would you like to remove the input or the algorithm? [Y/N]")
                    if choice == "Y":
                        obj.remove_arc_from(pred_object)
                        message = pred_object.latest_commit_message()
                        # git.add(pred_object.path)
                        # git.commit("{}/remove output arc".format(message))
                        obj.impress()


            alias_to_path = obj.config_file.read_variable("alias_to_path", {})
            path_to_alias = obj.config_file.read_variable("path_to_alias", {})
            for path in path_to_alias.keys():
                project_path = cherndb.project_path()
                pred_obj = VObject(project_path+"/"+path)
                if not obj.has_predecessor(pred_obj):
                    print("There seems being a zombine alias to {} in {}".format(pred_obj, obj))
                    choice = input("Would you like to remove it?[Y/N]")
                    if choice == "Y":
                        obj.remove_alias(obj.path_to_alias(path))
                        message = obj.latest_commit_message()
                        # git.add(obj.path)
                        # git.commit("{}/remove zombine alias".format(message))



    def copy_to(self, new_path):
        """
        FIXME
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
                    print("In the same tree")
                    # print("new path", new_path)
                    print("object", new_object)
                    print("relative_path", relative_path)
                    new_object.add_arc_from(new_path+"/"+relative_path)
                    alias1 = obj.path_to_alias(pred_object.invariant_path())
                    # alias2 = pred_object.path_to_alias(obj.path)
                    norm_path = os.path.normpath(new_path +"/"+ relative_path)
                    new_object.set_alias(alias1, VObject(norm_path).invariant_path())
                    # VObject(norm_path).set_alias(alias2, new_object.invariant_path())
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

        """
        for obj in queue:
            print("queue", self.successors())
            for pred_object in obj.predecessors():
                if self.relative_path(pred_object.path).startswith(".."):
                    obj.remove_arc_from(pred_object)
                    message = pred_object.latest_commit_message()
                    git.add(pred_object.path)
                    git.commit("{} + mv".format(message))

            for succ_object in obj.successors():
                print("debug")
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object)
                    message = succ_object.latest_commit_message()
                    git.add(succ_object.path)
                    git.commit("{} + mv".format(message))
        """

        # Deal with the impression
        for obj in queue:
            # Calculate the absolute path of the new directory
            if obj.object_type() == "directory":
                norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
                # git.add(norm_path+"/.chern")
                # git.add(norm_path+"/README.md")
                # git.commit("save directory")
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
                    new_object.add_arc_from(pred_object.path)
                    alias = obj.path_to_alias(pred_object.invariant_path())
                    new_object.set_alias(alias, pred_object.invariant_path())
                else:
                # if in the same tree
                    relative_path = self.relative_path(pred_object.path)
                    new_object.add_arc_from(new_path+"/"+relative_path)
                    print("In the same tree")
                    print("new path", new_path)
                    print("relative_path", relative_path)
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
                    message = pred_object.latest_commit_message()
                    # git.add(pred_object.path)
                    # git.commit("{}/mv".format(message))

            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object)
                    message = succ_object.latest_commit_message()
                    # git.add(succ_object.path)
                    # git.commit("{}/mv".format(message))

        # Deal with the impression
        for obj in queue:
            # Calculate the absolute path of the new directory
            print("Try to keep the impress of {}".format(obj))
            if obj.object_type() == "directory":
                continue
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            message = obj.latest_commit_message()
            # git.add(new_object.path)
            # git.commit("{} + mv".format(message))

        if self.object_type() == "directory":
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            # git.add(norm_path)
            # git.commit("move")
        shutil.rmtree(self.path)
        # git.rm(self.path)
        # git.commit("remove {}".format(self.path))

    def add(self, src, dst):
        if not os.path.exists(src):
            return
        utils.copy(src, self.path+"/"+dst)
        # git.add(self.path+"/"+dst)
        # git.commit("Add {}".format(dst))

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
                    message = pred_object.latest_commit_message()
                    # git.add(pred_object.path)
                    # git.commit("{} + mv".format(message))
            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object)
                    alias = succ_object.path_to_alias(succ_object.path)
                    succ_object.remove_alias(alias)
                    # git.add(succ_object.path)
                    # git.commit("remove {}".format(alias))

        shutil.rmtree(self.path)
        # git.rm(self.path)
        # git.commit("rm {}".format(self.invariant_path()))

    def sub_objects(self):
        """ return a list of the sub_objects
        """
        sub_directories = os.listdir(self.path)
        sub_object_list = []
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                obj = VObject(self.path+"/"+item)
                if obj.is_zombine():
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

    def latest_commit_message(self, is_global=False):
        if is_global:
            log = git.log('-n 1 --format="%s"').split("\n")
        else:
            # config_file = utils.ConfigFile(os.environ["HOME"] + "/.Chern/git-cache")
            consult_table = cherndb.consult_table
            # = config_file.read_variable("consult_table", {})
            last_consult_time, log = consult_table.get(self.path, (-1,-1))
            modification_time = csys.dir_mtime(self.path)

            if modification_time < last_consult_time:
                return log

            log = git.log('-n 1 --format="%s" -- {}'.format(self.path)).split("\n")

            consult_table[self.path] = (time.time(), log[0])
            # config_file.write_variable("consult_table", consult_table)
            return log[0][:42]

    def edit_readme(self):
        """
        FIXME
        need more editor support
        """
        call("vim {0}".format(self.path+"/README.md"), shell=True)
        # git.add(self.path+"/README.md")
        message = self.latest_commit_message()
        # git.commit("{}/edit readme".format(message))

    def commit(self):
        """ Commit the object
        """
        # git.add(self.path)
        commit_id = git.commit("commit all the files in {}".format(self.path))
        self.config_file.write_variable("commit_id", commit_id)
        # git.commit("save the commit id")

    def commit_id(self):
        """ Get the commit id
        """
        commit_id = self.config_file.read_variable("commit_id", None)
        if commit_id is None:
            raise Exception("")
        return commit_id

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


    def is_impressed(self, is_global=False):
        """ Judge whether the file is impressed
        """
        if not self.is_git_committed():
            return False
        latest_commit_message = self.latest_commit_message()
        if "Impress:" not in latest_commit_message:
            return False
        if self.impression() == "":
            return False
        pred = self.predecessors()
        if pred == []:
            return True
        pred_impression = []
        for input_object in pred:
            if not input_object.is_impressed_fast():
                return False
            else:
                pred_impression.append(input_object.impression())
        if sorted(pred_impression) == sorted(self.config_file.read_variable("pred_impression", [])):
            return True
        else:
            return False

    def impress(self):
        if self.object_type() != "task" and self.object_type() != "algorithm":
            return
        if self.is_impressed_fast():
            print("Already impressed.")
            return
        pred = self.predecessors()
        pred_impression = []

        for input_object in pred:
            if not input_object.is_impressed_fast():
                input_object.impress()
            pred_impression.append(input_object.impression())

        # self.config_file.write_variable("pred_impression", pred_impression)
        impression = uuid.uuid4().hex
        self.config_file.write_variable("impression", impression)
        impressions = self.config_file.read_variable("impressions", [])
        impressions.append(impression)
        self.config_file.write_variable("impressions", impressions)
        csys.mkdir(self.path+"/.chern/impressions/"+impression)
        for f in csys.list_dir(self.path):
            print(f)
            if f != ".chern" and f != "README.md":
                csys.copy(f, self.path+"/.chern/impressions/"+impression)
        impression_config = self.path+"/.chern/impressions/"+impression+"/dependences.json"
        impression_config.write_variable(pred_impressions)

    def impression(self):
        impression = self.config_file.read_variable("impression")
        return impression

    def readme(self):
        """
        FIXME
        Get the README String.
        I'd like it to support more
        """
        with open(self.path+"/README.md") as f:
            return f.read().strip("\n")

    def __getitem__(self, index):
        """
        FIXME
        This method should be written to realize the function like
        a.b.c
        """
        pass
