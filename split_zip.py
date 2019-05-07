#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import string

VERBOSE = False
files = 0
results = []
target_file = ""
target_size = 0
total_size = 0
new_file = ""

def main():
	global target_file, new_file, total_size
	file_list = {}
	if len(sys.argv) != 4:
		print("Usage: python3 split_zip.py <filename> <strip level>")
		sys.exit(0)
	#note: no error processing in this script. All commands are assumed to be correct!
	#stage 1: unzip the specified file into a tmp directory
	target_file = sys.argv[1]
	new_file = sys.argv[2]
	strip_amt = sys.argv[3] #move to 3
	cwd = os.getcwd()
	# tar -xzf {absolute}/../{target} -C {absolute}/tmp
	unzipcmd = "tar -xzf {}/../{} -C {}/tmp --strip-components {}".format(cwd, target_file, cwd, strip_amt)
	p = subprocess.run([unzipcmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
	#stage 2: get the sizes of the files and _attempt_ to split the contents into 2 even sizes portions
	flist = os.listdir(cwd+"/tmp")
	counter = 0
	for fl in flist:
		extension = fl[fl.rfind("."):]
		fpath = "/tmp/{}".format(fl)
		fpath2 = "/tmp/{}{}".format(counter, extension)
		results = os.stat(cwd+fpath)
		total_size += results.st_size
		os.rename(cwd+fpath, cwd+fpath2)
		counter += 1
	if VERBOSE == True:
		print("Total size of contents: {}".format(total_size))
	flist = os.listdir(cwd+"/tmp")
	for fl in flist:
		fpath = "/tmp/{}".format(fl)
		results = os.stat(cwd+fpath)
		file_list[fl] = results.st_size
	smallest_size = 0
	largest_size = 0
	for fl in file_list:
		size = file_list[fl]
		#fill in defaults
		if smallest_size == 0:
			smallest_size = size
		if largest_size == 0:
			largest_size = size
		#start here for consecutive runs
		if smallest_size > size:
			smallest_size = size
		if largest_size < size:
			largest_size = size
	collection1 = []
	collection2 = []
	shift = False
	for fl in file_list:
		if shift == False:
			collection1.append(fl)
			shift = True
		elif shift == True:
			collection2.append(fl)
			shift = False
	#stage 3: zip the collections into 2 seperate archives
	zlist = ""
	for x in collection1:
		zlist += " ./tmp/"+x
	#return these files to the "original" archive
	zip1cmd = "GZIP=-9 tar cvf {} {} --gzip".format(target_file, zlist)
	p2 = subprocess.run([zip1cmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
	#now remove the files
	rmcmd = "rm {}".format(zlist)
	p3 = subprocess.run([rmcmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
	#zip whatever is left in the tmp folder as the new zip file
	zip2cmd = "GZIP=-9 tar cvf {} {} --gzip".format(new_file, "./tmp")
	p4 = subprocess.run([zip2cmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
	#clean the tmp folder of any junk
	cleancmd = "rm ./tmp/*"
	p5 = subprocess.run([cleancmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
	#move the new archives to the archive folder
	mv1cmd = "mv {} {}".format(cwd+"/"+target_file, cwd+"/../"+target_file)
	mv2cmd = "mv {} {}".format(cwd+"/"+new_file, cwd+"/../"+new_file)
	#perform the new file move first
	p6 = subprocess.run([mv2cmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")
	p7 = subprocess.run([mv1cmd], stdout=subprocess.PIPE, shell=True, encoding="utf-8")

def insert(src, ins, pos):
	return src[:pos]+ins+src[pos:]

if __name__ == "__main__":
	main()

