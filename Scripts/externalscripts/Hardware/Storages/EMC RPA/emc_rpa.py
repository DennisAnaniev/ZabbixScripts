#!/usr/bin/env python

import os
import sys
import subprocess
import re
import requests
import ast
import json
import argparse
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Credentials
user = 'zabbix'
passw = '4Monit0r!'
hostIP = '10.45.101.192'
port = '7225'
###########
tmp_dir = '/usr/local/share/zabbix/externalscripts/rpa/'
filerpa_in = '/usr/local/share/zabbix/externalscripts/rpa/rpa_script.cli'
filerpa_out = '/usr/local/share/zabbix/externalscripts/rpa/rpas'
filegroup_in = '/usr/local/share/zabbix/externalscripts/rpa/group_script.cli'
filegroup_out = '/usr/local/share/zabbix/externalscripts/rpa/groups'
filesystem_out = '/usr/local/share/zabbix/externalscripts/rpa/system'
clusterArray = list()
groupArray = list()
rpastateArray = list()
ethArray = list()
fcArray = list()
rpastatisticArray = list()
##  CLI
clusterArrayCLI = list()
sanArrayCLI = list()
groupArrayCLI = list()
lagArrayCLI = list()
sysstatArrayCLI = list()

## for cluster (zabbix node)
groupClusterArray = list()
rpastateClusterArray = list()
ethClusterArray = list()
rpastatisticClusterArray = list()
fcClusterArray = list()
sanClusterArrayCLI = list()
sysstatClusterArrayCLI = list()


# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False)
ap.add_argument("--type", required=True)
ap.add_argument("--item", required=True)
ap.add_argument("--statusmode", required=False)
ap.add_argument("--id", required=False)
ap.add_argument("--test", required=False)
args = vars(ap.parse_args())

item_type = args["type"]
cluster_name = args["host"]


## state list > /tmp/rpa
def write_to_file(filename, data):
  with open(tmp_dir + filename + '.tmp', 'w+') as f1:
      f1.write(str(data))
      try:
	      os.remove(tmp_dir + filename)
      except OSError:
	      pass
      os.rename(tmp_dir + filename + '.tmp', tmp_dir + filename)
      f1.close()

## /tmp/rpa > state list
def read_from_file(filename):
  f1 = open(tmp_dir + filename, 'r')
  data1 = f1.read().replace("u'", "'")
  data2 = ast.literal_eval(data1)
  return data2

  
 ### get all data
