import subprocess
def upload(source, destination):
    subprocess.call("cp {0} {1}".format(source, destination), shell=True)

def download(source, destination):
    subprocess.call("cp {0} {1}".format(source, destination), shell=True)

def link(source, destination):
    subprocess.call("ln -s {0} {1}".format(source, destination), shell=True)

def run_standalone(source):
    subprocess.Popen("python {0}/run_standalone.py {0}".format(source), shell=True)

def check(source):
    os.chdir(source)
    subprocess.Popen("bash", shell=True)
