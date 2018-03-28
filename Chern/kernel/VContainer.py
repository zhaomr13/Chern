"""

"""
import subprocess
import Chern
from Chern.utils import utils
from Chern.kernel.VJob import VJob

class VContainer(VJob):
    """
    A VContainer should manage the physical container.
    The VContainer should be able to interact with the, or a
    A container should be able to be created from a task?
    What to determine a container?
    """
    def __init__(self, path):
        """
        Set the uuid
        """
        super(VContainer, self).__init__(path)
        pass

    def add_input(self, path, alias):
        self.add_arc_from(path)
        self.set_alias(alias, path)

    def inputs(self):
        """
        Input data.
        """
        inputs = filter(lambda x: x.job_type() == "container",
                        self.predecessors())
        return list(map(lambda x: Chern.VData.VData(x.path), inputs))


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
        parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
        parameters_file.write_variable(parameter, value)
        parameters = parameters_file.read_variable("parameters")
        if parameters is None:
            parameters = []
        parameters.append(parameter)
        parameters_file.write_variable("parameters", parameters)
        self.set_update_time()

    def storage(self):
        storage = self.config_file.read_variable("storage")
        if storage is None:
            return self.path + "/output"
        else:
            return storage

    def set_storage(self, path):
        self.config_file.write_variable("storage")

    def image(self):
        predecessors = self.predecessors()
        for pred_job in predecessors:
            if pred_job.job_type() == "image":
                return Chern.VImage.VImage(pred_job.path)
        return None

    def container_id(self):
        container_id = self.config_file.read_variable("container_id")
        return container_id

    def impression(self):
        impression = self.config_file.read_variable("impression")
        return impression

    def create_container(self, container_type="task"):
        mounts = "-v /data/{}:{}".format(self.impression(), self.storage())
        for input_container in self.inputs():
            mounts += " -v /data/{}:{}:ro".format(input_container.impression(),
                                                  input_container.storage())
        print(self.image().image_id())
        print(mounts)
        if container_type == "task":
            image_id = self.image().image_id()
        elif container_type == "data":
            image_id = "empty"
        ps = subprocess.Popen("docker create {0} {1}".format(mounts, image_id),
                              shell=True, stdout=subprocess.PIPE)
        ps.wait()
        container_id = ps.stdout.read().decode().strip()
        self.config_file.write_variable("container_id", container_id)

    def copy_arguments_file(self):
        arguments_file = self.path + "/arguments"
        ps = subprocess.Popen("docker cp {0} {1}:/root".format(arguments_file, self.container_id())
                              , shell=True)
        ps.wait()


    def parameters(self):
        """ Read the parameters file
        """
        parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
        parameters = parameters_file.read_variable("parameters", [])
        return parameters

    def create_arguments_file(self):
        try:
            parameters_file = utils.ConfigFile(self.path+"/.chern/parameters.py")
            parameters = self.parameters()
            parameter_str = ""
            for parameter in parameters:
                value = parameters_file.read_variable(parameter)
                parameter_str += "        storage[\"{0}\"] = \"{1}\";\n".format(parameter, value)
            folder_str = ""
            for folder in self.inputs():
                alias = self.path_to_alias(folder.path)
                location = "/data/" + folder.image_id()
                folder_str += "        storage[\"{0}\"] = \"{1}\";\n".format(alias, location)
            folder_str += "        storage[\"output\"] = \"/data/{0}\";\n".format(self.impression())
            argument_txt = """#ifndef CHERN_ARGUMENTS
#define CHERN_ARGUMENTS
#include <map>
#include <string>
namespace chern{{
class Parameters{{
  public:
    std::map<std::string, std::string> storage;

    Parameters() {{
{0}
    }}

    std::string operator [](std::string name) const {{
      return std::string(storage.at(name));
    }}
}};

class Folders{{
  public:
    std::map<std::string, std::string> storage;

    Folders() {{
{1}
    }}

    std::string operator [](std::string name) const {{
      return std::string(storage.at(name));
    }}
}};
}};
const chern::Parameters parameters;
const chern::Folders folders;
#endif
""".format(parameter_str, folder_str)
            with open(self.path+"/arguments", "w") as f:
                f.write(argument_txt)
        except Exception as e:
            raise e

    def set_parameters(self):
        pass

    def inspect(self):
        ps = subprocess.Popen("docker inspect {0}".format(self.container_id) )
        ps.wait()
        output = ps.communicate()[0]
        json_result = json.loads(output)
        return json_result[0]

    def status(self):
        status = self.config_file.read_variable("status")
        if status is None:
            return "submitted"
        return status
        status = self.inspect().get("State")
        if status.get("Running"):
            return "running"
        return status.get("Status")

    def kill(self):
        ps = subprocess.Popen("docker kill {0}".format(self.container_id()),
                              shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        ps.wait()

    def start(self):
        ps = subprocess.Popen("docker start -a {0}".format(self.container_id()),
                              shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        ps.wait()
        stdout = self.path + "/stdout"
        with open(stdout, "w") as f:
            f.write(ps.stdout.read().decode())
        return (ps.poll() == 0)

    def copy_inputs(self):
        inputs = self.inputs()
        for input_volume in inputs:
            subprocess.Popen("docker cp {0} {0}:dfasdfa", docker_file)

    def execute(self):
        self.config_file.write_variable("status", "running")
        try:
            self.create_arguments_file()
            self.create_container()
            self.copy_arguments_file()
            status = self.start()
        except Exception as e:
            with open(error_file, "w") as f:
                f.write(str(e))
            raise e
        if status :
            self.config_file.write_variable("status", "finished")
        else:
            self.config_file.write_variable("status", "failed")
