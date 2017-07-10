from Chern.VObject import VObject
from Chern import utils
import subprocess
import os
class VData(VObject):
    def __init__(self, file_name):
        print("load success")
        super(VData, self).__init__(file_name)

    def load_object(self):
        super(VData, self).load_object()

    def mk_data(self, file_name):
        pass

    def data(self):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        return config_file.read_variable("data")

    def set_data(self, path):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        config_file.write_variable("data", path)

    def add_task(self, path):
        config_file = utils.ConfigFile(self.path+"/.config.py")
        tasks = config_file.read_variable("tasks", path)
        tasks.append(task)
        config_file.write_variable("data", )


def create_data(path):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    with open(path + "/.config.py", "w") as f:
        f.write("object_type = \"data\"")
    with open(path + "/.README.md", "w") as f:
        f.write("Please write a specific README!")
    subprocess.call("vim %s/.README.md"%path, shell=True)


