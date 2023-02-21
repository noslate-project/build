#!/usr/bin/env bash

set -ex

DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$(dirname "$(dirname $DIRNAME)")"

VERSION=""
PUSH="false"
COMMIT_ARGS=()
while [ $# -gt 0 ]; do
case $1 in
'--author')
  COMMIT_ARGS+=("--author" "$2")
  shift
  ;;
'--push')
  PUSH=true
  ;;
'--version')
  VERSION="$2"
  shift
  ;;
esac
shift
done

if [ -z "$VERSION" ]; then
  echo "version is empty"
  exit 1
fi

COMMIT_MSG="Working on $VERSION"

repo forall -g base -c """
set -ex
pwd
git checkout -b $VERSION
"""

cd $REPO_ROOT/.repo/manifests
git checkout -b $VERSION
node ../../build/tools/manifest-cut-version.js --out tmp.xml ./default.xml $VERSION
mv tmp.xml default.xml
git add default.xml
git commit -m "$COMMIT_MSG" "${COMMIT_ARGS[@]}"

if [ "$PUSH" = "true" ]; then
repo forall -g base -c """
set -ex
git push -u origin $VERSION
"""
git push -u origin $BRANCH
fi

cd -
