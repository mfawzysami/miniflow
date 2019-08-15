from .tasks import *
import os


class Project(object):
    def __init__(self, name="myproject", base_dir="",data_dir="", **kwargs):
        self.name = name
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.args = kwargs
        self.vars = {}

    def prepare(self):
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        else:
            raise Exception("Project directory already exists, you can't mix multiple workflows/pipelines together , aborting....")

        if not os.path.exists(os.path.join(self.base_dir, "tmp")):
            tmp_dir = os.path.join(self.base_dir, "tmp")
            logs_dir = os.path.join(tmp_dir, "logs")
            tasks_dir = os.path.join(tmp_dir, "tasks")
            os.mkdir(tmp_dir)
            os.mkdir(logs_dir)
            os.mkdir(tasks_dir)
            self.vars["base_dir"] = self.base_dir
            self.vars["data_dir"] = self.data_dir
            self.vars["tmp_dir"] = tmp_dir
            self.vars["logs_dir"] = logs_dir
            self.vars["tasks_dir"] = tasks_dir

    def then(self, task):
        self.prepare()
        next_task = task
        if not task:
            raise Exception("Task should be an instance of a task")
        next_task.project = self
        return next_task
