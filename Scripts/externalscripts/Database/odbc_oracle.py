#!/usr/bin/env python

import pyodbc
import json
import sys
from os import popen,environ

DSN = sys.argv[1]
key = ["{#TBSPNAME}"]
CRED = {
        'pnnar':{
                'user':'zabbix',
                'password':'zabbix'
                },
    
        'ekfosdb':{
                'user':'zabbix',
                'password':'Z@bbix'
                },
        'IPS':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        
        
        'IBSO':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        
        'ALMDB_C':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        
        'RDM':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        'PRMZ':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        
        
        
        
        
        
        
        
        'SUPP_PROD':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        
        
        
        
        
        'ALMBNK':{
                'user':'zabbix',
                'password':'e8+7crJlOgimvkpvLaqSPmh'
                },
        
        'DLTBSGV':{
                'user':'zabbix',
                'password':'k3+RSRzTgARFcMFvaANqFaB'
                },
        'CREDREG':{
                'user':'zabbix',
                'password':'r4+BueDEIEYnjCfXsPgmkSC'
                },
	'IIBNRT':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        'TWO_PRIMARY':{
                'user':'ZABBIX',
                'password':'MD3B#4OCG'
                },

        'SRNRT':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },


'PROD':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },

'ZABBIX':{
                'user':'zabbix_main',
                'password':'150cmisokforagirl'
                                },


	'NARVAL':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },


    'SBNRT':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },


    'DS':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },

    'RBSD':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },

    'DLTBSGV':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },


    'TRDFXAG':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },

    'TWPG':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },


    'BROQ':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },


    'ICBCUS':{
                'user':'ZABBIX',
                'password':'PEWPEWPEWhandsup1'
                },

        'cb':{
                'user':'zabbix',
                'password':'PEWPEW_1PEWhandsup1'
                },
        
        'rb':{
                'user':'zabbix',
                'password':'PEWPEWPEWhandsup1'
                },
        
        
        }
dbquery = {
    'version': 'select banner from v$version where rownum=1;',
    'flashrecoveryarea': "select round((space_used - space_reclaimable)/(space_limit),3)*100 percent_used FROM V$RECOVERY_FILE_DEST;",
    'checkactive': "select to_char(case when inst_cnt > 0 then 1 else 0 end,'FM99999999999999990') retvalue from (select count(*) inst_cnt from v$instance where status = 'OPEN' and logins = 'ALLOWED' and database_status = 'ACTIVE');", 
    'rcachehit': "SELECT to_char((1 - (phy.value - lob.value - dir.value) / ses.value) * 100, 'FM99999990.9999') retvalue FROM   v$sysstat ses, v$sysstat lob,v$sysstat dir, v$sysstat phy WHERE  ses.name = 'session logical reads' AND dir.name = 'physical reads direct' AND lob.name = 'physical reads direct (lob)' AND phy.name = 'physical reads';",
    'dsksortratio': "SELECT to_char(d.value/(d.value + m.value)*100, 'FM99999990.9999') retvalue FROM  v$sysstat m, v$sysstat d WHERE m.name = 'sorts (memory)' AND d.name = 'sorts (disk)';",
    'activeusercount': "select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null and status='ACTIVE';",
    'usercount': "select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null;",
    'dbsize': "SELECT to_char(sum(  NVL(a.bytes - NVL(f.bytes, 0), 0)), 'FM99999999999999990') retvalue FROM sys.dba_tablespaces d, (select tablespace_name, sum(bytes) bytes from dba_data_files group by tablespace_name) a, (select tablespace_name, sum(bytes) bytes from dba_free_space group by tablespace_name) f WHERE d.tablespace_name = a.tablespace_name(+) AND d.tablespace_name = f.tablespace_name(+) AND NOT (d.extent_management like 'LOCAL' AND d.contents like 'TEMPORARY');",
    'dbfilesize': "select to_char(sum(bytes), 'FM99999999999999990') retvalue from dba_data_files;",
    'uptime': "select to_char((sysdate-startup_time)*86400, 'FM99999999999999990') retvalue from v$instance;",
    'hparsratio': "SELECT to_char(h.value/t.value*100,'FM99999990.9999') retvalue FROM  v$sysstat h, v$sysstat t WHERE h.name = 'parse count (hard)' AND t.name = 'parse count (total)';",
    'lastarclog': "select to_char(max(SEQUENCE#), 'FM99999999999999990') retvalue from v$log where archived = 'YES';",
    'lastapplarclog':  "select to_char(max(lh.SEQUENCE#), 'FM99999999999999990') retvalue from v$loghist lh, v$archived_log al where lh.SEQUENCE# = al.SEQUENCE# and applied='YES';",
     }


def sender(key, value):
    zabbix = '10.45.129.32'
    popen("zabbix_sender -z {0} -s {1} -k {2} -o '{3}'".format(zabbix,DSN,key,value)) 


