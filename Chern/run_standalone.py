import sys
from Chern.VTask import VTask
import imp

def run_standalone(task_path, algorithm_path):
    """ This function is designed to run a standalone python program
    """
    task = VTask(task_path)
    parameters_file_list = [task.path+"/.parameters.py"]
    while task.has_super_task():
        parameters_file_list.append(task.path + "/.parameters.py")

    parameters_file_list.reverse()
    for path in parameters_file_list:
        imp.load_source("run", path)
    imp.load_source("run", algorithm_path + "/main.py")

if __name__ == "__main__":
    task_path = sys.argv[1]
    algorithm_path = sys.argv[2]
    run_standalone(task_path, algorithm_path)

