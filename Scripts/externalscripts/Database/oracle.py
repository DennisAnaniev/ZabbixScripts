#!/usr/bin/env python

import cx_Oracle
import collections
import argparse
import sys
import ast
import os

tmp_dir = '/usr/local/share/zabbix/externalscripts/oracle/'

def nonestr(s):
    return 'NULL' if s is None else str(s)


# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False)
ap.add_argument("--type", required=True)
ap.add_argument("--item", required=True)
ap.add_argument("--statusmode", required=False)
ap.add_argument("--id", required=False)
ap.add_argument("--test", required=False)
args = vars(ap.parse_args())

# Credentials
u_credentials  =  {
        "SBL_RECOVERY_TST": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsbt-dbtgenora-scan.trosbank.trus.tsocgen',
					   'Port': '1525',
					   'Service': 'SBL_RECOVERY_TST',
                       },
        "MRT": {'User': 'XIBBAZ',
                       'Password': 'borjomi4',
                       'Host': 'rsb-dbpmosfmdb-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'MRT',
                       } ,

	"NFOBPM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': ' rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'NFOBPM_PRIMARY',
                       } ,
"NFOUI": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': ' rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'NFOUI_PRIMARY',
                       } ,

"BOSSHR_PRIMARY": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': ' rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'NFOUI_PRIMARY',
                       } ,



"DST_PRIMARY": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': ' rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'DST_PRIMARY',
                       } ,


"SAPBO": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': ' rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SAPBO_PRIMARY',
                       } ,


"SAS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.58',
					   'Port': '1523',
					   'Service': 'SAS',
                       } ,








"ADOIT8": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'ADOIT8',
                       } ,

"ZB3_MAIN": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosorai1-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'ZB3_MAIN',
                       } ,


"DCNM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosorai1-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'DCNM',
                       } ,







"UCM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosorai1-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'UCM_PRIMARY',
                       } ,

"ACS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosorai1-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'ACS_PRIMARY',
                       } ,

"DCNM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosorai1-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'DCNM_PRIMARY',
                       } ,

"IIBLOG": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosib-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'IIBLOG_PRIMARY',
                       } ,

"IIBNRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosib-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'IIBNRT_PRIMARY',
                       } ,










"IBSO": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'IBSO',
                       } ,

"H2H": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'H2H_PRIMARY',
                       } ,


"WFBPM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'WFBPM_PRIMARY',
		      } ,

"RISKTE": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosrhd-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'RISKTE_PRIMARY',
		      } ,






"RDM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'RDM',
                       } ,


"ACCED": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'ACCED',
                       } ,

"BROQ": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'BROQ',
                       } ,


"PPMCR": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'PPMCR',
                       } ,

"QUORUM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'QUORUM_PRIMARY',
                       } ,

"RBSD": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'RBSD_PRIMARY',
                       } ,







"ALMBNK": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbalmbnk.rosbank.rus.socgen',
					   'Port': '1521',
					   'Service': 'ALMBNK',
                       } ,


"DCSBNK": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbdcsbnk.rosbank.rus.socgen',
					   'Port': '1521',
					   'Service': 'DCSBNK',
                       } ,

"DOZOR5": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosdozdb.rosbank.rus.socgen',
					   'Port': '1521',
					   'Service': 'DOZOR5',
                       } ,








"SUPP": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SUPP',
                       } ,

"TIPLUS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmostfn-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'TIPLUS',
                       } ,







"PRMZ": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosoradg-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'PRMZ_PRIMARY',
                       } ,


"SASLIM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosoradg-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SASLIM_PRIMARY',
                       } ,

"IIBMON": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.17.128.249',
					   'Port': '2230',
					   'Service': 'IIBMON',
                       } ,







"DS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'DS',
                       } ,

"EQUEUE": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'EQUEUE',
                       } ,



"TRDFXAG": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'TRDFXAG',
                       } ,

"TWCMS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmostwc-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'TWCMS',
                       } ,

"TWO": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosahc-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'TWO',
                       } ,


"TWPG": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosahc-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'TWPG',
                       } ,








"FCS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'FCS',
                       } ,

"GZKH1": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'GZKH1',
                       } ,

"ICBCUS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'ICBCUS_PRIMARY',
                       } ,

"SMNRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0sm-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SMNRT_PRIMARY',
                       } ,

"SRNRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0sr-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SRNRT_PRIMARY',
                       } ,








"SECM": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SECM_PRIMARY',
                       } ,



"CB": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1,',
                       'Host': '172.20.0.44',
					   'Port': '1521',
					   'Service': 'cb.icb',
                       } ,

"CREDREG": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1,',
                       'Host': '172.20.0.13',
					   'Port': '1521',
					   'Service': 'credreg.oberon',
                       } ,

"ICS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.36',
					   'Port': '1521',
					   'Service': 'ics.vcs-ics',
                       } ,

"NARVAL": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '10.45.1.21',
					   'Port': '1521',
					   'Service': 'PNAR',
                       } ,


"RBPORTAL": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.13',
					   'Port': '1521',
					   'Service': 'rbportal.oberon',
                       } ,

"SDBORA2": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.40',
					   'Port': '1525',
					   'Service': 'sdbora2.charon',
                       } ,

"WHLOAN": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.22.130.29',
					   'Port': '1524',
					   'Service': 'whloan',
                       } ,









"PROD": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.22.130.27',
					   'Port': '1561',
					   'Service': 'PROD',
                       } ,



"QWORK": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.61',
					   'Port': '1521',
					   'Service': 'qwork.fly',
                       } ,

"RB": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.89',
					   'Port': '1521',
					   'Service': 'rb',
                       } ,








"DCSBNK": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.88',
					   'Port': '1521',
					   'Service': 'dcsbnk.rosbank',
                       } ,

