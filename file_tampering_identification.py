import glob, os
import hashlib
import json

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
		print filenameShort
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


		

rootPath = raw_input("Enter the directory path: ")
if rootPath[-1] != "/":
	rootPath += "/"
filePaths = filepathScan(rootPath)
print rootPath
hashdata = hashGenerator(filePaths,rootPath)
with open('hashdump.json', 'w') as fp:
    json.dump(hashdata, fp)
