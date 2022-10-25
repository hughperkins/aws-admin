import sys
import os
from os import path
from os.path import join
import os.path
from ruamel import yaml


def check_changes(filepath: str, data) -> str:
    """
    compares json dump of data with contents of file at filepath
    returns any differences as a structured string, and updates
    file at filepath
    """
    newString = yaml.safe_dump(data, default_flow_style = False )

    oldString = ''
    if os.path.isfile(filepath):
        f = open(filepath,'r')
        oldString = f.read()
        f.close()

    changesString = ''
    if(newString != oldString):
        changesString += 'changed:\n'
        changesString += 'old:\n'
        changesString += oldString + '\n'
        changesString += 'new:\n'
        changesString += newString + '\n'
        with open('%s~' % filepath, 'w') as f:
            f.write( newString )
        os.rename('%s~' % filepath, filepath)
    return changesString
