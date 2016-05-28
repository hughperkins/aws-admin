#!/bin/bash

ssh nimbix@$(python nimbix/ssh.py "$@")

