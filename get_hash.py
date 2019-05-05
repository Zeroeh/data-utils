#!/usr/bin/env python3

import hashlib
import os
import threading
import time

BLOCK_SIZE = 65536
results = []
finishes = 0
files = 0
last_result = 0
VERBOSE = True

def main():
	global files, finishes, last_result
	print("Grabbing file list...")
	list = grabList()
	files = len(list)
	print("Found {} files".format(files))
	print("Beginning hash calculations...")
	for fx in list:
		threading.Thread(target=getHash, kwargs=dict(f=fx)).start()
		#getHash(fx) #single thread
	while checkFinished() == False:
		time.sleep(60) #todo: maybe calculate based on file sizes?
		if finishes != last_result: #new adds within the last sleep
			print("Currently finished {} of {} files".format(finishes, files))
	print("Finished!")

def checkFinished():
	global finishes, files, last_result
	if finishes == files:
		saveOutput()
		return True
	else:
		if finishes == last_result:
			return False #dont update
		last_result = finishes
		return False

def getHash(f):
	global results, finishes, files
	hash_func = hashlib.sha1()
	try:
		with open("../"+f, "rb") as afile:
			buf = afile.read(BLOCK_SIZE)
			while len(buf) > 0:
				hash_func.update(buf)
				buf = afile.read(BLOCK_SIZE)
			if VERBOSE == True:
				print("{}:{}".format(hash_func.hexdigest(), f))
			fmt = "{}:{}".format(hash_func.hexdigest(), f)
			results.append(fmt)
			finishes += 1
	except IsADirectoryError as e:
		files -= 1

def grabList():
	path = "../."
	dir = os.listdir(path)
	if VERBOSE == True:
		for fd in dir:
			print(fd)
	return dir

def saveOutput():
	global results
	outFileName = "list.hash"
	new_new = open(outFileName, "w")
	for x in results:
		new_new.write(x+"\n")
	new_new.close()

if __name__ == "__main__":
	main()
