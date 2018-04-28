""" VAlgorithm
"""
import uuid
import time
import os
import subprocess

from Chern.kernel.VObject import VObject
from Chern.kernel.VImage import VImage
from Chern.kernel.ChernDatabase import ChernDatabase

from Chern.utils import utils
from Chern.utils import csys
from Chern.utils.utils import color_print
from Chern.utils import git
from Chern.utils.utils import colorize

cherndb = ChernDatabase.instance()

class VAlgorithm(VObject):
    """ Algorithm class
    """

    def helpme(self, command):
        from Chern.kernel.Helpme import algorithm_helpme
        print(algorithm_helpme.get(command, "No such command, try ``helpme'' alone."))

    def status(self, consult_id = None):
        """ query the status of the current algorithm.
        """
        if consult_id:
            consult_table = cherndb.status_consult_table
            # config_file.read_variable("impression_consult_table", {})
            cid, status = consult_table.get(self.path, (-1,-1))
            if cid == consult_id:
                return status

        if not self.is_impressed_fast():
            status = "new"
        elif not self.is_submitted():
            status  = "impressed"
        else:
            status = self.image().status()
        if consult_id:
            consult_table[self.path] = (consult_id, status)
        return status


    def jobs(self):
        impressions = self.config_file.read_variable("impressions", [])
        if impressions == []:
            return
        impression = self.config_file.read_variable("impression")
        for im in impressions:
            path = utils.storage_path() + "/" + im
            if not os.path.exists(path):
                continue
            if impression == im:
                short = "*"
            else:
                short = " "
            short += im[:8]
            status = VImage(path).status()
            print("{0:<12}   {1:>20}".format(short, status))

    def is_impressed_fast(self):
        consult_table = cherndb.impression_consult_table
        last_consult_time, is_impressed = consult_table.get(self.path, (-1,-1))
        modification_time = csys.dir_mtime( cherndb.project_path() )
        if modification_time < last_consult_time:
            return is_impressed
        is_impressed = self.is_impressed()
        consult_table[self.path] = (time.time(), is_impressed)
        return is_impressed

    def is_impressed(self):
        """ Judge whether impressed or not. Return a True or False.
        """
        if not self.is_git_committed():
            return False
        latest_commit_message = self.latest_commit_message()
        return "Impress:" in latest_commit_message

    def is_submitted(self):
        """ Judge whether submitted or not. Return a True or False.
        """
        if not self.is_impressed_fast():
            return False
        return cherndb.job(self.impression()) is not None

    def submit(self):
        """ Submit """
        if self.is_submitted():
            return ["[ERROR] {0} already submitted! Skip ``submit''.".format(self.invariant_path())]
        if not self.is_impressed_fast():
            self.impress()

        path = csys.storage_path() + "/" + self.impression()
        cwd = self.path
        utils.copy_tree(cwd, path)
        image = self.image()
        image.config_file.write_variable("job_type", "image")
        cherndb.add_job(self.impression())

    def resubmit(self):
        if not self.is_submitted():
            print("Not submitted yet.")
            return
        path = utils.storage_path() + "/" + self.impression()
        csys.rmtree(path)
        self.submit()

    def stdout(self):
        """ stdout
        """
        with open(self.image().path+"/stdout") as stdout_file:
            return stdout_file.read()

    def stderr(self):
        """ Std error
        """
        with open(self.image().path+"/stderr") as stderr_file:
            return stderr_file.read()

    def image(self):
        """ Get the image. If the image is not exists raise a exception.
        """
        path = utils.storage_path() + "/" + self.impression()
        if not os.path.exists(path):
            raise Exception("Image does not exist.")
        return VImage(path)

    def ls(self, show_readme=True, show_predecessors=True, show_sub_objects=True, show_status=False, show_successors=False):
        """ list the infomation.
        """
        super(VAlgorithm, self).ls(show_readme, show_predecessors, show_sub_objects, show_status, show_successors)
        parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        print(colorize("---- Parameters:", "title0"))
        for parameter in parameters:
            print(parameter)

        if show_status:
            status = self.status()
            if status == "built":
                status_color = "success"
            else:
                status_color = "normal"
            print(colorize("**** STATUS:", "title0"),
                colorize(self.status(), status_color) )

        if self.is_submitted() and self.image().error() != "":
            print(colorize("!!!! ERROR:\n", "title0"), self.image().error())
        files = os.listdir(self.path)
        for f in files:
            if not f.startswith(".") and f != "README.md":
                print(f)

    def add_parameter(self, parameter):
        """ Add a parameter to the parameters file
        """
        try:
            if parameter == "parameters":
                return ["[ERROR] A parameter is not allowed to be called ``parameters''"]
            parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
            parameters = parameters_file.read_variable("parameters", [])
            if parameter in parameters:
                return ["[ERROR] Fail to add parameter ``{}'', exist".format(parameter)]
            parameters.append(parameter)
            parameters_file.write_variable("parameters", parameters)
        except Exception as e:
            raise e

    def remove_parameter(self, parameter):
        """ Remove parameter
        """
        try:
            parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
            parameters = parameters_file.read_variable("parameters", [])
            if parameter not in parameters:
                return ["[ERROR] Fail to remove parameter ``{}'', not exist".format()]
            else:
                parameters.remove(parameter)
                return
        except Exception as e:
            raise e

def create_algorithm(path, use_template=False):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    os.mkdir(path+"/.chern")
    with open(path + "/.chern/config.py", "w") as config_file:
        config_file.write("object_type = \"algorithm\"\n")
        config_file.write("main_file = \"main.py\"\n")
    with open(path + "/README.md", "w") as readme_file:
        readme_file.write("Please write README for this algorithm")
    subprocess.call("vim {}/README.md".format(path), shell=True)
    if use_template:
        template_name = input("Please input the Dockerfile template type")
        print("Creating template, but hahahaha")
        return
