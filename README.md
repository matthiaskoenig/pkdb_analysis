# `pkdb_analysis` - PK-DB python interface
[![PyPI version](https://badge.fury.io/py/pkdb-analysis.svg)](https://badge.fury.io/py/pkdb-analysis)
[![Build Status](https://travis-ci.org/matthiaskoenig/pkdb_analysis.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/pkdb_analysis)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)
[![codecov](https://codecov.io/gh/matthiaskoenig/pkdb_analysis/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/pkdb_analysis)

<b><a href="https://orcid.org/0000-0002-4588-4925" title="0000-0002-4588-4925"><img src="./docs/images/orcid.png" height="15"/></a> Jan Grzegorzewski</b>
and
<b><a href="https://orcid.org/0000-0003-1725-179X" title="https://orcid.org/0000-0003-1725-179X"><img src="./docs/images/orcid.png" height="15" width="15"/></a> Matthias König</b>

This repository provides a python interface to PK-DB (https://pk-db.com) using the existing REST endpoints.

## Installation
To run the analysis scripts create a virtual environment with the required dependencies.
```
mkvirtualenv pkdb_analysis --python=python3.7
(pkdb_analysis) pip install -e .
```
To execute the tests on installation use
```
(pkdb_analysis) pip install -e . --install-option test
```

## Select PK-DB endpoint
`pkdb_analysis` can use any existing endpoint to a PKDB instance. 
To select the endpoint on which `PK-DB` is running set the respective environment variables. See for an example the `.env.local` for working with a locally running instance.
The environment variable can be exported via
```
set -a && source .env.local
```
Public instances of PK-DB are available from 
```
API_BASE=https://develop.pk-db.com
API_BASE=https://pk-db.com
``` 
By default the develop server is used.

## Changelog

### v0.1.4
* packaging interactive plot resources
* testing on installation

### v0.1.3
* fixing unit tests
* refactored table factory
* pip package

&copy; 2018-2020 Jan Grzegorzewski & Matthias König.