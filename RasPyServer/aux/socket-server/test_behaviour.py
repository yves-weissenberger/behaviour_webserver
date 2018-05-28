import os
import time
st = time.time()

with open("/home/pi/task_time.txt",'w') as f:
    f.write(st)