"RCAT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.13',
					   'Port': '1521',
					   'Service': 'rcat.rosbank',
                       } ,

"ROSF": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': '172.20.0.33',
					   'Port': '1521',
					   'Service': 'rosf.vcs',
                       } ,







"CPCBRF": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0ora2.rosbank.rus.socgen',
					   'Port': '1521',
					   'Service': 'CPCBRF',
                       } ,

"DWHNRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0cd-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'DWHNRT_PRIMARY',
                       } ,

"MRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosfmdb-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'mrt',
                       } ,








	"SBNRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmos0si-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SBNRT_PRIMARY',
                       } ,

"ODS_PROD": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosods-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'ODSRT_PRIMARY',
                       } ,

"SBLRTP": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosrrt-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SBLRTP_PRIMARY',
                       } ,

"IIBNRT": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosib-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'IIBNRT_PRIMARY',
                       } ,






"SMRTP": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosrrt-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'SMRTP_PRIMARY',
                       } ,

"IPS": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'ips-vcs.int.rosbnk.ru',
					   'Port': '1521',
					   'Service': 'IPS.VCS',
                       } ,


	"DLTBSGV": {'User': 'ZABBIX',
                       'Password': 'PEWPEWPEWhandsup1',
                       'Host': 'rsb-dbpmosora-scan.rosbank.rus.socgen',
					   'Port': '1525',
					   'Service': 'DLTBSGV_PRIMARY',
                       } ,

}

## state list > /tmp/unity
def write_to_file(filename, data):
  with open(tmp_dir + filename + '.tmp', 'w+') as f1:
      f1.write(str(data))
      try:
	      os.remove(tmp_dir + filename)
      except OSError:
	      pass
      os.rename(tmp_dir + filename + '.tmp', tmp_dir + filename)
      f1.close()

## /tmp/unity > state list
def read_from_file(filename):
  f1 = open(tmp_dir + filename, 'r')
  data1 = f1.read().replace("u'", "'")
  data2 = ast.literal_eval(data1)
  return data2

  # get credentials
credential = u_credentials.get(args["host"] )

if credential is not None:
	host = credential.get("Host")
	user = credential.get("User")
	pwd = credential.get("Password")
	port = credential.get("Port")
	service = credential.get("Service")
else:
	print "No credential to host " + (args["host"])
	sys.exit()

item_type = args["type"]
  

  ################################# ASM_DISKGROUP #################################
  
if item_type == 'ASM_DISKGROUP':

	# Data for Items
	if args["item"] == "Data":
	
		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		diskgroup_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, GROUP_NAME, TOTAL_MB, FREE_MB, USED_MB, USED_PCT, " + "\n" + \
		"nvl(FREE_MB_ITRS, 10000000) as FREE_MB_ITRS," + "\n" + \
		"nvl(FREE_MB_WTRS, 10000000) as FREE_MB_WTRS," + "\n" + \
		"nvl(FREE_MB_DTRS, 10000000) as FREE_MB_DTRS," + "\n" + \
		"nvl(USED_PCT_ITRS, 10000000) as USED_PCT_ITRS," + "\n" + \
		"nvl(USED_PCT_WTRS, 10000000) as USED_PCT_WTRS," + "\n" + \
		"nvl(USED_PCT_DTRS, 10000000) as USED_PCT_DTRS" + "\n" + \
		"from ZBV_ASM_DISKGROUP_FLG"
		
		cur = db.cursor()
		cur.execute(diskgroup_query_str)
		db_res = cur.fetchall()
		db.close()		
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)

		print "OK"


	# Data for Discovery
	if args["item"] == "Discovery":

		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		diskgroup_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, GROUP_NAME, TOTAL_MB, FREE_MB, USED_MB, USED_PCT, " + "\n" + \
		"nvl(FREE_MB_ITRS, 10000000) as FREE_MB_ITRS," + "\n" + \
		"nvl(FREE_MB_WTRS, 10000000) as FREE_MB_WTRS," + "\n" + \
		"nvl(FREE_MB_DTRS, 10000000) as FREE_MB_DTRS," + "\n" + \
		"nvl(USED_PCT_ITRS, 10000000) as USED_PCT_ITRS," + "\n" + \
		"nvl(USED_PCT_WTRS, 10000000) as USED_PCT_WTRS," + "\n" + \
		"nvl(USED_PCT_DTRS, 10000000) as USED_PCT_DTRS" + "\n" + \
		"from ZBV_ASM_DISKGROUP_FLG"
		
		cur = db.cursor()
		cur.execute(diskgroup_query_str)
		db_res = cur.fetchall()
		db.close()		
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)				
		
		# create json
		db_res_count = len(db_res) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for item in db_res:
			db_res_count -= 1 # to remove last comma
			
			item_id = str(item[4])
			INSTANCE_NAME = str(item[0]) 
			DB_UNIQUE_NAME = str(item[1])
			HOST_NAME = str(item[2])
			METRIC_GROUP = str(item[3])
			GROUP_NAME = str(item[4])
			TOTAL_MB = str(item[5])
			FREE_MB = str(item[6])
			USED_MB = str(item[7])
			USED_PCT = str(item[8])
			FREE_MB_ITRS = str(item[9])
			FREE_MB_WTRS = str(item[10])
			FREE_MB_DTRS = str(item[11])
			USED_PCT_ITRS = str(item[12])
			USED_PCT_WTRS = str(item[13])
			USED_PCT_DTRS = str(item[14])			

			if db_res_count <> 0:
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#GROUP_NAME}": "' + GROUP_NAME + '","{#TOTAL_MB}": "' + TOTAL_MB + '","{#FREE_MB}": "' + FREE_MB + '","{#USED_MB}": "' + USED_MB + '","{#USED_PCT}": "' + USED_PCT + '","{#FREE_MB_ITRS}": "' + FREE_MB_ITRS + '","{#FREE_MB_WTRS}": "' + FREE_MB_WTRS + '","{#FREE_MB_DTRS}": "' + FREE_MB_DTRS + '","{#USED_PCT_ITRS}": "' + USED_PCT_ITRS + '","{#USED_PCT_WTRS}": "' + USED_PCT_WTRS + '","{#USED_PCT_DTRS}": "' + USED_PCT_DTRS + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#GROUP_NAME}": "' + GROUP_NAME + '","{#TOTAL_MB}": "' + TOTAL_MB + '","{#FREE_MB}": "' + FREE_MB + '","{#USED_MB}": "' + USED_MB + '","{#USED_PCT}": "' + USED_PCT + '","{#FREE_MB_ITRS}": "' + FREE_MB_ITRS + '","{#FREE_MB_WTRS}": "' + FREE_MB_WTRS + '","{#FREE_MB_DTRS}": "' + FREE_MB_DTRS + '","{#USED_PCT_ITRS}": "' + USED_PCT_ITRS + '","{#USED_PCT_WTRS}": "' + USED_PCT_WTRS + '","{#USED_PCT_DTRS}": "' + USED_PCT_DTRS + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json	
		

	# items status
	if args["item"] == "Status" and args["id"] is not None:
		
		# /tmp/oracle/ > list of data for item status (all_items)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_all_items"
		items = read_from_file(filename)
		
		item_out = ""

		if args["statusmode"] == "free_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[5]
					break

		if args["statusmode"] == "total_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[6]
					break
					
		if args["statusmode"] == "used_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[7]
					break

		if args["statusmode"] == "used_pct":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[8]
					break					
		
		elif args["statusmode"] == "free_mb_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[9]
					break
					
		elif args["statusmode"] == "free_mb_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[10]
					break
					
		elif args["statusmode"] == "free_mb_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[11]
					break					
		
		elif args["statusmode"] == "used_pct_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[12]
					break
					
		elif args["statusmode"] == "used_pct_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[13]
					break
					
		elif args["statusmode"] == "used_pct_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[14]
					break
		
		print (item_out)	

		
