from __future__ import print_function
import subprocess
import boto3
import json
import os
import argparse
import boto3
import colorama
from colorama import init as colorama_init, Fore


def get_tag(tags, key):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE', 'default'))
    parser.add_argument('--region', default=os.environ.get('AWS_REGION', 'virginia'))
    parser.add_argument('--name', required=True)
    args = parser.parse_args()

    region_code_by_name = {
        'tokyo': 'ap-northeast-1',
        'virginia': 'us-east-1'
    }

    region_code = region_code_by_name[args.region]
    print('region_code', region_code)

    colorama_init()

    session = boto3.Session(profile_name=args.profile, region_name=region_code)
    ec2 = session.client('ec2')
    instance_by_name = {}
    for reserv in ec2.describe_instances()['Reservations']:
        # print('instance', instance)
        for instance in reserv['Instances']:
            name = get_tag(instance['Tags'], 'Name')
            if name is None:
                name = instance['InstanceId']
            # print(name)
    instance = instance_by_name[args.name]
    instance_id = instance['InstanceId']
    print(instance_id)
    ec2.stop_instances(InstanceIds=[instance_id])