if args["item"] == "Discovery" or args["item"] == "Data":

	# Clusters
	cl = "https://{0}:{1}/fapi/rest/5_1/clusters/".format(hostIP, port)
	req = requests.get(cl, auth=HTTPBasicAuth(user, passw), verify=False)
	for item in req.json()['clustersInformation']:
		clusterArray.append((item['clusterName'], item['clusterUID']['id']))
	#
	# Groups
	gr = "https://{0}:{1}/fapi/rest/5_1/groups/settings".format(hostIP, port)
	grtransfer = "https://{0}:{1}/fapi/rest/5_1/groups/transfer_state".format(hostIP, port)
	req = requests.get(grtransfer, auth=HTTPBasicAuth(user, passw), verify=False)
	for item in req.json()['innerSet']:
		groupName = item['groupName']
		transferState = item['transferState']
		sourceClusterName = item['sourceClusterName']
		groupArray.append((groupName, transferState, sourceClusterName))
	#
	# RPAs state, Ethernets status
	rpa = "https://{0}:{1}/fapi/rest/5_1/rpas/state".format(hostIP, port)
	req = requests.get(rpa, auth=HTTPBasicAuth(user, passw), verify=False)
	for item in req.json()['innerSet']:
		clusterUID = item['clusterUID']['id']
		for item in item['rpasState']:
			stat = item['status']
			rpaNumber = item['rpaUID']['rpaNumber']
			eth = item['interfacesStatus'][0]['networkInterface']
			ethstatus = item['interfacesStatus'][0]['interfaceStatus']
			remoteRPAsConnectivityStatus = item['remoteRPAsConnectivityStatus'][0]['connectivityStatus']
			majorVersion = str(item['version']['versionInformation']['major'])
			minorVersion = str(item['version']['versionInformation']['minor'])
			if re.search(r'\d+$', majorVersion) and re.search(r'\d+$', minorVersion):
				softstatus = "OK"
			else:
				softstatus = "Cannot determine software version"
			for item in item['localRPAsFiberConnectivityStatus']:
				if item['connectivityStatus'] == "OK":
					localRPAsFiberConnectivityStatus = "OK"
				else:
					localRPAsFiberConnectivityStatus = item['connectivityStatus']
					break
			rpastateArray.append((clusterUID, rpaNumber, stat, localRPAsFiberConnectivityStatus, softstatus))
			ethArray.append((clusterUID, rpaNumber, eth, ethstatus, remoteRPAsConnectivityStatus))
	#
	# FC
	for item in req.json()['innerSet']:
		clusterUID = item['clusterUID']['id']
		for item in item['rpasState']:
			rpaNumber = item['rpaUID']['rpaNumber']
			for item in item['initiatorsState']:
				fcArray.append((clusterUID, rpaNumber, item['portWWN']))
	#
	# RPAs statistics
	rpastatistic = "https://{0}:{1}/fapi/rest/5_1/rpas/statistics".format(hostIP, port)
	req = requests.get(rpastatistic, auth=HTTPBasicAuth(user, passw), verify=False)
	for item in req.json()['innerSet']:
		clusterUID = item['rpaUID']['clusterUID']['id']
		rpaNumber = item['rpaUID']['rpaNumber']
		cpu = item['cpuUsage']
		IncomingWrites = item['traffic']['applicationIncomingWrites']
		try:
			ratio = item['traffic']['connectionsCompressionRatio'][0]['compressionRatio']
		except IndexError:
			ratio = 0
		try:
			applicationTraffic = (item['traffic']['applicationThroughputStatistics']['connectionsOutThroughput'][0]['outThroughput'] + item['traffic']['applicationThroughputStatistics']['inThroughput']) * 8
			applicationTraffic = applicationTraffic / 1000000
		except IndexError:
			applicationTraffic = item['traffic']['applicationThroughputStatistics']['inThroughput'] * 8 / 1000000
		rpastatisticArray.append((clusterUID, rpaNumber, cpu, ratio, IncomingWrites, applicationTraffic))

		
	## CLI ##################################
	def protectwindowValue(x):
		timevalues = {'hr': 3600, 'days': 86400, 'weeks': 604800, 'months': 2592000}
		a = x.split()
		ii = 0
		protectvalue = 0
		for item in a:
			if item in timevalues:
				protectvalue = protectvalue + (int(a[ii - 1]) * timevalues[item])
			ii += 1
		return protectvalue
			
	cl = "https://{0}:{1}/fapi/rest/5_1/clusters/".format(hostIP, port)
	req = requests.get(cl, auth=HTTPBasicAuth(user, passw), verify=False)
	for item in req.json()['clustersInformation']:
		clusterArrayCLI.append(item['clusterName'])

	# SAN utilization (MBps)
	cli_rpastat = "sshpass -p {0} ssh -T -o StrictHostKeyChecking=no {1}@{2} < {3} > {4}".format(passw, user, hostIP, filerpa_in, filerpa_out)
	p = subprocess.Popen(cli_rpastat, shell=True)
	p.wait()
	f1 = open(filerpa_out, 'r')
	b = ""
	for line in f1:
		if line.strip().replace(':',"") in clusterArrayCLI:
			if b.split()[0] == 'Packet' or b == 'All RPAs:':
				cl_name = line.strip().replace(':',"")  
		if re.search("RPA " + r'\d+', line):
			rpa = line.strip().replace(':',"")
		if b == 'Application throughput:':
			if 'SAN:' in line:
				san = line.strip().split()
				if san[2] == 'bps':
					sanutil = int(san[1]) / 8000000
				elif san[2] == 'Mbps':
					sanutil = int(san[1]) / 8
				elif san[2] == 'Gbps':
					sanutil = int(san[1]) * 1000 / 8
				sanArrayCLI.append((cl_name, rpa, sanutil))
		if re.search(r'\w+', line):
			b = line.strip()
	f1.close()
	#
	# Replication lag
	grtransfer = "https://{0}:{1}/fapi/rest/5_1/groups/transfer_state".format(hostIP, port)
	req = requests.get(grtransfer, auth=HTTPBasicAuth(user, passw), verify=False)
	for item in req.json()['innerSet']:
		groupName = item['groupName']
		groupArrayCLI.append(groupName) 

	cli_groupstat = "sshpass -p {0} ssh -T -o StrictHostKeyChecking=no {1}@{2} < {3} > {4}".format(passw, user, hostIP, filegroup_in, filegroup_out)
	p = subprocess.Popen(cli_groupstat, shell=True)
	p.wait()
	f2 = open(filegroup_out, 'r')
	b = ""
	iii = 0
	for line in f2:
		if line.strip().replace(':',"") in groupArrayCLI:
			if b == 'Group:' or b.split(':')[0] == 'Average deduplication ratio':
				gr_name = line.strip().replace(':',"")
		if b == 'Copy stats:':
			copy_name = line.strip().replace(':',"")
		if b == 'Current:':
			protectwin = line.split(':')[1].lstrip()
			protectwinsec = protectwindowValue(protectwin)
		if 'Status:' in line:
			if iii % 2 == 0:
				protectwinstat = line.split(':')[1].lstrip()
			iii += 1       
		if re.search("Mode: " + r'\w+', b):
			prod_name = line.strip().replace(':',"")
		if 'Time:' in b:
			lag = line.strip().replace('Data: ',"").split()
			if lag[1] == 'KB':
	#            lag1 = lag[0].split('.')
				lagdata = int(float(lag[0]) * 1024)
			if lag[1] == 'MB':
	#            lag1 = lag[0].split('.')
				lagdata = int(float(lag[0]) * 1024 * 1024)
			if lag[1] == 'GB':
	#            lag1 = lag[0].split('.')
				lagdata = int(float(lag[0]) * 1024 * 1024 * 1024)
			if lag[1] == 'B':
				lagdata = 0
			lagArrayCLI.append((gr_name, prod_name, copy_name, lagdata, protectwinsec, protectwinstat))
		if re.search(r'\w+', line):
			b = line.strip()
	f2.close()
	#
	# System common status
	command1 = 'get_system_status category=all'
	cli_systemstat = "sshpass -p {0} ssh -T -o StrictHostKeyChecking=no {1}@{2} {3} > {4}".format(passw, user, hostIP, command1, filesystem_out)
	p = subprocess.Popen(cli_systemstat, shell=True)
	p.wait()
	f3 = open(filesystem_out, 'r')
	b = ""
	for line in f3:
		if 'System problems:' in line:
			line1 = line.split(':')
			sysstat = line1[1].lstrip()
		if any(ext in line for ext in clusterArrayCLI):
			cln = line.strip().replace(':', "")
		if 'RPAs' in line:
			rpastat = line.split(':')[1].lstrip()
		if 'Volumes' in line:
			volstat = line.split(':')[1].lstrip()
		if 'Splitters' in line:
			splitstat = line.split(':')[1].lstrip()
			
			sysstatArrayCLI.append((cln, sysstat, rpastat, volstat, splitstat))
	f3.close()
	#

	#print sanArrayCLI
	#print lagArrayCLI
	#print sysstatArrayCLI
	
	## CLI ##################################
		
	#print sanArrayCLI
	#print lagArrayCLI
	
	#print clusterArray
	#print groupArray
	#print rpastateArray
	#print ethArray
	#print rpastatisticArray
	#print fcArray		
	
	## node filter
	
	for cluster in clusterArray:
		if cluster[0] == cluster_name:
			cluster_id = cluster[1] 
	
	for group in groupArray:
		if group[2] == cluster_name:
			groupClusterArray.append((group[0], group[1], group[2]))		
	
	for rpa in rpastateArray:
		if rpa[0] == cluster_id:
			rpastateClusterArray.append((rpa[0], rpa[1], rpa[2], rpa[3], rpa[4]))		
	
	for eth in ethArray:
		if eth[0] == cluster_id:
			ethClusterArray.append((eth[0], eth[1], eth[2], eth[3], eth[4]))	
			
	for rpas in rpastatisticArray:
		if rpas[0] == cluster_id:
			rpastatisticClusterArray.append((rpas[0], rpas[1], rpas[2], rpas[3], rpas[4], rpas[5]))

	for fc in fcArray:
		if fc[0] == cluster_id:
			fcClusterArray.append((fc[0], fc[1], fc[2]))				

	for rpasan in sanArrayCLI:
		if rpasan[0] == cluster_name:
			sanClusterArrayCLI.append((rpasan[0], rpasan[1], rpasan[2]))		

	for sysstat in sysstatArrayCLI:
		if sysstat[0] == cluster_name:
			sysstatClusterArrayCLI.append((sysstat[0], sysstat[1], sysstat[2], sysstat[3], sysstat[4]))
			
	
