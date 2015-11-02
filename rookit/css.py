# -*- coding=utf-8 -*-
import csscompressor
from .files import get_files, get_dist_path


def csscompress(src, out):
    css = csscompressor.compress(open(src).read())
    open(out, 'w').write(css)


def compile_css_task(src_path, dist_path, 
                     folder_blacklist=None, file_blacklist=None,
                     task_dep=None):
    files = get_files(src_path, ext=['.css'], folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)
    for filename in files:
        out = get_dist_path(src_path, dist_path, filename)
        task = {
            'name': filename + ' --> ' + out,
            'actions': [(csscompress, [filename, out])],
            'targets': [out],
            'file_dep': files
        }
        if task_dep:
            task['task_dep'] = task_dep
        yield task
