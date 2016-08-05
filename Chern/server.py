import os
import Chern as chen

global_config_path = os.environ["HOME"] + "/.Chern"
if os.path.exists(global_config_path+"/server/lock") :
    print "Something is wrong because of server"
    exit(0)

print "server started ..."
while not os.path.exists(global_config_path+"/server/close") :
    config = utils.read_variables("configuration", global_config_path+"/configuration.py")
    projects_list = config.projects_list
    projects_path = config.projects_path
    for project in projects_list:
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
            task.start()

    # check jobs
    # check the job list
    # for in project list
    # check project
    time.sleep(10)
    pass


open(global_config_path+"/server/close", "a").close()
