#!/usr/bin/env python

# --------------------------------
#  Author: Artem "RaTRaZe" Kuzmin
#  Mail: <ratraze@gmail.com>
#  License: GPLv3                  
# --------------------------------

import json
import optparse
from os import popen

IPMIPATH = 'ipmitool'
CRED = {
        'HOST': {'User': 'zabbix',
                 'Password': 'zabbix2014',
                 'Interface': 'open',
                 'Host': '172.25.144.254',
                 'Auth': 'MD5'}
       }

Host = CRED.keys()[0]
CONNECT = IPMIPATH + " -U " + CRED[Host]['User'] + " -P " + CRED[Host]['Password'] +\
                     " -H " + CRED[Host]['Host'] + " -I " + CRED[Host]['Interface'] + " -A " + CRED[Host]['Auth'] +\
                     " "

#CONNECT = "{0} -U {1} -P {2} -H {3} -I {4} -A {5}  ".format(IPMIPATH, CRED[Host]['User'],
#                                            CRED[Host]['Password'], CRED[Host]['Host'],
#                                            CRED[Host]['Interface'], CRED[Host]['Auth'])


def discovery(jlist):
    print '{"data":'
    print str(jlist).replace("'", "")
    print '}'


def sensors(path):
    with popen(CONNECT + path) as rawdata:
        jsonlist = []
        keys = ['{#SENSORID}']
        for line in rawdata:
            data = [line.split('|')[0].strip()]
            jsonlist.append(json.dumps(dict(zip(keys, data))))
    discovery(jsonlist)


def overall(metric, path):
    data = []
    with popen(CONNECT + ' ' + path) as rawdata:
        for line in rawdata:
            for item in line.split(':'):
                data.append(item.strip())
            if metric in data:
                return data[1]
            data = []


def getsensor(ID, path):
    with popen(CONNECT + ' ' + path) as rawdata:
        for line in rawdata:
            if ID in line:
		print line.split('|')[1].strip()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--host", action="store")
    parser.add_option("--fru", action="store_true")
    parser.add_option("--chassis", action="store_true")
    parser.add_option("--sel", action="store_true")
    parser.add_option("--getsensor", action="store_true")
    parser.add_option("--sensors", action="store_true")
    parser.add_option("--id", action="store")
    parser.add_option('--item', action='store')
    args, option = parser.parse_args()
    if args.host in CRED.keys():
        Host = args.host
        CONNECT = "{0} -U {1} -P {2} -H {3} -I {4} -A {5}  ".format(IPMIPATH, CRED[Host]['User'],
                                                                    CRED[Host]['Password'], CRED[Host]['Host'],
                                                                    CRED[Host]['Interface'], CRED[Host]['Auth'])
    if args.sensors:
        sensors("sensor")
    if args.fru:
        print overall(args.item, "fru print 0")
    if args.chassis:
        print overall(args.item, "chassis status")
    if args.sel:
        print overall(args.item, "sel")
    if args.getsensor:
        getsensor(args.id, "sensor")
