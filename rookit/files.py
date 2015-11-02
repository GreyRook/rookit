# -*- coding=utf-8 -*-
import sys
import os
import shutil

def get_files(path, ext=None, folder_blacklist=None, file_blacklist=None):
    """
    get list of all files in folder (including sub)
    """
    if isinstance(ext, basestring):
        ext = [ext]
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        if folder_blacklist and \
                any([bl in dirpath+os.path.sep for bl in folder_blacklist]):
            continue

        for filename in filenames:
            if ext and all([not filename.endswith(e) for e in ext]):
                continue

            if file_blacklist and \
                    any([bl in filename for bl in file_blacklist]):
                continue

            files.append(os.path.join(dirpath, filename))
    return files
    
    
def get_dist_path(src_path, dist_path, filename):
    if filename.startswith(src_path):
        filename = filename[len(src_path):]
        while (filename.startswith(os.path.sep)):
            filename = filename[1:]
    out = os.path.join(dist_path, filename)
    if not os.path.isdir(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))
    return out

    
def copy_files_task(src_path, dist_path, ext=None,
                    folder_blacklist=None, file_blacklist=None,
                    task_dep=None):
    files = get_files(src_path, ext=ext, folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)
    for filename in files:
        out = get_dist_path(src_path, dist_path, filename)
        task = {
            'name': filename + ' --> ' + out,
            'actions': [(shutil.copy, [filename, out])],
            'targets': [out],
            'file_dep': [filename],
        }
        if task_dep:
            task['task_dep'] = task_dep
        yield task
