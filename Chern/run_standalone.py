import sys
task_path = sys.argv[1]
algorithm_path = sys.argv[2]

from Chern.VTask import VTask

task = VTask(task_path)
parameters = task.get_parameters()
parameters_file_list = []
while task.has_super_task():
    parameters_file_list.append(task.path + "/.parameters.py")

print("Running")

import imp
for path in parameters_file_list.reverse():
    imp.load_source("run", path)
imp.load_source("run", algorithm_path + "/main.py")
