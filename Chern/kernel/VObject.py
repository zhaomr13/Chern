import os
import shutil
import time
from Chern.utils import utils
from Chern.utils import csys
from Chern.utils.utils import debug
from Chern.utils.utils import colorize
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
        self.config_file = utils.ConfigFile(self.path+"/.chern/config.py")

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

    def is_modified(self):
        """ FIXME: may be replaced by the git commit method.
        Return whether this object object is modified.
        Check should be done before every use.
        """
        return False

    def object_type(self, path=None):
        """
        Return the type of the object under a specific path.
        If path is left blank, return the type of the object itself.
        """
        if path is None:
            path = self.path
        # simply read object_type in .chern/config.py
        config_file = utils.ConfigFile(path+"/.chern/config.py")
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
        if not cherndb.is_docker_started():
            color_print("!!Warning: docker not started", color="warning")
        if daemon_status() != "started":
            color_print("!!Warning: runner not started {}".format(daemon_status()), color="warning")
        print(colorize("README:", "comment"))
        print(colorize(self.readme(), "comment"))
        sub_objects = self.sub_objects()
        sub_objects.sort(key=lambda x:(x.object_type(),x.path))
        if sub_objects:
            print(colorize(">>>> Subobjects:", "title0"))
        for index, sub_object in enumerate(sub_objects):
            """
            if sub_object.object_type() == "task" and Chern.kernel.VTask.VTask(sub_object.path).status() == "done":
                sub_path = colorize(self.relative_path(sub_object.path), "success")
            elif sub_object.object_type() == "algorithm" and Chern.kernel.VAlgorithm.VAlgorithm(sub_object.path).status() == "built":
                sub_path = colorize(self.relative_path(sub_object.path), "success")
            else:
            """
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

    def add_arc_from(self, path):
        """ Add an link from the object contains in `path' to this object.
        FIXME: it directly operate the config_file of other object rather operate through.
        """
        config_file = utils.ConfigFile(path+"/.chern/config.py")
        succ_str = config_file.read_variable("successors", [])
        succ_str.append(self.invariant_path())
        config_file.write_variable("successors", succ_str)

        pred_str = self.config_file.read_variable("predecessors", [])
        pred_str.append(VObject(path).invariant_path())
        self.config_file.write_variable("predecessors", pred_str)

    def remove_arc_from(self, path):
        """
        Remove link from the path
        """
        config_file = VObject(path).config_file
        succ_str = config_file.read_variable("successors", [])
        succ_str.remove(self.invariant_path())
        config_file.write_variable("successors", succ_str)

        pred_str = self.config_file.read_variable("predecessors", [])
        pred_str.remove(VObject(path).invariant_path())
        self.config_file.write_variable("predecessors", pred_str)

    def add_arc_to(self, path):
        """
        FIXME
        Add a link from this object to the path object
        """
        config_file = utils.ConfigFile(path+"/.chern/config.py")
        pred_str = config_file.read_variable("predecessors")
        if pred_str is None:
            pred_str = []
        pred_str.append(self.invariant_path())
        config_file.write_variable("predecessors", pred_str)
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        succ_str = config_file.read_variable("successors")
        if succ_str is None:
            succ_str = []
        succ_str.append(VObject(path).invariant_path())
        config_file.write_variable("successors", succ_str)

    def remove_arc_to(self, path):
        print("Calling remove arc to ...")
        print(self)
        print(path)
        """
        FIXME
        remove the path to the path
        """
        config_file = VObject(path).config_file
        pred_str = config_file.read_variable("predecessors", [])
        pred_str.remove(self.invariant_path())
        config_file.write_variable("predecessors", pred_str)

        succ_str = self.config_file.read_variable("successors", [])
        succ_str.remove(VObject(path).invariant_path())
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
        project_path = cherndb.project_path()
        for path in pred_str:
            predecessors.append(VObject(project_path+"/"+path))
        return predecessors

    def cp(self, new_path):
        """
        FIXME
        """
        shutil.copytree(self.path, new_path)
        queue = self.sub_objects_recursively()

        # Make sure the related objects are all impressed
        for obj in queue:
            if not obj.is_impressed_fast():
                obj.impress()

        for obj in queue:
            # Calculate the absolute path of the new directory
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            new_object.clean_flow()
            new_object.clean_impressions()
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
                    obj.remove_arc_from(pred_object.path)
                    message = pred_object.latest_commit_message()
                    git.add(pred_object.path)
                    git.commit("{} + mv".format(message))

            for succ_object in obj.successors():
                print("debug")
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object.path)
                    message = succ_object.latest_commit_message()
                    git.add(succ_object.path)
                    git.commit("{} + mv".format(message))
        """

        # Deal with the impression
        for obj in queue:
            # Calculate the absolute path of the new directory
            if obj.object_type == "directory":
                continue
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            new_object.impress()
            # message = obj.latest_commit_message()
            # git.add(new_object.path)
            # git.commit("{} + mv".format(message))

    def path_to_alias(self, path):
        path_to_alias = self.config_file.read_variable("path_to_alias", {})
        return path_to_alias.get(path, "")

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

    def mv(self, new_path):
        """ mv to another path
        """
        shutil.copytree(self.path, new_path)
        queue = self.sub_objects_recursively()

        # Make sure the related objects are all impressed
        for obj in queue:
            if not obj.is_impressed_fast():
                obj.impress()

        for obj in queue:
            # Calculate the absolute path of the new directory
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            new_object.clean_flow()
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
                    obj.remove_arc_from(pred_object.path)
                    message = pred_object.latest_commit_message()
                    git.add(pred_object.path)
                    git.commit("{} + mv".format(message))

            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object.path)
                    message = succ_object.latest_commit_message()
                    git.add(succ_object.path)
                    git.commit("{} + mv".format(message))

        # Deal with the impression
        for obj in queue:
            # Calculate the absolute path of the new directory
            if obj.object_type == "directory":
                continue
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            new_object = VObject(norm_path)
            message = obj.latest_commit_message()
            git.add(new_object.path)
            git.commit("{} + mv".format(message))

        if self.object_type() == "directory":
            norm_path = os.path.normpath(new_path +"/"+ self.relative_path(obj.path))
            git.add(norm_path)
            git.commit("move")
        shutil.rmtree(self.path)
        git.rm(self.path)
        git.commit("remove {}".format(self.path))

    def add(self, src, dst):
        if not os.path.exists(src):
            return
        utils.copy(src, self.path+"/"+dst)
        git.add(self.path+"/"+dst)
        git.commit("Add {}".format(dst))

    def rm(self):
        """
        Remove this object.
        The important this is to unalias
        """
        queue = self.sub_objects_recursively()
        for obj in queue:
            for pred_object in obj.predecessors():
                if self.relative_path(pred_object.path).startswith(".."):
                    obj.remove_arc_from(pred_object.path)
                    alias = pred_object.path_to_alias(pred_object.path)
                    pred_object.remove_alias(alias)
                    message = pred_object.latest_commit_message()
                    git.add(pred_object.path)
                    git.commit("{} + mv".format(message))
            for succ_object in obj.successors():
                if self.relative_path(succ_object.path).startswith(".."):
                    obj.remove_arc_to(succ_object.path)
                    alias = succ_object.path_to_alias(succ_object.path)
                    succ_object.remove_alias(alias)
                    git.add(succ_object.path)
                    git.commit("remove {}".format(alias))

        shutil.rmtree(self.path)
        git.rm(self.path)
        git.commit("rm {}".format(self.invariant_path()))

    def sub_objects(self):
        """ return a list of the sub_objects
        """
        sub_directories = os.listdir(self.path)
        sub_object_list = []
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                object_type = self.object_type(self.path+"/"+item)
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
        return log[0]

    def edit_readme(self):
        """
        FIXME
        need more editor support
        """
        call("vim {0}".format(self.path+"/README.md"), shell=True)
        git.add(self.path+"/README.md")
        message = self.latest_commit_message()
        git.commit("{} + edit readme".format(message))

    def commit(self):
        """ Commit the object
        """
        git.add(self.path)
        commit_id = git.commit("commit all the files in {}".format(self.path))
        self.config_file.write_variable("commit_id", commit_id)
        git.commit("save the commit id")

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
        if sorted(pred_impression) == sorted(self.config_file.read_variable("pred_impression")):
            return True
        else:
            return False

    def impress(self):
        pred = self.predecessors()
        pred_impression = []

        for input_object in pred:
            if not input_object.is_impressed_fast():
                input_object.impress()
            pred_impression.append(input_object.impression())

        self.config_file.write_variable("pred_impression", pred_impression)
        impression = uuid.uuid4().hex
        self.config_file.write_variable("impression", impression)
        impressions = self.config_file.read_variable("impressions", [])
        impressions.append(impression)
        self.config_file.write_variable("impressions", impressions)
        git.add(self.path)
        git.commit("Impress: {0}".format(impression))

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
