#!/usr/bin/env python

import os, sys, signal, argparse, re
delim = '-'
prefix = False
verbose = False

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)


def main():
    global delim, prefix, verbose
    #flags to introduce: -r:for recursive renaming,
    #-v: for verbose renaming
    #-c: for confirmation before renaming
    #-s: for suggestion before renaming
    #-d: to provide a different delimiter
    #-reg: to provide a regex for renaming

    if verbose:
        print("delim being used: " + delim)
    if len(sys.argv) < 2:
        res = raw_input("Are you sure you want to rename everything in current directory? y/n")
        if(not res.lower().startswith('y')):
            print("Exiting without any changes..")
            sys.exit(1)
    print("Renaming files...")
    wd = os.getcwd() # get working directory
    file_list = os.listdir(wd) # get the list of files and directories in the cwd
    for i in file_list:
        if i.startswith('.'):
            print("Skipping hidden file: " + i)
        elif os.path.isfile(wd+'/'+i):
            try:
                if preview:
                    print(i + " -> " + ''.join(i.split(delim)[1:]).strip()) 
                elif prefix:
                    #keep everything before the first occurence of delim
                    os.rename(i, i.split(delim)[0].strip())
                else:
                    #default behaviour
                    #keep everything after the first occurence of delim
                    os.rename(i, ''.join(i.split(delim)[1:]).strip())
            except:
                print("Skipping file: " + i)

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    #argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help = "increase output verbosity to level 1", action = "store_true")
    parser.add_argument("-p", "--prefix", help = "keep prefix instead of suffix", action = "store_true")
    parser.add_argument("-d", "--delim", help = "set the delimiter for split filenames")
    parser.add_argument("-p", "--preview", help = "preview the effect without applying them", action = "store_true")
    args = parser.parse_args()
    verbose = bool(args.verbose)
    preview = bool(args.preview)
    prefix = bool(args.prefix)
    if args.delim:
        delim = str(args.delim)
    else:
        delim = '-'
    #print(args.echo)
    main()
