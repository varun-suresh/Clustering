# -*- coding: utf-8 -*-

from setuptools import (
    setup,
    find_packages)

runtime_packages = [
"Click==7.0",
"cycler==0.10.0",
"Flask==2.3.2",
"itsdangerous==1.1.0",
"Jinja2==3.1.6",
"kiwisolver==1.1.0",
"MarkupSafe==1.1.1",
"matplotlib==3.1.1",
"numpy==1.22.0",
"pandas==0.25.0",
"profilehooks==1.11.0",
"pyparsing==2.4.1.1",
"python-dateutil==2.8.0",
"pytz==2019.1",
"scipy==1.10.0",
"six==1.12.0",
"Werkzeug==3.1.4",
]

setup(
    name='approximate-nn-clustering',
    version='0.0.2',
    description='A modified version of rank order clustering',
    author='Varun Suresh',
    author_email='fab.varun@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=runtime_packages,
    )
