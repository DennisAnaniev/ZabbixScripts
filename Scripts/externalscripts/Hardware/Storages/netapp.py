#!/usr/bin/env python
import paramiko
from sys import argv

cred = {
        '10.46.84.135': {'username': 'zabbix',
                         'password': 'P@ssw0rd'
                         },
        '10.46.84.132': {'username': 'zabbix',
                         'password': 'P@ssw0rd'
                         }, 
        '10.46.84.133': {'username': 'zabbix',
                         'password': 'P@ssw0rd'
                         },
        '10.46.84.134': {'username': 'zabbix',
                         'password': 'P@ssw0rd'
                         },
	}


def cifs(host, metric):
    """
    Prints output from 'show cifs' command
    
    Args:
        host(str): host, where script must connect, and get info
        metric(str): field, that contains requested value  

    """
    stdin, stdout, stderr = ssh.exec_command("stats show cifs")
    for line in stdout.readlines():
        if metric in line:
            if metric == "latency":
                line = line.strip().split(':')[-1]
                print line.replace('ms', '')
            if metric == 'read': 
                line = line.strip().split(':')[-1]
                print line.replace('/s','')
            if metric == 'write': 
                line = line.strip().split(':')[-1]
                print line.replace('/s','')


def cifspeak(host):
    stdin, stdout, stderr = ssh.exec_command("stats show cifs:cifs:cifs_latency")
    out = stdout.readline()
    out = out.strip().split(':')[-1]
    out = out.replace('ms', '')
    if float(out) >= 5:
        print 0
    else:
        print 1


def fcp(host):
    stdin, stdout, stderr = ssh.exec_command("stats show fcp:fcp:fcp_latency")
    out = stdout.readlines()
    item = out[0]
    item = item.strip().split(':')[-1]
    print item.replace('ms', '')


def ifnet(host,intf,item):
    stdin, stdout, stderr = ssh.exec_command("stats show ifnet:" + intf + ":" + item)
    out = stdout.readlines()
    item = out[0]
    item = item.strip().split(':')[-1]
    print item.replace('b/s', '').replace('/s', '')

if __name__ in '__main__':
    if argv[1] in cred.keys():
        host = argv[1]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=cred[host]['username'], password=cred[host]['password'])
        if 'peak' in argv[2]:
            cifspeak(argv[1])
        if 'cifs' in argv[2]:
            cifs(argv[1], argv[3])
        if 'fcp' in argv[2]:
            fcp(argv[1])
        if 'ifnet' in argv[2]:
            ifnet(argv[1], argv[3], argv[4])
        ssh.close()
    else:
        print "Host is not in dictionary"