################################# ZBV_TABLESPACE #################################
					
elif item_type == 'ZBV_TABLESPACE':

	# Data for Items
	if args["item"] == "Data":

		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		tablespace_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, TABLESPACE_NAME, CURRENT_MB, MAX_MB, USED_MB, AVAILABLE_MB, USED_OF_MAX_PCT, " + "\n" + \
		"nvl(AVAILABLE_MB_ITRS, 10000000) as AVAILABLE_MB_ITRS," + "\n" + \
		"nvl(AVAILABLE_MB_WTRS, 10000000) as AVAILABLE_MB_WTRS, " + "\n" + \
		"nvl(AVAILABLE_MB_DTRS, 10000000) as AVAILABLE_MB_DTRS,"  + "\n" + \
		"nvl(USED_OF_MAX_PCT_ITRS, 10000000) as USED_OF_MAX_PCT_ITRS,"  + "\n" + \
		"nvl(USED_OF_MAX_PCT_WTRS, 10000000) as USED_OF_MAX_PCT_WTRS,"  + "\n" + \
		"nvl(USED_OF_MAX_PCT_DTRS, 10000000) as USED_OF_MAX_PCT_DTRS"  + "\n" + \
		"from ZBV_TABLESPACE_FLG"

		cur = db.cursor()
		cur.execute(tablespace_query_str)
		db_res = cur.fetchall()
		db.close()
	
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)	

		print "OK"

		
	# Data for Discovery
	if args["item"] == "Discovery":

		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		tablespace_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, TABLESPACE_NAME, CURRENT_MB, MAX_MB, USED_MB, AVAILABLE_MB, USED_OF_MAX_PCT, " + "\n" + \
		"nvl(AVAILABLE_MB_ITRS, 10000000) as AVAILABLE_MB_ITRS," + "\n" + \
		"nvl(AVAILABLE_MB_WTRS, 10000000) as AVAILABLE_MB_WTRS, " + "\n" + \
		"nvl(AVAILABLE_MB_DTRS, 10000000) as AVAILABLE_MB_DTRS,"  + "\n" + \
		"nvl(USED_OF_MAX_PCT_ITRS, 10000000) as USED_OF_MAX_PCT_ITRS,"  + "\n" + \
		"nvl(USED_OF_MAX_PCT_WTRS, 10000000) as USED_OF_MAX_PCT_WTRS,"  + "\n" + \
		"nvl(USED_OF_MAX_PCT_DTRS, 10000000) as USED_OF_MAX_PCT_DTRS"  + "\n" + \
		"from ZBV_TABLESPACE_FLG"

		cur = db.cursor()
		cur.execute(tablespace_query_str)
		db_res = cur.fetchall()
		db.close()
	
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)			
		
		# create json
		db_res_count = len(db_res) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for item in db_res:
			db_res_count -= 1 # to remove last comma
		
			item_id = str(item[4])
			INSTANCE_NAME = str(item[0])
			DB_UNIQUE_NAME = str(item[1])
			HOST_NAME = str(item[2])
			METRIC_GROUP = str(item[3])
			TABLESPACE_NAME = str(item[4])
			CURRENT_MB = str(item[5])
			MAX_MB = str(item[6])
			USED_MB = str(item[7])
			AVAILABLE_MB = str(item[8])
			USED_OF_MAX_PCT = str(item[9])
			AVAILABLE_MB_ITRS = str(item[10])
			AVAILABLE_MB_WTRS = str(item[11])
			AVAILABLE_MB_DTRS = str(item[12])
			USED_OF_MAX_PCT_ITRS = str(item[13])
			USED_OF_MAX_PCT_WTRS = str(item[14])
			USED_OF_MAX_PCT_DTRS = str(item[15])			
						
			#zabbix_item_name = "instance: " + str(item[0]) + ", db: " + str(item[1]) + ", host: " + str(item[2]) + ", metric group: " + str(item[3]) + ", tablespace: " + str(item[4])
			#			,"{#USED_OF_MAX_PCT_DTRS}": "' + USED_OF_MAX_PCT_DTRS + '"
			
			if db_res_count <> 0: 
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#TABLESPACE_NAME}": "' + TABLESPACE_NAME + '","{#CURRENT_MB}": "' + CURRENT_MB + '","{#MAX_MB}": "' + MAX_MB + '","{#USED_MB}": "' + USED_MB + '","{#AVAILABLE_MB}": "' + AVAILABLE_MB + '","{#USED_OF_MAX_PCT}": "' + USED_OF_MAX_PCT + '","{#AVAILABLE_MB_ITRS}": "' + AVAILABLE_MB_ITRS + '","{#AVAILABLE_MB_WTRS}": "' + AVAILABLE_MB_WTRS + '","{#AVAILABLE_MB_DTRS}": "' + AVAILABLE_MB_DTRS + '","{#USED_OF_MAX_PCT_ITRS}": "' + USED_OF_MAX_PCT_ITRS + '","{#USED_OF_MAX_PCT_WTRS}": "' + USED_OF_MAX_PCT_WTRS + '","{#USED_OF_MAX_PCT_DTRS}": "' + USED_OF_MAX_PCT_DTRS + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#TABLESPACE_NAME}": "' + TABLESPACE_NAME + '","{#CURRENT_MB}": "' + CURRENT_MB + '","{#MAX_MB}": "' + MAX_MB + '","{#USED_MB}": "' + USED_MB + '","{#AVAILABLE_MB}": "' + AVAILABLE_MB + '","{#USED_OF_MAX_PCT}": "' + USED_OF_MAX_PCT + '","{#AVAILABLE_MB_ITRS}": "' + AVAILABLE_MB_ITRS + '","{#AVAILABLE_MB_WTRS}": "' + AVAILABLE_MB_WTRS + '","{#AVAILABLE_MB_DTRS}": "' + AVAILABLE_MB_DTRS + '","{#USED_OF_MAX_PCT_ITRS}": "' + USED_OF_MAX_PCT_ITRS + '","{#USED_OF_MAX_PCT_WTRS}": "' + USED_OF_MAX_PCT_WTRS + '","{#USED_OF_MAX_PCT_DTRS}": "' + USED_OF_MAX_PCT_DTRS + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
			
	# items status
	if args["item"] == "Status" and args["id"] is not None:
		
		# /tmp/oracle/ > list of data for item status (all_items)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_all_items"
		items = read_from_file(filename)
		
		item_out = ""

		if args["statusmode"] == "current_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[5]
					break

		elif args["statusmode"] == "max_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[6]
					break
					
		elif args["statusmode"] == "used_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[7]
					break
					
		elif args["statusmode"] == "used_of_max_pct":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[9]
					break
					
		elif args["statusmode"] == "available_mb":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[8]
					break

		elif args["statusmode"] == "available_mb_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[10]
					break
					
		elif args["statusmode"] == "available_mb_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[11]
					break
					
		elif args["statusmode"] == "available_mb_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[12]
					break
					
		elif args["statusmode"] == "used_of_max_pct_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[13]
					break
					
		elif args["statusmode"] == "used_of_max_pct_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[14]
					break
					
		elif args["statusmode"] == "used_of_max_pct_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[15]
					break					
		
		print (item_out)	


