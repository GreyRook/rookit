# -*- coding=utf-8 -*-
import sys
import subprocess as sp
import shutil
from .files import get_files, task_for_files


def compile(folder):
    assert isinstance(folder, list)
    cmd = ['jsx',]
    cmd += folder

    proc = sp.Popen(
        cmd,
        stdout=sp.PIPE)
    if proc.wait() != 0:
        print('jsx FAILED for {}'.format(folder))
        sys.exit(1)


def compile_jsx_task(src_path, dist_path,
                folder_blacklist=None, file_blacklist=None,
                task_dep=None, ext=None):
    if not ext:
        ext = ['.js']
    file_dep = get_files(src_path, ext=ext,
                         folder_blacklist=folder_blacklist,
                         file_blacklist=file_blacklist)
    targets = get_files(dist_path, ext=['.js'])
    _task = {
        'actions': [
            (compile, [src_path]),
        ],
        'file_dep': file_dep,
        'targets': targets,
    }
    if task_dep:
        _task['task_dep'] = task_dep
    return _task
