pkdb_analysis: PK-DB python interface
======================================

.. image:: https://github.com/matthiaskoenig/pkdb_analysis/workflows/CI-CD/badge.svg
   :target: https://github.com/matthiaskoenig/pkdb_analysis/workflows/CI-CD
   :alt: GitHub Actions CI/CD Status

.. image:: https://img.shields.io/pypi/v/pkdb_analysis.svg
   :target: https://pypi.org/project/pkdb_analysis/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pkdb-analysis.svg
   :target: https://pypi.org/project/pkdb-analysis/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pkdb-analysis.svg
   :target: http://opensource.org/licenses/LGPL-3.0
   :alt: GNU Lesser General Public License 3

.. image:: https://codecov.io/gh/matthiaskoenig/pkdb_analysis/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/matthiaskoenig/pkdb_analysis
   :alt: Codecov

.. image:: https://readthedocs.org/projects/pkdb_analysis/badge/?version=latest
   :target: https://pkdb_analysis.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3997539.svg
   :target: https://doi.org/10.5281/zenodo.3997539
   :alt: Zenodo DOI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

pkdb_analysis is a collection of python utilities to interact with
`PK-DB <https://pk-db.com>`__ via the available REST endpoints
(`https://pk-db.com/api/v1/swagger/ <https://pk-db.com/api/v1/swagger/>`__).

How to cite
===========
.. image:: https://zenodo.org/badge/3997539.svg
   :target: https://zenodo.org/badge/latestdoi/3997539
   :alt: Zenodo DOI

License
=======

* Source Code: `LGPLv3 <http://opensource.org/licenses/LGPL-3.0>`__
* Documentation: `CC BY-SA 4.0 <http://creativecommons.org/licenses/by-sa/4.0/>`__

The pkdb_analysis source is released under both the GPL and LGPL licenses version 2 or
later. You may choose which license you choose to use the software under.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License or the GNU Lesser General Public
License as published by the Free Software Foundation, either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

Funding
=======
Matthias König and Jan Grzegorzewski are supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054).


Installation
============
`pkdb_analysis` is available from `pypi <https://pypi.python.org/pypi/pkdb-analysis>`__ and
can be installed via::

    pip install pkdb-analysis

Develop version
---------------
The latest develop version can be installed via::

    pip install git+https://github.com/matthiaskoenig/pkdb_analysis.git@develop

Or via cloning the repository and installing via::

    git clone https://github.com/matthiaskoenig/pkdb_analysis.git
    cd pkdb_analysis
    pip install -e .

To install for development use::

    pip install -e .[development]


PK-DB endpoint
==============

`pkdb_analysis` requires an existing PK-DB endpoint, which can be set by setting the
respective environment variables.::

    set -a && source .env.local

The public instances of PK-DB are available from
```
API_BASE=https://pk-db.com
API_BASE=https://alpha.pk-db.com
API_BASE=https://develop.pk-db.com
```
By default the alpha server is used.


&copy; 2018-2020 Jan Grzegorzewski & Matthias König.