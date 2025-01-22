import boto3
import os
import argparse
from colorama import init as colorama_init

from aws_admin import aws_common, aws_init


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE', 'default'))
    parser.add_argument('--region', '-r', default=os.environ.get('AWS_REGION', 'virginia'))
    parser.add_argument('--name', '-n', type=str, required=True)
    parser.add_argument('--init', action='store_true')
    args = parser.parse_args()

    region_code = aws_common.region_code_by_name[args.region]
    print('region_code', region_code)

    colorama_init()

    session = boto3.Session(profile_name=args.profile, region_name=region_code)
    ec2 = session.client('ec2')
    instance = aws_common.get_instance(ec2=ec2, name=args.name)
    instance_id = instance['InstanceId']
    print(instance_id)
    ec2.start_instances(InstanceIds=[instance_id])
    print('Instance starting')

    if args.init:
        aws_init.init(profile=args.profile, region=args.region, name=args.name)
