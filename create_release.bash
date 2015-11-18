#/usr/bin/env bash
echo $1 > src/version.ini

git add src/version.ini
git commit -m "release $1"
git tag -a $1 -m "tag $1"

echo "$1+git" > src/version.ini
git add src/version.ini
git commit -m "postrelease for $1"

git push --follow-tags

echo "Update link+changelog+features in readme_de.bb.txt"
echo "Update posts in tribe forum and TEF-BND forum and post answer in both"
