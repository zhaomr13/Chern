from Chern.VObject import VObject
class VProject(VObject):
    def __init__(self, file_name):
        print("load success")
        super(VProject, self).__init__(file_name)

    def load_object(self):
        super(VProject, self).load_object()

    def mk_data(self, file_name):
        pass

