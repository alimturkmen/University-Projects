#!/usr/bin/python
import os, pwd, sys, hashlib, subprocess, re, argparse
pattern = "" #the pattern it will search
dirlist = [] #the list of the directories that it will look
parser = argparse.ArgumentParser()
parser.add_argument('-c', nargs=1)
parser.add_argument('-p', action='store_true')
parser.add_argument('-f', action='store_true')
parser.add_argument('-d', action='store_true')
parser.add_argument('pandd', nargs=argparse.REMAINDER)
args=parser.parse_args()
pandd = args.pandd #pattern and directory list
d = args.d 
f = args.f
p = args.p
c = args.c 

################################################################
	#this part designs the pattern and directory list

#seperates pattern and directory list
if pandd and ("\"" in pandd[0] or "\'" in pandd[0]):
	pattern += pandd[0] #first argument is pattern
	dirlist = pandd[1:] #rest is directory list
	pattern = pattern[1:-1] #gets rid of " " and '' signs
else:
	pattern += ".*" #if there is no given pattern looks all 
	dirlist = pandd

#if the given directory is not fullpath then adds the current working directory to the front
for dir in dirlist:
	if not os.path.isdir(dir):
		dir += os.getcwd() + "/" + dir

#if there is no given directory, looks the current working directory
if not dirlist:
	dirlist.append(os.getcwd())

################################################################
	#this part fills filelist and dirstack

#list of all files in the given directories
filelist = [] 
#stack of the directories in the given directories
dirstack = []

while dirlist:
	fullpathname = dirlist.pop() #the directory at the top of the list
	dirstack.append(fullpathname) 
	curlist = os.listdir(fullpathname) #list of the contents of the directory
	
	for fdname in curlist: #elements in the directory
 		newpath = fullpathname + "/" + fdname #fullpath of the element
 		if os.path.isdir(newpath):
 			dirlist.append(newpath)
 		else:	
 			filelist.append(newpath)

################################################################

#returns the SHA-256 hash of the file passed into it
def hash_file(filename):
   
   # makes a hash object
   h = hashlib.sha256()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

################################################################
	#this part finds the duplicate directories
if d:
	#stores directory names as keys and hash of these directories values
	dirs = {}
	#stores hashes of directories as keys and list of the all the directories with that hash as values
	dirmap = {}
	while dirstack:
		tempdir = dirstack.pop() #the directory at the top, in other words in the deepest place
		curlist = os.listdir(tempdir)
		if not curlist:
			h = hashlib.sha256(b'').hexdigest()
			if h in dirmap: #if there is already a directory with the that hash, appends the directory to the list
				dirmap[h].append(tempdir)
				dirs[tempdir] = h
			else: # if there is no directory with that hash, creates a list and puts the directory in to this list
				dirmap[h] = [tempdir]
				dirs[tempdir] = h
		else:
			htotal = '' #the sum of all content's hash
			for fdname in curlist: #elements in the directory
		 		newpath = tempdir + "/" + fdname #fullpath of the element
		 		if os.path.isdir(newpath):
		 			htotal += dirs[newpath]
		 		else:	
		 			htotal += hash_file(newpath)
			h = hashlib.sha256(htotal.encode()).hexdigest()
			if h in dirmap:
				dirmap[h].append(tempdir)
				dirs[tempdir] = h
			else:
				dirmap[h] = [tempdir]
				dirs[tempdir] = h

################################################################
	# this part finds the duplicate files
else:
	filemap = {} # the dictionary that stores hash of files as keys and file lists as values
	for file in filelist:
		h = hash_file(file)
		if h in filemap: #if there is already a file with the that hash, appends the file to the list
			filemap[h].append(file)
		else: # if there is no file with that hash, creates a list and puts the file in to this list
			filemap[h] = [file] 

################################################################
	#this part looks the given arguments and executes them
if d:
	for i in dirmap: # i is for hash values
		if len(dirmap[i])>1:
			dirmap[i].sort()
			if c:
				counter = 0; #counts the number of duplicates that match with pattern
				for k in dirmap[i]:
					if re.search(pattern, os.path.basename(k)):
						counter+=1
				if counter>1: #if there is no multiple duplicates than does nothing
					for j in dirmap[i]: #j is for directories in the list
						if re.search(pattern, os.path.basename(j)):
							cmd = c[0]+' "'+j+'"' #the received command and the duplicate directory
							output = os.system(cmd)
			else:
				ismatched = False #true if pattern is matched, false otherwise
				counter = 0;
				for k in dirmap[i]:
					if re.search(pattern, os.path.basename(k)):
						counter+=1
				if counter>1:
					for j in dirmap[i]:
						if re.search(pattern, os.path.basename(j)):
							print(j, end='   ') #prints 3 spaces between duplicates
							ismatched = True
					if ismatched:
						print("\n")
						ismatched = False
else:
	for i in filemap: # i is for hash values
		if len(filemap[i])>1:
			filemap[i].sort()
			if c:
				counter = 0;
				for k in filemap[i]:
					if re.search(pattern, os.path.basename(k)):
						counter+=1
				if counter>1:
					for j in filemap[i]: # j is for files in the list
						if re.search(pattern, os.path.basename(j)):
							cmd = c[0]+' "'+j+'"' #the received command and the duplicate file
							output = os.system(cmd)
			else:
				counter = 0; 
				for k in filemap[i]:
					if re.search(pattern, os.path.basename(k)):
						counter+=1
				if counter>1:
					ismatched = False #true if pattern is matched, false otherwise
					for j in filemap[i]:
						if re.search(pattern, os.path.basename(j)):
							print(j, end='   ') #prints 3 spaces between duplicates
							ismatched = True
					if ismatched:
						print("\n")
						ismatched = False


