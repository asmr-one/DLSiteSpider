#!/usr/bin/env python
from setuptools import setup

setup(
    install_requires=[open("requirements.txt").read().strip().split("\n")],
)
