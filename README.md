# data-utils
Some simple utilities to help with managing large sets of files.
Some things to note:
- These scripts were not created with safety in mind. The scripts essentially run raw os commands. If any target file contains unescaped data it could potentially cause an unintentional code execution.
- The main usage of these scripts when I created them was to run through database dumps and organize data.

# get_hash.py
- This script is useful for hashing all the files in the superdirectory. I mostly use this to quickly verify torrent files, as well as prepare a list of hashes when uploading a torrent. Results are only saved once the script is finished running.
- Usage: ``python3 get_hash.py``

# search.py
- This script invokes zgrep to search through many archives for the specified word. A thread is launched for each file found in the superdirectory. Results are continuously saved to file, so it is safe to kill the script early.
- Usage: ``python3 search.py searchstring``
- Issues: sometimes cannot decode certain foreign language encodings with just utf-8.

# split_zip.py
- This script is used to split 1 large archive file into 2 smaller, roughly equal, archive files. The purpose of this script is to split large archives into smaller ones, which speeds up search.py as a result.
- Usage: ``python3 split_zip.py old.tar.gz newfile.tar.gz 2``
- Issues: doesn't evenly split files right now, due to lack of me not wanting to make the algo for it.
- Notes: be sure your target archive contains at least 2 files lol. If anyone knows a novel way of speeding this up, please let me know.
