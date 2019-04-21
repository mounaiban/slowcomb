"""
setup-github — packaging script for slowcomb cloned from GitHub
"""

# Classifiers taken from the Python Software Foundation. Classifiers.
#  https://pypi.org/classifiers/

import os
import datetime
from setuptools import setup, find_packages

# Vital Info
#
PACKING_TIME_UTC = datetime.datetime.utcnow().isoformat()

# README: Dump the contents of README.rst
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README=readme.read()

VERSION = "1.1.dev.{0}".format(PACKING_TIME_UTC)

# Invocation of setup()
#
setup(
    name="slowcomb",
    version=VERSION,
    packages=find_packages(exclude=["*tests*, *demos"]),
    author="Mounaiban",
    author_email="whatever@mounaiban.com",
    description="""General-purpose combinatorics library with
    addressable (subscriptable) results""",
    keywords="combinatorics combination permutation mathematics library",
    long_description=README,
    project_urls={
        "Source Code" : "https://github.com/mounaiban/slowcomb",
        "Bug Tracker" : "https://github.com/mounaiban/slowcomb/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Operating System Independent",
        "Programming Language :: Python :: 3.7",
    ],
)

