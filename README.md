# Computer-Forensics-File-Tampering-Detection
The tool stores the md5 hash for all the files in the targeted directory and checks for tampering or modification of the files.


Status: Under Development
##Functionality Achieved:
### Hash Dump Generation.
- Itereate through input directory recursively.
- Generate MD5 hash of all the files in that directory.
- Store all the hash and file name dictionary in user defined file.
### Hash Dump Verification
- Iterate through input directory recursively.
- Take values from the user defined hashdump file.
- verify the hash for all the files and print if tampered.
