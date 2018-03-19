#!/usr/bin/python3
import daemon
import time
from daemon import pidfile
import sys
import subprocess
from Chern.utils import utils
from Chern.kernel.ChernDatabase import ChernDatabase
from Chern.kernel.VImage import VImage
from Chern.kernel.VContainer import VContainer
from Chern.kernel.VJob import VJob

cherndb = ChernDatabase.instance()

def execute():
    waitting_jobs = cherndb.jobs("submitted")
    for job in waitting_jobs:
        print("Flag ok", file=sys.stderr)
        flag = True
        for pred_object in job.predecessors():
            if pred_object == "container" and VContainer(pred_object.path).status() != "done":
                flag = False
                break
            if pred_object == "image" and VImage(pred_object.path).status() != "built":
                flag = False
                break
        if flag:
            job.execute()

def status():
    daemon_path = utils.daemon_path()
    return "started"
    # subprocess.call("kill {}".format(open(daemon_path + "/daemon.pid").read()), shell=True)

def start():
    daemon_path = utils.daemon_path()
    with daemon.DaemonContext(
        working_directory="/",
        pidfile=pidfile.TimeoutPIDLockFile(daemon_path + "/daemon.pid"),
        stderr=open(daemon_path + "/log", "w+"),
        ):
        while True:
            time.sleep(1)
            try:
                execute()
            except Exception as e:
                print(e)

def stop():
    daemon_path = utils.daemon_path()
    subprocess.call("kill {}".format(open(daemon_path + "/daemon.pid").read()), shell=True)
