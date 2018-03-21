from IPython.core.magic import register_line_magic

from Chern.interface import shell

@register_line_magic
def mkalgorithm(line):
    try:
        shell.mkalgorithm(line, inloop=False)
    except Exception as e:
        print(e)
        print("Fail to make algorithm")
del mkalgorithm

@register_line_magic
def mktask(line):
    try:
        shell.mktask(line, inloop=False)
    except Exception as e:
        print(e)
        print("Fail to make task")
del mktask

@register_line_magic
def mkdir(line):
    try:
        shell.mkdir(line, inloop=False)
    except Exception as e:
        print(e)
        print("Fail to make directory.")
del mkdir


