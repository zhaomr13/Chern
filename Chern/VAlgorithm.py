from Chern.VObject import VObject
from Chern import utils
import os
import subprocess
from Chern import ChernManager
from Chern.utils import debug
from Chern.utils import colorize

class VAlgorithm(VObject):
    def __init__(self, file_name):
        super(VAlgorithm, self).__init__(file_name)

    def status(self):
        """
        query the status of the current algorithm.
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
        image_id = self.config_file.read_variable("image_id")
        if image_id is None:
            return "new"
        if image_id == "error":
            return "error"
        image = self.image()
        if image.status == "missing":
            return "missing"
        if self.update_time() > image.update_time():
            return "new"
        return "built"

    def build(self):
        """
        Build the image to change the status of the Algorithm to builded.
        It will create a unique VImage object and the md5 of the VImage will be saved.
        """
        """
            What to do:
            first: copy all the files to a temporary file directory and next
            write a docker file
            then, you should build the docker file
        """
        tmp_dir = "/tmp{0}".format(uuid.uuid4().hex)
        utils.mkdir(tmp_dir)
        cwd = self.path
        os.chdir(tmp_dir)
        utils.copy(cwd+"/*", tmp_dir)
        start_file = open("start.py", "w")
        start_file.write("""from Chern import ChernAlgorithm
algorithm = ChernAlgorithm.get_instance()
ChernAlgorithm.host_path = {0}
imp.load_module()
algorithm.generate_docker_file()
""".format(tmp_dir))
        subprocess.Popen("python start.py")
        if ps:
            print("Error Build the image, please check your configuration")
        ps = subprocess.Popen("docker build {}")
        self.config_file.write("image_id", image_id)
        self.set_update_time()

    def image(self):
        image_id = self.config_file.read_variable("image_id")
        return VImage.consult_image(image_id)

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
            print(parameter, end=" = ")
            print(parameters_file.read_variable(parameter))
        print(colorize("**** STATUS:", "title0"), self.status())





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

