#!/bin/bash

# Setting the environment for this project
export CHERNSYSROOT=/Users/zhaomr/workdir/Chern

# Setting the enviroment for the binnary file
export PATH="${CHERNSYSROOT}/bin:${PATH}"
export PYTHONPATH="${CHERNSYSROOT}:${PYTHONPATH}"
#export PYTHONDONTWRITEBYTECODE=1

Chern() {
    python3 ${CHERNSYSROOT}/bin/ChernMain "$@"
    #--std_command_path="${HOME}/.Chern/tmp/execuable"
    #while read line ; do
        #eval $line
    #done < "${HOME}/.Chern/tmp/execuable"
}

ChernDaemon() {
    ${CHERNSYSROOT}/bin/ChernDaemon "$@"
    #--std_command_path="${HOME}/.Chern/tmp/execuable"
    #while read line ; do
        #eval $line
    #done < "${HOME}/.Chern/tmp/execuable"
}

ServerDaemon() {
    ${CHERNSYSROOT}/bin/ServerDaemon "$@"
    #--std_command_path="${HOME}/.Chern/tmp/execuable"
    #while read line ; do
        #eval $line
    #done < "${HOME}/.Chern/tmp/execuable"
}

alias chern=Chern
alias chen=Chern
