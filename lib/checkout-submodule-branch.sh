#!/bin/bash

if ! cd "$1"; then
  echo >&2 "Failed to cd to ${1@Q}; aborting"
  exit 1
fi

names=( $(git branch --contains HEAD --format '%(refname:short)') )

if [[ " ${names[*]} " == *" main "* ]]; then
  branch=main
elif [[ " ${names[*]} " == *" master "* ]]; then
  branch=master
elif (( ${names#} )); then
  branch=${names[0]}
else
  echo >&2 "No branch found; skipping"
  exit 0
fi

git checkout "$branch"
