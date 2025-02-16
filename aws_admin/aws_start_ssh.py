import argparse
import time
import boto3
import os
import sys
from ruamel.yaml import YAML

from aws_admin import aws_common, aws_init


yaml = YAML()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE', 'default'))
    parser.add_argument('--region', '-r', default=os.environ.get('AWS_REGION', 'virginia'))
    parser.add_argument('--tunnel-ports', '-t', type=int, nargs='+')
    parser.add_argument('--dynamic-port', '-d', type=int)
    parser.add_argument('--name', '-n', type=str, required=True)
    parser.add_argument('--key-path', '-k', '-i', type=str)
    parser.add_argument('--init', action='store_true')
    args = parser.parse_args()

    region_code = aws_common.region_code_by_name[args.region]

    with open('config.yaml') as f:
        config = yaml.load(f)

    session = boto3.Session(profile_name=args.profile, region_name=region_code)
    ec2 = session.client('ec2')
    instance = aws_common.get_instance(ec2=ec2, name=args.name)
    if instance is None:
        print(f'Instance {args.name} not found')
        sys.exit(1)

    instance_id = instance['InstanceId']
    print(instance_id, file=sys.stderr)
    ec2.start_instances(InstanceIds=[instance_id])
    print('Instance starting', file=sys.stderr)
    time.sleep(1)

    if args.init:
        aws_init.init(profile=args.profile, region=args.region, name=args.name)

    instance = aws_common.get_instance(ec2=ec2, name=args.name)
    while 'PublicIpAddress' not in instance:
        print('Instance either not up, or has no public IP address', file=sys.stderr)
        time.sleep(1)
        instance = aws_common.get_instance(ec2=ec2, name=args.name)

    instance_ip = instance['PublicIpAddress']
    aws_common.wait_instance_up(instance_ip)
    
    instance_id = instance['InstanceId']
    key_path = args.key_path
    if key_path is None:
        key_path = config['key_path']
    tunnel_l = []
    if args.tunnel_ports is not None:
        for port in args.tunnel_ports:
            tunnel_l.append(f'-L {port}:localhost:{port}')
    tunnel_str = ' '.join(tunnel_l)
    if args.dynamic_port:
        tunnel_str += f" -D {args.dynamic_port}"
    print(
        f"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {tunnel_str} "
        f"-i {key_path} ubuntu@{instance_ip}")
