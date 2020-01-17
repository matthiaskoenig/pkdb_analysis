#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
import os
from setuptools import find_packages
from setuptools import setup

setup_kwargs = {}


def read(*names, **kwargs):
    """ Read file info in correct encoding. """
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


# version from file
verstrline = read('pkdb_analysis/_version.py')
mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
if mo:
    verstr = mo.group(1)
    setup_kwargs['version'] = verstr
else:
    raise RuntimeError("Unable to find version string")

setup_kwargs['long_description'] = "Python module for the interaction with PKDB."

# parse requirements.txt
required = []

with open('requirements.txt') as f:
    lines = f.read().splitlines()
    for item in lines:
        if item.startswith('#'):
            continue
        elif item.startswith('-e'):
            continue
        else:
            required.append(item)

setup(
    name='pkdb_analysis',
    description='PK-DB analysis',
    url='https://github.com/matthiaskoenig/pkdb_analysis',
    author='Matthias König and Jan Grzegorzewski',
    author_email='konigmatt@googlemail.com',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Cython',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    keywords='pharmacokinetics data',
    packages=find_packages(),
    package_data={
      '': ['../requirements.txt'],
    },
    entry_points={},
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    extras_require={},
    **setup_kwargs)
