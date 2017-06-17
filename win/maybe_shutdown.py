import os
from os import path
import subprocess
import sys


flag_file = 'c:\\dontshutdown.flag'

if path.isfile(flag_file):
    os.unlink(flag_file)
    print('removed %s. not shutting down' % flag_file)
    sys.exit(0)

print('shutting down...')
print(subprocess.check_output([
    'shutdown', '/f', '/t', '0', '/s'
]).decode('utf-8'))
