# -*- coding=utf-8 -*-
import sys
import subprocess as sp
from .files import get_files, _task_for_files

UGLIFYJS = 'uglifyjs'


def uglify(src, dst):
    """
    uglify src file as output file dst
    """
    cmd = [
        UGLIFYJS,
        '--mangle',
        '--compress', 'drop_console=true', # remove console.log
        src,
        '-o', dst,
    ]
    # TODO: generate map file
    sp.check_call(cmd)


def uglify_task(src_path, dist_path,
                folder_blacklist=None, file_blacklist=None, task_dep=None):
    files = get_files(src_path, ext=['.js', '.json'],
                      folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)
    yield _task_for_files(uglify, src_path, dist_path, files)
