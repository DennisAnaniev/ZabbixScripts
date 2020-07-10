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

	'rb':{
	'user':'zabbix',
    'password':'PEWPEWPEWhandsup1'
    }    
        }
dbquery = {
    'version': 'select banner from v$version where rownum=1;',
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
    cursor.execute("SELECT ts.tablespace_name,size_info.megs_alloc, size_info.megs_free, size_info.megs_used, size_info.pct_used, size_info.MAX FROM (SELECT a.tablespace_name, a.bytes_alloc megs_alloc, (NVL (b.bytes_free, 0)) megs_free,  ( (a.bytes_alloc - NVL (b.bytes_free, 0))) megs_used, ROUND ( (NVL (b.bytes_free, 0) / a.bytes_alloc) * 100) Pct_Free, 100 - ROUND ( (NVL (b.bytes_free, 0) / a.bytes_alloc) * 100) Pct_used,  (maxbytes) MAX FROM ( SELECT f.tablespace_name, SUM (f.bytes) bytes_alloc, SUM ( DECODE (f.autoextensible, 'YES', f.maxbytes, 'NO', f.bytes)) maxbytes FROM dba_data_files f GROUP BY tablespace_name) a, ( SELECT f.tablespace_name, SUM (f.bytes) bytes_free FROM dba_free_space f GROUP BY tablespace_name) b WHERE a.tablespace_name = b.tablespace_name(+) UNION ALL SELECT h.tablespace_name,  (SUM (h.bytes_free + h.bytes_used)) megs_alloc,  ( SUM ( (h.bytes_free + h.bytes_used) - NVL (p.bytes_used, 0)) ) megs_free,  (SUM (NVL (p.bytes_used, 0))) megs_used, ROUND ( ( SUM ( (h.bytes_free + h.bytes_used) - NVL (p.bytes_used, 0)) / SUM (h.bytes_used + h.bytes_free)) * 100) Pct_Free, 100 - ROUND ( ( SUM ( (h.bytes_free + h.bytes_used) - NVL (p.bytes_used, 0)) / SUM (h.bytes_used + h.bytes_free)) * 100) pct_used,  (SUM (f.maxbytes)) MAX FROM sys.v_$TEMP_SPACE_HEADER h, sys.v_$Temp_extent_pool p, dba_temp_files f WHERE p.file_id(+) = h.file_id AND p.tablespace_name(+) = h.tablespace_name AND f.file_id = h.file_id AND f.tablespace_name = h.tablespace_name GROUP BY h.tablespace_name) size_info, sys.dba_tablespaces ts WHERE ts.tablespace_name = size_info.tablespace_name")
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
toad("SELECT SUM (DECODE (TYPE, 'BACKGROUND', 1, 0)) system_sessions, SUM ( DECODE (TYPE, 'BACKGROUND', 0, DECODE (Status, 'ACTIVE', 0, 1))) inactive_users FROM V$SESSION;", ["sessions", "inactive"])
toad("SELECT 100 * ( 1 - ( (SELECT VALUE FROM V$SYSSTAT WHERE name = 'physical reads') / ( (SELECT VALUE FROM V$SYSSTAT WHERE name = 'consistent gets') + (SELECT VALUE FROM V$SYSSTAT WHERE name = 'db block gets')))) FROM DUAL;", ["buffercachehit"])
toad("SELECT 100 - SUM (DECODE (name, 'table scans (long tables)', VALUE, 0)) / ( SUM ( DECODE (name, 'table scans (long tables)', VALUE, 0)) + SUM ( DECODE (name, 'table scans (short tables)', VALUE, 0))) * 100 indexed_sql FROM V$SYSSTAT WHERE 1 = 1 AND (NAME IN ('table scans (long tables)', 'table scans (short tables)'));", ["indexedsql"])
toad("SELECT (1 - (Sum(misses) / Sum(gets))) * 100 FROM v$latch;", ["latchhit"])
toad("SELECT 100 - SUM (gets)/ SUM (gethits) FROM V$LIBRARYCACHE WHERE 1 = 1 AND namespace = 'SQL AREA';", ["sqlarehits"])
complex("SELECT en.name, TO_CHAR (nvl(time_waited,0), 'FM99999999999999990') retvalue FROM v$system_event se RIGHT JOIN v$event_name en ON se.event = en.name WHERE en.name IN ( 'log file switch completion', 'log file sync', 'buffer busy waits', 'free buffer waits', 'log file parallel write', 'enqueue', 'db file sequential read', 'db file scattered read',  'db file single write', 'db file parallel write', 'direct path read', 'direct path write', 'latch free') ORDER BY en.name;", ["bufbusywaits", "dbprllwrite", "dbscattread", "dbseqread", "dbsnglwrite", "directread", "directwrite","freebufwaits", "latchfree", "logprllwrite", "logswcompletion", "logfilesync"])
complex("select name, to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name IN ('user commits', 'user rollbacks', 'enqueue deadlocks', 'redo writes', 'table scans (long tables)', 'table scan rows gotten', 'index fast full scans (full)', 'bytes sent via SQL*Net to client', 'bytes received via SQL*Net from client', 'SQL*Net roundtrips to/from client', 'logons current') order by name;", ['netroundtrips', 'netresv', 'netsent', 'deadlocks', 'indexffs', 'logonscurrent', 'redowrites', 'tblrowsscans', 'tblscans', 'commits', 'rollbacks']);
complex("SELECT pn, SUM (bytes) FROM (SELECT NVL (pool, name) pn, bytes FROM V$SGASTAT) GROUP BY pn ORDER BY pn;", ['buffercache', 'fixedsga', 'javapool', 'largepool', 'logbuffer', 'sharedpool'])
complex("SELECT name, bytes FROM V$SGASTAT WHERE name IN ('dictionary cache', 'free memory', 'sql area', 'row cache', 'library cache') AND pool = 'shared pool' UNION ALL SELECT 'misc', SUM (bytes) FROM V$SGASTAT WHERE name NOT IN ('library cache', 'dictionary cache', 'free memory', 'sql area') AND pool = 'shared pool';", ['sqlarea', 'librarycache', 'freememory', 'rowcache', 'misc'])
complex("WITH wait_categories AS (SELECT CASE WHEN name LIKE '%latch%' OR name LIKE '%mutex%' OR name LIKE 'cursor:%' OR name IN ('library cache pin') THEN 'Latch/mutex' WHEN name LIKE 'direct path%temp' THEN 'Temp Segment I/O' WHEN name IN ('db file sequential read', 'log file sync', 'buffer busy waits','smon timer','virtual circuit status','rdbms ipc reply','process startup','control file heartbeat','refresh controlfile command') THEN name WHEN name IN ('free buffer space', 'write complete waits') THEN 'DBWR waits' WHEN name LIKE '%flashback%' THEN 'Flashback log wait' WHEN name IN ('gc cr block 2-way', 'gc cr block 3-way') THEN 'RAC interconnect' WHEN name LIKE 'enq%' OR name IN ('row cache lock') THEN 'Lock' WHEN name in ('SQL*Net message from dblink','SQL*Net more data from client','SQL*Net more data to client','SQL*Net message to dblink','SQL*Net message to client','SQL*Net more data from dblink') THEN 'Network' WHEN name in ('db file scattered read','direct path read','direct path write','db file parallel read','db file single write') THEN 'User I/O' WHEN name like '%parallel write' OR name in ('control file sequential read','async disk IO','log file sequential read','log file single write') THEN 'System I/O' WHEN name in ('log buffer space','sort segment request','log file switch') THEN 'Configuration' WHEN name in ('SQL*Net break/reset to client') THEN 'Application' WHEN name in ('library cache load lock') THEN 'Concurrency' WHEN name LIKE 'log file switch%' THEN 'log file switch' ELSE 'other' END AS wait_type, name FROM v$event_name e WHERE name NOT IN('SQL*Net message from client','rdbms ipc message','pmon timer','dispatcher timer','smon timer','virtual circuit status','single-task message','HS message to agent')) SELECT wait_type, ROUND (SUM (time_waited_micro) / 1000) time_waited_ms FROM v$system_event e, wait_categories c WHERE c.name = e.event GROUP BY wait_type ORDER BY wait_type", ["administrativeevents", "applicationevents", "concurrencyevents", "latchmutexevents", "lockevents", "networkevents", "otherevents", "systemioevents", "tempevents", "userioevents", "bufferbusyevents", "dbfileseqreadevents", "logfileswitchevents", "logfilesyncevents"])
print "OK"
