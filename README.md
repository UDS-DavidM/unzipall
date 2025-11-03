This program will unzip all archives in a given directory, including subdirectories.
It will immediately clean up after itself, thereby allowing extracing huge archive collections without
occupying too much disk space during the procedure. 

Supports most common archive types (7z, Zip, Rar, Zpaq, Tar, Gz, Bz2, Xz, Zipx). Has the ability to extract nested archives recursively.

Requirements:\
patoolib (```pip install patool```)\
send2trash (```pip install send2trash```)\
ufuncts (included)

Usage:\
This program is intended to be used within an interactive Python interpreter environment. Call the function "unzip_all" on the target directory with optional arguments.
