#!/usr/bin/env python

import argparse
from os import popen
import json

WSADMINCLI = "/home/bell/wsadmin/wsadmin.sh"

CRED = {
       '172.22.144.19':{
                        'host':'172.22.144.19',
                        'port':'8879',
                        'hostname':'ISRWS',
                        'username':'rbs-ldap_was',
                        'password':'Cathfflv123 '
                       },
       '10.45.6.13':{
                     'host':'10.45.6.13',
                     'port':'8879',
                     'hostname':'TESTWS',
                     'username':'wasadmin',
                     'password':'Cathfflv '                                                                                                                         },
                                                                                                                                                                   
    }


def sender(hostname, key, value):
    zabbix = '10.45.129.32'
    popen("zabbix_sender -z {0} -s {1} -k {2} -o '{3}'".format(zabbix,hostname,key,value))


def checkconn(out):
    if not "Connected" in out:
        sender(CRED[args.host]['hostname'], "connection_status", "Failed")
        raise RuntimeError("Connection failed")
        return False
    else:
        sender(CRED[args.host]['hostname'], "connection_status", "Successful")
        return True

def getapps():
    key = ['{#APP}', '{#CLUSTER}', '{#SERVER}']
    jsonlist = []
    script = '/usr/lib/zabbix/externalscripts/websphere_scripts/getapps_test.py'
    out = popen(" {0} -f '{1}' ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0], item[1], item[2]]
            if 'WASX7026W:' in data:
                continue
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_{2}_status]".format(item[0], item[1], item[2]), item[3])
            jsonlist.append(json.dumps(dict(zip(key, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out.replace("\\", "")


def getinst():
    keys = ['{#INST}', '{#NODE}']
    jsonlist = []
    script = "/usr/lib/zabbix/externalscripts/websphere_scripts/get_instances.py"
    out = popen("{0} -f {1} ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0], item[1]]
            if 'WASX8011W' in data:
                continue
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_status]".format(item[0], item[1]), item[2])
            jsonlist.append(json.dumps(dict(zip(keys, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out

def check_cluster_status():
    out = popen("""{0} -c "AdminControl.getAttribute(AdminControl.completeObjectName('type=Cluster,*'),'state')" """.format(CONNECT)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        if 'WASX7026W' in out[0]:
            return out[1].replace("'", "")
        if "websphere.cluster" in out[0]:
            return out[0].replace("'", "")
        else:
            return "N/A"


def testconnection():
    key = ['{#SOURCE}']
    jsonlist = []
    script = '/usr/lib/zabbix/externalscripts/websphere_scripts/connections.py'
    out = popen(" {0} -f '{1}' ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            if 'WASX7' in item[0]:
                continue
            name = "_".join(item[:-1])
            name = name.replace('"', '')
            data = [name]
            sender(CRED[args.host]['hostname'], "was[{0}_slow_status]".format(name), item[-1])
            jsonlist.append(json.dumps(dict(zip(key, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        sender(CRED[args.host]['hostname'], "slow_connections", out)
#        print out.replace("\\", "")


def getheaps():
    keys = ['{#PROCESS}', '{#NODE}', '{#HEAPMAX}', '{#HEAPFREE}']
    jsonlist = []
    script = "/usr/lib/zabbix/externalscripts/websphere_scripts/heapsize.py"
    out = popen("{0} -f {1} ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0], item[1]]
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_heapmax]".format(item[0], item[1]), item[2])
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_heapfree]".format(item[0], item[1]), item[3])
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_prctfree]".format(item[0], item[1]), item[4])
            jsonlist.append(json.dumps(dict(zip(keys, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out


def getcpu():
    keys = ['{#PROCESS}', '{#NODE}', '{#CPU}']
    jsonlist = []
    script = "/usr/lib/zabbix/externalscripts/websphere_scripts/cpu.py"
    out = popen("{0} -f {1} ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0], item[1]]
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_CPU%]".format(item[0], item[1]), item[2])
            jsonlist.append(json.dumps(dict(zip(keys, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out


def getthreads():
    keys = ['{#PROCESS}', '{#NODE}', '{#ACTIVECURR}', '{#POOLCURR}', '{#POOLHIGH}', '{TIMECOUNT#}']
    jsonlist = []
    script = "/usr/lib/zabbix/externalscripts/websphere_scripts/threads.py"
    out = popen("{0} -f {1} ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
#        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0], item[1]]
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_activecurr]".format(item[0], item[1]), item[2])
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_poolcurr]".format(item[0], item[1]), item[3]) 
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_poolhigh]".format(item[0], item[1]), item[4])
            sender(CRED[args.host]['hostname'], "was[{0}_on_{1}_avgtime]".format(item[0], item[1]), item[5])
            jsonlist.append(json.dumps(dict(zip(keys, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out


def getsessions():
    keys = ['{#NAME}','{#PROCESS}', '{#NODE}', '{#SESSIONS}']
    jsonlist = []
    script = "/usr/lib/zabbix/externalscripts/websphere_scripts/sessions.py"
    out = popen("{0} -f {1} ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0], item[1], item[2]]
            sender(CRED[args.host]['hostname'], "was[{0}_{1}_on_{2}_sessions]".format(item[0], item[1], item[2]), item[3])
            jsonlist.append(json.dumps(dict(zip(keys, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out


def getlistenports():
    keys = ['{#NAME}','{#STATUS}']
    jsonlist = []
    script = "/usr/lib/zabbix/externalscripts/websphere_scripts/listenports.py"
    out = popen("{0} -f {1} ".format(CONNECT, script)).read()
    if checkconn(out):
        out = out.split('\n')[2:]
        out.remove("")
        for item in out:
            item = item.split()
            data = [item[0]]
            sender(CRED[args.host]['hostname'], "was[{0}_started]".format(item[0]), item[1])
            jsonlist.append(json.dumps(dict(zip(keys, data))))
        out = '{{"data":{0} }}'.format(str(jsonlist).replace("'", ""))
        print out


if '__main__' in __name__:
    parser = argparse.ArgumentParser(description='WebSphere Application Status')
    parser.add_argument('-host', action="store")
    parser.add_argument('-getapps', action="store_true")
    parser.add_argument('-appstatus', action="store")
    parser.add_argument('-getinst', action='store_true')
    parser.add_argument('-cluster', action='store_true')
    parser.add_argument('-testconnect', action='store_true')
    parser.add_argument('-getheaps', action='store_true')
    parser.add_argument('-getcpu', action='store_true')
    parser.add_argument('-getthreads', action='store_true')
    parser.add_argument('-getsessions', action='store_true')
    parser.add_argument('-getlistenports', action='store_true')
    args = parser.parse_args()
    if args.host:
        host = CRED[args.host]
        CONNECT = "{0} -lang jython -host {1} -port {2} -user {3} -password {4}".format(WSADMINCLI, CRED[args.host]['host'], CRED[args.host]['port'], CRED[args.host]['username'], CRED[args.host]['password'])
    if args.getapps:
        getapps()
    if args.appstatus:
        check_app_status(args.appstatus)
    if args.getinst:
        getinst()
    if args.cluster:
        print check_cluster_status()
    if args.testconnect:
        testconnection()
    if args.getheaps:
        getheaps()
    if args.getcpu:
        getcpu()
    if args.getthreads:
        getthreads()
    if args.getsessions:
        getsessions()
    if args.getlistenports:
        getlistenports()
