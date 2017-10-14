"""
VData module, contains a class and a function.
The class VData is the VObject whose type is data.
The function will create a VData from a path.
"""
import os
import uuid
import time
import imp
import subprocess
from Chern import utils
from Chern.VObject import VObject
from Chern.utils import colorize
class VData(VObject):
    """
    Virtual Data.
    """
    def ls(self):
        """
        First use the VObject ls, and then print the supported sites of this data
        FIXME: list the files in the local site
        """
        super(VData, self).ls()
        sites = self.get_sites()
        print(colorize("---- Supported sites of this data:", "title0"))
        for site in sites:
            print(site, end=" ")
        print("\n")

    def get_sites(self):
        """
        Read the sites variable from the config file of this data.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        sites = config_file.read_variable("sites")
        if sites is None:
            return []
        return sites

    def check(self, site="local"):
        """
        Upload the dependence file
        """
        pwd = os.getcwd()
        if site == "local":
            os.chdir(self.get_physics_position())
            subprocess.call("bash", shell=True)
        else:
            chern_config_path = os.environ["HOME"] + "/.Chern"
            site_module = imp.load_source("site", chern_config_path+"/"+site+".py")
            site_module.check(self.get_physics_position(site))
        os.chdir(pwd)

    def add_site(self, site):
        """
        Add a site for the current data.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        sites = config_file.read_variable("sites")
        if sites is None:
            sites = []
        sites.append(site)
        config_file.write_variable("sites", sites)

    def remove_site(self, site):
        """
        Remove a site from the current data. If the site is not in the data, do nothing.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        sites = config_file.read_variable("sites")
        if sites is None:
            return
        if site in sites:
            sites.remove(site)
        config_file.write_variable("sites", site)

    def add_rawdata(self, path, site):
        """
        Create a rawdata.
        """
        new_version = self.new_version()
        self.new_version()
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        rawdata = config_file.read_variable("rawdata")
        if rawdata is None:
            rawdata = []
        rawdata.append((new_version, "+" + rawdata))
        config_file.write_variable("site", site)
        config_file.write_variable("rawdata", rawdata)
        # self.link(path, self.get_physics_position(site), site)
        self.set_update_time(site)

    def link(self, source, destination, site):
        chern_config_path = os.environ["HOME"] + "/.Chern"
        site_module = imp.load_source("site", chern_config_path+"/"+site+".py")
        site_module.link(source, destination)

    def new_version(self, site):
        """
        Create a new version of the data.
        And the new version will replace the old one.
        The old one can be found through git.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        versions = config_file.read_variable("versions")
        if versions is None:
            versions = {}
        versions[site] = uuid.uuid4().hex
        config_file.write_variable("versions", versions)
        os.mkdir(self.get_physics_position(site))

    def status(self, site):
        """
        Read the run status
        """
        pass

    def latest_version(self, site):
        """
        Get the latest version.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        versions = config_file.read_variable("versions")
        return versions[site]

    def set_update_time(self, site):
        """
        Setup the time.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        update_times = config_file.read_variable("update_times")
        if update_times is None:
            update_times = {}
        update_times[site] = time.time()
        config_file.write_variable("update_times", update_times)

    def get_update_time(self, site):
        """
        Read the update time of a site.
        """
        config_file = utils.ConfigFile(self.path+"/.chern/config.py")
        update_times = config_file.read_variable("update_times")
        if update_times is None:
            return 0
        return update_times.get(site, 0)

    def get_physics_position(self, site):
        """
        Read the physics position of a site of a data.
        """
        chern_config_path = os.environ.get("HOME") + "/.Chern"
        config_file = utils.ConfigFile(chern_config_path +"/config.py")
        sites = config_file.read_variable("sites")
        return sites[site] +"/data/"+ self.latest_version(site)


def create_data(path, inloop=False):
    """
    Make a new data and its update time should be 0.
    """
    path = utils.strip_path_string(path)
    os.mkdir(path)
    os.mkdir(path+"/.chern")
    with open(path + "/.chern/config.py", "w") as config_file:
        config_file.write("object_type = \"data\"")
    with open(path + "/README.md", "w") as readme_file:
        readme_file.write("Please write a specific README!")
    if not inloop:
        subprocess.call("vim %s/README.md"%path, shell=True)

