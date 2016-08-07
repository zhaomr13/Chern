import os
import Chern as chen
from Chern import utils
from Chern.task import task

# global configurations
global_config_path = os.environ["HOME"] + "/.Chern"
rest_ncpus = 100

# Why do I need such a lock?
# if os.path.exists(global_config_path+"/server/lock") :
# print "Something is wrong because of server"
# exit(0)

print "server started."
# Setup a running tasks list for every project
running_jobs = {}

# Data structure for saving running tasks status
from collections import namedtuple
task_type = namedtuple("task_type", ["pid", "name", "poll_status", "previous_node", "next_node"])

class running_jobs_list:
    def __init__(self):
        self.size = 0
        self.tail = None

    def append(self, pid, name):
        new_node = task_type(pid, name, None, next_node, tail, None)
        if self.tail is not None:
            self.tail.next_node = new_node
        self.tail = new_node
        self.size += 1

    def remove(self):
        remove_list = []
        present = self.tail
        while present is not None:
            present.poll_status = present.pid.poll()
            if present.poll_status is not None:
                remove_list.append(present)
                if present.next_node is not None:
                    present.next_node.previous_node = present.previous_node
                if present.previous_node is not None:
                    present.previous_node.next_node = present.new_node
                if present is self.tail:
                    self.tail = present.previous_node
                size -= 1
            present = present.previous_node
        return remove_list


def get_tasks_name_list(project, status):
    return ["hello"]

# Loop forever to start applications
while not os.path.exists(global_config_path+"/server/lock") :

    # Get the global configurations
    global_config = utils.read_variables("config", global_config_path+"/config.py")
    projects_list = global_config.projects_list
    projects_path = global_config.projects_path

    # Loop over all the projects
    for project in projects_list:
        # Create new list for new project
        if not project in running_jobs:
            running_jobs[project] = running_jobs_list()
        # Remove the finished jobs and change the status according to the return value
        finished_list = running_jobs[project].remove()
        for t in finished_list:
            rest_ncpus += t.ncpus
            change_task_status(project, t.name, t.poll_status)

        # Add new jobs according to cpus
        tasks_name_list = get_tasks_name_list(project, status = "new")
        for task_name in tasks_name_list:
            t = task(task_name, project)
            if not t.check_start(rest_ncpus):
                continue
            rest_ncpus -= t.ncpus
            ps = t.start()
            running_jobs[project].append(ps, t.name)



        """
        c = utils.read_variables("tasks", projects_path[project])
        #ncpus = c.ncpus
        for index, ps in enumerate(running_jobs):
            # reminder : this is a quite slow process that can be accerated
            # if finished
            if ps != None and ps.poll() != None:
                ps = None

        for tasks in tasks_list:
            # tryto start tasks
            task = task(name)
            change_task_status(project, task_name, "starting")
            task.start()
            change_task_status(project, task_name, "running")
        """

    # check jobs
    # check the job list
    # for in project list
    # check project
    time.sleep(10)
    pass


open(global_config_path+"/server/close", "a").close()
print "server closed."
