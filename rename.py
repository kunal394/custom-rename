#!/usr/bin/env python

import os, sys


def main():
    #flags to introduce: -r:for recursive renaming,
    #-v: for verbose renaming
    #-c: for confirmation before renaming
    #-s: for suggestion before renaming
    #-d: to provide a different delimiter
    #-reg: to provide a regex for renaming
    if len(sys.argv) < 2:
        res = raw_input("Are you sure you want to rename everything in current directory? y/n")
        if(not res.lower().startswith('y')):
            print("Exiting without any changes..")
            sys.exit(1)
    print("Renaming files...")
    delim = '-'
    wd = os.getcwd() # get working directory
    file_list = os.listdir('.') # get the list of files and directories in the cwd
    for i in file_list:
        if os.path.isfile(wd+'/'+i):
            try:
                os.rename(i, ''.join(i.split(delim)[1:]).strip())
            except:
                print("Skipping file: " + i)

if __name__ == '__main__':
    main()
