#!/usr/bin/env python

import paramiko
import sys
import argparse
from os import popen

CRED = {'10.43.112.4': {'IP':'10.43.112.4',
                        'username':'zabbix',
                        'hostname':'RSB-DSPMOS0DD1',
                        'password':'3tUjAPru'
                        },
        '10.43.112.5': {'IP':'10.43.112.5',
                        'username':'zabbix',
                        'hostname':'RSB-DSPMOS1DD1',
                        'password':'3tUjAPru'
                        },
       }

 
def sender(hostname, key, value):
    zabbix = '10.45.129.32'
    popen("zabbix_sender -z {0} -s {1} -k {2} -o '{3}'".format(zabbix,hostname,key,value))


def compression(metric):
    """
    Executes command on ssh console, and parse output data

    Args:
        metric(str): value, that required to return
    
    """
    stdin, stdout, stderr = ssh.exec_command("filesys show compression")
    for line in stdout.readlines():
        if "Currently" in line:
            line = line.split()[2:]
            if metric == "dedup":
                print line[4].replace("x","")
            if metric == "dedpct":
                print line[5].replace("(","").replace(")","")


def performance():
    stdin, stdout, stderr = ssh.exec_command("system show performance view legacy duration 5 min")
    out = stdout.readlines()[3].split("/")
    out = filter(lambda a: len(a)>0, out)
    sender(CRED[args.H]['hostname'], "netread", out[2].split()[3])
    sender(CRED[args.H]['hostname'], "netwrite", out[2].split()[4])
    sender(CRED[args.H]['hostname'], "cpuavg", out[11].split()[0].split('%')[0])
    sender(CRED[args.H]['hostname'], "cpupeak", out[11].split()[1].split('%')[0])
    sender(CRED[args.H]['hostname'], "streamread", out[6].split()[-1])
    sender(CRED[args.H]['hostname'], "streamwrite", out[7].split()[0])
    print "OK"


if "__main__" in __name__:
    parser = argparse.ArgumentParser(description='DataDomain Monitoring Info Gathering Script')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    parser.add_argument('-H', action="store")
    parser.add_argument('-dedup', action="store_true")
    parser.add_argument('-dedpct', action="store_true")
    parser.add_argument('-perf', action="store_true")
    args = parser.parse_args()
    if args.H:
        if args.H in CRED.keys():
            ssh.connect(CRED[args.H]['IP'], username=CRED[args.H]['username'], password=CRED[args.H]['password'])
    if args.dedup:
        compression("dedup")
    if args.dedpct:
        compression("dedpct")
    if args.perf:
        performance()
    ssh.close()
