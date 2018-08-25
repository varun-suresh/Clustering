# -*- coding: utf-8 -*-

from setuptools import (
    setup,
    find_packages)

runtime_packages = [
    'flask == 0.12.3',
    'numpy==1.12.1',
    'matplotlib==1.5.2',
    'profilehooks==1.9.0',
    'pandas==0.20.2',
    'scipy==0.19.0'
]

setup(
    name='approximate-nn-clustering',
    version='0.0.1',
    description='A modified version of rank order clustering',
    author='Varun Suresh',
    author_email='fab.varun@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=runtime_packages,
    )
