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
        for dirpath, dirnames, filenames in os.walk(os.path.join(path, impression)):
            for f in filenames:
                fullpath = os.path.join(dirpath, f)
                relpath = os.path.relpath(dirpath, os.path.join(path, impression))
                tar.add(fullpath, arcname=os.path.join(relpath, f))
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
        r = requests.get("http://127.0.0.1:5000/status/{}".format(impression))
        return r.text

    def output_files(self, host, impression):
        url = self.url(host)
        r = requests.get("http://127.0.0.1:5000/outputs/{}".format(impression))
        return r.text.split()

    def get_file(self, host, impression, filename):
        url = self.url(host)
        r = requests.get("http://127.0.0.1:5000/getfile/{}/{}".format(impression, filename))
        return r.text