def db_discovery():
    jsonlist = []
    cursor.execute('SELECT tablespace_name FROM dba_tablespaces;')
    for line in cursor:
        data = [line[0]]
        jsonlist.append(json.dumps(dict(zip(key, data))))

    jsonencode(jsonlist,'tablespaces')


def job_failures():
    jsonlist = []
    key = ["{#ID}"]
    cursor.execute("select JOB, FAILURES, BROKEN from dba_jobs where last_date > sysdate - 14")
    row = cursor.fetchall()
    for r in row:
            data = [int(r[0])]
            jsonlist.append(json.dumps(dict(zip(key, data))))
            sender("oracle[job_failures_{0}]".format(int(r[0])), int(r[1]))
            sender("oracle[job_status_{0}]".format(int(r[0])), r[2])
    jsonencode(jsonlist,'jobid')


def complex(query, items):
    ## Use this for columns
    cursor.execute(query)
    row = cursor.fetchall()
    lst = [item[1] for item in row]
    lst = zip(items, lst)
    for item in lst:
        sender(str(item[0]), str(item[1]))


def tbsp_query():
    cursor.execute("""SELECT a.tablespace_name, SUM (a.bytes) CURRENT_bytes,SUM (DECODE (b.maxextend, NULL, A.BYTES, b.maxextend * 8192)) 
		    MAX_bytes, SUM (a.bytes) - c.Free USED_bytes, SUM (DECODE (b.maxextend, NULL, A.BYTES, b.maxextend * 8192)) - (SUM (a.bytes) - c.Free)
		    FREE_bytes, round(100 * (SUM (a.bytes) - c.Free) / (SUM (DECODE (b.maxextend, NULL, A.BYTES, b.maxextend * 8192))), 1)
		    USED_PCT FROM dba_data_files a, sys.filext$ b,
		    (  SELECT d.tablespace_name, SUM (NVL (c.bytes, 0)) Free
		    FROM dba_tablespaces d, DBA_FREE_SPACE c
		    WHERE d.tablespace_name = c.tablespace_name(+)
		    GROUP BY d.tablespace_name) c
		    WHERE a.file_id = b.file#(+) AND a.tablespace_name = c.tablespace_name
		    GROUP BY a.tablespace_name, c.Free
		    ORDER BY tablespace_name;
                          """)
    row = cursor.fetchall()
    items = ["tbs_size", "tbs_free_size", "tbs_used", "tbs_used_percent", "tbs_maxsize_size"]
    for item in row:
        for i in items:
            sender("oracle[{0}_{1}]".format(i, item[0]), str(item[items.index(i)+1]))

   

def jsonencode(jlist, title=''):
    data = '{{"data":{0} }}'.format(str(jlist).replace("'", ""))
    sender(title, data)


def toad(query, items):
    ## Use it for rows
    cursor.execute(query)
    row = cursor.fetchone()
    lst = zip(items,row)
    for item in lst:
        sender(item[0], int(item[1]))


environ['ORACLE_HOME'] = '/usr/lib/oracle/11.2/client64' 
connect = pyodbc.connect('DSN={0};UID={1};PWD={2};'.format(DSN, CRED[DSN]['user'], CRED[DSN]['password']))
cursor = connect.cursor()
for k in dbquery:
    try:
        cursor.execute(dbquery[k])
        row = cursor.fetchone()
        sender(k, row[0])
    except TypeError:
        sender(k, 'n/a')

