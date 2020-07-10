#!/usr/bin/env python

from os import popen
import json
import optparse

USER = 'Zabbix'
PASSWORD = 'Cegthgfhjkm14'
CRED = [
'RSB-DBPMOS1C71', 
'RSB-ASMOSPH1', 
'rsb-aspmosICMRB', 
'SGI-CLP-BBLST', 
'RSB-DBPSMQUTRMI',
'RSB-DSPMOSAQUA1', 
'RSB-DSPMOSAQUA2', 
'RSB-DBCMOSFODB1', 
'RSB-ASLABO2SRV', 
'rsb-aspmosCCMP', 
'rsb-aspmosICMRA', 
'rsb-dbpmos0icmt', 
'rsb-aspmosAW02', 
'RSB-ASPMOSCCMP', 
'RSB-DBSCOMACS', 
'RSB-DBSCOMDW', 
'RSB-ISPMOSCSTMS', 
'RSB-EXPMOSVONE', 
'RSB-EXMOSSCCM', 
'RSB-EXPMOSVARS2', 
'RSB-DBPMOSDYNMX', 
'rsb-dbMOSctxsql', 
'RSB-DBMOSTCSQL1', 
'RSB-ASPMOSDRPZR', 
'RSB-DBPMOSSMVC1', 
'RSB-DBPMOSSMNR1', 
'RSB-DBPMOS0DBOR', 
'RSB-DBPMOS0SQL', 
'RSB-DBPMOS1C', 
'RSB-DBPMOS1C81', 
'RSB-DBPMOSSQL5', 
'RSB-DBPMOSSER1C', 
'rsb-dbpmossmp5t', 
'RSB-ASPMOSQUICK', 
'RSB-ASPMOS1CLSN', 
'rsb-dbpLsng1', 
'RSB-DBPRBSTAFF', 
'RSB-DBPMOSCTIO3', 
'RSB-DBPMOSCTIO4', 
'RSB-CLPMOSCTIO-CTIO_AG', 
'RSB-DBPMOSHERM1', 
'RSB-DBPMOSSQL11', 
'RSB-DBPMOSSQL1', 
'RSB-DBPMOSSQL2', 
'RSB-DBPMOSSQL3', 
'RSB-DBPMOSSQL10', 
'RSB-DBPMOSSQL11', 
'RSB-DBPMOSSQL4', 
'RSB-DBPMOSSQL8', 
'RSB-DSCTXSQL', 
'RSBZ-DSCTXSQL1',                  
'RSB-DBPMOSSQLFO', 
'RSBZ-DBPMOS0MB', 
'rsb-aspbsmbd', 
'RSB-DBPMOSGADB', 
'RSB-DBPMOSCCR01', 
'RSB-DBPMOSCCR02', 
'RSB-DSPMOSWT01', 
'RSB-ISPMOSTNG1', 
'RSB-ISPMOSTNG2', 
'rsb-dbpmos1icmt', 
'SQLSIRON', 
'RSB-DBPMOSMPZ1', 
'RSB-ASUSTU-SGI', 
'rsb-aspmosAW01', 
'rsb-aspmosCTIO1', 
'Rsb-dbpmosCTIO3', 
'RSB-ASPMOSCTIO2', 
'RSB-DBPMOSSQL9', 
'RSB-CLPMOSWXT01', 
'RSB-DBPMOSCLR1', 
'RSB-ASPMOSDIAS1', 
'RSB-ASPMOSDIAS2', 
'RSB-DBPMOS0MPZ2', 
'RSB-ASPMOSCTIR1', 
'RSB-ASPMOSCTIR2', 
'RSB-DBPMOSNODE4', 
'RSB-DBPMOSNODE5', 
'RSB-CLP-IBNKLST', 
'RSB-DBPMOSSQL6', 
'RSB-CLP-SQLLST', 
'RSB-CLP-HERMLST', 
'RSB-CLP-HPSMLST', 
'RSB-ASPMOS1CLSN', 
'rsb-dbpmoscase', 
'RSB-DBPMOSWXT', 
]

def database_discovery(connect):
    """
    Selecting all databases inside MSSQL, and prints it json formatted

    """
    keys = ["{#DBNAME}"]
    jsonlist = []
    databases = popen('echo "select name from master.sys.databases where state = 0" | isql -v ' + connect + '').read()
    databases = databases.replace("|", "")
    databases = databases.replace(" ", '')
    databases = databases.splitlines()
    databases = databases[13:-4]
    for db in databases:
         data = [db]
         jsonlist.append(json.dumps(dict(zip(keys,data))))
    print '{"data":'
    print str(jsonlist).replace("'","")
    print '}'

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--host", action='store')
    args, option = parser.parse_args()
    try:
        if args.host in CRED:
            connect = "{0} {1} {2}".format(args.host, USER, PASSWORD)
            database_discovery(connect)
    except IndexError, e:
        print e

