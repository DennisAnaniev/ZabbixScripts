#!/usr/bin/env python

# --------------------------------
# Author: Artem "RaTRaZe" Kuzmin
# Mail: <ratrage@gmail.com>
#  License: GPLv3                  
# --------------------------------
import optparse
import json
from os import popen, mkdir, rename, remove

NAVICLI = '/opt/Navisphere/bin/naviseccli'
CRED =  {
        "SM22-CERT-1142-SPA": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.101.160',
                       'Dir': 'SM22-CERT-1142-SPA',
                       },
        "SM22-PROD-0045": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '172.22.248.20',
                       'Dir': 'SM22-PROD-0045',
                       },
        "SM22-PROD-T1-1439": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.101.152',
                       'Dir': 'SM22-PROD-T1-1439',
                       },
        "SM22-PROD-T2-0371": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.101.154',
                       'Dir': 'SM22-PROD-T2-0371',
                       },
    "BR7-PROD-0047": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.109.177',
                       'Dir': 'BR7-PROD-0047',
                       },
        "BR7-PROD-T1-1442": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.109.152',
                       'Dir': 'BR7-PROD-T1',
                       },
        "BR7-PROD-T2-0369": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.109.154',
                       'Dir': 'BR7-PROD-T2-0369',
                       },
        "SM22-PROD-T2-0966": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.101.195',
                       'Dir': 'SM22-PROD-T2-0966',
                       },
    "SM22-PROD-T2-0443": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.101.156',
                       'Dir': 'SM22-PROD-T2-0443',
                       },
    
    
      "SM22-PROD-T2-0964": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.101.193',
                       'Dir': 'SM22-PROD-T2-0964',
                       },
      "BR7-PROD-T2-0965": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.109.208',
                       'Dir': 'BR7-PROD-T2-0965',
                       },
      
    "BR7-PROD-T2-0963": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.109.206',
                       'Dir': 'BR7-PROD-T2-0963',
                       },
            
       "BR7-PROD-T2-0372": {'User': 'monitor',
                       'Password': '4Mon!t0r',
                       'Host': '10.45.109.156',
                       'Dir': 'BR7-PROD-T2-0372',
                       },
}
TMP_DIR = '/tmp/emc/'


lun_items = ["RAID Type", "State", "LUN Capacity(Megabytes)"]
portstate_items = ['SP Name', 'SP Port ID', 'Link Status', 'Port Status', 'Speed Value']
storagepool_items = ['Pool Name', 'State', 'Status', 'Consumed Capacity (GBs)', 'Available Capacity (GBs)',
                     'Percent Full', 'Total Subscribed Capacity (GBs)']
cache_items = ['SP Read Cache State', 'SP Write Cache State', 'Dirty Cache Pages (MB)', 'SPA Read Cache State',
               'SPA Write Cache State', 'SPB Read Cache State', 'SPB Write Cache State']
fastcache_items = ['Percentage Dirty SPA', 'Percentage Dirty SPB']
agent_items = ['Agent Rev', 'Model', 'Model Type', 'Serial No']
spbusy_items = ['Prct Busy', 'Prct Idle']
power_temp_items = ['Name', 'Power Status', 'Power Present', 'Power Rolling Average', 'Temp Status', 'Temp Present',
                    'Temp Rolling Average']
disk_items = ['Enclosure', 'State']


def datagather():
    """
    Function open a connect for each key in 'request_list',
    write output to a file with .tmp in the end of a name,
    trying to remove old file, and rename new one without .tmp

    """
    request_list = {
        'agent': 'getagent',
        'spbusy': 'getcontrol',
        'cache': 'cache -sp -info',
        'fastcache': 'cache -fast -info',
        'storagepool': 'storagepool -list -availableCap -consumedCap -subscribedCap -prcntFull -state -rtype -status',
        'luns': 'getlun -name -state',
        'faults': 'faults -list',
        'disks': 'getdisk -state',
        'env': 'environment -list -enclosure',
        'ports': 'getall -hba'
    }
    try:
        mkdir(TMP_DIR)
    except OSError:
        pass
    for request in request_list.keys():
        with popen(CONNECT + request_list[request]) as rawdata:
            with open(TMP_DIR + request + ".tmp", 'w+') as textdata:
                textdata.write(rawdata.read())
                try:
                    remove(TMP_DIR + request)
                except OSError:
                    pass
                rename(TMP_DIR + request + ".tmp", TMP_DIR + request)
    return 'OK'


def getinfo(path, items, value):
    """
    Function read from file, that was created by datagather() in 'TMP_DIR', splits data to dictionary
    and return value for requested key
    
    Args:
        path(str): path to file
        items(list): global list of parameters, 'cache_items' for example
        value(str): name of the key, that value is required.

    """
    with open(path, 'r') as parseit:
        data = []
        for line in parseit:
            for item in items:
                if item in line:
                    line = line.replace(" ", "")
                    line = line.rstrip()
                    data.append(line.split(':')[1])
                if len(data) == len(items):
                    print data[items.index(value)]
                    data = []


def check_storagepool(items, name, value):
    """
    Function prints requested value from file

    Args:
        items(list): global list of parameters, 'cache_items' for example
        name(str): name of requested storage pool
        value(str): requested parameter. 
        If equals 'discovery' - returns json formatted list of storage pools

    """
    jsonlist = []
    keys = ['{#NAME}']
    with open(TMP_DIR + 'storagepool', 'r') as parseit:
        data = []
        for line in parseit:
            for item in items:
                if item in line:
                    line = line.replace(" ", "")
                    line = line.rstrip()
                    data.append(line.split(':')[1])
            if len(data) == len(items):
                if value == 'discovery':
                    jsonlist.append(json.dumps(dict(zip(keys, data))))
                else:
                    if name in data:
                        print data[items.index(value)]
                data = []
    if len(jsonlist):
        discovery(jsonlist)


