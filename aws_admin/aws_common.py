import socket
import sys
import time


region_code_by_name = {
    'tokyo': 'ap-northeast-1',
    'tok': 'ap-northeast-1',
    'tk': 'ap-northeast-1',
    'virginia': 'us-east-1'
}


def get_tag(tags, key):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']


def get_instance(ec2, name: str):
    instance_by_name = {}
    for reserv in ec2.describe_instances()['Reservations']:
        for instance in reserv['Instances']:
            if instance['State']['Name'] == 'terminated':
                continue
            _name = get_tag(instance['Tags'], 'Name')
            if _name is None:
                _name = instance['InstanceId']
            instance_by_name[_name] = instance
    instance = instance_by_name.get(name, None)
    return instance


def wait_instance_up(instance_ip: str) -> None:
    connected = False
    while not connected:
        try:
            socket.create_connection((instance_ip, 22), timeout=1)
            connected = True
        except socket.timeout:
            print('.', end='', flush=True, file=sys.stderr)
            time.sleep(1)
        except ConnectionRefusedError:
            print('.', end='', flush=True, file=sys.stderr)
            time.sleep(1)
    print('', file=sys.stderr)
