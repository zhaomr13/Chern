from Chern.VObject import VObject
from Chern.VImage import VImage
from Chern import utils
import uuid
from Chern import git
import os
import uuid
import subprocess
from Chern import ChernManager
from Chern.utils import debug
from Chern.utils import colorize
from Chern.ChernDatabase import ChernDatabase
cherndb = ChernDatabase.instance()

class VAlgorithm(VObject):
    def __init__(self, file_name):
        super(VAlgorithm, self).__init__(file_name)

    def commit(self):
        """ Commit the object
        """
        git.add(self.path)
        commit_id = git.commit("commit all the files in {}".format(self.path))
        self.config_file.write_variable("commit_id", commit_id)
        git.commit("save the commit id")

    def impress(self):
        """ Commit the object
        """
        impression = uuid.uuid4().hex
        self.config_file.write_variable("impression", impression)
        git.add(self.path)
        git.commit("Impress: {0}".format(impression))

    def commit_id(self):
        """ Get the commit id
        """
        commit_id = self.config_file.read_variable("commit_id")
        return commit_id

    def status(self):
        """ query the status of the current algorithm.
        the status information will be saved in the local directory.
        It is used for version control.
        The possible status are:
            new: the algorithm is updated but t
            built: the algorithm is built successfully with a md5 number, and the corresponding are.
            missing: the algorithm is built successfully with a md5 number
            error: the algorithm is not built successfully..

        Everytime there is a change of the file, there should be a update time for the project.
        if the lastest built time is less than the update time, the project should be marked as "new".
        If the project is not new, there should be the latest built md5. try to find whether the md5 of the.
        """
        if not self.is_impressed():
            return "new"
        if not self.is_submitted():
            return "impressed"
        return self.image().status()

    def is_impressed(self, is_global=False):
        if not self.is_git_committed():
            return False
        latest_commit_message = self.latest_commit_message()
        return "Impress:" in latest_commit_message

    def is_submitted(self):
        if not self.is_impressed():
            return False
        if cherndb.job(self.impression()) is not None:
            return True
        else:
            return False

    def submit(self):
        if not self.is_impressed():
            self.impress()
        path = utils.storage_path() + "/" + self.impression()
        cwd = self.path
        utils.copy_tree(cwd, path)

    def image(self):
        path = utils.storage_path() + "/" + self.impression()
        return VImage(path)

    def ls(self):
        """
        Option to
        """
        super(VAlgorithm, self).ls()
        parameters_file = utils.ConfigFile(self.path+"/parameters.py")
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        print(colorize("---- Parameters:", "title0"))
        for parameter in parameters:
            print(parameters_file.read_variable(parameter))
        print(colorize("**** STATUS:", "title0"), self.status())

    def add_parameter(self, parameter):
        """
        Add a parameter to the parameters file
        """
        if parameter == "parameters":
            print("A parameter is not allowed to be called parameters")
            return
        parameters_file = utils.ConfigFile(self.path+"/parameters.py")
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        parameters.append(parameter)
        parameters_file.write_variable("parameters", parameters)
        self.set_update_time()

    def remove_parameter(self, parameter):
        self.config_file.read_variable("parameters")
        pass

    ## FIXME the number of datafiles should not be specificied in the algorithm file
    def add_input(self, input):
        # FIXME add input file for this project
        pass

    def add_output(self, output):
        # FIXME add output file for this project
        pass

def create_algorithm(path, inloop=False):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    os.mkdir(path+"/.chern")
    with open(path + "/.chern/config.py", "w") as f:
        f.write("object_type = \"algorithm\"\n")
        f.write("main_file = \"main.py\"\n")
    with open(path + "/README.md", "w") as f:
        f.write("Please write README for this algorithm")
    subprocess.call("vim %s/README.md"%path, shell=True)
    with open(path + "/main.py", "w") as f:
        f.write("""# Please write the main file for this algorithm
# A demo is:
from Chern import ChernExec
inputfile = inputs["input"]+"/tree1.root"
outputfile = outputs["output"]+"/tree.root"
ps = ChernExec("root -l -q {}/selection.C".format(path), path)
ps.send(inputfile)
ps.send(outputfile)
ps.exit()""")
    subprocess.call("vim %s/main.py"%path, shell=True)

def abandoned():
    os.chdir(path)
    start_file = open("start.py", "w")
    start_file.write("""from Chern.ChernAlgorithm import ChernAlgorithm
algorithm = ChernAlgorithm.get_instance()
algorithm.host_path = "{0}"
algorithm.load_source()
algorithm.write_docker_file()
print("I am running")
""".format(tmp_dir))
    start_file.close()