################################# ZBV_PROCESSES #################################
		
elif item_type == 'ZBV_PROCESSES':

	# Data for Items
	if args["item"] == "Data":
	
		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		processes_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, RESOURCE_NAME, USED, LIMIT, FREE, USED_PCT," + "\n" + \
		"nvl(FREE_ITRS, 10000000) as FREE_ITRS," + "\n" + \
		"nvl(FREE_WTRS, 10000000) as FREE_WTRS," + "\n" + \
		"nvl(FREE_DTRS, 10000000) as FREE_DTRS," + "\n" + \
		"nvl(USED_PCT_ITRS, 10000000) as USED_PCT_ITRS," + "\n" + \
		"nvl(USED_PCT_WTRS, 10000000) as USED_PCT_WTRS," + "\n" + \
		"nvl(USED_PCT_DTRS, 10000000) as USED_PCT_DTRS" + "\n" + \
		"from ZBV_PROCESSES_FLG"

		cur = db.cursor()
		cur.execute(processes_query_str)
		db_res = cur.fetchall()
		db.close()
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)	

		print "OK"


	# Data for Discovery
	if args["item"] == "Discovery":

		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		processes_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, RESOURCE_NAME, USED, LIMIT, FREE, USED_PCT," + "\n" + \
		"nvl(FREE_ITRS, 10000000) as FREE_ITRS," + "\n" + \
		"nvl(FREE_WTRS, 10000000) as FREE_WTRS," + "\n" + \
		"nvl(FREE_DTRS, 10000000) as FREE_DTRS," + "\n" + \
		"nvl(USED_PCT_ITRS, 10000000) as USED_PCT_ITRS," + "\n" + \
		"nvl(USED_PCT_WTRS, 10000000) as USED_PCT_WTRS," + "\n" + \
		"nvl(USED_PCT_DTRS, 10000000) as USED_PCT_DTRS" + "\n" + \
		"from ZBV_PROCESSES_FLG"

		cur = db.cursor()
		cur.execute(processes_query_str)
		db_res = cur.fetchall()
		db.close()
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)				
		
		# create json
		db_res_count = len(db_res) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for item in db_res:
			db_res_count -= 1 # to remove last comma
		
			item_id = str(item[4])		
			INSTANCE_NAME = str(item[0])		
			DB_UNIQUE_NAME = str(item[1])	
			HOST_NAME = str(item[2])	
			METRIC_GROUP = str(item[3])	
			RESOURCE_NAME = str(item[4])	
			USED = str(item[5])	
			LIMIT = str(item[6])	
			FREE = str(item[7])	
			USED_PCT = str(item[8])	
			FREE_ITRS = str(item[9])	
			FREE_WTRS = str(item[10])	
			FREE_DTRS = str(item[11])	
			USED_PCT_ITRS = str(item[12])	
			USED_PCT_WTRS = str(item[13])	
			USED_PCT_DTRS = str(item[14])				
			
			if db_res_count <> 0: 
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#RESOURCE_NAME}": "' + RESOURCE_NAME + '","{#USED}": "' + USED + '","{#LIMIT}": "' + LIMIT + '","{#FREE}": "' + FREE + '","{#USED_PCT}": "' + USED_PCT + '","{#FREE_ITRS}": "' + FREE_ITRS + '","{#FREE_WTRS}": "' + FREE_WTRS + '","{#FREE_DTRS}": "' + FREE_DTRS + '","{#USED_PCT_ITRS}": "' + USED_PCT_ITRS + '","{#USED_PCT_WTRS}": "' + USED_PCT_WTRS + '","{#USED_PCT_DTRS}": "' + USED_PCT_DTRS + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#RESOURCE_NAME}": "' + RESOURCE_NAME + '","{#USED}": "' + USED + '","{#LIMIT}": "' + LIMIT + '","{#FREE}": "' + FREE + '","{#USED_PCT}": "' + USED_PCT + '","{#FREE_ITRS}": "' + FREE_ITRS + '","{#FREE_WTRS}": "' + FREE_WTRS + '","{#FREE_DTRS}": "' + FREE_DTRS + '","{#USED_PCT_ITRS}": "' + USED_PCT_ITRS + '","{#USED_PCT_WTRS}": "' + USED_PCT_WTRS + '","{#USED_PCT_DTRS}": "' + USED_PCT_DTRS + '"}'
				
		zabbix_inventory_json += ']}'
		print zabbix_inventory_json			
			
			
	# items status
	if args["item"] == "Status" and args["id"] is not None:
		
		# /tmp/oracle/ > list of data for item status (all_items)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_all_items"
		items = read_from_file(filename)
		
		item_out = ""
		
		if args["statusmode"] == "used":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[5]
					break
					
		elif args["statusmode"] == "limit":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[6]
					break		

		elif args["statusmode"] == "free":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[7]
					break		

		elif args["statusmode"] == "used_pct":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[8]
					break		

		elif args["statusmode"] == "free_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[9]
					break		

		elif args["statusmode"] == "free_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[10]
					break	

		elif args["statusmode"] == "free_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[11]
					break						
					
		elif args["statusmode"] == "used_pct_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[12]
					break
					
		elif args["statusmode"] == "used_pct_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[13]
					break
					
		elif args["statusmode"] == "used_pct_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[14]
					break
						
		print (item_out)						
		
		
