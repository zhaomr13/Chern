import json
import os
import subprocess
from Chern.VJob import VJob
"""
This should have someting
A image can be determined uniquely by the ?
"""
class VImage(VJob):
    def __init__(self, file_name):
        super(VImage, self).__init__(file_name)

    def inspect(self):
        ps = subprocess.Popen("docker inspect {0}".format(self.image_id.decode()), shell=True, stdout=subprocess.PIPE)
        info = ps.communicate()
        json_info = json.loads(info[0])
        return json_info[0]

    def status(self):
        status = self.config_file.read_variable("status")
        if status is None:
            return "submitted"
        else:
            return status

    def image_id(self):
        image_id = self.read_variable("image_id")
        return image_id

    def build(self):
        """
        Build the image to change the status of the Algorithm to builded.
        It will create a unique VImage object and the md5 of the VImage will be saved.
        """
        """
            What to do:
            first: copy all the files to a temporary file directory and next
            write a docker file
            then, you should build the docker file
        """
        os.chdir(self.path)
        ps = subprocess.Popen("python3 start.py", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(ps.communicate())
        ps.wait()
        ps = subprocess.Popen("docker build .", shell=True, stdout=subprocess.PIPE)
        ps.wait()
        info = ps.communicate()[0]
        image_id = info.split()[-1]
        self.config_file.write_variable("image_id", image_id)
