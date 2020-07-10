#!/usr/bin/env python
# Version: 0.1
# Author: Artem "RaTRaZe" Kuzmin

from os import popen
from sys import argv
from ConfigParser import SafeConfigParser
import json

DB2CLIPATH='/opt/ibm/db2/V10.5/cfg/db2cli.ini'
DSN = argv[1]


def parseit():
    """
    Function opens db2cli.ini, and trying to find "Username" and "Password" field in the file,
    and connect to db, that specified by argv.

    Returns:
        Connect string, that can be used by isql

    Raises:
        BaseException:
            if username or password was not found in db2cli.ini

    """
    parser = SafeConfigParser()
    parser.read(DB2CLIPATH)
    if parser.has_option(DSN, 'Username') and parser.has_option(DSN, 'Password'):
        connect = "{0} {1} {2}".format(DSN, parser.get(DSN, 'Username'), parser.get(DSN, 'Password'))
    else:
        print "You need to have username and password to be set up in DB2CLIPATH"
        raise BaseException
    return connect


def database_discovery(connect):
    """
    Functions prints list of databases in json format.

    Args:
        connect(str):   connection string for isql

    Returns:
        list of databases in json format

    """
    keys = ["{#DBNAME}"]
    jsonlist = []
    databases = popen('echo "select substr(tablespace_name,1,30) as TBSPC_NAME from'\
                      ' table(snapshot_tbs_cfg(' + "'" + DSN + "'" + ' ,-1)) as snapshot_tbs_cfg" | isql -v ' + connect).read()
    #print databases
    databases = databases.replace("|", "")
    databases = databases.replace(" ", '')
    databases = databases.splitlines()
    databases = databases[13:-4]
    for db in databases:
        data = []
        data.append(db)
        jsonlist.append(json.dumps(dict(zip(keys, data))))
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'


def partnum_plus_tbsp(connect):
    """
    Function prints list of tablespaces along with its partition number

    Args:
        connect(str): connection string for isql
    """
    keys = ["{#TBSPNAME}", "{#PARTNUM}"]
    jsonlist = []
    with popen('echo "select varchar(s.tbsp_name,20) tbsp_name,s.dbpartitionnum from sysibmadm.snaptbsp_part s,sysibmadm.snaptbsp d where d.TBSP_NAME=s.TBSP_NAME and s.dbpartitionnum=d.dbpartitionnum and s.tbsp_current_size is not null order by s.tbsp_name,s.dbpartitionnum;" | isql -v ' + connect) as rawdata:
         text = rawdata.read()
         text = text.replace("|", "")
         text = text.splitlines()
         text = text[15:-4]
         for item in text:
             data = item.strip().split()
             jsonlist.append(json.dumps(dict(zip(keys, data))))
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'


if __name__ == '__main__':
    if len(argv) == 3:
        partnum_plus_tbsp(parseit())
    else:
        database_discovery(parseit())
