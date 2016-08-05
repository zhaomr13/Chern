import os
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/configuration.py"

class task:
    def __init__(self, name, algorithm = None, algorithm_type = None, recreate = True):
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
        if not os.path.exists(task_path) :
            open(task_path, "a").close()
        dic = [(key, value) for key, value in vars(self).iteritems()]
        #print dic
        from imp import load_source
        utils.write_variables(load_source(self.name, task_path), task_path, dic)
        #utils.write_variables("")
        print vars(self)
        print "finished register job"

    def start_binary():
        print "Binary Job started"
        """
        from subprocess import Popen
        ps = Popen("", )
        return ps
        """

    def load_variable():
        pass


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


