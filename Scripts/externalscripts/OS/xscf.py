#!/usr/bin/env python

import paramiko
import re
import json
import optparse
from os import mkdir

TMP_DIR = '/tmp/sun/'

CRED = {'10.45.36.62': {'IP': '10.45.36.62',
                        'Username': 'zabbix',
                        'Password': 'zabbix123',
                        'File': '10.45.36.62'
                        }
        }

Host = CRED.keys()[0]


def discovery(jsonlist):
    jsonlist = set(jsonlist) #unique
    jsonlist = list(jsonlist)
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'


def connect(ip, user, pwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username = user, password = pwd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read()

def writetofile(data):
    try:
        mkdir(TMP_DIR)
    except OSError:
        pass
    with open(TMP_DIR+CRED[Host]['File'], 'w+') as rawdata:
        rawdata.write(data)
    print 'OK'


def mem(host, board, item):
    jsonlist = []
    keys = ['{#BOARD}', '{#UNIT}']
    boardtr = 0
    with open(TMP_DIR+CRED[Host]['File'], 'r+') as info:
        for line in info:
            if item == 'discovery': 
                if re.search('MEMB#', str(line)):
                    board = line.strip().split(" ")[0]
                if re.search('MEM#', line):
                    unit = line.strip().split(" ")[0]
                    data = [board, unit]    
                    jsonlist.append(json.dumps(dict(zip(keys, data))))
            else:
                if board in line:
                    boardtr = 1
                if item in line and boardtr:
                    status = line.strip().split(' ')[1]
                    status = status.split(':')[1]
                    status = status.replace(';', '')
                    return status
    if len(jsonlist):
        discovery(jsonlist)


def cpu(host, item):
    jsonlist = []
    keys = ['{#UNIT}']
    with open(TMP_DIR + CRED[Host]['File'], 'r') as info:
        for line in info:
            if re.search('CPUM#', str(line)):
                unit = line.strip().split(' ')[0]
                if item == 'discovery': 
                    data = [unit] 
                    jsonlist.append(json.dumps(dict(zip(keys, data))))
                else:
                    if item in line:
                        status = line.strip().split(' ')[1]
                        status = status.split(':')[1]
                        status = status.replace(';', '')
                        return status
    if len(jsonlist):
        discovery(jsonlist)


def other(host, item):
    jsonlist = []
    keys = ['{#UNIT}']
    units = ['MBU', 'DDC', 'IOU', 'OPNL', 'PSU', 'FAN_']
    with open(TMP_DIR+CRED[Host]['File'], 'r+') as info:
        for line in info:
            if item == 'discovery':
                for u in units:
                    if re.search(u, str(line)):
                        unit = line.strip().split(' ')[0]
                        data = [unit]
                        jsonlist.append(json.dumps(dict(zip(keys, data))))
            else:
                if item in line:
                    status = line.strip().split(' ')[1]
                    status = status.split(':')[1]
                    status = status.replace(';', '')
                    return status
    if len(jsonlist):
        discovery(jsonlist)


if '__main__' in __name__:
    parser = optparse.OptionParser()
    parser.add_option("--host", action="store")
    parser.add_option("--gather", action="store_true")
    parser.add_option("--environment", action="store_true")
    parser.add_option("--cpu", action="store_true")
    parser.add_option("--mem", action="store_true")
    parser.add_option("--oth", action="store_true")
    parser.add_option("--board", action='store')
    parser.add_option('--item', action='store')
    args, option = parser.parse_args()
    if args.host in CRED.keys():
        Host = args.host
    if args.gather:
        conn = connect(CRED[Host]['IP'], CRED[Host]['Username'], CRED[Host]['Password'], "showhardconf")
        writetofile(conn)
    if args.environment:
        conn = connect(CRED[Host]['IP'], CRED[Host]['Username'], CRED[Host]['Password'], "showenvironment")
        print conn.split(':')[1].replace('C', '')
        #too lazy to write another func 4 it.
    if args.cpu:
        print cpu(Host, args.item)
    if args.mem:
        print mem(Host, args.board, args.item)
    if args.oth:
        print other(Host, args.item) 