################################# ZBV_FRA #################################

elif item_type == 'ZBV_FRA':

	# Data for Items
	if args["item"] == "Data":
	
		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		fra_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, FRA_GROUP, CURRENT_MB, USED_MB, MAX_MB, FREE_MB, USED_PCT," + "\n" + \
		"nvl(FREE_MB_ITRS, 10000000) as FREE_MB_ITRS," + "\n" + \
		"nvl(FREE_MB_WTRS, 10000000) as FREE_MB_WTRS," + "\n" + \
		"nvl(FREE_MB_DTRS, 10000000) as FREE_MB_DTRS," + "\n" + \
		"nvl(USED_PCT_ITRS, 10000000) as USED_PCT_ITRS," + "\n" + \
		"nvl(USED_PCT_WTRS, 10000000) as USED_PCT_WTRS," + "\n" + \
		"nvl(USED_PCT_DTRS, 10000000) as USED_PCT_DTRS" + "\n" + \
		"from ZBV_FRA_FLG"		

		cur = db.cursor()
		cur.execute(fra_query_str)
		db_res = cur.fetchall()
		db.close()
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)		
		
		print "OK"


	# Data for Discovery
	if args["item"] == "Discovery":

		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		fra_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, FRA_GROUP, CURRENT_MB, USED_MB, MAX_MB, FREE_MB, USED_PCT," + "\n" + \
		"nvl(FREE_MB_ITRS, 10000000) as FREE_MB_ITRS," + "\n" + \
		"nvl(FREE_MB_WTRS, 10000000) as FREE_MB_WTRS," + "\n" + \
		"nvl(FREE_MB_DTRS, 10000000) as FREE_MB_DTRS," + "\n" + \
		"nvl(USED_PCT_ITRS, 10000000) as USED_PCT_ITRS," + "\n" + \
		"nvl(USED_PCT_WTRS, 10000000) as USED_PCT_WTRS," + "\n" + \
		"nvl(USED_PCT_DTRS, 10000000) as USED_PCT_DTRS" + "\n" + \
		"from ZBV_FRA_FLG"		

		cur = db.cursor()
		cur.execute(fra_query_str)
		db_res = cur.fetchall()
		db.close()
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)					
		
		# create json
		db_res_count = len(db_res) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for item in db_res:
			db_res_count -= 1 # to remove last comma
		
			item_id = str(item[4])		
			INSTANCE_NAME = str(item[0])		
			DB_UNIQUE_NAME = str(item[1])		
			HOST_NAME = str(item[2])		
			METRIC_GROUP = str(item[3])		
			FRA_GROUP = str(item[4])		
			CURRENT_MB = str(item[5])		
			USED_MB = str(item[6])		
			MAX_MB = str(item[7])		
			FREE_MB = str(item[8])		
			USED_PCT = str(item[9])		
			FREE_MB_ITRS = str(item[10])		
			FREE_MB_WTRS = str(item[11])		
			FREE_MB_DTRS = str(item[12])		
			USED_PCT_ITRS = str(item[13])		
			USED_PCT_WTRS = str(item[14])		
			USED_PCT_DTRS = str(item[15])		
			
			if db_res_count <> 0: 
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#FRA_GROUP}": "' + FRA_GROUP + '","{#CURRENT_MB}": "' + CURRENT_MB + '","{#USED_MB}": "' + USED_MB + '","{#MAX_MB}": "' + MAX_MB + '","{#FREE_MB}": "' + FREE_MB + '","{#USED_PCT}": "' + USED_PCT + '","{#FREE_MB_ITRS}": "' + FREE_MB_ITRS + '","{#FREE_MB_WTRS}": "' + FREE_MB_WTRS + '","{#FREE_MB_DTRS}": "' + FREE_MB_DTRS + '","{#USED_PCT_ITRS}": "' + USED_PCT_ITRS + '","{#USED_PCT_WTRS}": "' + USED_PCT_WTRS + '","{#USED_PCT_DTRS}": "' + USED_PCT_DTRS + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#FRA_GROUP}": "' + FRA_GROUP + '","{#CURRENT_MB}": "' + CURRENT_MB + '","{#USED_MB}": "' + USED_MB + '","{#MAX_MB}": "' + MAX_MB + '","{#FREE_MB}": "' + FREE_MB + '","{#USED_PCT}": "' + USED_PCT + '","{#FREE_MB_ITRS}": "' + FREE_MB_ITRS + '","{#FREE_MB_WTRS}": "' + FREE_MB_WTRS + '","{#FREE_MB_DTRS}": "' + FREE_MB_DTRS + '","{#USED_PCT_ITRS}": "' + USED_PCT_ITRS + '","{#USED_PCT_WTRS}": "' + USED_PCT_WTRS + '","{#USED_PCT_DTRS}": "' + USED_PCT_DTRS + '"}'			

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json						
			

	# items status
	if args["item"] == "Status" and args["id"] is not None:
		
		# /tmp/oracle/ > list of data for item status (all_items)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_all_items"
		items = read_from_file(filename)
		
		item_out = ""
		
		if args["statusmode"] == "current":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[5]
					break
			
		elif args["statusmode"] == "used":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[6]
					break		
					
		elif args["statusmode"] == "max":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[7]
					break			

		elif args["statusmode"] == "free":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[8]
					break							

		elif args["statusmode"] == "used_pct":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[9]
					break	

		elif args["statusmode"] == "free_mb_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[10]
					break			

		elif args["statusmode"] == "free_mb_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[11]
					break							

		elif args["statusmode"] == "free_mb_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[12]
					break		

		elif args["statusmode"] == "used_pct_itrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[13]
					break	
					
		elif args["statusmode"] == "used_pct_wtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[14]
					break	
					
		elif args["statusmode"] == "used_pct_dtrs":
			for item in items:
				item_id = str(item[4])
				if item_id == args["id"]:
					item_out = item[15]
					break						
					
		print (item_out)		
					
					
