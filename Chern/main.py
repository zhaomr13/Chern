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
def machine(command):
    """ Start or stop the chern machine"""
    if command == "start":
        daemon_start()
    elif command == "stop":
        daemon_stop()

def start_chern_ipython():
    profile_path = os.path.abspath(csys.local_config_dir()+"/profile")
    start_ipython(argv=["--profile=chern", "--ipython-dir="+profile_path])
    ip = get_ipython()
    del ip.magics_manager.magics["line"]["ls"]
    del ip.magics_manager.magics["line"]["ll"]
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

def main():
    cli()

@cli.command()
def prologue():
    """ A prologue from the author """
    print("""
Chern: A data analysis management toolkit
Author: Mingrui Zhao
        2013 - 2017       @ Center of High Energy Physics, Tsinghua University
        2017 - 2018(now)  @ Department of Nuclear Physics, China Institute of Atomic Energy
Email: mingrui.zhao@mail.labz0.org

I started the project when I was a undergraduate student in Tsinghua University and working for LHCb collaboration.
And the software in LHCb is usually named after the Great name, such as ``Gauss'' and ``Davinci''.
The term ``Chern''(陈) is a common surname in China and it is usually written as ``Chen'' in English now.
The unusual spelling "Chern" is a transliteration in the old Gwoyeu Romatzyh (GR) romanization used in the early twentieth century China.
Nowadays, when written in the form of ``Chern'', it usually refer to ``Shiing-Shen Chern'',
the great Chinese-American mathematician who made fundamental contributions to differential geometry and topology.
The well-known ``Chern classes'', ``Chern–Gauss–Bonnet theorem'' and many others are named after him.
At the same time, my girlfriend has the same surname in Chinese with S.S.Chern.
This is the origin of the software name.
""")

