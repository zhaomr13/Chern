"""

"""
from Chern.VJob import VJob
class VContainer(VJob):
    """
    A VContainer should manage the physical container.
    The VContainer should be able to interact with the, or a
    A container should be able to be created from a task?
    What to determine a container?
    """
    def __init__(self):
        """
        Set the uuid
        """
        super(VContainer, self).__init__(file_name)
        pass

    def add_input(self, path, alias):
        self.add_arc_from(path)
        self.set_alias(alias, path)


    def add_output(self, path, alias):
        if VObject(path).predecessors() != []:
            print("An output should only have only one input")
            return
        self.add_arc_to(path)
        self.set_alias(alias, path)
        self.set_update_time()

    def add_output(self, path, alias):
        if VObject(path).predecessors() != []:
            print("An output should only have only one input")
            return
        self.add_arc_to(path)
        self.set_alias(alias, path)

    def add_algorithm(self, path):
        """
        Add a algorithm
        """
        algorithm = self.algorithm()
        if algorithm is not None:
            print("Already have algorithm, will replace it")
            self.remove_algorithm()
        self.add_arc_from(path)

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


    def add_input(self):
        pass

    def add_output(self):
        pass

    def image(self):
        pass

    def set_parameters(self):
        pass

    def inspect(self):
        ps = subprocess.Popen("docker inspect {0}".format(self.container_id) )
        ps.wait()
        output = ps.communicate()[0]
        json_result = json.loads(output)
        return json_result[0]

    def status(self):
        status = self.inspect().get("State")
        if status.get("Running"):
            return "running"
        return status.get("Status")

    def start(self):
        subprocess.Popen("docker start {0}".format(self.image().image_id()) )
        pass

    def copy_inputs(self):
        inputs = self.inputs()
        for input_volume in inputs:
            subprocess.Popen("docker cp {0} {0}:dfasdfa", docker_file)

    def execute(self):
        self.start()
        self.copy_inputs()
        self.copy_parameters()
        self.run()
