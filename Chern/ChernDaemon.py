#!/usr/bin/python3
import daemon
import time
from daemon import pidfile
import subprocess
from Chern import utils
from Chern.ChernDatabase import ChernDatabase
from Chern.VImage import VImage
from Chern.VVolume import VVolume
from Chern.VContainer import VContainer
from Chern.VJob import VJob

cherndb = ChernDatabase.instance()

def execute():
    waitting_jobs = cherndb.jobs("waitting")
    for path in waitting_jobs:
        job = VJob(path)
        flag = True
        for pred_object in job.predecessors():
            if pred_object == "volume" and VVolume(pred_object.path).status() != "generated":
                flag = False
                break
            if pred_object == "container" and VContainer(pred_object.path).status() != "done":
                flag = False
                break
            if pred_object == "image" and VImage(pred_object.path).status() != "built":
                flag = False
                break
        if flag:
            if job.job_type() == "volume":
                VVolume(path).transfer()
            if job.job_type() == "container":
                VContainer(path).execute()
            if job.job_type() == "image":
                VImage(path).execute()

def status():
    daemon_path = utils.daemon_path()
    return "started"
    # subprocess.call("kill {}".format(open(daemon_path + "/daemon.pid").read()), shell=True)

def start():
    daemon_path = utils.daemon_path()
    with daemon.DaemonContext(
        working_directory="/",
        pidfile=pidfile.TimeoutPIDLockFile(daemon_path + "/daemon.pid"),
        stderr=open(daemon_path + "/log", "w+")
        ):
        while True:
            time.sleep(1)
            execute()

def stop():
    daemon_path = utils.daemon_path()
    subprocess.call("kill {}".format(open(daemon_path + "/daemon.pid").read()), shell=True)
