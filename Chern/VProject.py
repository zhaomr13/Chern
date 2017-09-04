from Chern.VObject import VObject
from Chern.utils import debug
class VProject(VObject):
    pass

    def helpme(self, command):
        if command == "":
            print("""Hello, you are in the VProject object, what would you like to do?
The commands to use:
    cd [object]
    ls : list the containings
    mktask :
    mkalgorithm :
    mkdata
""")
        elif command == "cd":
            print("""The usage of cd:
    cd [object]
                  """)

