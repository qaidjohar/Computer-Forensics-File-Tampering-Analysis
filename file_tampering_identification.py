#!/usr/bin/env python

import glob, os
import hashlib
import json
import argparse
import sys

def parse_args():
	#Create the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate", help="Generates the hashdump file for the selected directory.",action="store_true")
    parser.add_argument("-c", "--check", help="Checks for file tampering using the hashdump file.",action="store_true")
    parser.add_argument("-d", "--dump", help="Path to the hashdump file. Example: -d /root/username/xyz/hashdump.json")
    parser.add_argument("-p", "--path", help="Directory path for generation/checking. Example: -p /root/username/xyz/impDir/")
    return parser#.parse_args()
    


def md5(fname):
	"""
	Cacualte the MD5 hash of the file given as input.
	Returns the hash value of the input file.
	"""
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


def hashGenerator(filePaths,rootPath):
	"""
	Iterating files in filePaths list variable 
	and calling md5 function to calculate hash.
	Then storing it in a dictionary named data 
	and returning it.
	"""
	data = {}
	for filename in filePaths:
		hashdump = md5(filename)
		filenameShort = filename.replace(rootPath,"")
		#print filenameShort
		data[filenameShort] = hashdump	
	return data

def filepathScan(directory):
    """
    This will scan through the directory specified recursively 
    and store the paths of each file in list and return the list.
    """
    filePaths = []  # List which will store all of the full filepaths.
    # walk the directory tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Getting complete file path by join. 
            path = os.path.join(root, filename)
            filePaths.append(path)  # Add it to the list.
    return filePaths  #returning the list with path of all files


def generate(dumpfile,path):
	if path[-1] != "/":
		path += "/"
	filePaths = filepathScan(path)
	#print rootPath
	hashdata = hashGenerator(filePaths,path)
	with open(dumpfile, 'w') as fp:
	    json.dump(hashdata, fp)

def check(dumpfile,path):
	if path[-1] != "/":
		path += "/"
	filePaths = filepathScan(path)
	#print rootPath
	hashdata = hashGenerator(filePaths,path)
	with open(dumpfile, 'r') as fp:
		verificationData = json.load(fp)
	for key in hashdata:
		if key in verificationData:
			if hashdata[key] != verificationData[key]:
				print str(key) + " is tampered."
		else:
			print str(key) + " hashdump data not available."
			
	for key in verificationData:
		if not key in hashdata:
			print str(key) + " is deleted/unavailable."



########################################
######### Start of Program #############
########################################

if __name__ == "__main__":
	parse = parse_args()
	args = parse.parse_args()
	if args.dump and args.path:
		if os.path.isdir(args.dump):
			print "Invalid Input. dump should be a file, not a directory."
			sys.exit(1)
		if not os.path.isdir(args.path):
			print "Invalid Input. path should be a directory, not a file."
			sys.exit(1)
		
		if args.generate:
			generate(args.dump, args.path)
		elif args.check:
			check(args.dump, args.path)
		else:
			print "Invalid Command Line Arguments. \n"
			parse.print_help()
			sys.exit(1)
	else:
		print "Invalid Command Line Arguments. \n" 
		parse.print_help()
		sys.exit(1)
