from subprocess import Popen
from subprocess import PIPE

class ChernExec(Popen):
    def __init__(self, cmd, path):
        super(ChernExec, self).__init__(cmd.format(path=path), shell=True, stdin=PIPE)

    def send(self, cmd):
        self.stdin.write(cmd+" ")

    def sendline(self, cmd):
        self.stdin.write(cmd+"\n")

    def exit(self):
        self.wait()
        exit(self.poll())


