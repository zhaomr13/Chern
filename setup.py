from distutils.coimport sys
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

PACKAGE = "Chern"
NAME = "Chern"
DESCRIPTION = "A data analysis framework for High Energy Physics"
AUTHOR = "Mingrui Zhao"
AUTHOR_EMAIL = "mingrui.zhao@mail.labz0.org"
URL = "https://github.com/zhaomr13/Chern"
VERSION = __import__(PACKAGE).__version__

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License, Version 2.0",
    url = URL,
    packages=["Chern"],
    classifiers = [
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: System :: Software Distribution',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',

    ],
    zip_safe=False,
    keywords = "Analysis Perservation",
    packages = find_packages(exclude=[])
    install_requires = [
        "click", "colored"
    ]
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'Chern = main:main'
        ]
    }
)
