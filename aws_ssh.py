import argparse
import boto3
import os
import sys
from ruamel import yaml
import aws_common


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
    key_path = config['key_path']
    instance_ip = instance['PublicIpAddress']
    print(f'ssh -o StrictHostKeyChecking=no -i {key_path} ubuntu@{instance_ip}')
