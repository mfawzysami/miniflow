from miniflow import *


p = Project(base_dir="/home/snouto/bioinf/miniflow",data_dir="/home/snouto/bioinf/data")
p.then(Task("echo","echo 'Hello World'",notify=True,mail_message="Echo Job has finished."))

p.run()