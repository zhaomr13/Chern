import os
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/configuration.py"

class task:
    def __init__(self, name, algorithm, algorithm_type, recreate = True):
        global global_config_path
        config = utils.read_variables("configuration", global_config_path)
        self.name = name
        self.algorithm = algorithm
        self.algorithm_type = algorithm_type
        self.project = config.current_project
        print self.project
    parents = []
    comment = ""
    input_files = ""
    output_files = ""
    project = ""

    def register(self) :
        # save the configuration
        print "starting to register job"
        global global_config_path
        config = utils.read_variables("configuration", global_config_path)
        project_path = config.projects_path[self.project]
        if not os.path.exists(project_path + "/.config/tasks") :
            os.mkdir(project_path+"/.config/tasks")
        task_path = project_path + "/.config/tasks/" + self.name + ".py"
        dic = {key:value for key, value in self.__dict__.iteritems()}
        print dic
        #utils.write_variables("")
        print "finished register job"

    def start_binary():
        print "Binary Job started"
        """
        from subprocess import Popen
        ps = Popen("", )
        return ps
        """

    def start_davinci():
        print "DaVinci Job started"

    def start_gauss():
        print "Gauss Job started"

    def start():
        if self.algorithm_type == "binary":
            return start_binary()
        if self.algorithm_type == "davinci":
            return start_davinci()
        if self.algorithm_type == "gauss":
            return start_gauss()


