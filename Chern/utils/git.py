import subprocess
def add(line):
    subprocess.call("git add {}".format(line), shell=True, stdout=subprocess.PIPE)

def commit(line):
    subprocess.call("git commit -m \"{}\"".format(line), shell=True, stdout=subprocess.PIPE)
    ps = subprocess.Popen("git rev-parse HEAD", shell=True, stdout=subprocess.PIPE)
    ps.wait()
    return ps.stdout.read().decode().strip()

def log(line):
    ps = subprocess.Popen("git --no-pager log {}".format(line), shell=True, stdout=subprocess.PIPE)
    ps.wait()
    return ps.stdout.read().decode()

def rm(line):
    subprocess.call("git rm -rf {}".format(line), shell=True, stdout=subprocess.PIPE)
