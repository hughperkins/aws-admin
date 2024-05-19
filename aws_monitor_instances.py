"""
This is designed to run from cron, and email you when instances start or stop
"""
import sys
import os
from os import path
from os.path import join
import os.path
from ruamel import yaml
import json
import boto3

from aws_lib import check_changes, email_lib


def run():
    script_dir = path.dirname(path.realpath(__file__))


    with open(join(script_dir, 'config.yaml')) as f:
        config = yaml.safe_load(f)

    # session = boto3.Session(profile_name=config['profile'], region_name='us-east-1')
    session = boto3.Session(region_name='us-east-1')
    ec2 = session.client('ec2')

    instanceInfos = []
    for reserv in ec2.describe_instances()['Reservations']:
        for instance in reserv['Instances']:
            if instance['State']['Name'] in ['terminated', 'stopped']:
                continue
            instanceInfo = {}
            instanceInfo['id'] = str(instance['InstanceId'])
            instanceInfo['state'] = str(instance['State']['Name'])
            instanceInfo['type'] = str(instance['InstanceType'])
            instanceInfo['publicip'] = str(instance.get('PublicIpAddress', ''))
            instanceInfo['name'] = instanceInfo['publicip']
            for tag in instance.get('Tags', []):
                if str(tag['Key']) == 'Name':
                    instanceInfo['name'] = str(tag['Value'])
            instanceInfos.append( instanceInfo )

    changes_string = check_changes.check_changes(join(script_dir, '.monitor_cache.txt'), instanceInfos)
    if changes_string != '':
        print(changes_string)
        if config['send_smtp']:
            email_lib.send_email(
                config['smtp_server'],
                config['smtp_port'],
                config['smtp_username'],
                config['smtp_password'],
                config['smtp_from_email'],
                config['smtp_to_email'],
                config['smtp_subject'],
                changes_string
            )


if __name__ == '__main__':
    run()
