#!/bin/bash

# First make your commits for the desired version 

# Now it is possible to commit the new version inside setup.py
VERSION=$1
sed -i "s~version='.*'~version='${VERSION}'~" setup.py
sed -i "s~/archive/.*\.tar~/archive/${VERSION}\.tar~g" setup.py
git commit setup.py -m "updating tag for version ${VERSION}"
git push

# After, you create a new release on github
echo "Have you created the release on github? If no do it now and type (yes) after"
select yn in "yes" "no"; do
    case $yn in
    # Now we can upload it on PyPI
        yes ) python3 setup.py sdist bdist_wheel; python3 -m twine upload dist/*;;
        no ) exit;;
    esac
done

# deleting build artifacts
rm -r build
rm -r dist
rm -r *.egg-info
