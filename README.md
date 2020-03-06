# `pkdb_analysis` - PK-DB python interface
[![Build Status](https://travis-ci.org/matthiaskoenig/pkdb_analysis.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/pkdb_analysis)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)

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

To install the optional support for jupyter notebooks use
```
(pkdb_analysis) pip install jupyterlab
(pkdb_analysis) pip install ipykernel
(pkdb_analysis) python -m ipykernel install --user --name pkdb_analysis
```
The scripts are running against a given endpoint on which the PKDB backend is running.

## Select PK-DB endpoint
`pkdb_analysis` can use any existing endpoint to a PKDB instance. 
To select the endpoint on which `PK-DB` is running set the respective environment variables.
See for an example the `.env.local` for working with a locally running instance.

To interact with PKDB the API endpoint and the user information have to be set.
To use a local instance set
```
API_BASE=http://0.0.0.0:8000/
USER=admin
PASSWORD=pkdb_admin
```
Two publically available instances are running at 
```
API_BASE=https://develop.pk-db.com
``` 
and 
```
API_BASE=https://pk-db.com
```

&copy; 2018-2020 Jan Grzegorzewski & Matthias König.