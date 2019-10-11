# pkdb_analysis - PKDB Analysis scripts
This repository contains meta-analyses and example use cases of the data in the PKDB database.

## Installation
To run the analysis scripts create a virtual environment with the required dependencies.
```
mkvirtualenv pkdb_analysis --python=python3
(pkdb_analysis) pip install -r requirements.txt
(pkdb_analysis) pip install -e .
(pkdb_analysis) ipython kernel install --user --name pkdb_analysis
```
Subsequently the virtualenv must be registered as jupyter kernel to use it for the analysis.-

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
-

### Start pkdb backend
The scripts use the REST API of PKDB. Consequently, a running REST endpoint is required.
This can either be the online database at `pk-db.com` or a locally running instance of 
the backend
```
workon pkdb
(pkdb) cd path/to/pkdb
(pkdb) sudo sysctl -w vm.max_map_count=262144
(pkdb) docker-compose up 
```

&copy; 2018-2019 Jan Grzegorzewski & Matthias König.
