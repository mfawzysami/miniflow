from .tasks import *
import os


class Project(object):
    def __init__(self, name="myproject", base_dir="",data_dir="", **kwargs):
        self.name = name
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.args = kwargs
        self.vars = {}
        self.tasks = {}
        self.counter = 1
        self.prepared = False

    def prepare(self):
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        tmp_dir = os.path.join(self.base_dir, "tmp")
        logs_dir = os.path.join(tmp_dir, "logs")
        tasks_dir = os.path.join(tmp_dir, "tasks")
        if not os.path.exists(os.path.join(self.base_dir, "tmp")):
            os.mkdir(tmp_dir)
            os.mkdir(logs_dir)
            os.mkdir(tasks_dir)
        self.vars["base_dir"] = self.base_dir
        self.vars["data_dir"] = self.data_dir
        self.vars["tmp_dir"] = tmp_dir
        self.vars["logs_dir"] = logs_dir
        self.vars["tasks_dir"] = tasks_dir

    def then(self, task):
        if not self.prepared:
            self.prepare()
            self.prepared = True

        next_task = task
        if not task:
            raise Exception("Task should be an instance of a task")
        next_task.project = self
        self.tasks[self.counter] = next_task
        self.counter += 1
        return self

    def run(self):
        print("Starting MiniFlow Pipeline")
        for index in range(1,len(self.tasks.items())+1):
           executing_task = self.tasks[index]
           executing_task.run()
        print ("Finished Pipeline")

