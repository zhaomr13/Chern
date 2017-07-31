import sys
import os
import imp

def run_standalone(path):
    """ This function is designed to run a standalone python program
    """
    # while task.has_super_task():
    # parameters_file_list.append(task.path + "/.parameters.py")
    parameters_file = path + "/parameters.py"
    input_output_file = path + "/inputs_outputs.py"
    main_file = path + "/main.py"
    if os.path.exists(parameters_file):
        imp.load_source("run", parameters_file)
    if os.path.exists(input_output_file):
        imp.load_source("run", input_output_file)
    if os.path.exists(main_file):
        imp.load_source("run", main_file)

if __name__ == "__main__":
    path = sys.argv[1]
    run_standalone(path)
