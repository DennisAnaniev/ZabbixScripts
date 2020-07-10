#!/usr/bin/env python

from os import popen
import json
import optparse
import subprocess

CRED = {'PUSP' : {'User':'zabbix',
                  'Password':'Cegthgfhjkm14'
                  },
'DBPSMQUTRMI':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
          },
'RSB-DBPRBSTAFF':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },
'RSB-DSCTXSQL':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },
'RSBZ-DSCTXSQL1':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                      },                  
'RSB-DBPMOSSQLFO':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSBZ-DBPMOS0MB':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPBSMBD':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },



'MOSCMSI':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ISPMOSTNG1':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ISPMOSTNG2':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },


'RSB-DBPMOSMPZ1':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },


'RSB-ASUSTU-SGI':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSAW01':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSCTIO1':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSCTIO2':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },


'RSB-ASPMOSAW01':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
		},

'RSB-DBPMOSSQL9':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-DBPMOSSQL11':{'User': 'Zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },



'RSB-DBPMOSSQL1':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-CLPMOSWXT01':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-DBPMOSCLR1':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSDIAS1':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSDIAS2':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSCTIR1':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },

'RSB-ASPMOSCTIR2':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },
'rsb-dbpmoscase':{'User': 'zabbix',
                   'Password': 'Cegthgfhjkm14'
                  },







'RSB-DBPMOSWXT':{'User': 'zabbix',
                       'Password': 'Cegthgfhjkm14'
                  },
}
def database_discovery(connect):
    """
    Selecting all databases inside MSSQL, and prints it json formatted

    """
    keys = ["{#DBNAME}"]
    jsonlist = []
    databases = popen('echo "select name from master..sysdatabases" | isql -v ' + connect + '').read()
    databases = databases.replace("|", "")
    databases = databases.replace(" ", '')
    databases = databases.splitlines()
    databases = databases[13:-4]
    for db in databases:
         data = [db]
         jsonlist.append(json.dumps(dict(zip(keys, data))))
    #print connect
    print '{"data":'
    print str(jsonlist).replace("'", "")
    print '}'
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--host", action='store')
    args, option = parser.parse_args()
    try:
        if args.host in CRED.keys():
            connect = "{0} {1} {2}".format(args.host, CRED[args.host]['User'], CRED[args.host]['Password'])
            database_discovery(connect)
    except IndexError, e:
        print e

"""
   UnComment next section and run script without parameters to see, which servers are available
"""
#"""
for key in CRED:
   #you can add servers into [] to exclude them, if the process hangs on them
    if key not in []:
        print key
        database_discovery(key + " " + CRED[key]['User'] + " " + CRED[key]['Password'])
#"""
