# -*- coding=utf-8 -*-
import io
import os
import subprocess as sp

from PIL import Image
import shutil

from . import files


BASE = os.path.abspath(os.path.dirname(__file__))
OPTIPNG = 'optipng'
SVGO = 'svgo'
CJPEG = os.path.join(os.path.expanduser("~"), 'apps', 'mozjpeg', 'cjpeg') # TODO evil


def optimize(src, dst):
    files.create_dist_path(dst)

    if src.endswith('.png'):
        sp.check_call([OPTIPNG, '-out', dst, src])
    elif src.endswith('.svg'):
        sp.check_call([SVGO, '--multipass', '-i', src, '-o', dst])
    else:
        shutil.copy(src, dst)


def convert_to_jpg(src, dst, quality=80):
    files.create_dist_path(dst)

    img = Image.open(src)
    tmp = io.StringIO()
    img.save(tmp, format="PPM")
    cmd = [CJPEG, '-quality', str(quality)]
    proc = sp.Popen(cmd, stdout=open(dst, 'w'), stdin=sp.PIPE)
    proc.stdin.write(tmp.getvalue())
    proc.stdin.close()
