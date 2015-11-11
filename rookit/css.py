# -*- coding=utf-8 -*-
import csscompressor
from .files import _task_for_files, get_files


def csscompress(src, out):
    css = csscompressor.compress(open(src).read())
    open(out, 'w').write(css)


def compile_css_task(src_path, dist_path,
                     folder_blacklist=None, file_blacklist=None,
                     task_dep=None):
    files = get_files(src_path, ext=['.css'],
                      folder_blacklist=folder_blacklist,
                      file_blacklist=file_blacklist)

    yield _task_for_files(csscompress, src_path, dist_path, files)
