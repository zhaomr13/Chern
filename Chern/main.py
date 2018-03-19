""" """
import click
import os
import Chern
from IPython import start_ipython, get_ipython
from Chern.kernel.ChernDaemon import start as daemon_start
from Chern.kernel.ChernDaemon import stop as daemon_stop

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ Chern command only is equal to `Chern ipython`
    """
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
        manager = Chern.ChernManager.get_manager()
        manager.init_project()
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
    print("started")
    profile_path = os.path.abspath(os.path.dirname(__file__) + "/data")
    print(profile_path)
    start_ipython(argv=["--profile=chern", "--ipython-dir="+profile_path])
    ip = get_ipython()
    del ip.magics_manager.magics["line"]["ls"]
    del ip.magics_manager.magics["line"]["mv"]
    del ip.magics_manager.magics["line"]["rm"]
    del ip.magics_manager.magics["line"]["cp"]
    del ip.magics_manager.magics["line"]["mkdir"]

def main():
    cli()
