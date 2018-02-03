git stash
git checkout -b temp
git branch -d master
git push origin --delete master REM may do nothing or fail ... that is ok.
git fetch --all --prune
git checkout -b master
git stash pop
git branch -d temp
git branch push origin --delete temp
git fetch --all --prune
git push --set-upstream origin master
git rm -cached *.xml
REM continue as normal ?? In theory.

REM !Important note! Do these _13_ steps on each computer you own.