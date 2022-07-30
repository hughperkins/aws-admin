"""
mounts nfs server
"""

import os
import argparse
import sys
import boto3
import aws_common
from ruamel import yaml


def run_cmd(cmd):
    print(cmd)
    ret = os.system(cmd)
    assert ret == 0


def remote_cmd(key_path, instance_ip, cmd):
    run_cmd(f'ssh -o StrictHostKeyChecking=no -i {key_path} ubuntu@{instance_ip} {cmd}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE', 'default'))
    parser.add_argument('--region', default=os.environ.get('AWS_REGION', 'virginia'))
    parser.add_argument('--name', type=str, required=True)
    args = parser.parse_args()

    region_code_by_name = {
        'tokyo': 'ap-northeast-1',
        'virginia': 'us-east-1'
    }

    region_code = region_code_by_name[args.region]
    print('region_code', region_code)

    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    session = boto3.Session(profile_name=args.profile, region_name=region_code)
    ec2 = session.client('ec2')
    if args.name != '':
        instance_by_name = {}
        for reserv in ec2.describe_instances()['Reservations']:
            # print('instance', instance)
            for instance in reserv['Instances']:
                name = aws_common.get_tag(instance['Tags'], 'Name')
                if name is None:
                    name = instance['InstanceId']
                # print(name)
                instance_by_name[name] = instance
        instance = instance_by_name[args.name]
        instance_id = instance['InstanceId']
    else:
        instance_id = args.id
    print(instance_id)

    key_path = config['key_path']
    instance_ip = instance['PublicIpAddress']
    nfs_ip = config['nfs_ip']

    init_script = f"""
#!/bin/bash

set -x
set -e

sudo apt-get update
# dependencies for pyenv
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

sudo apt-get install -y nfs-client
if [[ ! -d /persist ]]; then {{
    sudo mkdir -m 000 /persist
}} fi
sudo mount {nfs_ip}:/nfs-data /persist
sudo hostname {args.name}

if ! grep persist /home/ubuntu/.bashrc; then {{
    touch /persist/.bashrc
    cat >> /home/ubuntu/.bashrc <<EOF
export HOME=/persist
source /persist/.bashrc
cd
pwd
EOF
}} fi
"""
    with open(f'/tmp/init_{args.name}.sh', 'w') as f:
        f.write(init_script)
    run_cmd(f'scp -o StrictHostKeyChecking=no -i {key_path} /tmp/init_{args.name}.sh ubuntu@{instance_ip}:/tmp/init.sh')
    run_cmd(f'ssh -o StrictHostKeyChecking=no -i {key_path} ubuntu@{instance_ip} bash /tmp/init.sh')