db_discovery()
job_failures()
tbsp_query()
toad("SELECT SUM (DECODE (name, 'db block changes', VALUE, 0)) block_changes, SUM (DECODE (name, 'db block gets', VALUE, 0)) current_reads, SUM (DECODE (name, 'consistent gets', VALUE, 0)) consistent_reads, SUM (DECODE (name, 'physical reads', VALUE, 0)) datafile_reads, SUM (DECODE (name, 'physical writes', VALUE, 0)) datafile_writes, SUM (DECODE (name, 'parse count (total)', VALUE, 0)) parse_count, SUM (DECODE (name, 'execute count', VALUE, 0)) execute_count FROM v$sysstat WHERE name IN ('db block changes', 'db block gets', 'consistent gets', 'physical reads', 'physical writes', 'parse count (total)', 'execute count');", ["dbblockchanges", "dbblockgets", "consistentgets", "physicalreads", "physicalwrites", "parsecount", "executecount"])
toad(" SELECT SUM (DECODE (TYPE, 'BACKGROUND', 1, 0)) system_sessions, SUM ( DECODE (TYPE, 'BACKGROUND', 0, DECODE (Status, 'ACTIVE', 0, 1))) inactive_users FROM V$SESSION;", ["sessions", "inactive"])
toad("SELECT 100 * ( 1 - ( (SELECT VALUE FROM V$SYSSTAT WHERE name = 'physical reads cache') / ( (SELECT VALUE FROM V$SYSSTAT WHERE name = 'consistent gets from cache') + (SELECT VALUE FROM V$SYSSTAT WHERE name = 'db block gets from cache')))) FROM DUAL;", ["buffercachehit"])
toad("SELECT 100 - SUM (DECODE (name, 'table scans (long tables)', VALUE, 0)) / ( SUM ( DECODE (name, 'table scans (long tables)', VALUE, 0)) + SUM ( DECODE (name, 'table scans (short tables)', VALUE, 0))) * 100 indexed_sql FROM V$SYSSTAT WHERE 1 = 1 AND (NAME IN ('table scans (long tables)', 'table scans (short tables)'));", ["indexedsql"])
toad("SELECT (1 - (Sum(misses) / Sum(gets))) * 100 FROM v$latch;", ["latchhit"])
toad("SELECT 100 - SUM (gets)/ SUM (gethits) FROM V$LIBRARYCACHE WHERE 1 = 1 AND namespace = 'SQL AREA';", ["sqlarehits"])
complex("SELECT en.name, TO_CHAR (time_waited, 'FM99999999999999990') retvalue FROM v$system_event se RIGHT JOIN v$event_name en ON se.event = en.name WHERE en.name IN ( 'log file switch completion', 'log file sync', 'buffer busy waits', 'free buffer waits', 'log file parallel write', 'enqueue', 'db file sequential read', 'db file scattered read',  'db file single write', 'db file parallel write', 'direct path read', 'direct path write', 'latch free') ORDER BY en.name;", ["bufbusywaits", "dbprllwrite", "dbscattread", "dbseqread", "dbsnglwrite", "directread", "directwrite","freebufwaits", "latchfree", "logprllwrite", "logswcompletion", "logfilesync"])
complex("select name, to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name IN ('user commits', 'user rollbacks', 'enqueue deadlocks', 'redo writes', 'table scans (long tables)', 'table scan rows gotten', 'index fast full scans (full)', 'bytes sent via SQL*Net to client', 'bytes received via SQL*Net from client', 'SQL*Net roundtrips to/from client', 'logons current') order by name", ['netroundtrips', 'netresv', 'netsent', 'deadlocks', 'indexffs', 'logonscurrent', 'redowrites', 'tblrowsscans', 'tblscans', 'commits', 'rollbacks']);
complex("SELECT pn, SUM (bytes) FROM (SELECT NVL (pool, name) pn, bytes FROM V$SGASTAT) GROUP BY pn ORDER BY pn;", ['buffercache', 'fixedsga', 'javapool', 'largepool', 'logbuffer', 'sharedpool'])
complex("SELECT name, bytes FROM V$SGASTAT WHERE name IN ('dictionary cache', 'free memory', 'sql area', 'row cache', 'library cache') AND pool = 'shared pool' UNION ALL SELECT 'misc', SUM (bytes) FROM V$SGASTAT WHERE name NOT IN ('library cache', 'dictionary cache', 'free memory', 'sql area') AND pool = 'shared pool';", ['sqlarea', 'librarycache', 'freememory', 'rowcache', 'misc'])
complex("WITH wait_categories AS (SELECT CASE WHEN name LIKE '%latch%' OR name LIKE '%mutex%' OR name LIKE 'cursor:%' OR name IN ('library cache pin') THEN 'Latch/mutex' WHEN name LIKE 'direct path%temp' THEN 'Temp Segment I/O'WHEN name IN ('db file sequential read', 'log file sync', 'buffer busy waits') THEN name WHEN name IN ('free buffer space', 'write complete waits') THEN 'DBWR waits' WHEN name LIKE '%flashback%' THEN 'Flashback log wait' WHEN name IN ('gc cr block 2-way', 'gc cr block 3-way') THEN 'RAC interconnect' WHEN name LIKE 'enq:%' OR name IN ('row cache lock') THEN 'Lock' WHEN name LIKE 'log file switch%' THEN 'log file switch' WHEN wait_class LIKE 'User I/O' THEN 'User I/O' ELSE wait_class END AS wait_type, name, wait_class FROM v$event_name e WHERE wait_class <> 'Idle') SELECT wait_type, ROUND (SUM (time_waited_micro) / 1000) time_waited_ms FROM v$system_event e, wait_categories c WHERE 1 = 1 AND c.name = e.event GROUP BY wait_type ORDER BY wait_type", ["administrativeevents", "applicationevents", "concurrencyevents", "latchmutexevents", "lockevents", "networkevents", "otherevents", "systemioevents", "tempevents", "userioevents", "bufferbusyevents", "dbfileseqreadevents", "logfileswitchevents", "logfilesyncevents"])
print "OK"
