class task:
    def __init__(self, name, algorithm, recreate = True)():
        self.name = name
        self.algorithm = algorithm
    parents = []
    comment = ""
    input_files = ""
    output_files = ""
    project = ""

    def register() :
        # save the configuration
        from Chern import utils
        import os
        config = utils.read_variables("configuration", os.environ["HOME"]+"/.Chern/configuration.py")
        project_path = config.projects_path[project]
        task_path = project_path + "/.config/tasks/" + name + ".py"
        variable_lists
        utils.write_variables("")

    def start_binary()
        print "Binary Job started"
        """
        from subprocess import Popen
        ps = Popen("", )
        return ps
        """

    def start_davinci()
        print "DaVinci Job started"

    def start_gauss()
        print "Gauss Job started"

    def start():
        if self.algorithm == "binary":
            return start_binary()
        if self.algorithm == "davinci":
            return start_davinci()
        if self.algorithm == "gauss"
            return start_gauss()


