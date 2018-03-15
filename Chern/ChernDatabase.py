"""
"""
import os
import Chern.utils as utils
from Chern.VJob import VJob
from Chern.VVolume import VVolume
from Chern.VContainer import VContainer
from Chern.VImage import VImage

class ChernDatabase(object):
    ins = None
    def __init__(self):
        self.global_config_path = utils.local_config_path()

    @classmethod
    def instance(cls):
        if cls.ins is None:
            cls.ins = ChernDatabase()
        return cls.ins

    def job(self, id):
        storage_path = utils.storage_path()
        if os.path.exists(storage_path+"/"+id):
            return VJob(storage_path+"/"+id)
        else:
            return None

    def jobs(self, condition):
        storage_path = utils.storage_path()
        jobs_list_file = utils.ConfigFile(storage_path+"/jobs.py")
        job_id_list = jobs_list_file.read_variable("jobs_list")
        if job_id_list is None:
            job_id_list = []
        job_list = []
        for job_id in job_id_list:
            job = VJob(storage_path + "/" + job_id)
            if job.job_type() == "volume":
                job = VVolume(job.path)
            elif job.job_type() == "container":
                job = VContainer(job.path)
            elif job.job_type() == "image":
                job = VImage(job.path)
            if job.status() == condition:
                job_list.append(job)
        return job_list


    def get_current_project(self):
        """ Get the name of the current working project.
        If there isn't a working project, return None
        """
        global_config_file = utils.ConfigFile(self.global_config_path)
        current_project = global_config_file.read_variable("current_project")
        if current_project is None:
            return None
        else:
            projects_path = global_config_file.read_variable("projects_path")
            path = projects_path.get(current_project, "no_place|")
            if path == "no_place|":
                projects_path[current_project] = "no_place|"
            if not os.path.exists(path):
                projects_path.pop(current_project)
                if projects_path != {}:
                    current_project = list(projects_path.keys())[0]
                else:
                    current_project = None
                global_config_file.write_variable("current_project", current_project)
                global_config_file.write_variable("projects_path", projects_path)
                return self.get_current_project()
            else:
                return current_project


    def project_path(self):
        """ Get The path of a specific project.
        You must be sure that the project exists.
        This function don't check it.
        """
        project_name = self.get_current_project()
        global_config_file = utils.ConfigFile(self.global_config_path)
        projects_path = global_config_file.read_variable("projects_path")
        return projects_path[project_name]



