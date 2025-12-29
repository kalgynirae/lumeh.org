#!/bin/bash

if (( $(git submodule foreach --quiet --recursive 'if [[ -n $(git status --porcelain) ]]; then echo >&2 "Uncommitted changes in $sm_path"; echo uncommitted; fi' | wc -l) > 0 )); then
  echo >&2 "$0: There are uncommitted changes in at least one submodule"
  exit 1
fi

git submodule update --init --checkout --recursive
git submodule foreach --recursive 'cd "$toplevel" && lib/checkout-submodule-branch.sh "$sm_path"'
