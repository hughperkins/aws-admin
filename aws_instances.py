from __future__ import print_function
import subprocess
import boto3
import json
import argparse
import os
import boto3
from ruamel import yaml
import colorama
from colorama import init as colorama_init, Fore


def get_tag(tags, key):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE', config['profile']))
    parser.add_argument('--region', default=os.environ.get('AWS_REGION', config['default-region']))
    parser.add_argument('--prefix', default=os.environ.get('AWS_PREFIX', ''))
    args = parser.parse_args()

    region_code_by_name = {
        'tokyo': 'ap-northeast-1',
        'virginia': 'us-east-1'
    }

    region_code = region_code_by_name.get(args.region, args.region)
    print('')
    print(region_code + ':')

    colorama_init()

    print(
        'Name'.ljust(18) +
        'State'.ljust(10) +
        'Type'.ljust(16) +
        # instance.get('PublicIpAddress', '').ljust(14) +
        # instance.get('PrivateIpAddress', '').ljust(14)
    '')

    session = boto3.Session(profile_name=args.profile, region_name=region_code)
    ec2 = session.client('ec2')
    instance_by_name = {}
    for reserv in ec2.describe_instances()['Reservations']:
        for instance in reserv['Instances']:
            if instance['State']['Name'] == 'terminated':
                continue
            name = get_tag(instance['Tags'], 'Name')
            if name is None:
                name = instance['InstanceId']
            instance_by_name[name] = instance
            if name.startswith(args.prefix):
                color = Fore.RESET
                if instance['State']['Name'] == 'stopped':
                    color = Fore.RED
                elif instance['State']['Name'] == 'running':
                    color = Fore.GREEN
                elif instance['State']['Name'] == 'stopping':
                    color = Fore.BLUE
                elif instance['State']['Name'] == 'pending':
                    color = Fore.BLUE
                outstr = (
                    color + name.ljust(18) + Fore.RESET +
                    color + instance['State']['Name'].ljust(10) + Fore.RESET +
                    instance.get('InstanceType', '').ljust(16) +
                    # instance.get('PublicIpAddress', '').ljust(14) +
                    # instance.get('PrivateIpAddress', '').ljust(14)
                '')
                # outstr += color + instance['State']['Name'] + Fore.RESET
                print(outstr)
    print('')
