"""
A module
"""
import os
import subprocess
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

    def add_parameter(self, parameter, value):
        """
        Add a parameter to the parameters file
        """
        if parameter == "parameters":
            print("A parameter is not allowed to be called parameters")
        parameters_file = utils.CondfigFile(self.path+"/.chern/parameters.py")
        parameters_file.write_varialbe(parameter, value)
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        parameters.append(parameter)
        parameters_file.write_variable("parameters", parameters)

    def remove_parameter(self, parameter):
        """
        Remove a parameter to the parameters file
        """
        if parameter == "parameters":
            print("parameters is not allowed to remove")
            return
        parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
        parameters = parameters_file.read_variable("parameters")
        if parameter not in parameters:
            print("Parameter not found")
            return
        parameters.remove(parameter)
        parameters_file.write_variable(parameter, None)
        parameters_file.write_variable("parameters", parameters)
        self.set_update_time()

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
