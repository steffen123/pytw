#/usr/bin/env bash
echo $1 > src/version.ini

git add src/version.ini
git commit -m "release $1"
git tag $1

echo "$1+git" > src/version.ini
git add src/version.ini
git commit -m "postrelease for $1"