def check_lun(items, name, value):
    jsonlist = []
    keys = ['{#NAME}']
    with open(TMP_DIR + 'luns', 'r') as rawdata:
        luns = []
        for line in rawdata:
            if "Name" in line: 
                luns.append("".join(line.split()[1:]))
            for item in items:
                if item in line:
                    line = line.replace(" ", "")
                    line = line.rstrip()
                    luns.append(line.split(':')[1])
            if len(luns) == len(items) + 1:
                if value == 'discovery':
                    jsonlist.append(json.dumps(dict(zip(keys, luns))))
                else:
                    if name in luns:
                        print luns[items.index(value)]
                luns = []
    if len(jsonlist):
        discovery(jsonlist)


def check_faults():
    """
    Function prints data from 'faults' file, inside 'TMP_DIR' directory

    """
    with open(TMP_DIR + 'faults', 'r') as parseit:
        print parseit.read()


def check_disk(items, name, value):
    jsonlist = []
    disks = []
    keys = ['{#NAME}']
    with open(TMP_DIR + "disks", 'r') as parseit:
        for line in parseit:
            if 'Enclosure' in line:
                line = line.rstrip()
                disks.append(line)
            if 'State' in line:
                line = line.rstrip()
                line = line.replace(" ", "")
                disks.append((line.split(':')[1]))
            if len(disks) == 2:
                if value == 'discovery':
                    jsonlist.append(json.dumps(dict(zip(keys, disks))))
                else:
                    if name in disks:
                        print disks[items.index(value)]
                disks = []
    if len(jsonlist):
        discovery(jsonlist)


def check_power_temp(items, name, value):
    jsonlist = []
    data = []
    keys = ['{#NAME}']
    with open(TMP_DIR + 'env', 'r') as parseit:
        for line in parseit:
            if 'Bus' in line:
                line = line.rstrip()
                data.append(line)
            if 'Status' in line:
                line = line.rstrip()
                line = line.replace(" ", "")
                data.append((line.split(':')[1]))
            if 'Present' in line:
                line = line.rstrip()
                line = line.replace(" ", "")
                data.append((line.split(':')[1]))
            if 'Rolling' in line:
                line = line.rstrip()
                line = line.replace(" ", "")
                data.append((line.split(':')[1]))
            if len(data) == len(items):
                if value == 'discovery':
                    jsonlist.append(json.dumps(dict(zip(keys, data))))
                else:
                    if name in data:
                        print data[items.index(value)]
                data = []
    if len(jsonlist):
        discovery(jsonlist)


def check_portstate(items, name, value):
    data = []
    keys = ['{#NAME}']
    spport = 0
    jsonlist = []
    with open(TMP_DIR + 'ports', 'r') as parseit:
        for line in parseit:
            if 'SPPORT' in line:
                spport = 1
            for item in items:
                if item in line:
                    line = line.replace(" ", "")
                    line = line.rstrip()
                    if spport:
                        data.append(line.split(':')[1])
                if len(data) == len(items):
                    spname = " ".join(data[0:2])
                    data.pop(0)
                    data.pop(0)
                    data.insert(0, spname)
                    if value == 'discovery':
                        jsonlist.append(json.dumps(dict(zip(keys, data))))
                    else:
                        if name in data:
                            print data[items.index(value) - 1]
                    data = []
    if len(jsonlist):
        discovery(jsonlist)


def discovery(jsonlist):
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--gather", action="store_true")
    parser.add_option("--host", action="store")
    parser.add_option("--agent", action="store_true")
    parser.add_option("--cache", action="store_true")
    parser.add_option("--fastcache", action="store_true")
    parser.add_option("--storagepool", action="store_true")
    parser.add_option("--spbusy", action="store_true")
    parser.add_option("--faults", action="store_true")
    parser.add_option("--powertemp", action="store_true")
    parser.add_option("--lun", action="store_true")
    parser.add_option("--disk", action="store_true")
    parser.add_option("--ports", action="store_true")
    parser.add_option('--name', action='store')
    parser.add_option('--item', action='store')
    args, option = parser.parse_args()
    try:
        if args.host:
            CONNECT = "{0} -User {1} -Password {2} -Scope 0 -h {3}  ".format(NAVICLI ,CRED[args.host]['User'],
                                                                                      CRED[args.host]['Password'],
                                                                                      CRED[args.host]['Host'])
            TMP_DIR += CRED[args.host]['Dir'] + "/"
        else:
            print "To find help: ./emc_clariion.py -h"
        if args.gather:
            print datagather()
        if args.agent:
            getinfo(TMP_DIR + 'agent', agent_items, args.item)
        if args.cache:
            getinfo(TMP_DIR + 'cache', cache_items, args.item)
        if args.fastcache:
            getinfo(TMP_DIR + 'fastcache', fastcache_items, args.item)
        if args.spbusy:
            getinfo(TMP_DIR + 'spbusy', spbusy_items, args.item)
        if args.storagepool:
            check_storagepool(storagepool_items, args.name, args.item)
        if args.lun:
            check_lun(lun_items, args.name, args.item)
        if args.ports:
            check_portstate(portstate_items, args.name, args.item)
        if args.faults:
            check_faults()
        if args.powertemp:
            check_power_temp(power_temp_items, args.name, args.item)
        if args.disk:
            check_disk(disk_items, args.name, args.item)
    except ValueError, e:
        print e
