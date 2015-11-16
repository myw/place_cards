#!/usr/bin/env python

import os

try:
  from setuptools import setup
except ImportError:
  from ez_setup import use_setuptools
  use_setuptools()
  from setuptools import setup


def lopen(fname, mode='r'):
  return open(os.path.join(os.path.dirname(__file__), fname), mode=mode)


def load_reqs(fname):
  with lopen(fname) as f:
    reqs = [x.strip() for x in f.readlines()
            if not (x.strip().startswith('#') or x.strip().startswith('-e'))]
    return reqs


setup(
  name='place_cards',
  version='0.1.0',
  description='Automatically generate place cards from a template',
  author='Misha Wolfson',
  author_email='mywolfson@gmail.com',
  long_description=lopen('README.md').read(),
  packages=[
    'place_cards',
  ],
  zip_safe=True,
  install_requires=load_reqs('requirements/base.txt'),
  classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities',
  ],
)
