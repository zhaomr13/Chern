import os
import uuid
import imp
import subprocess
import Chern
from Chern.VObject import VObject
from Chern import utils
from Chern import git
from Chern.utils import debug
from Chern.utils import colorize
class VTask(VObject):
    def ls(self):
        super(VTask, self).ls()
        parameters_file = utils.ConfigFile(self.path+"/parameters.py")
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        print(colorize("---- Parameters:", "title0"))
        for parameter in parameters:
            print(parameter, end=" = ")
            print(parameters_file.read_variable(parameter))
        print(colorize("**** STATUS:", "title0"), self.status())

    def inputs(self):
        """
        Input data.
        """
        inputs = filter(lambda x: x.object_type() == "data", self.predecessors())
        return list(map(lambda x: Chern.VData.VData(x.path), inputs))

    def outputs(self):
        """
        Output data.
        """
        outputs = filter(lambda x: x.object_type() == "data", self.successors())
        return list(map(lambda x: Chern.VData.VData(x.path), outputs))

    def _check_parameters(self):
        """
        Check parameters
        """
        algorithm = self.algorithm()
        parameters = algorithm.parameters()
        return False
        return True

    def _check_data(self):
        """
        Check data
        """
        algorithm = self.algorithm()
        inputs = self.inputs()
        outputs = self.outputs()

    def commit(self):
        """
        change the task status from new to started.
        The status are:
            1. Check the connection between the algorithm and the task
            2. Check the status of the algorithm
            3. Check the parameter and the connection between the input data, output data and the task.
            4. Check the existence of the input volume.
            5. Create the output volume.
            4. Create a container.
            6. connect the input data, output data and the volume.
            7. start the run
        """
        if self.status() != "new":
            print("The task can be committed only if its status is \"new\"")
            return
        algorithm = self.algorithm()
        if algorithm is None:
            algorithm = EmptyAlgorithm
        if algorithm.status() != "built":
            print("The Algorithm is not built yet, please commit the algorithm first")
            return
            # FIXME: The unbuilt algorithm should be built automatically
        if not _check_parameters(algorithm):
            print("The algorithm has different parameters with the task")
            return
        if not check_data(algorithm):
            print("The data is not correspond")
            return
        inputs = self.inputs()
        for input_data in inputs:
            if input_data.status() != "done":
                print("not finished")
                return
        outputs = self.outptus()
        container = self.new_container()
        for output_data in outputs:
            output_data.new_volume()
        for input_volume in self.inputs().volume():
            container.connect(input_volume, "input")
        for output_volume in self.outputs().volume():
            container.connect(output_volume, "output")
        container.start()

    def status(self):
        """
        """
        if self.container() is None:
            return "new"
        if self.algorithm().status() != "built":
            return "new"
        if self.algorithm().image() != self.container().image():
            return "new"

        for input_data in self.inputs():
            if input_data.status() != "done":
                return "new"
        for input_data, input_volume in zip(self.inputs(), self.container().inputs()):
            if input_data.volume().uid() != input_volume.uid():
                return "new"
        return self.container().status()

    def container(self):
        container_id = self.config_file.read_variable("container_id")
        if container_id is None:
            return None
        return VContainer(self.container_id)

    def add_algorithm(self, path):
        """
        Add a algorithm
        """
        algorithm = self.get_algorithm()
        if algorithm is not None:
            print("Already have algorithm, will replace it")
            self.remove_algorithm()
        self.add_arc_from(path)
        self.set_update_time()

    def remove_algorithm(self):
        """
        Remove the algorithm
        """
        algorithm = self.get_algorithm()
        if algorithm is None:
            print("Nothing to remove")
        else:
            self.remove_arc_from(algorithm.path)
        self.set_update_time()

    def get_algorithm(self):
        """
        Return the algorithm
        """
        predecessors = self.get_predecessors()
        debug(predecessors)
        for pred_object in predecessors:
            if pred_object.object_type() == "algorithm":
                return pred_object
        print("No algorithm found")
        return None


    def check(self, site="local"):
        """
        Upload the dependence file
        """
        pwd = os.getcwd()
        if site == "local":
            os.chdir(self.get_physics_position())
            subprocess.call("bash", shell=True)
        else:
            chern_config_path = os.environ["HOME"] + "/.Chern"
            site_module = imp.load_source("site", chern_config_path+"/"+site+".py")
            site_module.check(self.get_physics_position(site))
        os.chdir(pwd)

    def add_input(self, path, alias):
        self.add_arc_from(path)
        self.set_alias(alias, path)
        self.set_update_time()

    def remove_input(self, alias):
        path = self.alias_to_path(alias)
        if path == "":
            print("Alias not found")
            return
        self.remove_arc_from(path)
        self.remove_alias(alias)
        self.set_update_time()

    def add_output(self, path, alias):
        if VObject(path).get_predecessors() != []:
            print("An output should only have only one input")
            return
        self.add_arc_to(path)
        self.set_alias(alias, path)
        self.set_update_time()

    def remove_output(self, alias):
        path = self.alias_to_path(alias)
        if path is None:
            print("Alias not found")
            return
        self.remove_arc_to(path)
        self.remove_alias(alias)
        self.set_update_time()

    def parameters(self):
        """
        Read the parameters file
        """
        parameters_file = utils.ConfigFile(self.path+"parameters")
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            return {}
        else:
            return parameters

    def add_parameter(self, parameter, value):
        """
        Add a parameter to the parameters file
        """
        if parameter == "parameters":
            print("A parameter is not allowed to be called parameters")
            return
        parameters_file = utils.ConfigFile(self.path+"/parameters.py")
        parameters_file.write_variable(parameter, value)
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        parameters.append(parameter)
        parameters_file.write_variable("parameters", parameters)
        self.set_update_time()

    def remove_parameter(self, parameter):
        """
        Remove a parameter to the parameters file
        """
        if parameter == "parameters":
            print("parameters is not allowed to remove")
            return
        parameters_file = utils.ConfigFile(self.path+"/parameters.py")
        parameters = parameters_file.read_variable("parameters")
        if parameter not in parameters:
            print("Parameter not found")
            return
        parameters.remove(parameter)
        parameters_file.write_variable(parameter, None)
        parameters_file.write_variable("parameters", parameters)
        self.set_update_time()

def create_task(path, inloop=False):
    path = utils.strip_path_string(path)
    os.mkdir(path)
    os.mkdir(path+"/.chern")
    open(path + "/parameters.py", "w").close()
    with open(path + "/.chern/config.py", "w") as f:
        f.write("object_type = \"task\"")
    with open(path + "/README.md", "w") as f:
        f.write("Please write README for this task")
    subprocess.call("vim %s/README.md"%path, shell=True)
