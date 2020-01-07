# `pkdb_analysis` - Computational analysis based on PK-DB


This repository contains meta-analyses and example use cases of the data in the PKDB database.

## Installation
To run the analysis scripts create a virtual environment with the required dependencies.
```
mkvirtualenv pkdb_analysis --python=python3
(pkdb_analysis) pip install -r requirements.txt
(pkdb_analysis) pip install -e .
(pkdb_analysis) pip install jupyterlab
(pkdb_analysis) pip install ipykernel
(pkdb_analysis) python -m ipykernel install --user --name pkdb_analysis

```
The scripts are running against a given endpoint on which the PKDB backend is running.


Subsequently the virtualenv must be registered as jupyter kernel to use it for the analysis.

### Install Circos
follow instructions on 
`http://circos.ca/documentation/tutorials/configuration/distribution_and_installation/`.
and install Circos 
 
Install missing perl modules:

`http://www.circos.ca/documentation/tutorials/configuration/perl_and_modules/`
Check which modules are missing
```
circos -modules
```
Install them
```
sudo apt-get install libgd-gd2-perl

```
```
sudo perl -MCPAN -e shell
...
cpan[1]>install Math::Bezier
...
```
- download Circos


&copy; 2018-2020 Jan Grzegorzewski & Matthias König.
