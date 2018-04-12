""" """
import click
import os
import Chern
from IPython import start_ipython, get_ipython
from Chern.kernel import VProject
from Chern.kernel.ChernDaemon import start as daemon_start
from Chern.kernel.ChernDaemon import stop as daemon_stop
from Chern.utils import csys
from Chern.kernel.ChernDatabase import ChernDatabase
cherndb = ChernDatabase.instance()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ Chern command only is equal to `Chern ipython`
    """
    if is_first_time():
        start_first_time()
    if ctx.invoked_subcommand is None:
        try:
            start_chern_ipython()
        except:
            print("Fail to start ipython")

@cli.command()
def config():
    """ Configue the software"""
    print("Configuration is not supported yet")

@cli.command()
def ipython():
    """ Start IPython """
    try:
        start_chern_ipython()
    except:
        print("Fail to start ipython")

@cli.command()
def init():
    """ Add the current directory to project """
    try:
        VProject.init_project()
        start_chern_ipython()
    except Exception as e:
        print(e)
        print("Fail to start ipython")

@cli.command()
@click.argument("path", type=str)
def use(path):
    """ Use a directory as the project"""
    try:
        VProject.use_project(path)
        start_chern_ipython()
    except:
        print("Fail to start ipython")

@cli.command()
@click.argument("command", type=str)
def daemon(command):
    """ Start or stop the daemon"""
    if command == "start":
        daemon_start()
    elif command == "stop":
        daemon_stop()

def start_chern_ipython():
    profile_path = os.path.abspath(csys.local_config_dir()+"/profile")
    start_ipython(argv=["--profile=chern", "--ipython-dir="+profile_path])
    ip = get_ipython()
    del ip.magics_manager.magics["line"]["ls"]
    del ip.magics_manager.magics["line"]["mv"]
    del ip.magics_manager.magics["line"]["rm"]
    del ip.magics_manager.magics["line"]["cp"]
    del ip.magics_manager.magics["line"]["mkdir"]

def is_first_time():
    if not os.path.exists(csys.local_config_dir()):
        return True
    if not os.path.exists(csys.local_config_dir()+"/profile"):
        return True
    if cherndb.projects() == []:
        return True
    return False

def start_first_time():
    csys.mkdir(csys.local_config_dir())
    data_path = os.path.abspath(os.path.dirname(__file__) + "/data/profile")
    csys.copy_tree(data_path, csys.local_config_dir()+"/profile")

@cli.command()
def prologue():
    """ A prologue from the author """
    print("""
Chern: A data analysis management toolkit
Author: Mingrui Zhao, dedicated to Sidan
2013 - 2017 @ Center of High Energy Physics, Tsinghua University
2017 -  now @ Department of Nuclear Physics, China Institute of Atomic Energy
Email: mingrui.zhao@mail.labz0.org""")

def main():
    cli()
