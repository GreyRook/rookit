# -*- coding=utf-8 -*-
import os
import compileall
from .files import get_files, abs_path


def compile(path):
    """
    compile .py to pyc
    """
    compileall.compile_dir(path, maxlevels=100, quiet=True)


def compile_python_task(src, ext=None,
                        folder_blacklist=None, file_blacklist=None,
                        task_dep=None):
    """
    compile all python folder in given folder task
    """

    if not ext:
        ext = ['.py']
    file_dep = get_files(src, ext=ext, folder_blacklist=folder_blacklist,
                         file_blacklist=file_blacklist)
    targets = [abs_path(src, f+'c') for f in file_dep]
    _task = {
        'actions': [
            (compile, [src]),
        ],
        'file_dep': file_dep,
        'targets': targets,
    }
    if task_dep:
        _task['task_dep'] = task_dep
    return _task
