"""
Chern class for communicate to local and remote server.
"""

import tarfile
import os
import requests
from Chern.utils import csys
from Chern.utils import metadata
class ChernCommunicator(object):
    ins = None
    def __init__(self):
        self.local_config_path = csys.local_config_path()
        self.config_file = metadata.ConfigFile(self.local_config_path+"/hosts.json")

    @classmethod
    def instance(cls):
        if cls.ins is None:
            cls.ins = ChernCommunicator()
        return cls.ins

    def submit(self, host, path, impression, readme=None):
        tarname = "/tmp/{}.tar.gz".format(impression)
        tar = tarfile.open(tarname, "w:gz")
        for dirpath, dirnames, filenames in os.walk(os.path.join(path, impression, "contents")):
            for f in filenames:
                fullpath = os.path.join(dirpath, f)
                tar.add(fullpath, arcname=os.path.join("contents", f))
        if readme is not None:
            tar.add(readme, "README.md")
        tar.close()

        files = { "{}.tar.gz".format(impression) : open(tarname, "rb").read() }
        url = self.url(host)
        requests.post(url, data = {'tarname': "{}.tar.gz".format(impression)}, files = files)

    def add_host(self, host, url):
        pass

    def localhost(self):
        return "http://127.0.0.1:5000/upload"
        # return self.config_file.read_variable("localhost")

    def url(self, host):
        return "http://127.0.0.1:5000/upload"
        # hosts
        return hosts[host]

    def status(self, host, impression):
        url = self.url(host)
        r = requests.get("http://127.0.0.1:5000/test")
        return r.text
