#!/usr/bin/env python

# --------------------------------
#  Author: Artem "RaTRaZe" Kuzmin
#  Mail: <ratraze@gmail.com>
#  License: GPLv3
# --------------------------------

from os import popen, mkdir, remove, rename
import json
from re import match
import optparse

DSCLI = '/opt/ibm/dscli/dscli'
TMP_DIR = '/tmp/ibmds/'
CRED = {
        'IBM.2107-75CLD40': {'User': 'zabbix',
        'Password': 'm0nitorADM!',
        'hmc1': '10.45.98.136',
        'hmc2': '10.45.98.136',
        'scriptfile': '/usr/local/share/zabbix/externalscripts/ibmds_scripts/IBM.2107-75CLD40.txt',
        'dir': 'IBM.2107-75CLD40',
        'devid': 'IBM.2107-75CLD41'
        }
        }
        


Host = CRED.keys()[0]
CONNECT = ''

keys = ['{#NAME}']


def discovery(jsonlist):
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'


def gather():
    """
    Gather info from console, and put it in file, inside TMP_DIR.
    
    """
    try:
        mkdir(TMP_DIR)
    except OSError:
        pass
    with popen(CONNECT) as rawdata:
        with open(TMP_DIR + CRED[Host]['dir'] + '.tmp', 'w+') as textdata:
            textdata.write(rawdata.read())
    try:
        remove(TMP_DIR + CRED[Host]['dir'])  
    except OSError:
        pass
    rename(TMP_DIR + CRED[Host]['dir'] + '.tmp', TMP_DIR + CRED[Host]['dir'])
    print 'OK'


def raids(metric, name=''):
    with open(TMP_DIR + CRED[Host]['dir'], 'r') as rawdata:
        jsonlist = []
        for line in rawdata:
            line = line.rstrip()
            line = line.split(':')
            if metric == 'discovery':
                if "RAID" in line[0]:
                    jsonlist.append(json.dumps(dict(zip(keys, line))))
            else:
                header = ['NAME', 'ID', 'stgtype', "rankgrp", 'status', 'availstor',
                          '%alloc', 'available', 'reserved', 'numvols']
                if match("\['" + name + "'", str(line)):
                    print line[header.index(metric)]
    if metric == 'discovery':
        discovery(jsonlist)


def arrays(metric, name=''):
    with open(TMP_DIR + CRED[Host]['dir'], 'r') as rawdata:
        jsonlist = []
        for line in rawdata:
            line = line.rstrip()
            line = line.split(':')
            if metric == 'discovery':
                if 'A' in line[0][0]:
                    jsonlist.append(json.dumps(dict(zip(keys, line))))
            else:
                header = ['Array', 'State', 'Data', 'RAIDtype', 'arsite', 'Rank', 'DA Pair', 'DDMcap']
                if match("\['" + name + "'", str(line)):
                    print line[header.index(metric)]
    if metric == 'discovery':
        discovery(jsonlist)


def ranks(metric, name=''):
    with open(TMP_DIR + CRED[Host]['dir'], 'r') as rawdata:
        jsonlist = []
        for line in rawdata:
            line = line.rstrip()
            line = line.split(':')
            if metric == 'discovery':
                if 'R' in line[0][0] and len(line) < 10:
                    jsonlist.append(json.dumps(dict(zip(keys, line))))
            else:
                header = ['ID', 'Group', 'State', 'datastate', 'Array', 'RAIDtype', 'extpoolID', 'stgtype']
                if match("\['" + name + "'", str(line)):
                    print line[header.index(metric)]
    if metric == 'discovery':
        discovery(jsonlist)


def interfaces(metric, name=''):
    with open(TMP_DIR + CRED[Host]['dir'], 'r') as rawdata:
        jsonlist = []
        for line in rawdata:
            line = line.rstrip()
            line = line.split(':')
            if metric == 'discovery':
                if 'I0' in line[0][0:2]:
                    jsonlist.append(json.dumps(dict(zip(keys, line))))
            else:
                header = ['ID', 'WWPN', 'State', 'Type', 'topo', 'portgrp']
                if match("\['" + name + "'", str(line)):
                    print line[header.index(metric)]
    if metric == 'discovery':
        discovery(jsonlist)


def ddm(metric, name=''):
    with open(TMP_DIR + CRED[Host]['dir'], 'r') as rawdata:
        jsonlist = []
        for line in rawdata:
            line = line.rstrip()
            line = line.split(':')
            if metric == 'discovery':
                if 'IBM' in line[0] and len(line) == 6:
                    jsonlist.append(json.dumps(dict(zip(keys, line))))
            else:
                header = ['ID', 'DA Pair', 'dkcap (10^9B)', 'dkuse', 'arsite', 'State']
                if match("\['" + name + "'", str(line)):
                    print line[header.index(metric)]
    if metric == 'discovery':
        discovery(jsonlist)


def envir(metric, name=''):
    with open(TMP_DIR + CRED[Host]['dir'], 'r') as rawdata:
        for line in rawdata:
            line = line.rstrip()
            line = line.split(':')
            if metric == 'Testmode':
                if 'ER Test Mode' in line[0]:
                    print line[0].split(' ')[-1]
            if metric == 'Powerusage':
                if 'ER Power Usage' in line[0]:
                    print line[0].split(' ')[-1] 
            if metric  == 'Inlettemp':
                if 'ER Inlet Temp' in line[0]:
                    print line[0].split(' ')[-1]
            if metric == 'iops':
                if 'ER I/O Usage' in line[0]:
                    print line[0].split(' ')[-1]
            if metric == 'datausage':
                if 'ER Data Usage' in line[0]:
                    print line[0].split(' ')[-1]
            if metric == 'recorded':
                if 'ER Recorded' in line[0]:
                    line = " ".join(line).split(' ')[7:9]
                    print ':'.join(line)
	    
 
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--host", action="store")
    parser.add_option("--raid", action="store_true")
    parser.add_option("--array", action="store_true")
    parser.add_option("--rank", action="store_true")
    parser.add_option("--interface", action="store_true")
    parser.add_option("--ddm", action="store_true")
    parser.add_option("--envir", action="store_true")
    parser.add_option("--gather", action="store_true")
    parser.add_option("--metric", action="store")
    parser.add_option("--name", action="store")
    args, option = parser.parse_args()
    try:
        if args.host in CRED.keys():
            Host = args.host
            CONNECT = "{0} -hmc1 {1} -hmc2 {2} -user {3} -passwd {4} -script {5}".format(DSCLI,
                                                                                         CRED[Host]['hmc1'],
                                                                                         CRED[Host]['hmc2'],
                                                                                         CRED[Host]['User'],
                                                                                         CRED[Host]['Password'],
                                                                                         CRED[Host]['scriptfile']
                                                                                        )
        if args.raid:
            raids(args.metric, args.name)
        if args.array:
            arrays(args.metric, args.name)
        if args.rank:
            ranks(args.metric, args.name)
        if args.interface:
            interfaces(args.metric, args.name)
        if args.ddm:
            ddm(args.metric, args.name)
        if args.envir:
            envir(args.metric)
        if args.gather:
            gather()
    except ValueError, e:
        print e
