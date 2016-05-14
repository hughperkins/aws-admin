from __future__ import print_function, unicode_literals

import sys
import os
import os.path
import yaml
import json
import subprocess

aws_path = sys.executable.replace('python', 'aws')
contents = subprocess.check_output([
  aws_path,
  'ec2',
  'describe-instances',
  '--filters', 'Name=instance-state-code,Values=16'
])

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
    for tag in inst['Tags']:
      if str(tag['Key']) == 'Name':
        instanceInfo['name'] = str(tag['Value'])
    instanceInfos.append( instanceInfo )

newString = yaml.safe_dump(instanceInfos, default_flow_style = False )

oldString = ''
if os.path.isfile('oldlines.txt'):
    f = open('oldlines.txt','r')
    oldString = f.read()
    f.close()

if(newString != oldString):
   print('changed: old:')
   print( oldString )
   print('new:')
   print( newString )
   f = open('~oldlines.txt', 'w')
   f.write( newString )
   f.close()
   os.rename( '~oldlines.txt', 'oldlines.txt' )

