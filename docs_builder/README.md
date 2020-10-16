# Documentation
Make sure you have uploaded the tests in the database you work with. This can be set by the environment variable `API_BASE` (e.g. in `.env.local`). 
To create the documentation use
```
(pkdb_analysis) cd docs
(pkdb_analysis) pip install -r requirements-docs.txt
```

To create notebooks and documentation use
(pandocs needs to be installed https://pandoc.org/installing.html)
```
(pkdb_analysis) ./make_docs.sh
```
To only create the html from existing `*.rst` files use
```
(pkdb_analysis) make html
```

The documentation is build using `sphinx` with the
[sphinx-rtd-theme](https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html)
