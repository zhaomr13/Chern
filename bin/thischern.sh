#!/bin/bash

# Setting the environment for this project
export CHERNSYSROOT=/home/zhaomr/workdir/Chern

# Setting the enviroment for the binnary file
export PATH="${CHERNSYSROOT}/bin:${PATH}"
export PYTHONPATH="${CHERNSYSROOT}:${PYTHONPATH}"

Chern() {
    ${CHERNSYSROOT}/bin/init.py "$@" --std_command_path=${CHERNSYSROOT}/tmp/execuable
    while read line ; do
        eval $line
    done < ${CHERNSYSROOT}/tmp/execuable
}

alias chern=Chern
alias chen=Chern
