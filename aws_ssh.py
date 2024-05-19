import argparse
import boto3
import os
import sys
from ruamel.yaml import YAML
import aws_common


yaml = YAML()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE', 'default'))
    parser.add_argument('--region', default=os.environ.get('AWS_REGION', 'virginia'))
    parser.add_argument('--tunnel-ports', type=int, nargs='+')
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--key-path', type=str)
    args = parser.parse_args()

    region_code_by_name = {
        'tokyo': 'ap-northeast-1',
        'virginia': 'us-east-1'
    }

    region_code = region_code_by_name[args.region]

    with open('config.yaml') as f:
        config = yaml.load(f)

    session = boto3.Session(profile_name=args.profile, region_name=region_code)
    ec2 = session.client('ec2')
    instance = aws_common.get_instance(ec2=ec2, name=args.name)
    if instance is None:
        print(f'Instance {args.name} not found')
        sys.exit(1)
    instance_id = instance['InstanceId']
    if 'PublicIpAddress' not in instance:
        print('Instance either not up, or has no public IP address')
        sys.exit(1)
    instance_ip = instance['PublicIpAddress']
    key_path = args.key_path
    if key_path is None:
        key_path = config['key_path']
    tunnel_l = []
    if args.tunnel_ports is not None:
        for port in args.tunnel_ports:
            tunnel_l.append(f'-L {port}:localhost:{port}')
    tunnel_str = ' '.join(tunnel_l)
    print(f'ssh -o StrictHostKeyChecking=no {tunnel_str} -i {key_path} ubuntu@{instance_ip}')
