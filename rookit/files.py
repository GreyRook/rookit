# -*- coding=utf-8 -*-
import sys
import os
import fnmatch
import shutil


def get_files(src_path, ext=None, folder_blacklist=None, file_blacklist=None):
    """
    get list of all files in folder (including subfolder)

    returns file path relative to the src-folder
    """
    if isinstance(ext, str):
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


def get_files2(src_path, ext=None, folder_blacklist=[], file_blacklist=[]):
    """
    get list of all files in folder (including subfolder)

    returns file path relative to the src-folder
    """
    if isinstance(ext, str):
        ext = [ext]
    files = []

    folder_blacklist_effective = []
    for folder in folder_blacklist:
        folder = folder.strip('/')
        folder_blacklist_effective.append(folder)
        folder_blacklist_effective.append(folder + '/*')

    for dirpath, dirnames, filenames in os.walk(src_path):
        rel_folder = dirpath[len(src_path):]
        rel_folder = rel_folder.strip('/')
        if folder_blacklist and \
                any([fnmatch.fnmatch(rel_folder, bl) for bl in folder_blacklist_effective]):
            continue

        for filename in filenames:
            if ext and all([not filename.endswith(e) for e in ext]):
                continue

            if file_blacklist and \
                    any([fnmatch.fnmatch(filename, bl) for bl in file_blacklist]):
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


def create_dist_path(dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    return dst_dir


def copy(src, dst):
    create_dist_path(dst)
    shutil.copy(src, dst)


def _task_for_file(task, src_path, dist_path, filename, task_dep=None):
    dst = abs_path(dist_path, filename)
    src = abs_path(src_path, filename)

    create_dist_path(dst)

    _task = {
        'name': '{}'.format(filename),
        'basename': '{} --> {}'.format(src_path, dist_path),
        'actions': [(task, [src, dst])],
        'targets': [dst],
        'file_dep': [src],
    }
    if task_dep:
        _task['task_dep'] = task_dep
    yield _task


def _task_for_files(task, src_path, dist_path, files, task_dep=None):
    """
    execute a task for all files
    """
    for filename in files:
        yield _task_for_file(task, src_path, dist_path, filename, task_dep=task_dep)


def copy_file_task(src_path, dist_path, filename, task_dep=None):
    """
    generate task to copy single file "filename" from src_path to dist_path
    """
    yield _task_for_file(copy, src_path, dist_path, filename, task_dep=task_dep)


def copy_files_task(src_path, dist_path, ext=None,
                    folder_blacklist=None, file_blacklist=None,
                    task_dep=None):
    """
    copy all files from src_path to dist_path. Includes subfolders.
    """

    for filename in get_files(src_path, ext=ext,
                              folder_blacklist=folder_blacklist,
                              file_blacklist=file_blacklist):
        yield _task_for_file(copy, src_path, dist_path, filename, task_dep=task_dep)


def copy_files_task2(src_path, dist_path, ext=None,
                    folder_blacklist=None, file_blacklist=None,
                    task_dep=None):
    """
    copy all files from src_path to dist_path. Includes subfolders.
    """

    for filename in get_files2(src_path, ext=ext,
                               folder_blacklist=folder_blacklist,
                               file_blacklist=file_blacklist):
        yield _task_for_file(copy, src_path, dist_path, filename, task_dep=task_dep)