################################# ZBV_UPTIME #################################

elif item_type == 'ZBV_UPTIME':

	# Data for Items
	if args["item"] == "Data":
	
		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		uptime_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, TO_CHAR (STARTUP_TIME), TO_CHAR(UPTIME_INTERVAL), UPTIME_MI," + "\n" + \
		"nvl(UPTIME_MI_ITRS, 10000000) as UPTIME_MI_ITRS," + "\n" + \
		"nvl(UPTIME_MI_WTRS, 10000000) as UPTIME_MI_WTRS," + "\n" + \
		"nvl(UPTIME_MI_DTRS, 10000000) as UPTIME_MI_DTRS" + "\n" + \
		"from ZBV_UPTIME_FLG"
		
		cur = db.cursor()
		cur.execute(uptime_query_str)
		db_res = cur.fetchall()
		db.close()
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)			
		
		print "OK"
	

	# Data for Discovery
	if args["item"] == "Discovery":

		dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
		db = cx_Oracle.connect(user, pwd, dsn_tns)
		
		uptime_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME, METRIC_GROUP, TO_CHAR (STARTUP_TIME), TO_CHAR(UPTIME_INTERVAL), UPTIME_MI," + "\n" + \
		"nvl(UPTIME_MI_ITRS, 10000000) as UPTIME_MI_ITRS," + "\n" + \
		"nvl(UPTIME_MI_WTRS, 10000000) as UPTIME_MI_WTRS," + "\n" + \
		"nvl(UPTIME_MI_DTRS, 10000000) as UPTIME_MI_DTRS" + "\n" + \
		"from ZBV_UPTIME_FLG"
		
		cur = db.cursor()
		cur.execute(uptime_query_str)
		db_res = cur.fetchall()
		db.close()
		
		# list of data for item status (all_items) > /tmp/oracle/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
		write_to_file(filename, db_res)			

		# create json
		db_res_count = len(db_res) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for item in db_res:
			db_res_count -= 1 # to remove last comma
			
			item_id = str(item[3])
			INSTANCE_NAME = str(item[0])
			DB_UNIQUE_NAME = str(item[1])
			HOST_NAME = str(item[2])
			METRIC_GROUP = str(item[3])
			STARTUP_TIME = str(item[4])
			UPTIME_INTERVAL = str(item[5])
			UPTIME_MI = str(item[6])			
			UPTIME_MI_ITRS = str(item[7])
			UPTIME_MI_WTRS = str(item[8])
			UPTIME_MI_DTRS = str(item[9])		
			
			if db_res_count <> 0: 
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#STARTUP_TIME}": "' + STARTUP_TIME + '","{#UPTIME_INTERVAL}": "' + UPTIME_INTERVAL + '","{#UPTIME_MI}": "' + UPTIME_MI + '","{#UPTIME_MI_ITRS}": "' + UPTIME_MI_ITRS + '","{#UPTIME_MI_WTRS}": "' + UPTIME_MI_WTRS + '","{#UPTIME_MI_DTRS}": "' + UPTIME_MI_DTRS + '"}, '	
			else: # to remove last comma
				zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#STARTUP_TIME}": "' + STARTUP_TIME + '","{#UPTIME_INTERVAL}": "' + UPTIME_INTERVAL + '","{#UPTIME_MI}": "' + UPTIME_MI + '","{#UPTIME_MI_ITRS}": "' + UPTIME_MI_ITRS + '","{#UPTIME_MI_WTRS}": "' + UPTIME_MI_WTRS + '","{#UPTIME_MI_DTRS}": "' + UPTIME_MI_DTRS + '"}'			

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json					

			
	# items status
	if args["item"] == "Status" and args["id"] is not None:
		
		# /tmp/oracle/ > list of data for item status (all_items)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_all_items"
		items = read_from_file(filename)
		
		item_out = ""
		
		if args["statusmode"] == "startup_time":
			for item in items:
				item_id = str(item[3])
				if item_id == args["id"]:
					item_out = item[4]
					break
			
		elif args["statusmode"] == "uptime_interval":
			for item in items:
				item_id = str(item[3])
				if item_id == args["id"]:
					item_out = item[5]
					break					
		
		elif args["statusmode"] == "uptime_mi":
			for item in items:
				item_id = str(item[3])
				if item_id == args["id"]:
					item_out = item[6]
					break				

		elif args["statusmode"] == "uptime_mi_itrs":
			for item in items:
				item_id = str(item[3])
				if item_id == args["id"]:
					item_out = item[7]
					break							
					
		elif args["statusmode"] == "uptime_mi_wtrs":
			for item in items:
				item_id = str(item[3])
				if item_id == args["id"]:
					item_out = item[8]
					break			

		elif args["statusmode"] == "uptime_mi_dtrs":
			for item in items:
				item_id = str(item[3])
				if item_id == args["id"]:
					item_out = item[9]
					break						
					
		print (item_out)		
