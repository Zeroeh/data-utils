#!/usr/bin/env python3

import threading
import os
import sys
import subprocess
import time
import signal
import string

VERBOSE = False
files = 0
results = []
finishes = 0
last_result = 0
target = ""
globalfd = None

def main():
	global target, files, globalfd
	target = sys.argv[1]
	list = grabList()
	files = len(list)
	globalfd = open("results.search", "w")
	signal.signal(signal.SIGINT, sigHandler)
	for fd in list:
		threading.Thread(target=searchFile, kwargs=dict(f=fd)).start()
	while checkFinished() == False:
		time.sleep(60)
		if finishes != last_result:
			print("Currently finished {} of {} searches".format(finishes, files))
	print("Finished!")

def searchFile(f):
	global results, finishes, files, target, globalfd
	try:
		fd = open("../"+f, "rb")
		fd.close()
		batch = "\n{}\n".format(f)
		tstr = "-a \"{}\" ".format(target)
		fstr = "{}".format(os.getcwd()+"/../"+f)
		finalstr = "zgrep "+tstr+fstr
		p = subprocess.run([finalstr], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
		batch += str(p.stdout)
		globalfd.write(batch)
		globalfd.flush()
		finishes += 1
		results.append(batch)
		if VERBOSE == True:
			print(batch)
	except IsADirectoryError as e:
		files -= 1
	except UnicodeDecodeError as e:
		print("Bad decode result (alternate language encoding): {} | {}".format(f, e))

def checkFinished():
	global finishes, files, last_result
	if finishes == files:
		return True
	else:
		if finishes == last_result:
			return False
		last_result = finishes
		return False

def grabList():
	path = "../."
	dir = os.listdir(path)
	return dir

def sigHandler(signum, frame):
	sys.exit(0)

if __name__ == "__main__":
	main()
