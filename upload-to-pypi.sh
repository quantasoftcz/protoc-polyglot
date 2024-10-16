
# first, make sure to increase the "post" number in pyproject.toml: e.g. from 0.0.1-1 to 0.0.1-2

# remove cache folder
rm -rf ./dist
# build Python package
hatchling build
# upload package to PyPi
twine upload -p $PYPI_KEY dist/*

# update the package locally, the first run checks for remote updates, the second one updates the package
pip install protoc-polyglot --upgrade
pip install protoc-polyglot --upgrade