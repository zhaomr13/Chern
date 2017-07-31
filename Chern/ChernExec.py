import subprocess
from subprocess import Popen
from subprocess import PIPE

class ChernExec(Popen):
    def __init__(self, cmd, path):
        super(ChernExec, self).__init__(cmd, shell=True, stdin=PIPE, stderr=PIPE)

    def send(self, cmd):
        self.stdin.write(cmd+" ")

    def sendline(self, cmd):
        self.stdin.write(cmd+"\n")

    def exit(self):
        self.wait()
        exit(self.poll())


