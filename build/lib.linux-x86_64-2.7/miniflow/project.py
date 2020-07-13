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
        # tmp_dir = os.path.join(self.base_dir, "tmp")
        logs_dir = os.path.join(self.base_dir, "logs")
        # tasks_dir = os.path.join(tmp_dir, "tasks")
        if not os.path.exists(os.path.join(self.base_dir, "logs")):
            os.mkdir(logs_dir)
        self.vars["base_dir"] = self.base_dir
        self.vars["data_dir"] = self.data_dir
        self.vars["tmp_dir"] = self.base_dir
        self.vars["logs_dir"] = logs_dir
        self.vars["tasks_dir"] = self.base_dir

    def then(self, task):
        if not self.prepared:
            self.prepare()
            self.prepared = True

        next_task = task
        if not task:
            raise Exception("Task should be an instance of a task")
        next_task.project = self
        self.tasks[self.counter] = ("task",next_task)
        self.counter += 1
        return self

    def then_in_future(self,procedure):
        if not procedure:
            raise Exception("You have to supply a callable python function")
        if not self.prepared:
            self.prepare()
            self.prepared = True

        self.tasks[self.counter] = ("future",procedure)
        self.counter += 1
        return self



    def run(self):
        print("Starting MiniFlow Pipeline")
        previous_task = None
        for index in range(1,len(self.tasks.items())+1):
           type , executing_task = self.tasks[index]
           if type =='task':
               if previous_task:
                   executing_task.project.vars['previous_dir'] = previous_task.self_dir
               executing_task.run()
               previous_task = executing_task
           else:
               future_task = executing_task(self)
               if future_task and isinstance(future_task,Task):
                   if previous_task:
                       future_task.project.vars['previous_dir'] = previous_task.self_dir
                   future_task.run()
                   previous_task = future_task

        print ("Finished Pipeline")

