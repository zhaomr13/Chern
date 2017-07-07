#!/usr/bin/python

from Chern.VObject import VObject
from Chern.VAlgorithm import VAlgorithm #as _VAlgorithm
from Chern.VTask import VTask #as _VTask
from Chern.VData import VData #as _VData
from Chern.VDirectory import VDirectory
VObject.sub_types = {"Algorithm":VAlgorithm, "Task":VTask, "Data":VData, "Directory":VDirectory}

from Chern import utils

__author__ = 'Mingrui Zhao'
__version__ = '3'
__version_info = ()
__revision__ = ''
__license__ = ''
__date__ = ''
