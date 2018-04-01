from IPython.core.magic import register_line_magic

from Chern.interface import shell

import click
from click.testing import CliRunner
runner = CliRunner()

#----------
@click.command()
@click.argument("object")
@click.option('--use-template', is_flag=True, help="Use a template")
def mkalgorithm(object, use_template):
    shell.mkalgorithm(object, use_template)
click_mkalgorithm = mkalgorithm

@register_line_magic
def mkalgorithm(line):
    result = runner.invoke(click_mkalgorithm, line.split())
    print(result.output.rstrip("\n"))
del mkalgorithm

#----------
@click.command()
@click.argument("object")
def mktask(object):
    shell.mktask(object)
click_mktask = mktask

@register_line_magic
def mktask(line):
    result = runner.invoke(click_mktask, line.split())
    print(result.output.rstrip("\n"))
del mktask

#----------
@click.command()
@click.argument("object")
def mkdir(object):
    print("hello?")
    shell.mkdir(object)
click_mkdir = mkdir

@register_line_magic
def mkdir(line):
    result = runner.invoke(click_mkdir, line.split())
    print(result.output.rstrip("\n"))
del mkdir
