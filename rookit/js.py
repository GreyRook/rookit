# -*- coding=utf-8 -*-
import sys
import subprocess as sp
from .files import get_files, task_for_files


def uglify(in_file, out_file):
    cmd = [
        'uglifyjs',
        '--mangle',
        '--compress', 'drop_console=true', # remove console.log
        in_file,
        '-o', out_file,
    ]

    proc = sp.Popen(
        cmd,
        stdout=sp.PIPE)
    if proc.wait() != 0:
        print('uglifyjs FAILED for {}'.format(in_file))
        sys.exit(1)


def uglify_task(src_path, dist_path,
                folder_blacklist=None, file_blacklist=None, task_dep=None):
    files = get_files(src_path, ext=['.js', '.json'],
                      folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)
    yield task_for_files(uglify, src_path, dist_path, files)
