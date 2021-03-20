# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
import os

"""
if you want to install dependencies only, do:
pip3 install -r requirements.txt
"""
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + "/requirements.txt"
install_requires = []  # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


setup(
    name="ChordNova",
    version="3.0.0",
    author="Wenge Chen, Ji-woon Sim",
    author_email="rcxwex@163.com",
    maintainer="Osbert Ngok",
    maintainer_email="me@osbertngok.com",
    description="ChordNova is a powerful open-source chord progression analysis plus generation software with unprecedentedly detailed control over chord trait parameters.",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
)

