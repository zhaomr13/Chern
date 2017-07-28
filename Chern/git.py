import subprocess
def add(line):
    subprocess.call("git add {}".format(line), shell=True)

def commit(line):
    subprocess.call("git commit -a -m \"{}\"".format(line), shell=True)

def rm(line):
    subprocess.call("git rm -r {}".format(line), shell=True)
