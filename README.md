# `pkdb_analysis` - Computational analysis based on PK-DB

This repository contains meta-analyses and example use cases of the data in the PKDB database.

## Installation
To run the analysis scripts create a virtual environment with the required dependencies.
```
mkvirtualenv pkdb_analysis --python=python3.7
(pkdb_analysis) pip install -e .
# optional for jupyter notebooks
(pkdb_analysis) pip install jupyterlab
(pkdb_analysis) pip install ipykernel
(pkdb_analysis) python -m ipykernel install --user --name pkdb_analysis
```
The scripts are running against a given endpoint on which the PKDB backend is running.

&copy; 2018-2020 Jan Grzegorzewski & Matthias König.
