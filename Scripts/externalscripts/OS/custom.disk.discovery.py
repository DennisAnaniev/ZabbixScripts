#!/usr/bin/env python
# Version: 0.6
# Author: Artem "RaTRaZe" Kuzmin
from subprocess import call
from os import remove
from sys import argv

ZABBIX_HOST = 'RSB-ISPMOSZBX01'
AGENT_CONF = "/etc/zabbix/zabbix_agentd.conf"


def discovery():
    first = 1
    call(["iostat -d -p ALL | awk '{print$1}' | grep ram -A 99 | grep -v '^$' > /tmp/disk.discovery.tmp"],
         shell=True)
    with open("/tmp/disk.discovery.tmp", "r") as tmp:
        print '{"data":[',
        for line in tmp:
            if first:
                first = 0
            else:
                print ",",
            print "{" + '"{#DISK}":' + '"' + line.strip() + '"' + "}",
        print ']}',


def iostat():
    call(["iostat -d -p ALL 1 5 | awk '{print$1,$2}' > /tmp/iostat.tmp"], shell=True)
    data = reversed(list(open("/tmp/iostat.tmp", 'r')))
    sender = open("/tmp/zabbix.sender.tmp", 'wt')
    for line in data:
        if "Device" in line:
            break
        try:
                disk, value = line.split()[0], line.split()[1]
                disk = ZABBIX_HOST + " disk.iops[" + disk + "] " + value + "\n"
                sender.write(disk)
        except IndexError:
            pass
    sender.close()


def send():
    call(["zabbix_sender -c {0} -i /tmp/zabbix.sender.tmp 1>/dev/null".format(AGENT_CONF)], shell=True)

if __name__ == "__main__":
    if len(argv) == 1:
        iostat()
        send()
    try:
        if argv[1] == "discovery":
            discovery()
    except IndexError:
        pass
#    try:
#        remove("/tmp/disk.discovery.tmp")
#        remove("/tmp/iostat.tmp")
#        remove("/tmp/zabbix.sender.tmp")
#    except OSError:
#        pass
