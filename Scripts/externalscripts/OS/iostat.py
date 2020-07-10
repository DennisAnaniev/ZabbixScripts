#!/usr/bin/env python
# Version: 0.5
# Author: Artem "RaTRaZe" Kuzmin
from subprocess import call
from sys import argv
from os import remove


def getpart():
    sdalist = []
    disklist = ["sd", "hd", "hdisk"]
    call(["lsblk -l > /tmp/iostat.tmp"], shell=True)
    with open("/tmp/iostat.tmp", "r") as file:
        for line in file:
            for item in disklist:
                if item in line.split()[0]:
                    sdalist.append(line.split()[0])
            if len(argv) == 1:
                break
            if line.split()[-1] == argv[1]:
                if line.split()[-2] == "lvm":
                    return sdalist[-1]
                    break
                else:
                    return line.split()[0]
        return "ZBX_NOTSUPPORTED"

if getpart() != "ZBX_NOTSUPPORTED":
    try:
            call(["iostat -p ALL -d 1 3 | grep " + getpart() +
                  "|tail -n 1 | awk '{print$2}'"], shell=True)
    except TypeError:
        print "ZBX_NOTSUPPORTED"
try:
    remove("/tmp/iostat.tmp")
except OSError:
    pass
