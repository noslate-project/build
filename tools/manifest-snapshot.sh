#!/usr/bin/env bash

set -ex

DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$(dirname "$(dirname $DIRNAME)")"

BRANCH="snapshot"
COMMIT_MSG="Verion Snapshot"
PUSH="false"
COMMIT_ARGS=()
while [ $# -gt 0 ]; do
case $1 in
'--author')
  COMMIT_ARGS+=("--author" "$2")
  shift
  ;;
'-b')
  BRANCH=$2
  shift
  ;;
'-m')
  COMMIT_MSG=$2
  shift
  ;;
'--push')
  PUSH=true
  ;;
esac
shift
done

cd $REPO_ROOT/.repo/manifests
git checkout -b $BRANCH
repo manifest -r -o tmp.xml
mv tmp.xml default.xml
git add default.xml
git commit -m "$COMMIT_MSG" "${COMMIT_ARGS[@]}"

if [ "$PUSH" = "true" ]; then
git push origin $BRANCH
fi

cd -
