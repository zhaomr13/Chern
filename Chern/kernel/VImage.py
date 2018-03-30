import json
import os
import sys
import subprocess
from Chern.kernel.VJob import VJob
"""
This should have someting
A image can be determined uniquely by the ?
"""
class VImage(VJob):
    def __init__(self, file_name):
        super(VImage, self).__init__(file_name)

    def inspect(self):
        ps = subprocess.Popen("docker inspect {0}".format(self.image_id().decode()), shell=True, stdout=subprocess.PIPE)
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
        image_id = self.config_file.read_variable("image_id")
        return image_id.decode()


    def execute(self):
        self.config_file.write_variable("status", "building")
        try:
            entrypoint = open(self.path+"/entrypoint.sh", "w")
            # entrypoint.write("""#!/bin/bash\n$@\nmd5sum output\n""")
            entrypoint.write("""#!/bin/bash\n$@\n""")
            entrypoint.close()
            self.build()
        except Exception as e:
            self.append_error("Fail to build the image!\n"+str(e))
            self.config_file.write_variable("status", "failed")
            raise e
        self.config_file.write_variable("status", "built")

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
        ps = subprocess.Popen("docker build .", shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ps.wait()
        if ps.poll() != 0:
            raise Exception(ps.stderr.read().decode())
        info = ps.communicate()[0]
        image_id = info.split()[-1]
        self.config_file.write_variable("image_id", image_id)
