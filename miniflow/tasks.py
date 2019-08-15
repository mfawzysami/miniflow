
from executor import execute
from jinja2 import Template
from .email import send_email


def check_error(e):
    try:
        return e.message
    except Exception as r:
        return str(e)





class Task(object):

    def __init__(self, name, command, *positional, **kwargs):
        self.name = name
        self.command = command
        self.positional = positional
        self.args = kwargs
        self.project = None


    def __preprocess_param__(self,param):
       try:
           if not param or not self.project:
               return param
           t = Template(param)
           return t.render(**self.project.vars)
       except Exception as e:

           return param


    def prepare(self):
        import os
        if self.project and not os.path.exists(os.path.join(self.project.base_dir,"tmp/tasks/{0}".format(self.name))):
            task_dir = os.path.join(self.project.base_dir,"tmp/tasks/{0}".format(self.name))
            self.self_dir = task_dir
            os.mkdir(task_dir)
            if self.project:
                self.project.vars["{0}_dir".format(self.name)] = task_dir

    def __get_params__(self):
        if len(self.args.items()) > 0:
            params = ["--{0}={1}".format(k, self.__preprocess_param__(v)) for k, v in self.args.items() if "mail_" not in k]
            return " ".join(params)
        else:
            return ""

    def logit(self,output):
        import os
        try:
            if self.project and os.path.exists(os.path.join(self.project.base_dir,"tmp/logs")):
                with open(os.path.join(self.project.base_dir,"tmp/logs/{0}_logs.txt".format(self.name)),mode='w+') as writer:
                    writer.write(output)

        except Exception as e:
            print(check_error(e))

    def run(self):
        try:
            self.prepare()
            tool_command = self.command
            if not tool_command:
                raise Exception("Can't rfrun the current task {0} , no command specified".format(self.name))

            tool_command = self.__preprocess_param__(tool_command)

            if len(self.positional) > 0:
                preprocessed_positionals = [self.__preprocess_param__(param) for param in self.positional]
                tool_command += " " + " ".join(preprocessed_positionals)

            full_command = "{0} {1}".format(tool_command,self.__get_params__())

            # now execute the current task
            print("Executing : {0}".format(full_command))
            logs = execute(full_command,capture=True)
            self.logit(logs)
            if self.args.get('notify',False):
                self.notify(self.args.get('mail_receiver', None), self.args.get('mail_message', None))

            return self

        except Exception as e:
            msg = check_error(e)
            print(msg)
            self.logit(msg)

    def then(self, task):
        next_task = self
        try:
            # run the current task before branching to another task
            self.run()
            # then try the next task
            if task and isinstance(task, Task):
                next_task = task
            else:
                raise Exception("Next Task should be an instance of a task")

            next_task.project = self.project
            return next_task

        except Exception as e:
            print(check_error(e))



    def notify(self, email=None, message=None):
        try:
            if self.project:
                send_email(self.project.args,mail_message=message)
        except Exception as e:
            msg = check_error(e)
            print (msg)
