from Chern.VObject import VObject
class VTask(VObject):
    def __init__(self):
        super(VTask, self).__init__(file_name)

    def load_object(self):
        super(VTask, self).__init__(file_name)

    def mk_task(self, file_name):
        pass

    def mk_sub_task(self, file_name):
        pass

    def run(self):
        pass

    def has_super_task(self):
        pass


def create_task(path):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    with open(path + "/.config.py", "w") as f:
        f.write("object_type = \"task\"")
    with open(path + "/.README.md", "w") as f:
        f.write("Please write README for this task")
    subprocess.call("vim %s/.README.md"%path, shell=True)
