"""
VData module, contains a class and a function.
The class VData is the VObject whose type is data.
The function will create a VData from a path.
"""
import os
import uuid
import time
import imp
import subprocess
from Chern import utils
import Chern
from Chern.VObject import VObject
from Chern.utils import colorize
from Chern import git

class VData(VObject):
    """
    Virtual Data.
    """
    def ls(self):
        """ First use the VObject ls, and then print the supported sites of this data
        FIXME: list the files in the local site
        """
        super(VData, self).ls()
        print("Status: {0}".format(self.status()))

    def is_committed(self):
        """
        """
        if not self.is_git_committed():
            return False
        if self.task() == None:
            return True
        task_commit_id = self.config_file.read_variable("task_commit_id")
        if self.task().is_committed() and self.commit_id() == task_commit_id:
            return True
        else:
            return False

    def impress(self):
        pred = []
        task = self.task()
        if task is not None and (not task.is_impressed()):
            task.impress()
        if task is not None:
            pred.append(task.impression())
        self.config_file.write_variable("pred_impression", pred)
        impression = uuid.uuid4().hex
        self.config_file.write_variable("impression", impression)
        git.add(self.path)
        git.commit("Impress: {0}".format(impression))

    def is_impressed(self, is_global=False):
        """ Judge whether the file is impressed
        """
        if not self.is_git_committed():
            return False
        latest_commit_message = self.latest_commit_message()
        if "Impress:" not in latest_commit_message:
            return False
        task = self.task()
        if task is None:
            return True
        pred = []
        if not task.is_impressed():
            return False
        else:
            pred.append(task.impression())
        if pred == sorted(self.config_file.read_variable("pred_impression")):
            return True
        else:
            return False

    def submit(self):
        if self.is_submitted():
            return
        if not self.is_impressed():
            self.impress()
        path = utils.storage_path() + "/" + self.impression()
        cwd = self.path
        utils.copy_tree(cwd, path)

    def is_submitted(self):
        return False

    def add(self, file_name):
        """ add expected data to this file.
        """
        self.config_file.write()
        git.add(self.path)

    def task(self):
        predecessors = self.predecessors()
        if predecessors == []:
            return None
        else:
            return Chern.VTask.VTask(predecessors[0].path)

    def link(self, source, destination, site):
        chern_config_path = os.environ["HOME"] + "/.Chern"
        site_module = imp.load_source("site", chern_config_path+"/"+site+".py")
        site_module.link(source, destination)

    def new_version(self, site):
        """
        Create a new version of the data.
        And the new version will replace the old one.
        The old one can be found through git.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        versions = config_file.read_variable("versions")
        if versions is None:
            versions = {}
        versions[site] = uuid.uuid4().hex
        config_file.write_variable("versions", versions)
        os.mkdir(self.get_physics_position(site))

    def check_output(self):
        return self.volume().exists()

    def status(self, site=None):
        """
        The status of the VData should be quite complicated:
            On remote: Generated, Downloaded
            Local empty: don't match,
        Read the run status
        The status of the data should be:
            1. empty
            2. filling
            3. filled
            The problem is to determine, when is the data container is filled?
            If the preceding task is running, the data status should be filling
            If the preceding task is finished, the data status should be filled
            What should a contaier do?
        """
        if not self.is_impressed():
            return "new"
        if not self.is_submitted():
            return "impressed"
        if self.volume().filled():
            return "downloaded"
        if self.task().status() == "finished":
            return "generated"
        return "generating"

    def latest_version(self, site):
        """
        Get the latest version.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        versions = config_file.read_variable("versions")
        return versions[site]

    def get_physics_position(self, site):
        """
        Read the physics position of a site of a data.
        """
        chern_config_path = os.environ.get("HOME") + "/.Chern"
        config_file = utils.ConfigFile(chern_config_path +"/config.py")
        sites = config_file.read_variable("sites")
        return sites[site] +"/data/"+ self.latest_version(site)


def create_data(path, inloop=False):
    """
    Make a new data and its update time should be 0.
    """
    path = utils.strip_path_string(path)
    os.mkdir(path)
    os.mkdir(path+"/.chern")
    with open(path + "/.chern/config.py", "w") as config_file:
        config_file.write("object_type = \"data\"")
    with open(path + "/README.md", "w") as readme_file:
        readme_file.write("Please write a specific README!")
    if not inloop:
        subprocess.call("vim %s/README.md"%path, shell=True)

