# -*- coding: utf-8 -*-

# @File    : setup.py
# @Date    : 2020-11-20
# @Author  : Dothion

from setuptools import setup, find_packages

setup(
   name='OldSeaMap',
   version='0.0.1',
   packages=find_packages('src'),
   install_requires=['pampy', 'funcy']
)
