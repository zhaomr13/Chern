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

