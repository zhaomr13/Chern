#!/bin/bash

# Setting the environment for this project
export CHERNSYSROOT=/home/zhaomr/workdir/Chern

# Setting the enviroment for the binnary file
export PATH="${CHERNSYSROOT}/bin:${PATH}"
export PYTHONPATH="${CHERNSYSROOT}:${PYTHONPATH}"

Chern() {
    ${CHERNSYSROOT}/bin/Chern "$@"
    #--std_command_path="${HOME}/.Chern/tmp/execuable"
    #while read line ; do
        #eval $line
    #done < "${HOME}/.Chern/tmp/execuable"
}

alias chern=Chern
alias chen=Chern
