"""
Iterate over the dropbox directory and store all of the .dbignore patterns into a cache, then print out any file that should be ignored
"""
import argparse
import os
import sys
import platform
from Bio import trie
from Bio import triefind

# Quick check for either linux or OSX
if platform.system() == "Linux":
    prefix = "/home/tabboud"
else:
    prefix = "/Users/tabboud"

DROPBOX_DIR = prefix + '/Dropbox'
IGNORE_FILE = '.dbignore'
cache = trie.trie()

def cache_patterns(ignore_file):
    """ Open and read the patterns in an ignore file
    Args:
        ignore_file: IgnoreFile object
    NOTES:
        see dir.c:add_excludes for reading the file and storing the patterns in
        el
    """
    ignore_path = ignore_file.path
    if not os.path.isfile(ignore_path):
        print "ERROR: %s is not a file" % ignore_path
        return
    with open(ignore_path, 'r') as fp:
        for pattern in fp.readlines():
            pattern = pattern.strip()
            ignore_file.patterns.append(pattern)

def find_all_ignores(db_dir, ignore_files):
    """ Print all files that are ignored in the db_dir
    Args:
        db_dir: Dropbox Directory
        ignore_files: list of IgnoreFile objects
    """
    for root, dirs, files in os.walk(db_dir):
        # look at each ignore_file and then compare the paths
        for ignore_file in ignore_files:
            if ignore_file.path in root:
                print "found it"
                # We found the directory to start ignoring
                # need to compare the pattern to each file in this directory
                print files

# Utility methods
def has_dropbox_prefix(filepath):
    """Check if a filepath has the dropbox prefix
    Returns:
        True if it does, False otherwise
    """
    db_prefix = prefix + "/Dropbox"
    common_prefix = os.path.commonprefix([filepath, db_prefix])
    if common_prefix == db_prefix:
        return True
    else:
        return False

def is_dbignore(filepath):
    basename = os.path.basename(filepath)
    if basename == IGNORE_FILE:
        return True
    else:
        return False


def find_ignores(db_dir):
    """ find all the .dbignore files """
    ignores = []
    for root, dirs, files in os.walk(db_dir):
        if IGNORE_FILE in files:
            print "Ignore file: %s" % os.path.join(root, IGNORE_FILE)
            ignores.append(os.path.join(root, IGNORE_FILE))
    return ignores


def add_to_cache(ignore_files=None):
    """ Add all ignore files and patterns to the cache
    Args:
        ignore_files: List of strings
    """
    if ignore_files is None:
        print "No ignore file recieved"
        return
    for ignore_file in ignore_files:
        with open(ignore_file, 'r') as fp:
            # read in all the patterns
            ignore_patterns = []
            for line in fp.readlines():
                line = line.strip()
                if line == '':
                    continue
                else:
                    ignore_patterns.append(line)
                # Insert into the global trie
                #print "Adding (%s) into trie" % (repr(ignore_patterns))
                cache[ignore_file.encode('utf-8')] = ignore_patterns


def ignore(filepath):
    """ Main ignore function
    Returns:
        True if it should be ignored, False otherwise
    """
# 1. Check if the file is in the Dropbox Directory
    if not has_dropbox_prefix(filepath):
        print "not in db directory"
        return False
    else:
# 2. Check if its a .dbignore file
        if is_dbignore(filepath):
            print "dbignore file"
            return True
        else:
# 3. See if this file matches any of the patterns in the cache
# find the closest dbignore
            print "Not Implemented"
            def match(string, trie):
                """match(string, trie) -> longest key or None
                Find the longest key in the trie that matches the beginning of the
                string.
                """
                longest = None
                for i in range(len(string)):
                    substr = string[:i + 1]
                    if not trie.has_prefix(substr):
                        break
                    if substr in trie:
                        longest = substr
                return longest

            print cache.keys() 
            matches = match(filepath, cache)
            print "--> matches: %s " % repr(matches)

            return True


if __name__ == '__main__':
    print "===>"
    parser = argparse.ArgumentParser(description='Determine if we should ignore a particular file or not')
    #parser.add_argument('--sum', dest='accumulate', action='store_const', help='sum the integers')
    parser.add_argument('input_file', help='File to test against')
    args = parser.parse_args()

    #1. Find all ignore files
    ignore_files = find_ignores(DROPBOX_DIR)

    #2. Add the ignore files to the cache
    add_to_cache(ignore_files)

    if ignore(args.input_file) is True:
        print "True: ignore (%s)" % args.input_file
    else:
        print "False: do NOT ignore (%s)" % args.input_file
    print "<==="

