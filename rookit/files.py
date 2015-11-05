# -*- coding=utf-8 -*-
import sys
import os
import shutil

def get_files(src_path, ext=None, folder_blacklist=None, file_blacklist=None):
    """
    get list of all files in folder (including subfolder)

    returns file path relative to the src-folder
    """
    if isinstance(ext, basestring):
        ext = [ext]
    files = []
    for dirpath, dirnames, filenames in os.walk(src_path):
        if folder_blacklist and \
                any([bl in dirpath+os.path.sep for bl in folder_blacklist]):
            continue

        for filename in filenames:
            if ext and all([not filename.endswith(e) for e in ext]):
                continue

            if file_blacklist and \
                    any([bl in filename for bl in file_blacklist]):
                continue

            files.append(
                os.path.relpath(
                    os.path.join(dirpath, filename),
                    src_path
                )
            )
    return files


def abs_path(path, filename):
    """
    get absolute path
    """
    assert not filename.startswith(os.path.sep)
    out = os.path.join(path, filename)
    return out


def create_dist_path(out_file):
    out_dir = os.path.dirname(out_file)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)


def copy_file_task(src_path, dist_path, filename, task_dep=None):
    """
    generate task to copy single file "filename" from src_path to dist_path
    """
    out_file = abs_path(dist_path, filename)
    in_file = abs_path(src_path, filename)

    create_dist_path(out_file)

    task = {
        'name': '{} --> {}'.format(in_file, out_file),
        'actions': [(shutil.copy, [in_file, out_file])],
        'targets': [out_file],
        'file_dep': [in_file],
    }
    if task_dep:
        task['task_dep'] = task_dep
    return task


def copy_files_task(src_path, dist_path, ext=None,
                    folder_blacklist=None, file_blacklist=None,
                    task_dep=None):
    """
    copy all files from src_path to dist_path. Includes subfolders.
    """
    files = get_files(src_path, ext=ext, folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)
    for filename in files:
        # TODO: mengle with copy_file_task
        task = copy_file_task(src_path, dist_path, filename, task_dep=task_dep)
        yield task



def task_for_files(task, src_path, dist_path, files, task_dep=None):
    """
    execute a task for all files
    """
    for filename in files:
        out_file = abs_path(dist_path, filename)
        in_file = abs_path(src_path, filename)

        create_dist_path(out_file)

        _task = {
            'name': in_file + ' --> ' + out_file,
            'actions': [(task, [in_file, out_file])],
            'targets': [out_file],
            'file_dep': [in_file],
        }
        if task_dep:
            _task['task_dep'] = task_dep
        yield _task
