"""
A module
"""
from Chern.VObject import VObject
from Chern import utils
import os
from Chern import git
import subprocess
class VDirectory(VObject):
    """
    Nothing more to do for this VDirectory.
    """
    pass

    def add_parameter(self, parameter, value):
        """
        Add a parameter to the parameters file
        """
        if parameter == "parameters":
            print("A parameter is not allowed to be called parameters")
        parameters_file = utils.CondfigFile(self.path+"/parameters.py")
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
        parameters_file = utils.ConfigFile(self.path+"parameters.py")
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
    os.mkdir(path)
    with open(path + "/.chern/config.py", "w") as f:
        f.write("object_type = \"directory\"")
    with open(path + "/README.md", "w") as f:
        f.write("Please write README for this directory")
    subprocess.call("vim %s/README.md"%path, shell=True)
