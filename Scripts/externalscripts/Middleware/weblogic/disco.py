#!/usr/bin/env python

import json
from os import popen
from sys import argv

WLST_PATH = "/products/weblogic/wlserver_10.3/common/bin/wlst.sh"
DIR_PATH = "/usr/lib/zabbix/"

def sender(hostname, key, value):
    zabbix = '10.45.129.32'
    popen("zabbix_sender -z {0} -s {1} -k '{2}' -o '{3}'".format(zabbix,hostname,key,value))

def discovery(script, keys):
     with popen("{0} {1}{2}".format(WLST_PATH, DIR_PATH, script)) as file:
	key = ["{#NAME}"]
	jsonlist = []
        start = 0
        for line in file:
	    data = []
            if "Start" in line:
                start = 1
	    if "Exiting" in line:
	        start = 0
            if start:
	        if len(line.split()) > 1:
		    data.append(line.split()[0])
		    jsonlist.append(json.dumps(dict(zip(key, data))))
		    sender("apps1", "wlst[{0}_{1}]".format(line.split()[0], keys), line.split()[1])
	out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out 


if "__main__" in __name__:
    if len(argv) != 3:
        raise ValueError("Usage: ./disco.py <script_name> <key_name> ")
    else:
        discovery(argv[1], argv[2])
