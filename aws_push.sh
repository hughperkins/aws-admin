#!/bin/bash

IPADDRESS=nfs.aws.hughperkins.com

LOCALFOLDER=$PWD
REMOTEFOLDER=${PWD/\/Users\/hugh/\/persist/}

echo REMOTEFOLDER ${REMOTEFOLDER}

git diff > gitdiff.txt
git log -n 3 > gitlog.txt

rsync \
    --exclude '*.pt' \
    --exclude '__pycache__' \
    --exclude 'logs' \
    --exclude '.cache.txt' \
    --exclude 'pull' \
    --exclude '*.ipynb' \
    --exclude '.DS_Store' \
    --exclude '_vizdoom.ini' \
    --exclude '*.lmp' \
    --exclude '*.png' \
    --exclude '*.gz' \
    --exclude '*.whl' \
    --exclude 'recordings/' \
    --exclude '.pytest_cache/' \
    --exclude '.python-version' \
    --exclude 'dist/' \
    -av -e "ssh -i ~/ec2/2handmbp2022.pem" \
    ${PWD}/ ubuntu@${IPADDRESS}:${REMOTEFOLDER}/

    # --exclude '.git' \
