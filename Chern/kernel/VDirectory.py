"""
A module
"""
import os
import subprocess
import Chern
from Chern.utils import utils
from Chern.utils import git
from Chern.kernel.VObject import VObject
class VDirectory(VObject):
    """
    Nothing more to do for this VDirectory.
    """
    def helpme(self, command):
        from Chern.kernel.Helpme import directory_helpme
        print(directory_helpme.get(command, "No such command, try ``helpme'' alone."))

    def status(self):
        sub_objects = self.sub_objects()
        for sub_object in sub_objects:
            if sub_object.object_type() == "task":
                if Chern.kernel.VTask.VTask(sub_object.path).status() != "done":
                    return "unfinished"
            elif sub_object.object_type() == "algorithm":
                if Chern.kernel.VAlgorithm.VAlgorithm(sub_object.path).status() != "built":
                    return "unfinished"
            elif Chern.kernel.VDirectory.VDirectory(sub_object.path).status() != "finished":
                return "unfinished"
        return "finished"



def create_directory(path, inloop=False):
    path = utils.strip_path_string(path)
    parent_path = os.path.abspath(path+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "project" and object_type != "directory":
        raise Exception("create directory only under project or directory")
    os.mkdir(path)
    os.mkdir(path+"/.chern")
    with open(path + "/.chern/config.py", "w") as f:
        f.write("object_type = \"directory\"")
    directory = VObject(path)
    git.add(path+"/.chern")
    git.commit("Create directory at {}".format(
        directory.invariant_path()))
    with open(path + "/README.md", "w") as f:
        f.write("Please write README for directory {}".format(
            directory.invariant_path() ) )
    directory.edit_readme()