### end get all data		

if item_type == 'system' :
#System Status
#1 System status
#2 RPAs status
#3 Volumes status
#4 Splitters status

	# Data for Items
	if args["item"] == "Data":
	
		# list of data for item status (transfer state) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "System_data"
		write_to_file(filename, sysstatClusterArrayCLI)
		
		print "OK"

	# items status
	if args["item"] == "Status":
		
		# /tmp/oracle/ > list of data for item status (all_items)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_"  + "System_data"
		items = read_from_file(filename)		

		if args["statusmode"] == "SystemStatus":
				print items[0][1]

		elif args["statusmode"] == "RPAstatus":
				print items[0][2]
		
		elif args["statusmode"] == "VolumeStatus":
				print items[0][3]		
		
		elif args["statusmode"] == "SplitterStatus":
				print items[0][4]			
		
		
if item_type == 'rep_group':
#[0]	name
#[3]	replication lag

	# Data for Items
	if args["item"] == "Data":		
	
		# list of data for item status (transfer state) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Transfer_State"
		write_to_file(filename, groupClusterArray)			
		
		## CLI
		
		# list of data for item status (replication lag) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Rep_lag"
		write_to_file(filename, lagArrayCLI)
		
		# list of data for item status (Protection Window sec) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "PW"
		write_to_file(filename, lagArrayCLI)		
		
		# list of data for item status (Protection Window status) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "PWStatus"
		write_to_file(filename, lagArrayCLI)			
		
		print "OK"
		
	# Data for Discovery
	if args["item"] == "Discovery":
		
		# create json
		group_count = len(groupClusterArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for component in groupClusterArray:
			group_count -= 1 # to remove last comma
		
			group_name= component[0]
			group_id= component[0]
			zabbix_component_name = str(group_name)
			
			if group_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + group_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + group_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
	
	
	# transfer_state
	if args["item"] == "Status" and args["statusmode"] == "Transfer_State" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (transfer_state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				transfer_state = item[1]
				break
		
		print (transfer_state)		
	
	
	# replication lag
	if args["item"] == "Status" and args["statusmode"] == "Rep_lag" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (replication lag)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				rep_lag = item[3]
				break
		
		print (rep_lag)				

	# Protection Window (sec)
	if args["item"] == "Status" and args["statusmode"] == "PW" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (replication lag)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				pw = item[4]
				break
		
		print (pw)	
		
	# Protection Window Status
	if args["item"] == "Status" and args["statusmode"] == "PWStatus" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (replication lag)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				PWStatus = item[5]
				break
		
		print PWStatus		
		
		
if item_type == 'rpa':

#[0]	ID cluster
#[1]	number     "RPA" + number
#[2]	status
#[3]	connectivity status local RPA
#[4]	software status

#RPA (metrics)
#[0]	ID cluster
#[1]	number      "RPA" + number
#[2]	CPU usage
#[3]	compression ratio
#[4]	incoming writes
#[5]	throughput

	# Data for Items
	if args["item"] == "Data":			

		# list of data for item status (Status) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, rpastateClusterArray)		
	
		# list of data for item status (local connectivity status) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "LCon_stat"
		write_to_file(filename, rpastateClusterArray)				
	
		# list of data for item status (SStatus) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "SStatus"
		write_to_file(filename, rpastateClusterArray)
		
		## RPA metrics

		# list of data for item status (CPU) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "CPU"
		write_to_file(filename, rpastatisticClusterArray)		

		# list of data for item status (compression ratio) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "CRatio"
		write_to_file(filename, rpastatisticClusterArray)			
		
		# list of data for item status (incoming writes) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "IWrite"
		write_to_file(filename, rpastatisticClusterArray)			
		
		# list of data for item status (throughput) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Throughput"
		write_to_file(filename, rpastatisticClusterArray)

		## RPA CLI 

		# list of data for item status (RPA SAN utilization) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "SAN"
		write_to_file(filename, sanClusterArrayCLI)		

		print "OK"
		
	# Data for Discovery
	if args["item"] == "Discovery":

	
		# create json
		rpa_count = len(rpastateClusterArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for component in rpastateClusterArray:
			rpa_count -= 1 # to remove last comma
		
			rpa_name= str(component[1])
			rpa_id= str(component[1])
			zabbix_component_name = "RPA" + str(rpa_name)
			
			if rpa_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + rpa_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + rpa_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json	
		

	# status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (rpa_status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				rpa_status = item[2]
				break
		
		print (rpa_status)		
		
	#	connectivity status local 
	if args["item"] == "Status" and args["statusmode"] == "LCon_stat" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (LCon_stat)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				lcon_stat = item[3]
				break
		
		print (lcon_stat)	

	#	software status
	if args["item"] == "Status" and args["statusmode"] == "SStatus" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (SStatus)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				sstatus = item[4]
				break
		
		print (sstatus)			

	#	CPU Usage
	if args["item"] == "Status" and args["statusmode"] == "CPU" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (CPU Usage)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				cpu_usage = item[2]
				break
		
		print (cpu_usage)	

	#	compression ratio
	if args["item"] == "Status" and args["statusmode"] == "CRatio" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (compression ratio)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				cratio = item[3]
				break
		
		print (cratio)	

	#	incoming writes
	if args["item"] == "Status" and args["statusmode"] == "IWrite" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (incoming writes)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				iwrite = item[4]
				break
		
		print (iwrite)		

	#	Throughput
	if args["item"] == "Status" and args["statusmode"] == "Throughput" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (incoming writes)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				throughput = item[5]
				break
		
		print (throughput)			
		
	#	RPA SAN utilization
	if args["item"] == "Status" and args["statusmode"] == "SAN" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (incoming writes)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			rpa_name = "RPA " + str(args["id"])
			if str(item[1]) == rpa_name:
				san_u = item[2]
				break
		
		print (san_u)					

		
if item_type == 'eth':

#[0]	ID cluster
#[1]	number      "RPA" + number
#[2]	ethernet interface
#[3]	status
#[4]	connectivity status remote RPA

	# Data for Items
	if args["item"] == "Data":		
	
		# list of data for item status (Status) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, ethClusterArray)		
		
		# list of data for item status (connectivity status remote) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "RCon_stat"
		write_to_file(filename, ethClusterArray)		

		print "OK"

	# Data for Discovery
	if args["item"] == "Discovery":
		
	
		# create json
		rpa_count = len(ethClusterArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for component in ethClusterArray:
			rpa_count -= 1 # to remove last comma
		
			eth_interface= str(component[2])
			eth_number= str(component[1])
			eth_id = str(component[1])
			zabbix_component_name = "RPA" + str(eth_number) + " " + str(eth_interface)
			
			if rpa_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + eth_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + eth_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json	
		

	# status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (Status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				eth_status = item[3]
				break
		
		print (eth_status)		
		
	# remote connectivity status
	if args["item"] == "Status" and args["statusmode"] == "RCon_stat" and args["id"] is not None:
		
		# /tmp/rpa > list of data for item status (remote connectivity status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[1]) == args["id"]:
				rcon_stat = item[4]
				break
		
		print (rcon_stat)	
		

if item_type == 'fc':

#[0]	ID cluster
#[1]	number     "RPA" + number
#[2]	VVN

	# Data for Items
	if args["item"] == "Data":	
		
		# list of data for item status (Data) > /tmp/rpa/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Data"
		write_to_file(filename, fcClusterArray)		
		
		print "OK"
		
	# Data for Discovery
	if args["item"] == "Discovery":
		
		
		# create json
		rpa_count = len(fcClusterArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for component in fcClusterArray:
			rpa_count -= 1 # to remove last comma
		
			fc_name= str(component[1])
			fc_vvn= str(component[2])
			fc_id = str(component[2])
			zabbix_component_name = "RPA" + str(fc_name) + " (" + str(fc_vvn) + ")"
			
			if rpa_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + fc_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + fc_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json			
		
		
	# remote connectivity status
	if args["item"] == "Status" and args["statusmode"] == "Data" and args["id"] is not None:
		
		## /tmp/rpa > list of data for item status (remote connectivity status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		
		items = read_from_file(filename)
		
		for item in items:
			if str(item[2]) == args["id"]:
				fc_name = "RPA" + str(item[1])
				break
		
		print (fc_name)			