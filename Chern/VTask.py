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

    def get_inputs(self):
        """
        Input data.
        """
        inputs = filter(lambda x: x.object_type() == "data", self.get_predecessors())
        return list(map(lambda x: Chern.VData.VData(x.path), inputs))

    def get_outputs(self):
        """
        Output data.
        """
        outputs = filter(lambda x: x.object_type() == "data", self.get_successors())
        return list(map(lambda x: Chern.VData.VData(x.path), outputs))

    def status(self):
        """
        Get the status of the current task.
        """
        version = self.latest_version()
        if version is None:
            return "new"
        else:
            physics_position = self.get_physics_position()
            if os.path.exists(physics_position+"/finished"):
                return "finished"
            elif os.path.exists(physics_position+"/started"):
                return "started"
            else:
                return "submitted"

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

    def get_sites(self):
        """
        Get all the available sites for the project.
        """
        chern_config_path = os.environ["CHERNCONFIGPATH"] + "/config.py"
        config_file = utils.ConfigFile(chern_config_path)
        return config_file.read_variable("sites")

    def get_site(self):
        """
        Get the available site for this object.
        """
        sites = set(self.get_sites())
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        for input_object in inputs:
            sites = sites & set(input_object.get_sites())
        for output_object in outputs:
            sites &= set(output_object.get_sites())
        for site in self.get_sites():
            if site in sites:
                return site
        return None

    def new_version(self, site):
        """
        Create a new version of the task.
        """
        config_file = utils.ConfigFile(self.path+"/.config.py")
        version = uuid.uuid4().hex
        config_file.write_variable("version", version)
        chern_config_path = os.environ["CHERNCONFIGPATH"]+"/config.py"
        config_file = utils.ConfigFile(chern_config_path)
        sites = config_file.read_variable("sites")
        os.mkdir(self.get_physics_position())
        os.mkdir(self.get_physics_position(site))

    def prepare_task_file(self, site):
        io_file = utils.ConfigFile(self.get_physics_position() + "/inputs_outputs.py")
        debug("The io file is", io_file)
        inputs = self.get_inputs()
        debug(inputs)
        outputs = self.get_outputs()
        input_files = {}
        output_files = {}
        for input_data in inputs:
            alias = self.path_to_alias(input_data.path)
            input_files[alias] = input_data.get_physics_position(site)
        for output_data in outputs:
            alias = self.path_to_alias(output_data.path)
            output_files[alias] = output_data.get_physics_position(site)
        output_files["stdout"] = self.get_physics_position(site)+"/stdout"
        output_files["stderr"] = self.get_physics_position(site)+"/stderr"
        io_file.write_variable("inputs", input_files)
        io_file.write_variable("outputs", output_files)
        io_file.write_variable("path", self.get_physics_position(site))

    def latest_version(self):
        """
        Get the last version of the task.
        """
        config_file = utils.ConfigFile(self.path+"/.config.py")
        version = config_file.read_variable("version")
        return version

    def submit(self):
        """
        Submit the task to a site.
        """
        site = self.get_site()
        if site is None:
            print("No available site found!")
            return
        # Calculate the dependence
        max_input_time = self.get_update_time()
        inputs = self.get_inputs()
        for input_data in inputs:
            update_time = input_data.get_update_time(site)
            max_input_time = max(max_input_time, update_time)
        algorithm = self.get_algorithm()
        if algorithm is not None:
            max_input_time = max(max_input_time, algorithm.get_update_time())
        outputs = self.get_outputs()
        update = False
        debug("max_input_time", max_input_time)
        for output_data in outputs:
            debug("output")
            debug(output_data)
            debug(output_data.get_update_time(site))
            if output_data.get_update_time(site) < max_input_time:
                update = True
                break
        if not update:
            print("Nothing to update")
            return
        for output_data in outputs:
            debug(output_data)
            debug("set output version")
            output_data.new_version(site)
            output_data.set_update_time(site)
        self.new_version(site)
        self.prepare_task_file(site)

        physics_position = self.get_physics_position(site)
        self.upload(self.path+"/*", physics_position, site)

        io_file = self.get_physics_position() + "/inputs_outputs.py"
        self.upload(io_file, physics_position, site)
        debug(algorithm)
        if algorithm is not None:
            self.upload(algorithm.path+"/*", physics_position, site)
        run_file = os.environ["CHERNSYSROOT"] +"/bin/run_standalone.py"
        self.upload(run_file, physics_position, site)
        # self.run_standalone(site)

    def run_standalone(self, site):
        """
        Standalone run the project
        """
        chern_config_path = utils.strip_path_string(os.environ.get("CHERNCONFIGPATH"))
        global_config_path = chern_config_path+"/config.py"
        config_file = utils.ConfigFile(global_config_path)
        site_module = imp.load_source("site", "/home/zhaomr/.Chern"+"/"+site+".py")
        site_module.run_standalone(self.get_physics_position(site))

    def get_physics_position(self, site="local"):
        """
        Calculate the physics position of the last site
        """
        chern_config_path = utils.strip_path_string(os.environ.get("CHERNCONFIGPATH"))
        if site == "local":
            return os.path.normpath(chern_config_path+"/local/task/"+self.latest_version())
        global_config_path = chern_config_path +"/config.py"
        config_file = utils.ConfigFile(global_config_path)
        sites = config_file.read_variable("sites")
        return os.path.normpath(sites[site]+"/task/"+self.latest_version())

    def upload(self, source, destination, site):
        """
        Upload the dependence file
        """
        chern_config_path = utils.strip_path_string(os.environ.get("CHERNCONFIGPATH"))
        global_config_path = chern_config_path+"/config.py"
        config_file = utils.ConfigFile(global_config_path)
        sites = config_file.read_variable("sites")
        site_module = imp.load_source("site", "/home/zhaomr/.Chern"+"/"+site+".py")
        site_module.upload(source, destination)

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
        if VObject(path).get_predecessors() == []:
            print("The output is empty")
            return
        path = self.alias_to_path(alias)
        self.remove_arc_to(path)
        self.remove_alias(alias)
        self.set_update_time()

    def has_super_task(self):
        config_file = utils.ConfigFile(self.path + "/../.config.py")
        return config_file.read_variable("object_type") == "task"

    def get_parameters(self):
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
    with open(path + "/.config.py", "w") as f:
        f.write("object_type = \"task\"")
    with open(path + "/.README.md", "w") as f:
        f.write("Please write README for this task")
    subprocess.call("vim %s/.README.md"%path, shell=True)
