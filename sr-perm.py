#!/usr/bin/python
#Solution: Store the key-values "file:mode" or "dir:mode" for every files(include files, subdir, files in subdir) in one two-dimensional array(one python dictionary object). We will treat dir and file as one thing. And finally the program will store this array in one file sr-perm. When recover the permissions, the program will read the permissions from the store file.
import sys
import os
import string
import pickle

#the dictionary to store the permissions
dic_files_perm = {}

#-------------------------Functions Begin----------------------------------------------------------------------------------
#function modify_perm: modify the permission for the permission changed files
def modify_perm(dic_perm):
    for (path, mode) in dic_perm.items():
	os.chmod(path, mode)
    return

#function get_perm_changed_files: get the permission changed(compared to the saved permissions) files 
def get_perm_changed_files(current, saved):
    changed_files_perm = {}
    for (k, v) in current.items():
	if saved.has_key(k) and saved[k] != current[k]:
	    changed_files_perm[k] = saved[k]
    return changed_files_perm
        
#function get_files_perm: get the permissions for all files(include files, subdir, files in subdir) below the given path
def get_files_perm(path):  
    #list the files in the path
    file_list = os.listdir(path)  
    #one file in one loop
    for file in file_list:
	current_file = path + '/' + file
        dic_files_perm[current_file] = os.stat(current_file).st_mode
        if os.path.isdir(current_file):  
	    #recursion
            get_files_perm(current_file)  
    return

#------------------------------------Functions End----------------------------------

if len(sys.argv) < 3 or (not os.path.isdir(os.path.abspath(sys.argv[1]))) or (sys.argv[2] != "-s" and sys.argv[2] != "-r"):
    print "Usage: sr-perm.py path -s/-r"
    print "       -s: save permissions"
    print "       -r: recover permissions"
    sys.exit()

p_path = os.path.abspath(sys.argv[1])
p_operation = sys.argv[2]
saved = os.path.dirname(sys.argv[0]) + "/s-perm"

#get permissions to the dictionary: dic_files_perm
get_files_perm(p_path)

if p_operation == "-s":
    if not os.path.isfile(saved):
        os.system("touch " + saved)
    file = open(saved, 'w')
    pickle.dump(dic_files_perm, file)
else:
    if not os.path.isfile(saved):
        print saved + " is not existed, please save the permissions first!"
        sys.exit()
    file = open(saved, 'r')
    modify_perm( get_perm_changed_files(dic_files_perm, pickle.load(file)) )


file.close()

