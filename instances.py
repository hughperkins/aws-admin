from __future__ import print_function
import subprocess
import boto3
import json
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
    parser.add_argument('--profile', default='default')
    parser.add_argument('--region', default='virginia')
    parser.add_argument('--prefix', default='')
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
    # ec2 = session.resource('ec2')
    # print(dir(ec2))
    # help(ec2)

    # data = json.loads(subprocess.check_output([
    #     'aws', '--profile', args.profile, 'ec2', 'describe-instances', '--region', args.region]).decode('utf-8'))
    # print('data.keys()', data.keys())
    # instances
    instance_by_name = {}
    for reserv in ec2.describe_instances()['Reservations']:
        # print('instance', instance)
        for instance in reserv['Instances']:
            name = get_tag(instance['Tags'], 'Name')
            if name is None:
                name = instance['InstanceId']
            # print(name)
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
                    instance.get('PublicIpAddress', '').ljust(14) +
                    instance.get('PrivateIpAddress', '').ljust(14))
                outstr += color + instance['State']['Name'] + Fore.RESET
                print(outstr)
            # ip =
    # print('instance[0]', instance[0])
    # for instance in instances
