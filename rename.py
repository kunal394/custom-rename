#!/usr/bin/env python

import os, sys, signal, argparse, re
delim = '-'
suffix = False
verbose = False
preview = False
confirm = False
persistent_confirm = False

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

def parse_arguments():
    global delim, suffix, verbose, preview, confirm, persistent_confirm
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help = "Increase output verbosity to level 1", action = "store_true")
    parser.add_argument("-s", "--suffix", help = "Remove suffix instead of prefix", action = "store_true")
    parser.add_argument("-d", "--delim", help = "Set the delimiter for spliting filenames")
    parser.add_argument("-p", "--preview", help = "Preview the effect without applying them", action = "store_true")
    parser.add_argument("-c", "--confirm", help = """Preview and then confirm before renaming. Default behaviour is do not confirm.\
            Overrides every other argument.""", action = "store_true")
    parser.add_argument("--pc", help = "Persistent-Confirm. Confirm before rename of every file", action = "store_true")
    args = parser.parse_args()
    verbose = bool(args.verbose)
    preview = bool(args.preview)
    suffix = bool(args.suffix)
    confirm = bool(args.confirm)
    persistent_confirm = bool(args.pc) 
    preview = preview or verbose
    if args.delim:
        delim = str(args.delim)
    else:
        delim = '-'
    print(args)
    sys.exit(1)

def confirm_change():
    preview = True
    persistent_confirm = False
    rename()
    confirm_message()
    preview = False
    rename()

def confirm_message():
    response = raw_input("Are you sure you want to rename? y/n: ")
    response = response.strip()
    if(response != "yes" and response != "y"):
        print("Exiting without any changes..")
        sys.exit(1)

def preview_change(file_name):
    global delim, suffix, verbose, preview, confirm, persistent_confirm
    if suffix:
        suffix_preview(file_name)
    else:
        prefix_preview(file_name)

def rename_file(file_name):
    global delim, suffix, verbose, preview, confirm, persistent_confirm
    if suffix:
        remove_suffix(file_name)
    else:
        remove_prefix(file_name)

def suffix_preview(file_name):
    print(file_name + " ==> " + file_name.split(delim)[0].strip())

def prefix_preview(file_name):
    print(file_name + " ==> " + ''.join(file_name.split(delim)[1:]).strip()) 

def remove_suffix(file_name):
    #keep everything before the first occurence of delim
    os.rename(file_name, file_name.split(delim)[0].strip())

def remove_prefix(file_name):
    #default behaviour
    #keep everything after the first occurence of delim
    os.rename(file_name, ''.join(file_name.split(delim)[1:]).strip())
    
def rename():
    global delim, suffix, verbose, preview, confirm, persistent_confirm
    wd = os.getcwd() # get working directory
    file_list = os.listdir(wd) # get the list of files and directories in the cwd
    for file_name in file_list:
        if file_name.startswith('.'):
            print("Skipping hidden file: " + file_name)
        elif os.path.isfile(wd + '/' + file_name):
            try:
                if persistent-confirm:
                    preview_change(file_name)
                    confirm_message()
                    rename_file(file_name)
                elif preview:
                    preview_change(file_name)
                else:
                    rename_file(file_name)
            except Exception as e:
                print("Skipping file: " + file_name + ". Error: " + str(e))

def main():
    global delim, suffix, verbose, preview, confirm, persistent_confirm
    #TODO: flags to introduce: 
    #-r:for recursive renaming,
    #-s: for suggestion before renaming
    #-reg: to provide a regex for renaming

    parse_arguments()
    if verbose:
        print("delim being used: " + delim)
    if confirm():
        confirm_change()
    else:
        rename()


    rename()

if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    parse_arguments()
    main()
