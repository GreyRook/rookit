#!/usr/bin/env python

from distutils.core import setup

setup(name='rookit',
      version='0.1.0',
      description='grey rook scripts for doit',
      author='Andreas Bresser',
      author_email='a.bresser@greyrook.com',
      url='',
      packages=['rookit'],
      install_requires=['doit==0.26.0', 'pyaml', 'csscompressor', 'nodeenv']
)
