"""
terminate all instances not in allowed_instances.yaml file
"""

from __future__ import print_function, unicode_literals

import sys
import os
from os import path
from os.path import join
import os.path
import yaml
import json
import subprocess

conf_dir = sys.argv[1]

script_dir = path.dirname(path.realpath(__file__))
# print('script_dir', script_dir)
aws_path = sys.executable.replace('python', 'aws')

with open(join(conf_dir, 'allowed_instances.yaml'), 'r') as f:
  allowed_instances = set(yaml.load(f))
#print('allowed_instances', allowed_instances)

regions = 'us-west-1 us-west-2 ap-southeast-1 us-east-1 eu-west-1 sa-east-1 ap-southeast-2 ap-northeast-1'.split(' ')
#print('regions', regions)

instances = []
for region in regions:
#    print('region', region)
    contents = subprocess.check_output([
      aws_path,
      '--region', region,
      'ec2',
      'describe-instances',
      '--filters', 'Name=instance-state-code,Values=16'
    ])
    data = json.loads(contents)

    for res in data['Reservations']:
      for inst in res['Instances']:
        if inst.get('InstanceLifecycle', '') == 'spot':
          continue
        instanceId = str(inst['InstanceId'])
        if instanceId not in allowed_instances:
          print('terminating', instanceId)
          print(subprocess.check_output([
            aws_path,
            '--region', region,
            'ec2',
            'terminate-instances',
            '--instance-ids', instanceId
          ]))

