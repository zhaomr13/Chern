from Chern.VObject import VObject
class VDirectory(VObject):
    def __init__(self, file_name, parent):
        super(VDirectory, self).__init__(file_name, parent)
        with open(self.path+"/.type", "w") as type_file:
            type_file.write("Directory")

    def load_object(self):
        super(VDirectory, self).load_object()

    def mk_data(self, file_name):
        pass