################################# ZBV_LOCK #################################

elif item_type == 'ZBV_LOCK':

        # Data for Items
        if args["item"] == "Data":

                dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
                db = cx_Oracle.connect(user, pwd, dsn_tns)

                lock_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME,METRIC_GROUP,SID," + "\n" + \
                "STATUS, USERNAME, OSUSER, MACHINE, MODULE, LOCK_TYPE, MODE_HELD, MODE_REQUESTED, OBJECT_TYPE, WAITED_OBJECT, BLOCK, CTIME, WAIT4LOCK_MI, CURRENT_SQL_ID," + "\n" + \
                "nvl(WAIT4LOCK_MI_ITRS, 10000000) as WAIT4LOCK_MI_ITRS," + "\n" + \
                "nvl(WAIT4LOCK_MI_WTRS, 10000000) as WAIT4LOCK_MI_WTRS," + "\n" + \
                "nvl(WAIT4LOCK_MI_DTRS, 10000000) as WAIT4LOCK_MI_DTRS" + "\n" + \
                "from ZBV_LOCK_FLG"

                cur = db.cursor()
                cur.execute(lock_query_str)
                db_res = cur.fetchall()
                db.close()

                # list of data for item status (all_items) > /tmp/oracle/
                filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
                write_to_file(filename, db_res)

                print "OK"


        # Data for Discovery
        if args["item"] == "Discovery":

                dsn_tns = cx_Oracle.makedsn(str(host), str(port), service_name=str(service))
                db = cx_Oracle.connect(user, pwd, dsn_tns)

                lock_query_str = "select INSTANCE_NAME, DB_UNIQUE_NAME, HOST_NAME,METRIC_GROUP,SID," + "\n" + \
                "STATUS, USERNAME, OSUSER, MACHINE, MODULE, LOCK_TYPE, MODE_HELD, MODE_REQUESTED, OBJECT_TYPE, WAITED_OBJECT, BLOCK, CTIME, WAIT4LOCK_MI, CURRENT_SQL_ID," + "\n" + \
                "nvl(WAIT4LOCK_MI_ITRS, 10000000) as WAIT4LOCK_MI_ITRS," + "\n" + \
                "nvl(WAIT4LOCK_MI_WTRS, 10000000) as WAIT4LOCK_MI_WTRS," + "\n" + \
                "nvl(WAIT4LOCK_MI_DTRS, 10000000) as WAIT4LOCK_MI_DTRS" + "\n" + \
                "from ZBV_LOCK_FLG"

                cur = db.cursor()
                cur.execute(lock_query_str)
                db_res = cur.fetchall()
                db.close()

                # list of data for item status (all_items) > /tmp/oracle/
                filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "all_items"
                write_to_file(filename, db_res)

                # create json
                db_res_count = len(db_res) # to remove last comma
                zabbix_inventory_json = '{"data":['

                for item in db_res:
                        db_res_count -= 1 # to remove last comma

                        item_id                    = nonestr(item[4])
                        INSTANCE_NAME              = nonestr(item[0])
                        DB_UNIQUE_NAME             = nonestr(item[1])
                        HOST_NAME                  = nonestr(item[2])
                        METRIC_GROUP               = nonestr(item[3])
                        SID                        = nonestr(item[4])
                        STATUS                     = nonestr(item[5])
                        USERNAME                   = nonestr(item[6])
                        OSUSER                     = nonestr(item[7])
                        MACHINE                    = nonestr(item[8])
                        MODULE                     = nonestr(item[9])
                        LOCK_TYPE                  = nonestr(item[10])
                        MODE_HELD                  = nonestr(item[11])
                        MODE_REQUESTED             = nonestr(item[12])
                        OBJECT_TYPE                = nonestr(item[13])
                        WAITED_OBJECT              = nonestr(item[14])
                        BLOCK                      = nonestr(item[15])
                        CTIME                      = nonestr(item[16])
                        WAIT4LOCK_MI               = nonestr(item[17])
                        CURRENT_SQL_ID             = nonestr(item[18])
                        WAIT4LOCK_MI_ITRS          = nonestr(item[19])
                        WAIT4LOCK_MI_WTRS          = nonestr(item[20])
                        WAIT4LOCK_MI_DTRS          = nonestr(item[21])

                        if db_res_count <> 0:
                                zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#SID}": "' + SID + '","{#LOCK_TYPE}": "' + LOCK_TYPE + '","{#MODE_HELD}": "' + MODE_HELD + '","{#MODE_REQUESTED}": "' + MODE_REQUESTED + '","{#WAIT4LOCK_MI}": "' + WAIT4LOCK_MI + '","{#BLOCK}": "' + BLOCK + '","{#USERNAME}": "' + USERNAME + '","{#OSUSER}": "' + OSUSER + '","{#PROGRAM}": "' + PROGRAM + '","{#TERMINAL}": "' + TERMINAL + '","{#MODULE}": "' + MODULE + '","{#OBJECT_TYPE}": "' + OBJECT_TYPE + '","{#OBJECT}": "' + OBJECT + '","{#STATUS}": "' + STATUS + '","{#SQL_ID}": "' + SQL_ID + '","{#WAIT4LOCK_MI_ITRS}": "' + WAIT4LOCK_MI_ITRS + '","{#WAIT4LOCK_MI_WTRS}": "' + WAIT4LOCK_MI_WTRS + '","{#WAIT4LOCK_MI_DTRS}": "' + WAIT4LOCK_MI_DTRS + '"}, '
                        else: # to remove last comma
                                zabbix_inventory_json += '{"{#ID}": "' + item_id + '","{#INSTANCE_NAME}": "' + INSTANCE_NAME + '","{#DB_UNIQUE_NAME}": "' + DB_UNIQUE_NAME + '","{#HOST_NAME}": "' + HOST_NAME + '","{#METRIC_GROUP}": "' + METRIC_GROUP + '","{#SID}": "' + SID + '","{#LOCK_TYPE}": "' + LOCK_TYPE + '","{#MODE_HELD}": "' + MODE_HELD + '","{#MODE_REQUESTED}": "' + MODE_REQUESTED + '","{#WAIT4LOCK_MI}": "' + WAIT4LOCK_MI + '","{#BLOCK}": "' + BLOCK + '","{#USERNAME}": "' + USERNAME + '","{#OSUSER}": "' + OSUSER + '","{#PROGRAM}": "' + PROGRAM + '","{#TERMINAL}": "' + TERMINAL + '","{#MODULE}": "' + MODULE + '","{#OBJECT_TYPE}": "' + OBJECT_TYPE + '","{#OBJECT}": "' + OBJECT + '","{#STATUS}": "' + STATUS + '","{#SQL_ID}": "' + SQL_ID + '","{#WAIT4LOCK_MI_ITRS}": "' + WAIT4LOCK_MI_ITRS + '","{#WAIT4LOCK_MI_WTRS}": "' + WAIT4LOCK_MI_WTRS + '","{#WAIT4LOCK_MI_DTRS}": "' + WAIT4LOCK_MI_DTRS + '"}'

                zabbix_inventory_json += ']}'
                print zabbix_inventory_json


        # items status
        if args["item"] == "Status" and args["id"] is not None:

                # /tmp/oracle/ > list of data for item status (all_items)
                filename = str(args["host"]) + "_" +  str(args["type"])  + "_all_items"
                items = read_from_file(filename)

                item_out = "99999999999999999"

                if args["statusmode"] == "lock_type":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[5])
                                        break

                elif args["statusmode"] == "mode_held":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[6])
                                        break

                elif args["statusmode"] == "mode_requested":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[7])
                                        break

                elif args["statusmode"] == "wait4Lock_mi":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[8])
                                        break

                elif args["statusmode"] == "block":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[9])
                                        break

                elif args["statusmode"] == "username":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[10])
                                        break

                elif args["statusmode"] == "osuser":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[11])
                                        break

                elif args["statusmode"] == "program":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[12])
                                        break

                elif args["statusmode"] == "terminal":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[13])
                                        break

                elif args["statusmode"] == "module":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[14])
                                        break

                elif args["statusmode"] == "object_type":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[15])
                                        break

                elif args["statusmode"] == "object":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[16])
                                        break

                elif args["statusmode"] == "status":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[17])
                                        break

                elif args["statusmode"] == "sql_id":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[18])
                                        break

                elif args["statusmode"] == "wait4Lock_mi_itrs":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[19])
                                        break

                elif args["statusmode"] == "wait4Lock_mi_wtrs":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[20])
                                        break

                elif args["statusmode"] == "wait4Lock_mi_dtrs":
                        for item in items:
                                item_id = str(item[4])
                                if item_id == args["id"]:
                                        item_out = nonestr(item[21])
                                        break

                print (item_out)




