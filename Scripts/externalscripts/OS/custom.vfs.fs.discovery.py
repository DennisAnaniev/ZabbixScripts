#! /usr/bin/env python
# Author: Artem "RaTRaZe" Kuzmin
# Version: 0.1

from os import remove
from subprocess import call

default_threshold = 10
custom = {
    '/': 5
}

call(["lsblk -l | grep / > /tmp/fsdisco.tmp"], shell=True)
with open("/tmp/fsdisco.tmp", "r") as tmp:
    first = 1
    print '{"data":[',
    for line in tmp:
        if first:
            first = 0
        else:
            print ",",
        print "{" + '"{#FSNAME}":' + '"' + line.split()[-1] + '",',
        if line.split()[-1] in custom:
            print '"{#THRESHOLD}":"' + str(custom[line.split()[-1]]) + '"' + "}",
        else:
            print '"{#THRESHOLD}":"' + str(default_threshold) + '"' + "}",
    print ']}',
try:
    remove("/tmp/fsdisco.tmp")
except OSError:
    pass
