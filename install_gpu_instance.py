"""
target context:
- ubuntu 16.04
- python 3 is available
"""
import subprocess
import time
import argparse
import os
from os import path


childenv = os.environ.copy()
HOME = os.environ['HOME']


def install_pytorch():
    if not path.isdir('%s/conda' % HOME):
        print(subprocess.check_output([
            'bash', '/mldata/Miniconda3-latest-Linux-x86_64.sh',
            '-b',
            '-p', '%s/conda' % HOME
        ]).decode('utf-8'))
    if not path.isdir('%s/conda/envs/pytorch' % HOME):
        print(subprocess.check_output([
            '%s/conda/bin/conda' % HOME,
            'create',
            '-n', 'pytorch',
            '-q', '-y'
        ]).decode('utf-8'))

    # equivalent of activation:
    childenv['PATH'] += ':%s/conda/envs/pytorch/bin' % HOME
    childenv['CONDA_PREFIX'] = '%s/conda/envs/pytorch' % HOME
    childenv['CONDA_DEFAULT_ENV'] = 'pytorch'

    print(subprocess.check_output([
        'conda',
        'install',
        'pytorch', 'cuda80',
        '-c' 'soumith'
        '-y'
    ], env=childenv).decode('utf-8'))


def run(components):
    for component, func in {'pytorch': install_pytorch}.items():
        if component in components:
            func()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--components', type=str, default='all', help='[all|pytorch], comma-separated')
    args = parser.parse_args()
    args.components = set(args.components.split(','))
    run(**args.__dict__)
