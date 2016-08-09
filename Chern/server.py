import os
import Chern as chen
from Chern import utils
from Chern.task import task
import time

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
class task_type:
    def __init__(self, pid, name, poll_status, ncpus, previous_node, next_node):
        self.pid = pid
        self.name = name
        self.poll_status = poll_status
        self.ncpus = ncpus
        self.previous_node = previous_node
        self.next_node = next_node

    def link_to_previous(self, node):
        if node is None : return
        node.next_node = self
        self.previous_node = node

    def link_to_next(self, node):
        if node is None : return
        node.previous_node = self
        self.next_node = node

class running_jobs_list:
    def __init__(self):
        self.size = 0
        self.tail = None

    def append(self, pid, name, ncpus):
        print "append things"
        new_node = task_type(pid, name, None, ncpus, self.tail, None)
        new_node.link_to_previous(self.tail)
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
                    present.new_node.link_to_previous(present.previous_node)
                if present is self.tail:
                    self.tail = present.previous_node
                self.size -= 1
            present = present.previous_node
        return remove_list


def get_tasks_name_list(project, status):
    # print global_config_path
    global_config = utils.read_variables("global_config", global_config_path+"/config.py")
    # print dir(global_config)
    projects_path = global_config.projects_path
    project_config_path = projects_path[project]
    project_config = utils.read_variables("project_config", project_config_path+"/.config/config.py")
    tasks_list = project_config.tasks_list if "tasks_list" in dir(project_config) else {}
    # print "tasks list here:?", tasks_list
    return [key for key, value in tasks_list.items() if value in status]

def change_task_status(project, name, status):
    # print "changing project", project, "name", name, "status to", status
    # print global_config_path
    global_config = utils.read_variables("global_config", global_config_path+"/config.py")
    projects_path = global_config.projects_path
    project_config_path = projects_path[project]
    project_config = utils.read_variables("project_config", project_config_path+"/.config/config.py")
    tasks_list = project_config.tasks_list
    if status == 0:
        tasks_list[name] = "completed"
    else:
        tasks_list[name] = "error %d"%status
    utils.write_variables(project_config, project_config_path+"/.config/config.py", [("tasks_list", tasks_list)])
    task_config = utils.read_variables("task_config", project_config_path+"/.config/tasks/" + name + ".py")
    utils.write_variables(task_config, project_config_path+"/.config/tasks/"+name+".py", [("status", tasks_list[name])])
    # print "finished changing status"


# Loop forever to start applications
while not os.path.exists(global_config_path+"/server.closed") :

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
        tasks_name_list = get_tasks_name_list(project, status = ["new"])
        # print "task_name_list = ", tasks_name_list
        for task_name in tasks_name_list:
            # print "project = ", project
            t = task(task_name, project = project, new_project = False)
            if not t.check_start(rest_ncpus):
                continue
            rest_ncpus -= t.ncpus
            ps = t.start()
            running_jobs[project].append(ps, t.name, t.ncpus)



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
    time.sleep(1)
    pass


#open(global_config_path+"/server/close", "a").close()
print "server closed."
