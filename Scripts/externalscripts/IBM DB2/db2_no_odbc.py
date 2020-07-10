#!/usr/bin/env python
# Version: 0.2
# Author: Artem "RaTRaZe" Kuzmin
# Author: Maksim Zinal, IBM EE/A

from subprocess import Popen, PIPE, STDOUT
import optparse
import json

DB2CLIPATH='/opt/ibm/db2/V10.5/bin/db2'

CRED = {
        'DEMO1':{'User':'db2inst1',
               'Password':'Gfhjkm1'
               },
        'DWH':{'User':'rbs-ldapzabbix',
               'Password':'uWR.vT2e5B6L1=k4'
               },
        'MART':{'User':'rbs-ldapzabbix',
               'Password':'uWR.vT2e5B6L1=k4'
               },
        'CMD':{'User':'zabbix',
               'Password':'uWR.vT2e5B6L1=k4'
               },
        'DATAHUB':{'User':'rbs-ldapzabbix',
               'Password':'uWR.vT2e5B6L1=k4'
               },
        'DHUB_F':{'User':'rbs-ldapzabbix',
               'Password':'uWR.vT2e5B6L1=k4'
               },
        }


def connect(DSN):
    """
    Function formats connect string and opens connection to db

    Args:
        DSN(str):
           Specified by optparse argument, must be equal to entry in db2 catalog
    """
    if DSN in CRED.keys():
        CONNECT = "{0} connect to {1} user {2} using {3}".format(DB2CLIPATH, DSN, CRED[DSN]['User'], CRED[DSN]['Password'])
        Popen(CONNECT, shell=True, close_fds=True, stdout=PIPE, stderr=STDOUT).stdout.read()
    else:
        print "DSN in not found. It must be specified in CRED dictionary"

def db2query(CMD):
    """
    Function executes a query over DB2 CLP and returns the result as a list of strings

    Args:
        TEXT(CMD):
           A query text to be executed
    """
    return Popen(DB2CLIPATH + """ " """ +  CMD + """ " """, shell=True, close_fds=True, stdout=PIPE).stdout.read().splitlines()


def discovery():
    """
    Function discovery all tablespaces in db2
    """
    keys = ["{#PARTNUM}", "{#TBSPNAME}"]
    jsonlist = []
    CMD = "select DBPARTITIONNUM, tbsp_name from table(MON_GET_TABLESPACE(null, -2)) order by DBPARTITIONNUM, tbsp_name"
    out = db2query(CMD)
    out = out[3:-3]
    for line in out:
        line = line.strip().split()
        jsonlist.append(json.dumps(dict(zip(keys, line))))
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'


def action(name, tbspname, partnum):
    """
    Function prints output from pre-defined sql query

    Args:
        name(str): query type
        tbspname(str): tablespace name
        partnum(int): partition number of tablespace

    """
    if name == 'deadlocks':
        CMD = "select DEADLOCKS from sysibmadm.snapdb where SUBSTR (DB_NAME, 1, 20) like UPPER('%" + DSN + "%')"
        out = db2query(CMD)
        out = out[3]
        print out.strip()
    if name == 'version':
        CMD = "SELECT SERVICE_LEVEL FROM SYSIBMADM.ENV_INST_INFO"
        out = db2query(CMD)
        out = out[-4].split()[1]
        print out
    if name == 'freeprct':
        CMD = "select integer(round(TBSP_FREE_PAGES*100.0/TBSP_USABLE_PAGES,0)) from table(MON_GET_TABLESPACE(null, -2)) where tbsp_name ='" \
              + tbspname + "' and DBPARTITIONNUM =" + partnum
        out = db2query(CMD)
        out = out[-4]
        print out.strip()
    if name == 'freegb':
        CMD = "select TBSP_FREE_PAGES * TBSP_PAGE_SIZE from table(MON_GET_TABLESPACE(null, -2)) where tbsp_name = '" \
              + tbspname + "' and DBPARTITIONNUM =" + partnum
        out = db2query(CMD)
        out = out[-4]
        print out.strip()
    if name == 'usedgb':
        CMD = "select TBSP_USED_PAGES * TBSP_PAGE_SIZE USED_GB from table(MON_GET_TABLESPACE(null, -2)) where tbsp_name='" \
              + tbspname + "' and DBPARTITIONNUM =" + partnum
        out = db2query(CMD)
        out = out[-4]
        print out.strip()
    if name == 'usablegb':
        CMD = "select TBSP_USABLE_PAGES * TBSP_PAGE_SIZE USABLE_GB from table(MON_GET_TABLESPACE(null, -2)) where tbsp_name='" \
              + tbspname + "' and DBPARTITIONNUM=" + partnum
        out = db2query(CMD)
        out = out[-4]
        print out.strip()
    if name == 'state':
        CMD = "select TBSP_state from table(MON_GET_TABLESPACE(null, -2)) where tbsp_name='" + tbspname + "' and DBPARTITIONNUM=" + partnum
        out = db2query(CMD)
        out = out[-4]
        print out.strip()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--discovery", action="store_true")
    parser.add_option("--tbsp", action='store', default='')
    parser.add_option('--partnum', action='store', default=0)
    parser.add_option("--host", action='store')
    parser.add_option('--name', action='store')
    args, option = parser.parse_args()
    try:
        if args.host:
            DSN = args.host
            connect(DSN)
        if args.discovery:
            discovery()
        if args.name:
            action(args.name, args.tbsp, args.partnum)
    except IndexError, e:
        print e
