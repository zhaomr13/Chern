from Chern.VObject import VObject
from Chern.utils import debug
class VProject(VObject):
    def __init__(self, file_name):
        debug("VProject:__init__")
        debug("VProject:__init__")
        super(VProject, self).__init__(file_name)

    def load_object(self):
        super(VProject, self).load_object()

    def mk_data(self, file_name):
        pass

