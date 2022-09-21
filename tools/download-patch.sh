#!/usr/bin/env bash

set -ex

DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$(dirname "$(dirname $DIRNAME)")"

HELP=$(cat <<END
download-patch.sh <name:ref> [name:ref]...
END
)

PROJ=()
while [ $# -gt 0 ]; do
case $1 in
'--help')
  printf $HELP
  exit
  ;;
*)
  PROJ+=($1)
  ;;
esac
shift
done

for proj in ${PROJ[@]}; do
  segments=(${proj//:/ })
  SCRIPTS=$(cat <<-END
    set -x
    git merge --abort
    rev=\$(git rev-parse ${segments[1]})
    if [ "\$?" != '0' ]; then
      rev=\$(git rev-parse origin/${segments[1]})
      if [ "\$?" != '0' ]; then
        exit 1
      fi
    fi
    set -e
    git merge \$rev
END
)
  repo forall ${segments[0]} -c "bash -c '$SCRIPTS'"
done
