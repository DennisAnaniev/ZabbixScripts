#!/usr/bin/env python
# Version: 0.2
# Author: Artem "RaTRaZe" Kuzmin
from subprocess import call
from os import remove
from sys import argv 

DSN = 'host'
USER = 'zabbix'
PASSWORD = 'zabbix'

CRED = {
        'host':{
                'user':'zabbix',
                'password':'Cegthgfhjkm14',
                'DSN':'host'
                }
        }

if len(argv) != 2:
    raise ArgumentError('Not enough arguments')
else:
    host = argv[1]


call(["echo select DBName from monOpenDatabases | isql -v {0} {1} {2} -w > /tmp/sybase.discovery.tmp".format(CRED[host]['DSN'],
                                                                                                          CRED[host]['user'],
                                                                                                          CRED[host]['password'])],
                                                                                                          shell=True)
first = 1
with open("/tmp/sybase.discovery.tmp", "r") as file:
    db = [line.split("<")[0] for line in file if "</font>" in line]

#db.remove("")
print '{"data":[',
for item in db:
    if first:
        print "\t"
        first = 0
    else:
        print "\t,"

    print "\t{"
    print "\t\t"+'"{#DBNAME}":'+'"'+item.strip()+'"'+"\n"
    print "\t}"
print '\t]\n}'
