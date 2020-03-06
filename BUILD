#!/bin/bash

# First make your commits for the desired version 

# After, you create a new release on github

# Now it is possible to create the new version and upload it on PyPI
VERSION=$1
sed -i "s~version='.*'~version='${VERSION}'~" setup.py
sed -i "s~/archive/.*\.tar~/archive/${VERSION}\.tar~g" setup.py
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
rm -r build
rm -r dist
rm -r *.egg-info
