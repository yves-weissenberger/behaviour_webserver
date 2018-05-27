import time

if __name__ == "__main__":
	st = time.time()
	while True:

		if (time.time() - st)>5:
			print (time.time() - st)
			st = time.time()