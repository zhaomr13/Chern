import imp

"""
class ChernExec(Popen):
    def __init__(self, cmd, path):
        super(ChernExec, self).__init__(cmd.format(path=path), shell=True, stdin=PIPE)

    def send(self, cmd):
        self.stdin.write((cmd+" ").encode())
        self.stdin.flush()

    def sendline(self, cmd):
        self.stdin.write((cmd+"\n").encode())
        self.stdin.flush()

    def exit(self):
        self.wait()
        exit(self.poll())
"""

class ChernAlgorithm(object):
    instance = None
    host_path = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = ChernAlgorithm()
        return cls.instance

    def load_source(self):
        imp.load_source("user_runner", self.host_path+"/ChernRunner.py")

    def __init__(self):
        self.envs = []
        self.commands = []
        pass

    def base(self, arg):
        self.base = arg

    def env(self, arg):
        self.envs.append(arg)

    def command(self, arg):
        self.commands.append(arg)

    def write_docker_file(self):
        docker_file = open("{0}/Dockerfile".format(self.host_path), "w")
        docker_file.write("FROM {0}\n".format(self.base))
        docker_file.write("USER root\n")
        docker_file.write("ENV HOME /root\n")
        docker_file.write("WORKDIR /root\n")
        for env in self.envs:
            docker_file.write("ENV {0}\n".format(env))
        for command in self.commands:
            docker_file.write("RUN {0}\n".format(command))
