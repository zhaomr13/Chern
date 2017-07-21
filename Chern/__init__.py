"""
Chern
"""
from Chern import utils
from Chern.VObject import VObject
from Chern.VAlgorithm import VAlgorithm #as _VAlgorithm
from Chern.VTask import VTask #as _VTask
from Chern.VData import VData #as _VData
from Chern.VDirectory import VDirectory
from Chern.VProject import VProject

# VObject.sub_types = {"Algorithm":VAlgorithm, "Task":VTask, "Data":VData, "Directory":VDirectory}
__author__ = 'Mingrui Zhao'
__version__ = '3'
__version_info = ()
__revision__ = ''
__license__ = ''
__date__ = ''

def create_object_instance(path):
    """ Create an object instance
    """
    path = utils.strip_path_string(path)
    object_config_file = utils.ConfigFile(path+"/.config.py")
    object_type = object_config_file.read_variable("object_type")
    vobject_class = {"algorithm":VAlgorithm,
                     "task":VTask,
                     "data":VData,
                     "directory":VDirectory,
                     "project":VProject}
    return vobject_class[object_type](path)




