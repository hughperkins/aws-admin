#!/bin/bash

scriptdir=$(dirname $0)
cd ${scriptdir}
source ./setenv.sh

if [[ ! -v VIRTUALENV ]]; then {
    echo please create setenv.sh, and configure appropriately
    exit 1
} fi

if [[ ! -d $VIRTUALENV ]]; then {
    echo VIRTUALENV in setup.sh should point to a valid VIRTUALENV
    exit 1
} fi

source ${VIRTUALENV}/bin/activate

pip install -r requirements.txt
