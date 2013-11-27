#!/usr/bin/python

import setuptools

setuptools.setup(
    install_requires=open('requires.txt').readlines(),
    version = 1,
    name = 'signalfd',
    packages = ['signalfd'],
)

