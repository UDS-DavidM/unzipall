"""
This program will unzip all archives in a given directory, including subdirectories.
It will immediately clean up after itself, thereby allowing extracing huge archive collections without
occupying too much disk space during the procedure.
"""

import ufuncts
import patoolib as ptl
import os
import sys
from collections import Counter, deque
import send2trash

ver = "v3"
vdate = "2025.11.03"

root = r""
verbose = True
delete = True
dry = False
trash = True
recursive = True
force = False

supported_formats = {"zip","7z","rar","zpaq","zipx","xz",
                     "tar", "gz", "bz2"}

def unzip_all(root=root, dry=dry, delete=delete, trash=trash, recursive=recursive):
    global fileslist, typecount, totalnum, success, error, deletion_error
    remove = send2trash.send2trash if trash else os.unlink
    fileslist = [x for x in ufuncts.subfileslist(root) if ufuncts.extension(x) in supported_formats]
    typecount = Counter([ufuncts.extension(x) for x in fileslist])
    totalnum = len(fileslist)

    print(f"Detected {totalnum} archive files.")

    if not totalnum: print("\nNothing to be done."); return

    q = deque(fileslist)
    discovered = 0
    processed = 0
    success = 0
    error = 0
    deletion_error = 0
    while q:
        file = q.popleft()
        processed += 1
        print(f"({processed}/{totalnum+discovered}) Unpacking {file}... ", end="")
        try:
            outdir = file.removesuffix(ufuncts.extension(file, dot=True)).strip()
            if os.path.isdir(outdir) and not force:
                print(f"\nDirectory '{outdir}' already exists - skipping.")
                continue
            if not dry:
                os.makedirs(outdir, exist_ok=True)
                ptl.extract_archive(file, verbosity=-1, outdir=outdir, interactive=False)
                if not os.path.isdir(outdir):
                    raise OSError(f"\nFailed to create output directory '{outdir}'.")
            success += 1
            
            #cleanup original archive
            if delete and not dry:
                try:
                    remove(file)
                except Exception as _e:
                    print(f"\nDeletion Error ({file}): {_e}", file=sys.stderr)
                    deletion_error += 1
                    
            #recursively discover nested archives
            if recursive and os.path.isdir(outdir):
                try:
                    inner = [p for p in ufuncts.subfileslist(outdir) if ufuncts.extension(p) in supported_formats]
                    if inner:
                        q.extend(inner)
                        discovered += len(inner)
                except Exception as _scan_e:
                    print(f"\nWarning: Could not scan '{outdir}' for nested archives: {_scan_e}", file=sys.stderr)
                    
        except Exception as e:
            print(f"\n{file}: {e}", file=sys.stderr)
            error += 1
            continue
        
        print("OK")
            
    if success:
        print(f"\n{success} files successfully unpacked.")
        
    if error:
        print(f"\n{error} files failed to unpack.", file=sys.stderr)
        
    if deletion_error:
        print(f"\n{deletion_error} files could not be deleted.", file=sys.stderr)
        
    if recursive and discovered:
        print(f"\nDiscovered and processed {discovered} nested archive(s).")
        
    print("\nOK")
