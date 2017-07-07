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

def create_data(path):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    with open(path + "/.config.py", "w") as f:
        f.write("object_type = \"data\"")
    with open(path + "/.README.md", "w") as f:
        f.write("Please write a specific README!")
    subprocess.call("vim %s/.README.md"%path, shell=True)

