import os
import time
st = time.time()
while 1:

	if (time.time() - st)>5:
		st = time.time()
		print(time.time()-st)
