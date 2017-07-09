import os
from Chern import utils
# import Chern.VAlgorithm
# import Chern.VData
# import Chern.VTask

class VObject(object):
    """
    Virtual class of the objects, including VData, VAlgorithm, VData and VDirectory
    """
    def __init__(self, file_name):
        """
        Set the most important and common information to the objects:
            Their parent, path, and a empty sub_objects dict.
        """
        self.path = file_name

    def __str__(self):
        return "%s"%(self.path)

    def __repr__(self):
        return "%s"%(self.path)

    def get_type(self, path=None):
        """
        Return the type of the object under a specific path.
        If
        """
        if path is None:
            path = self.path
        config_file = utils.ConfigFile(path + "/" + ".config.py")
        return config_file.read_variable("object_type")
        # with open(path + "/" + ".type") as type_file:
        # return type_file.readline()[:-1]

    # def get_sub_object(self, path):
    # if sys.path.is_directory(self.path + "/" + path):
        # return VObject()

    def ls(self):
        # print(self.readme())
        # print(self.sub_objects())
        sub_objects = self.sub_objects()
        sub_objects.sort(key=lambda x:x[1])
        for item, object_type in sub_objects:
            print("{0:>10} {1:>20}".format(object_type, item))

    def mk_object(self, file_name):
        pass

    def sub_objects(self):
        sub_directories = os.listdir(self.path)
        sub_object_list = []
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                object_type = self.get_type(self.path+"/"+item)
                sub_object_list.append((item, object_type))
        return sub_object_list

    def readme(self):
        with open(self.path+"/.README.md") as f:
            return f.read()

    def edit_comment(self):
        pass

    def __getitem__(self, index):
        pass
        # return self.sub_objects[index]
        # return self.[index]

    def load_object(self):
        """
        Load a object from a directory. It will scan the
        sub_directories = os.listdir(self.path)
        for item in sub_directories:
            if os.path.isdir(self.path+"/"+item):
                object_type = self.get_type(self.path+"/"+item)
                for type_name,type_object in self.sub_types.items():
                    if object_type == type_name: self.sub_objects[item] = type_object(item, self)
                self.sub_objects[item].load_object()
        """
        return

