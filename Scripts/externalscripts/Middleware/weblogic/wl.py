#!/usr/bin/env python

import json
from os import popen

WLST_PATH = "/products/weblogic/wlserver_10.3/common/bin/wlst.sh"
DIR_PATH = "/usr/lib/zabbix/"
scripts = ["heaps.py", "JDBC.py", "threads.py"]

def sender(hostname, key, value):
    zabbix = '10.45.129.32'
    popen("zabbix_sender -z {0} -s {1} -k {2} -o '{3}'".format(zabbix,hostname,key,value))

for script in scripts:
    with popen(WLST_PATH + " " + DIR_PATH + script) as file:
        start = 0
        for line in file:
	    if "Destination unreachable" in line:
	        print "Connection Failed"
		break	
            if "Start" in line:
                start = 1
            if start:
                if len(line.split()) > 1:
	            sender("apps1", line.split()[0], line.split()[1])
        	#    print line 
print "OK"
