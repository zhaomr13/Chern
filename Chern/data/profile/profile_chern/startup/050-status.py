from IPython.core.magic import register_line_magic

from Chern.interface import shell

import click
from click.testing import CliRunner
runner = CliRunner()

#----------
@click.command()
def status():
    """ Show the status of the objects. """
    shell.status()
click_status = status

@register_line_magic
def status(line):
    result = runner.invoke(click_status, line.split())
    print(result.output.rstrip("\n"))
del status
