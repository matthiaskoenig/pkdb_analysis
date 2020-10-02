# Release information

## update documentation
* build documentation `cd docs_builder` and `./make_docs.sh 2>&1 | tee ./make_docs.log`

## create release
* sort imports (`isort src/pkdb_analysis`)
* code formating (`black src/pkdb_analysis`)
* make sure all tests run (`tox --`)
* update release notes in `release-notes`
* bump version (`bumpversion patch` or `bumpversion` minor)
* `git push --tags`


## test release
* test installation in virtualenv from pypi (install and runs tests)
```
mkvirtualenv test --python=python3.8
(test) pip install pkdb-analysis
```
