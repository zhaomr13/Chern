import os
import uuid
import imp
import time
import subprocess
import Chern
from Chern.kernel.VObject import VObject
from Chern.kernel.VContainer import VContainer
from Chern.kernel import VAlgorithm
from Chern.utils import utils
from Chern.utils import metadata
from Chern.utils.utils import debug
from Chern.utils.utils import colorize
from Chern.utils import csys

from Chern.kernel.ChernDatabase import ChernDatabase
from Chern.kernel.ChernCommunicator import ChernCommunicator
cherndb = ChernDatabase.instance()
cherncc = ChernCommunicator.instance()

class VTask(VObject):
    def helpme(self, command):
        from Chern.kernel.Helpme import task_helpme
        print(task_helpme.get(command, "No such command, try ``helpme'' alone."))

    def ls(self, show_readme=True, show_predecessors=True, show_sub_objects=True, show_status=False, show_successors=False):
        super(VTask, self).ls(show_readme, show_predecessors, show_sub_objects, show_status, show_successors)
        parameters, values = self.parameters()
        if parameters != []:
            print(colorize("---- Parameters:", "title0"))
        for parameter in parameters:
            print(parameter, end=" = ")
            print(values[parameter])

        if show_status:
            status = self.status()
            if status == "done":
                status_color = "success"
            else:
                status_color = "normal"
            print("****",status,"*****")
            print(colorize("**** STATUS:", "title0"),
                colorize(status, status_color) )

        if self.is_submitted() and self.container().error() != "":
            print(colorize("!!!! ERROR:\n", "title0"), self.container().error())
        if self.is_submitted():
            print("---------------")
            if not os.path.exists(self.container().path+"/output"):
                return
            files = os.listdir(self.container().path+"/output")
            if files == []: return
            files.sort()
            max_len = max([len(s) for s in files])
            columns = os.get_terminal_size().columns
            nfiles = columns // (max_len+5+7)
            for i, f in enumerate(files):
                if not f.startswith(".") and f != "README.md":
                    print(("docker:{:<"+str(max_len+5)+"}").format(f), end="")
                    if (i+1)%nfiles == 0:
                        print("")

    def inputs(self):
        """ Input data. """
        inputs = filter(lambda x: x.object_type() == "task", self.predecessors())
        return list(map(lambda x: VTask(x.path), inputs))

    def outputs(self):
        """ Output data. """
        outputs = filter(lambda x: x.object_type() == "task", self.successors())
        return list(map(lambda x: VTask(x.path), outputs))

    def resubmit(self, host = "local"):
        if not self.is_submitted():
            print("Not submitted yet.")
            return
        path = utils.storage_path() + "/" + self.impression()
        csys.rmtree(path)
        self.submit()

    def submit(self, host = "local"):
        if self.is_submitted():
            print("Already submitted")
            return
        if not self.is_impressed_fast():
            self.impress()
        cherncc.submit(host, self.path+"/.chern/impressions", self.impression())

    def view(self, file_name):
        if file_name.startswith("docker:"):
            path = self.container().path+"/output/"+file_name.replace("docker:", "").lstrip()
            if not csys.exists(path):
                print("File: {} do not exists".format(path))
                return
            subprocess.Popen("open {}".format(path), shell=True)

    def cp(self, source, dst):
        if source.startswith("docker:"):
            path = self.container().path+"/output/"+source.replace("docker:", "").lstrip()
            if not csys.exists(path):
                print("File: {} do not exists".format(path))
                return
            csys.copy(path, dst)




    def remove(self, remove_impression):
        impressions = self.config_file.read_variable("impressions", [])
        impression = self.config_file.read_variable("impression")
        if remove_impression == impression[:8]:
            print("The most recent job is not allowed to remove")
            return
        for im in impressions:
            path = utils.storage_path() + "/" + im
            if not os.path.exists(path):
                continue
            if remove_impression == im[:8]:
                print("Try to remove the job")
                container = VContainer(path)
                container.remove()
                return

    def jobs(self):
        impressions = self.config_file.read_variable("impressions", [])
        output_md5s = self.config_file.read_variable("output_md5s", {})
        if impressions == []:
            return
        impression = self.config_file.read_variable("impression")
        for im in impressions:
            path = utils.storage_path() + "/" + im
            if not os.path.exists(path):
                continue
            if impression == im:
                short = "*"
            else:
                short = " "
            short += im[:8]
            output_md5 = output_md5s.get(im, "")
            if output_md5 != "":
                short += " ({0})".format(output_md5[:8])
            status = VContainer(path).status()
            print("{0:<12}   {1:>20}".format(short, status))

    def stdout(self):
        with open(self.container().path+"/stdout") as f:
            return f.read()

    def stderr(self):
        with open(self.container().path+"/stderr") as f:
            return f.read()

    def is_submitted(self):
        if not self.is_impressed_fast():
            return False
        if cherndb.job(self.impression()) is not None:
            return True
        else:
            return False



    def output_md5(self):
        output_md5s = self.config_file.read_variable("output_md5s", {})
        return output_md5s.get(self.impression(), "")

    def status(self, consult_id = None, detailed = False):
        """
        """
        if consult_id:
            consult_table = cherndb.status_consult_table
            # config_file.read_variable("impression_consult_table", {})
            cid, status = consult_table.get(self.path, (-1,-1))
            if cid == consult_id:
                return status

        if not self.is_impressed_fast():
            if consult_id:
                consult_table[self.path] = (consult_id, "new")
            return "new"

        # hosts = cherncc.hosts()
        status = cherncc.status("local", self.impression())
        if consult_id:
            consult_table[self.path] = (consult_id, status)
        return status
        """
        if not self.is_submitted():
            if consult_id:
                consult_table[self.path] = (consult_id, "impressed")
            return "impressed"
        if self.algorithm() is not None:
            if self.algorithm().status() != "built":
                if consult_id:
                    consult_table[self.path] = (consult_id, "submitted")
                return "submitted"
            for input_data in self.inputs():
                if input_data.status(consult_id) != "done":
                    if consult_id:
                        consult_table[self.path] = (consult_id, "waitting")
                    return "waitting"
        status = self.container().status()
        if consult_id:
            consult_table[self.path] = (consult_id, status)

        if status == "done":
            output_md5 = self.output_md5()
            if output_md5 == "":
                output_md5 = self.container().output_md5()
                self.config_file.write_variable("output_md5", output_md5)
                output_md5s = self.config_file.read_variable("output_md5s", {})
                output_md5s[self.impression()] = output_md5
                self.config_file.write_variable("output_md5s", output_md5s)
        return status
        """

    def container(self):
        path = utils.storage_path() + "/" + self.impression()
        return VContainer(path)

    def add_source(self, path):
        """
        After add source, the status of the task should be done
        """
        md5 = csys.dir_md5(path)
        if self.is_impressed_fast() and md5 == self.output_md5():
            pass
        else:
            impression = uuid.uuid4().hex
            output_md5s = self.config_file.read_variable("output_md5s", {})
            impressions = self.config_file.read_variable("impressions", [])
            output_md5s[impression] = md5
            self.config_file.write_variable("output_md5s", output_md5s)
            self.config_file.write_variable("output_md5", md5)
            impressions.append(impression)
            self.config_file.write_variable("impression", impression)
            self.config_file.write_variable("impressions", impressions)
            git.add(self.path)
            git.commit("Impress: {0}".format(impression))

        job_path = utils.storage_path() + "/" + self.impression()
        cwd = self.path
        csys.copy_tree(cwd, job_path)
        container = VContainer(job_path)
        container.config_file.write_variable("job_type", "container")
        container.config_file.write_variable("status", "external")
        container.set_storage(path)
        cherndb.add_job(self.impression())

    def add_algorithm(self, path):
        """
        Add a algorithm
        """
        algorithm = self.algorithm()
        if algorithm is not None:
            print("Already have algorithm, will replace it")
            self.remove_algorithm()
        self.add_arc_from(VObject(path))


    def remove_algorithm(self):
        """
        Remove the algorithm
        """
        algorithm = self.algorithm()
        if algorithm is None:
            print("Nothing to remove")
        else:
            self.remove_arc_from(algorithm.path)

    def algorithm(self):
        """
        Return the algorithm
        """
        predecessors = self.predecessors()
        for pred_object in predecessors:
            if pred_object.object_type() == "algorithm":
                return VAlgorithm.VAlgorithm(pred_object.path)
        return None

    def add_input(self, path, alias):
        """ FIXME: judge the input type
        """
        obj = VObject(path)
        if obj.object_type() != "task":
            print("You are adding {} type object as input. The input is required to be a task.".format(obj.object_type()))
            return

        if self.has_alias(alias):
            print("The alias already exists. The original input and alias will be replaced.")
            original_object = VObject(cherndb.project_path()+"/"+self.alias_to_path(alias))
            self.remove_arc_from(original_object)
            self.remove_alias(alias)

        self.add_arc_from(obj)
        self.set_alias(alias, obj.invariant_path())

    def remove_input(self, alias):
        path = self.alias_to_path(alias)
        if path == "":
            print("Alias not found")
            return
        obj = VObject(cherndb.project_path()+"/"+path)
        self.remove_arc_from()
        self.remove_alias(alias)


    def add_output(self, file_name):
        """ FIXME: The output is now binding with the task
        """
        outputs = self.read_variable("outputs", [])
        outputs.append(file_name)
        self.write_variable("outputs", outputs)

    def remove_output(self, alias):
        """ FIXME: check existance
        """
        outputs = self.read_variable("outputs", [])
        outputs.append(file_name)
        self.write_variable("outputs", outputs)

    def parameters(self):
        """
        Read the parameters file
        """
        parameters_file = metadata.ConfigFile(self.path+"/parameters.json")
        parameters = parameters_file.read_variable("parameters", {})
        return sorted(parameters.keys()), parameters

    def add_parameter(self, parameter, value):
        """
        Add a parameter to the parameters file
        """
        parameters_file = metadata.ConfigFile(self.path+"/parameters.json")
        parameters = parameters_file.read_variable("parameters", {})
        parameters[parameter] = value
        parameters_file.write_variable("parameters", parameters)

    def remove_parameter(self, parameter):
        """
        Remove a parameter to the parameters file
        """
        parameters_file = metadata.ConfigFile(self.path+"/parameters.json")
        parameters = parameters_file.read_variable("parameters", {})
        if parameter not in parameters.keys():
            print("Parameter not found")
            return
        parameters.pop(parameter)
        parameters_file.write_variable("parameters", parameters)

def create_task(path):
    path = utils.strip_path_string(path)
    parent_path = os.path.abspath(path+"/..")
    object_type = VObject(parent_path).object_type()
    if object_type != "project" and object_type != "directory":
        return

    csys.mkdir(path+"/.chern")
    config_file = metadata.ConfigFile(path + "/.chern/config.json")
    config_file.write_variable("object_type", "task")
    task = VObject(path)

    with open(path + "/README.md", "w") as f:
        f.write("Please write README for task {}".format(task.invariant_path()))
