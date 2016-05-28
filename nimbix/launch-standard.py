"""
Usage:
  launch.py [options]

Options:
  --username username    username
  --apikey APIKEY    apikey
"""

from __future__ import print_function
import sys
import requests
from docopt import docopt

api_url = 'https://api.jarvice.com/jarvice'

args = docopt(__doc__)
username = args['--username']
apikey = args['--apikey']

if username == '' or apikey == '' or username is None or apikey is None:
  print('please provide apikey and username')
  sys.exit(1)

launch_data = {
  "machine": {
    "nodes": "1",
    "type": "ngd3"
  },
  "vault": {
    "readonly": False,
    "force": False,
    "name": "drop.jarvice.com"
  },
  "user": {
    "username": username,
    "apikey": apikey
  },
  "nae": {
    "force": False,
    "name": "foo2",
    "geometry": "1904x881",
    "ephemeral": False,
    "staging": True,
    "interactive": True
  }
}

res = requests.post('%s/submit' % api_url, json=launch_data)
print(res.status_code)
print(res.content)
print(res.status_code)

