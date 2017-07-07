import os
# import Chern.VAlgorithm
# import Chern.VData
# import Chern.VTask

class VObject(object):
    """
    Virtual class of the objects, including VData, VAlgorithm, VData and VDirectory
    """
    def __init__(self, file_name):
        # def __init__(self, file_name, parent):
        """
        Set the most important and common information to the objects:
            Their parent, path, and a empty sub_objects dict.
        """
        # self.parent = parent
        # if self.parent is None:
        self.path = file_name
        # else:
        # self.path = parent.path + "/" + file_name
        self.sub_objects = {}
        self.comments = ""

    def __str__(self):
        return "%s"%(self.path)

    def __repr__(self):
        return "%s"%(self.path)


    def load_object(self):
        """
        Load a object from a directory. It will scan the
        """
        pass
        sub_directories = os.listdir(self.path)
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                object_type = self.get_type(self.path+"/"+item)
                for type_name,type_object in self.sub_types.items():
                    if object_type == type_name: self.sub_objects[item] = type_object(item, self)
                self.sub_objects[item].load_object()

    def get_type(self, path=None):
        """
        Return the type of the object under a specific path.
        If
        """
        if path is None:
            path = self.path
        with open(path + "/" + ".type") as type_file:
            return type_file.readline()[:-1]

    # def get_sub_object(self, path):
    # if sys.path.is_directory(self.path + "/" + path):
        # return VObject()

    def ls(self):
        print(self.comments)
        print(self.sub_objects)

    def mk_object(self, file_name):
        pass

    def __getitem__(self, index):
        return self.sub_objects[index]
        # return self.[index]

