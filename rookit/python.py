# -*- coding=utf-8 -*-
import compileall
from .files import get_files


def compile(path):
    """
    compile .py to pyc
    """
    compileall.compile_dir(path, maxlevels=100, quiet=True)
    
    
def compile_python_task(src, 
                        folder_blacklist=None, file_blacklist=None,
                        task_dep=None):
    """
    compile all python folder in given folder task
    """
    if not task_dep:
        task_dep = []
    file_dep = get_files(src, ext=['.py'], folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)
    targets = [f+'c' for f in file_dep]
    return {
        'actions': [
            (compile, [src]),
        ],
        'file_dep': file_dep,
        'targets': targets,
        'task_dep': task_dep
    }
