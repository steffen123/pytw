#/usr/bin/env bash
echo $1 > src/version.ini

git add src/version.ini
git commit -m "release $1"
git tag -a $1 -m "tag $1"

echo "$1+git" > src/version.ini
git add src/version.ini
git commit -m "postrelease for $1"

git push --follow-tags

echo "Update changelog in readme_de.bb.txt"
echo "Update link+changelog+features in tribe forum and post answer"
