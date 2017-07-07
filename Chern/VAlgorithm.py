from Chern.VObject import VObject
class VAlgorithm(VObject):
    def __init__(self, file_name):
        super(VAlgorithm, self).__init__(file_name)

    def load_object(self):
        super(VAlgorithm, self).load_object()

    def mk_algorithm(self, file_name):
        super(VObject, self).mk_object(file_name)

def create_algorithm(path):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    with open(path + "/.config.py", "w") as f:
        f.write("object_type = \"algorithm\"")
        f.write("main_file = \"main.py\"")
    with open(path + "/.README.md", "w") as f:
        f.write("Please write README for this algorithm")
    subprocess.call("vim %s/.README.md"%path, shell=True)
    with open(path + "/main.py", "w") as f:
        f.write("Please write the main file for this algorithm")
    subprocess.call("vim %s/main.py"%path, shell=True)

def load_parameter(name):
    pass
