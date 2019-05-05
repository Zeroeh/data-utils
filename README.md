# data-utils
Some simple utilities to help with managing large sets of files.

# get_hash.py
- This script is useful for hashing all the files in the superdirectory. I mostly use this to quickly verify torrent files, as well as prepare a list of hashes when uploading a torrent. Results are only saved once the script is finished running.
- Usage: ``python3 get_hash.py``

# search.py
- This script invokes zgrep to search through many archives for the specified word. A thread is launched for each file found in the superdirectory. Results are continuously saved to file, so it is safe to kill the script early.
- Usage: ``python3 search.py searchstring``
- Issues: sometimes cannot decode certain foreign language encodings with just utf-8.
