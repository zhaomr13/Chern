""" """
import click
import os
from IPython import start_ipython, get_ipython
from Chern.ChernDaemon import start as daemon_start
from Chern.ChernDaemon import stop as daemon_stop

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ Chern command only is equal to `Chern daemon start` and `Chern ipython`
    """
    if ctx.invoked_subcommand is None:
        # try:
        daemon_start()
        # except:
        # print("Fail to start daemon")
        try:
            start_chern_ipython()
        except:
            print("Fail to start ipython")

@cli.command()
def config():
    """ Configue the software"""
    print("Configuration is not supported yet")

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
    profile_path = os.path.abspath(os.path.dirname(__file__) + "/../profile")
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

