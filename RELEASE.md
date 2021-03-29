# Release information

## update documentation
* build documentation `cd docs_builder` and `./make_docs.sh 2>&1 | tee ./make_docs.log`

## create release
* update release notes in `release-notes`
* make sure all tests run (`tox -p`)
* bump version (`bumpversion patch` or `bumpversion minor`)
* `git push --tags`


## test release
* test installation in virtualenv from pypi (install and runs tests)
```
mkvirtualenv test --python=python3.8
(test) pip install pkdb-analysis
```
