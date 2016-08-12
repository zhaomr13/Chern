import os
from Chern import utils
global_config_path = os.environ["HOME"]+"/.Chern/config.py"

class task:
    def __init__(self, name, algorithm = None, algorithm_type = None, project = None, new_project = True):
        global global_config_path
        global_config = utils.read_variables("global_config", global_config_path)
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
            projects_path = global_config.projects_path
            print projects_path, project
            print projects_path[project] + "/.config/tasks/" + name + ".py"
            task_config = utils.read_variables(name, projects_path[project] + "/.config/tasks/" + name + ".py")
            # print dir(task_config)
            dic = {key:value for key,value in task_config.__dict__.iteritems()}
            for key in dir(task_config):
                vars(self)[key] = dic[key]

        print self.project

    def register(self) :
        # save the config
        print "starting to register job"
        global global_config_path
        global_config = utils.read_variables("global_config", global_config_path)
        project_path = global_config.projects_path[self.project]
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
        project_config = utils.read_variables("project_config", project_path+"/.config/config.py")
        tasks_list = project_config.tasks_list if "tasks_list" in dir(project_config) else {}
        tasks_list[self.name] = "new"
        utils.write_variables(project_config, project_path+"/.config/config.py", [("tasks_list", tasks_list)])
        print "finished register job"

    def load_variable():
        pass

    def change_status(self):


    def check_start(self, ncpus = "1000"):
        if ncpus < self.ncpus :
            return False
        print "checking dependencies for ", self.name
        for p in self.partents:
            t = task(name = p, project = self.project)
            if t.status != "completed":
                return False
        return True


    def start_echo(self):
        print "start echo"
        print "echo program started"
        from subprocess import Popen
        ps = Popen("echo running ok", shell=True)
        return ps

    def start_binary(self):
        print "Binary Job started ..."

        global_config = utils.get_global_config()
        project_path = global_config.projects_path[self.project]

        os.chdir(project_path+"/tasks/"+self.name)

        for input_file, alias_name in self.input_files:
            task, name = tuple(input_file.split("/"))
            os.symlink(project_path+"/tasks/"+task+"/"+name, alias_name)

        output_file = open("stdout", "w")
        error_file = open("stderr", "w")
        from subprocess import Popen
        ps = Popen(project_path+"/Algs/"+algorithm+"/execuable.exe", shell=True, stdout=output_file, stderr = error_file)
        return ps

    def start_davinci(self):
        print "DaVinci Job started"

    def start_gauss(self):
        print "Gauss Job started"


    def start_copy_only(self):
        global_config = utils.get_global_config()
        project_path = global_config.projects_path[self.project]
        if not os.path.exists(project_path+"/tasks/"+self.name):
            os.mkdir(project_path+"/tasks/"+self.name)
        os.chdir(project_path+"/tasks/"+self.name)
        for input_file, alias_name in self.input_files:
            os.symlink(project_path+"/"+input_file, alias_name)
        from subprocess import Popen
        return Popen("echo Finished", shell=True)

    def start(self):
        if self.algorithm_type == "internal" and self.algorithm == "copy_only":
            return self.start_copy_only()

        if self.algorithm_type == "echo":
            return self.start_echo()

        if self.algorithm_type == "binary":
            return self.start_binary()

        if self.algorithm_type == "davinci":
            return self.start_davinci()

        if self.algorithm_type == "gauss":
            return self.start_gauss()


