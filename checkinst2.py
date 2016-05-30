from __future__ import print_function, unicode_literals

import sys
import os
from os import path
from os.path import join
import os.path
import yaml
import json
import subprocess
import checkchanges

script_dir = path.dirname(path.realpath(__file__))
# print('script_dir', script_dir)
aws_path = sys.executable.replace('python', 'aws')
contents = subprocess.check_output([
  aws_path,
  'ec2',
  'describe-instances',
  '--filters', 'Name=instance-state-code,Values=16'
]).decode('utf-8')
data = json.loads(contents)

instanceInfos = []
for res in data['Reservations']:
  for inst in res['Instances']:
    instanceInfo = {}
    instanceInfo['id'] = str(inst['InstanceId'])
    instanceInfo['state'] = str(inst['State']['Name'])
    instanceInfo['type'] = str(inst['InstanceType'])
    instanceInfo['publicip'] = str(inst['PublicIpAddress'])
    instanceInfo['name'] = instanceInfo['publicip']
    for tag in inst.get('Tags', []):
      if str(tag['Key']) == 'Name':
        instanceInfo['name'] = str(tag['Value'])
    instanceInfos.append( instanceInfo )

changesString = checkchanges.checkChanges(join(script_dir, 'oldlines.txt'), instanceInfos)
if changesString != '':
  print(changesString)

