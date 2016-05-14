#!/bin/bash

scriptdir=$(dirname $0)
psnum=$(ps -ef|grep 'b[a]sh' | wc -l)

if [[ $psnum != 2 ]]; then {
   # echo 'other connections present'>&2
   exit 0;
} fi

source $scriptdir/setenv.sh
source $VIRTUALENV/bin/activate

python $scriptdir/terminateinstances.py $CONFIGDIR

