"""
Created by Mingrui Zhao @ 2017
define some classes and functions used throughout the project
"""
# Load module
import os
import shutil
import uuid
from colored import fg, bg, attr

def colorize(string, color):
    """ Make the string have color
    """
    if color == "success":
        return fg("green")+string+attr("reset")
    elif color == "normal":
        return fg("blue")+ string +attr("reset")
    elif color == "running":
        return fg("yellow")+ string +attr("reset")
    elif color == "warning":
        return "\033[31m" + string + "\033[m"
    elif color == "debug":
        return "\033[31m" + string + "\033[m"
    elif color == "comment":
        return fg("blue")+ string +attr("reset")
    elif color == "title0":
        return fg("red")+attr("bold")+string+attr("reset")
    return string

def color_print(string, color):
    print(colorize(string, color))
