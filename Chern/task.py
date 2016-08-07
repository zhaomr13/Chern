import os
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/config.py"

class task:
    def __init__(self, name, algorithm = None, algorithm_type = None, project = None, new_project = True):
        global global_config_path
        global_config = utils.read_variables("config", global_config_path)
        self.name = name
        self.project = global_config.current_project if project == None else project
        if new_project:
            self.algorithm = algorithm
            self.algorithm_type = algorithm_type
            self.status = "new"
            self.partents = []
            self.comment = ""
            self.input_files = []
            self.output_files = []
            self.ncpus = 1
        else:
            projects_path_list = global_config.projects_path_list
            task_config = utils.read_variables(name, projects_path_list[project] + "/.config/tasks/" + name + "/.py")
            for key, value in vars(task_config):
                vars(self)[key] = value

        print self.project

    def register(self) :
        # save the config
        print "starting to register job"
        global global_config_path
        config = utils.read_variables("config", global_config_path)
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
        os.symlink()
        from subprocess import Popen
        ps = Popen("./execuable.exe", shell=True)
        return ps

    def load_variable():
        pass

    def check_start(self, ncpus = "1000"):
        if ncpus < self.ncpus :
            return False
        print "checking dependencies for ", self.name
        for p in self.partents:
            t = task(name = p, project = self.project)
            if t.status != "completed":
                return False
        return True

    def start_davinci():
        print "DaVinci Job started"

    def start_gauss():
        print "Gauss Job started"

    def start(self):
        if self.algorithm_type == "binary":
            return start_binary()
        if self.algorithm_type == "davinci":
            return start_davinci()
        if self.algorithm_type == "gauss":
            return start_gauss()


