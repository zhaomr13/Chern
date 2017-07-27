import sys
from Chern.VTask import VTask
import imp

def run_standalone(task, algorithm, inputs, outputs, site):
    """ This function is designed to run a standalone python program
    """
    parameters_file_list = [task.path+"/.parameters.py"]
    # while task.has_super_task():
    # parameters_file_list.append(task.path + "/.parameters.py")

    from Chern import run
    for input_object in inputs:
        alias = task.path_to_alias(input_object.path)
        phisics_position = input_object.physics_position()
        run.inputs[alias] = physics_position
    for output_object in
    parameters_file_list.reverse()
    for path in parameters_file_list:
        imp.load_source("Chern.run", path)
    imp.load_source("Chern.run", algorithm_path + "/main.py")

if __name__ == "__main__":
    task_path = sys.argv[1]
    algorithm_path = sys.argv[2]
    run_standalone(task_path, algorithm_path)

