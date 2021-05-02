#!/usr/bin/env bash

update () {
    [[ "${1}" == "" ]] && exit 127

    git add --all
    git commit --message "${1}"
    [[ "${2}" != "" ]] && git commit --amend "\n" \
        && git commit --amend "${2}"
    git push   
}; alias git-update=update
