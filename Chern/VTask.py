from Chern.VObject import VObject
from Chern import utils
import subprocess
import os
# from Chern.run_standalone import run_standalone
class VTask(VObject):
    def __init__(self, file_name):
        super(VTask, self).__init__(file_name)

    # def load_object(self):
    # super(VTask, self).__init__(file_name)

    def mk_task(self, file_name):
        pass

    def mk_sub_task(self, file_name):
        pass

    def run(self):
        subprocess.call("python {0}/run_standalone.py {1} {2}".format("/home/zhaomr/workdir/", self.path, self.get_algorithm()))

    def has_super_task(self):
        config_file = utils.ConfigFile(path + "/../.config.py")
        return config_file.read_variable("object_type") == "task"

    def set_algorithm(self, algorithm_path):
        config_file = utils.ConfigFile(path + "./config.py")
        config_file.write_variable("algorithm", algorithm_path)
    def unset_algorithm(self, path):
        pass

    def get_algorithm(self):
        config_file = utils.ConfigFile(path + "/.config.py")
        return config_file.read_variable("algorithm")


def create_task(path):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    with open(path + "/.config.py", "w") as f:
        f.write("object_type = \"task\"")
    with open(path + "/.README.md", "w") as f:
        f.write("Please write README for this task")
    subprocess.call("vim %s/.README.md"%path, shell=True)
