#!/usr/bin/env python

from os import popen
import subprocess
import sys
import time
import re
import os
import ast
import argparse
import json
import requests
import time
from collections import OrderedDict as od
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("--host", required=False)
ap.add_argument("--type", required=True)
ap.add_argument("--item", required=True)
ap.add_argument("--statusmode", required=False)
ap.add_argument("--id", required=False)
ap.add_argument("--test", required=False)
args = vars(ap.parse_args())

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers1 = {'Content-type':'application/json'}

tmp_dir = '/tmp/netapp/'
host = args["host"] 


# Credentials
hostIP = '10.46.64.14'
Port = '8444'
user = 'ro'
passwd = 'ro'

## state list > /tmp/netapp
def write_to_file(filename, data):
  with open(tmp_dir + filename + '.tmp', 'w+') as f1:
      f1.write(str(data))
      try:
	      os.remove(tmp_dir + filename)
      except OSError:
	      pass
      os.rename(tmp_dir + filename + '.tmp', tmp_dir + filename)
      f1.close()

## /tmp/netapp > state list
def read_from_file(filename):
  f1 = open(tmp_dir + filename, 'r')
  data1 = f1.read().replace("u'", "'")
  data2 = ast.literal_eval(data1)
  return data2

item_type = args["type"]

if item_type == 'disk':
	
	# Attributes position
	#[1]  - Host, [2] - ID, [3] -	Status, [4] -	InvalidDriveData, [5] -	Off-Line, [6] - Slot

	disk_host_n = 1
	disk_id_n = 2
	disk_status_n = 3
	disk_InvalidDriveData_n = 4
	disk_OffLine_n = 5
	disk_slot_n = 6
	
	if args["item"] == "Discovery":
	
		systemArray = list()
		diskArray = list()
		diskStatus = list()
		
		# Data for Discovery and Items
		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			diskID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/analysed-drive-statistics/".format(hostIP, Port, item[0])
			req = requests.get(diskID, auth=HTTPBasicAuth(user, passwd), verify=False)
			for item in req.json():
				diskArray.append((sysID, item['diskId'], sysName))
		i = 0
		for item in diskArray:
			diskStat = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/drives/{3}".format(hostIP, Port, diskArray[i][0], diskArray[i][1])
			req = requests.get(diskStat, auth=HTTPBasicAuth(user, passwd), verify=False)
			# Host
			if diskArray[i][2] == str(host):
				diskStatus.append((diskArray[i][0], diskArray[i][2], diskArray[i][1], req.json()['status'], req.json()['invalidDriveData'], req.json()['offline'], req.json()['physicalLocation']['slot']))
			i += 1
		
		items = diskStatus
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
			
		write_to_file(filename, items)

		# create json
		zabbix_inventory_json = '{"data":['
		
		for item in items:
			items_count -= 1 # to remove last comma
		
			disk_id = (item[(disk_id_n)])
			disk_slot = (item[(disk_slot_n)])
			disk_name = str (disk_slot) + " (" + str(disk_id) + ")"			
			zabbix_item_name = str(disk_name)
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + disk_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + disk_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json

		
	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[2] == args["id"]:
				disk_health_value = item[3]
				break
		
		print (disk_health_value)


elif item_type == 'pool':
	
	# Attributes position
	#[1]	Host
	#[2]	Name Pool
	#[3]	State
	#[4]	Used Space
	#[5]	Free Space
	#[6]	WWN

	pool_host_n = 1
	pool_id_n = 6
	pool_name_n = 2
	pool_state_n = 3
	pool_use_n = 4
	pool_free_n = 5
	
	if args["item"] == "Discovery":

		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		headers1 = {'Content-type':'application/json'}
		systemArray = list()
		poolArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			poolID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/storage-pools/".format(hostIP, Port, item[0])
			req = requests.get(poolID, auth=HTTPBasicAuth(user, passwd), verify=False)
			for item in req.json():
				if sysName == str(host):
					poolArray.append((sysID, sysName, item['label'], item['state'], item['usedSpace'], item['freeSpace'], item['worldWideName']))

		#print poolArray
		
		items = poolArray
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"		
		write_to_file(filename, items)
		
		# list of data for item status (Free Space) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "FreePercents"		
		write_to_file(filename, items)

		# create json
		zabbix_inventory_json = '{"data":['
		
		for item in items:
			items_count -= 1 # to remove last comma
		
			pool_id = (item[(pool_id_n)])
			pool_name = (item[(pool_name_n)])
			zabbix_item_name = str (pool_name) + " (" + str(pool_id) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + pool_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + pool_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
		

	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[6] == args["id"]:
				pool_health_value = item[3]
				break
				
		print str(pool_health_value)	

	# Item Free Space %
	if args["item"] == "Status" and args["statusmode"] == "FreePercents" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)		
		
		for item in items:
			if item[6] == args["id"]:
				pool_use_size = item[4]
				pool_free_size = item[5]
				pool_total_size = int(pool_use_size) + int(pool_free_size)			
				pool_sizeFree_in_percents = 	100 * int(pool_free_size)/int(pool_total_size)	
				
				break
				
		print int(pool_sizeFree_in_percents)				

		
elif item_type == 'lun':
	
	#[1]	Host
	#[2]	Name
	#[4]	WWN
	#[5]	Status
	#[6]	Size in bytes

	lun_host_n = 1
	lun_id_n = 3
	lun_name_n = 2
	lun_state_n = 4
	lun_size_n = 5

	if args["item"] == "Discovery":
	
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		headers1 = {'Content-type':'application/json'}
		systemArray = list()
		systemArray2 = list()
		lunArray = list()
		lunMArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			lunID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/volumes/".format(hostIP, Port, item[0])
			req = requests.get(lunID, auth=HTTPBasicAuth(user, passwd), verify=False)
			for item in req.json():
				if sysName == str(host):
					lunArray.append((sysID, sysName, item['label'], item['id'], item['status'], item['totalSizeInBytes']))
				

		# LUNs Metrics
		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray2.append((item['id'], item['name'], item['status']))

		# Hardware
		for item in systemArray2:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)

			lunsID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/analysed-volume-statistics/".format(hostIP, Port, item[0])
			req3 = requests.get(lunsID, auth=HTTPBasicAuth(user, passwd), verify=False)

			for item in req3.json():
				readPhysicalIOps = item['readPhysicalIOps']
				writePhysicalIOps = item['writePhysicalIOps']
				if sysName == str(host):
					lunMArray.append((sysName, item['volumeId'], item['volumeName'], item['combinedResponseTime'], int(item['combinedThroughput'] * 1000000), round(readPhysicalIOps + writePhysicalIOps, 1)))
	
		
		items = lunArray
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
		write_to_file(filename, items)

		# list of data for item status (response time) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "resTime"
		write_to_file(filename, lunMArray)		
		
		# list of data for item status (Throughput) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Throughput"
		write_to_file(filename, lunMArray)

		# list of data for item status (I/O) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "IO"
		write_to_file(filename, lunMArray)				
		
		# create json
		zabbix_inventory_json = '{"data":['
		
		for item in items:
			items_count -= 1 # to remove last comma
		
			lun_id = (item[(lun_id_n)])
			lun_name = (item[(lun_name_n)])
			zabbix_item_name = str (lun_name) + " (" + str(lun_id) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + lun_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + lun_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
		
		
	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[3] == args["id"]:
				lun_health_value = item[4]
				break
		
		print str(lun_health_value)

	# Item Response TIme
	if args["item"] == "Status" and args["statusmode"] == "resTime" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (response time)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[1] == args["id"]:
				lun_restime = item[3]
				break
		
		print float(lun_restime)		

	# Item Throughput
	if args["item"] == "Status" and args["statusmode"] == "Throughput" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (responce time)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[1] == args["id"]:
				lun_throughput = item[4]
				break
		
		print int(lun_throughput)	

	# Item I/O
	if args["item"] == "Status" and args["statusmode"] == "IO" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (I/O)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[1] == args["id"]:
				lun_io = item[5]
				break
		
		print float(lun_io)			

		
elif item_type == 'fcp':
	
	#[1]	Host
	#[2]	State
	#[3]	Is Degraded
	#[4]	MAC
	#[5]	Chennal
	#[6]	ID

	fcp_host_n = 1
	fcp_id_n = 6
	fcp_mac_n = 4
	fcp_degrade_n = 3
	fcp_chennal_n = 5
	fcp_updown_n = 2
	
	if args["item"] == "Discovery":
	
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		fcstatArray1 = list()
		fcstatArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))

		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)			
		# FC Utilization
			fcID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/interface-statistics/".format(hostIP, Port, item[0])
			req2 = requests.get(fcID, auth=HTTPBasicAuth(user, passwd), verify=False)
		#  						
			fc = req.json()['fibrePorts']
			for item in fc:
				if sysName == str(host):
					fcArray.append((sysID, sysName, item['linkStatus'], item['isDegraded'], item['addressId'], item['channel'], item['interfaceRef']))

			# fcp utilization
			for item in req2.json():
				if item['channelType'] == 'hostside':
					fcstatArray1.append((item['arrayId'], item['interfaceId'], item['readBytes'], item['writeBytes']))

		time.sleep(10)

		i = 0
		for item in systemArray:
			sysName = item[1]
			fcID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/interface-statistics/".format(hostIP, Port, item[0])
			req2 = requests.get(fcID, auth=HTTPBasicAuth(user, passwd), verify=False)
			for item in req2.json():
				if item['channelType'] == 'hostside':
					readBytes = int(item['readBytes'])
					writeBytes = int(item['writeBytes'])
					fcUtil = 100 * (readBytes - int(fcstatArray1[i][2]) + writeBytes - int(fcstatArray1[i][3])) / 10 / 8 / 134217728
					if sysName == str(host):
						fcstatArray.append((sysName, item['arrayId'], item['interfaceId'], readBytes - int(fcstatArray1[i][2]), writeBytes - int(fcstatArray1[i][3]), fcUtil))
					i += 1
		

		items = fcArray
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
			
		write_to_file(filename, items)
		
		# list of data for item status (fcp utilization) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "FCPutilization"
			
		write_to_file(filename, fcstatArray)		
		

		# create json
		zabbix_inventory_json = '{"data":['
		
		for item in items:
			items_count -= 1 # to remove last comma
		
			fcp_mac = (item[(fcp_mac_n)])
			fcp_chennal = (item[(fcp_chennal_n)])
			fcp_id = (item[(fcp_id_n)])
			
			zabbix_item_name = str (fcp_chennal) + " (" + str(fcp_mac) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + fcp_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + fcp_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json		
			

	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[6] == args["id"]:
				fcp_degrade = item[3]
				break
		
		print str(fcp_degrade)
		
	# FCP Utilization
	if args["item"] == "Status" and args["statusmode"] == "FCPutilization" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (FCP Utilization)
		# [0]	Host
		# [2]	ID
		# [5]	Utilize %
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[2] == args["id"]:
				fcp_utilize = item[5]
				break
		
		print int(fcp_utilize)


elif item_type == 'sp':
	
	#[1]	Host
	#[2]	State
	#[3]	Activ
	#[4]	S/N
	#[5]	Position
	#[6]	ID

	sp_host_n = 1
	sp_id_n = 6
	sp_sn_n = 4
	sp_state_n = 2
	sp_position_n = 5

	
	if args["item"] == "Discovery":
	
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		contrArray = list()
		fanArray = list()
		upsArray = list()
		cpustatArray = list()
	
		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))

		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)
			# CPU Utilization
			contrID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/analysed-controller-statistics/".format(hostIP, Port, item[0])
			req1 = requests.get(contrID, auth=HTTPBasicAuth(user, passwd), verify=False)
			#    
			contr = req.json()['controllers']
			for item in contr:
				if sysName == str(host):
					contrArray.append((sysID, sysName, item['status'], item['active'], item['serialNumber'].rstrip(), item['physicalLocation']['locationPosition'], item['controllerRef']))					

			# CPU Utilization
			for item in req1.json():
				if sysName == str(host):
					cpustatArray.append((item['controllerId'], item['maxCpuUtilization'], item['cpuAvgUtilization']))
			#			
		#print contrArray
		#print cpustatArray
	
		items = contrArray
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
			
		write_to_file(filename, items)
		
		
		# list of data for item status (CPU average Utilization) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "CPUaverage"
			
		write_to_file(filename, cpustatArray)		
		
		# create json
		zabbix_inventory_json = '{"data":['
	
		for item in items:
			items_count -= 1 # to remove last comma
		
			sp_sn = (item[(sp_sn_n)])
			sp_position = (item[(sp_position_n)])
			sp_id = (item[(sp_id_n)])
			
			zabbix_item_name = str (sp_position) + " (" + str(sp_sn) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + sp_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + sp_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json	
	
	
	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[6] == args["id"]:
				sp_state = item[2]
				break
		
		print str(sp_state)
		
	# Item CPU average Utilization
	if args["item"] == "Status" and args["statusmode"] == "CPUaverage" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				sp_cpu_ave = item[2]
				break
		
		print float(sp_cpu_ave)


elif item_type == 'fan':

	#[1]	Host
	#[2]	State
	#[3]	Slot
	#[4]	ID
	
	fan_host_n = 1
	fan_id_n = 4
	fan_slot_n = 3
	fan_state_n = 2
	
	if args["item"] == "Discovery":

		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		contrArray = list()
		fanArray = list()
		upsArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))

		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)
			fan = req.json()['fans']
			for item in fan:
				if sysName == str(host):
					fanArray.append((sysID, sysName, item['status'], item['physicalLocation']['slot'], item['fanRef']))

		#print fanArray

		items = fanArray
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
			
		write_to_file(filename, items)


		# create json
		zabbix_inventory_json = '{"data":['
	
		for item in items:
			items_count -= 1 # to remove last comma
		
			fan_state = (item[(fan_state_n)])
			fan_slot = (item[(fan_slot_n)])
			fan_id = (item[(fan_id_n)])
			
			zabbix_item_name = str (fan_slot) + " (" + str(fan_id) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + fan_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + fan_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json	


	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[4] == args["id"]:
				fan_state = item[2]
				break
		
		print str(fan_state)


elif item_type == 'ps':

	#[1]	Host
	#[2]	State
	#[3]	Location
	#[4]	ID		
	
	ps_host_n = 1
	ps_id_n = 4
	ps_location_n = 3
	ps_state_n = 2

	if args["item"] == "Discovery":

		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		contrArray = list()
		fanArray = list()
		upsArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name']))

		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)
			ups = req.json()['powerSupplies']
			for item in ups:
				if sysName == str(host):
					upsArray.append((sysID, sysName, item['status'], item['physicalLocation']['slot'], item['powerSupplyRef']))        

		#print upsArray
		
		items = upsArray
		items_count = len(items) # to remove last comma
		#print diskStatus
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
			
		write_to_file(filename, items)
		
		
		# create json
		zabbix_inventory_json = '{"data":['
	
		for item in items:
			items_count -= 1 # to remove last comma
		
			ps_state = (item[(ps_state_n)])
			ps_location = (item[(ps_location_n)])
			ps_id = (item[(ps_id_n)])
			
			zabbix_item_name = str (ps_location) + " (" + str(ps_id) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + ps_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + ps_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json	
		
		
	# Item Status
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[4] == args["id"]:
				ps_state = item[2]
				break
		
		print str(ps_state)
		

elif item_type == 'battery':

	#[1]	Host
	#[2]	State
	#[3]	Slot
	#[4]	battery can expire
	#[5]	ID
	
	battery_state_n = 2
	battery_slot_n = 3
	battery_id_n = 5

	if args["item"] == "Discovery":
	
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		batArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name'], item['status']))

		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)
			
			battery = req.json()['batteries']
			for item in battery:
				if sysName == str(host):
					batArray.append((sysID, sysName, item['status'], item['physicalLocation']['slot'], item['batteryCanExpire'], item['batteryRef']))

		items = batArray
		items_count = len(items) # to remove last comma		
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
			
		write_to_file(filename, items)
		
		# list of data for item status (Can Expire) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "CanExpire"
			
		write_to_file(filename, items)		
		
		# create json
		zabbix_inventory_json = '{"data":['
	
		for item in items:
			items_count -= 1 # to remove last comma
		
			battery_slot = (item[(battery_slot_n)])
			battery_id = (item[(battery_id_n)])
			
			zabbix_item_name = str (battery_slot_n) + " (" + str(battery_id_n) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + battery_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + battery_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
		

	# Item Status (Health)
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[5] == args["id"]:
				battery_Health = item[2]
				break
		
		print str(battery_Health)		


	# Item Status (battery can expire)
	if args["item"] == "Status" and args["statusmode"] == "CanExpire" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[5] == args["id"]:
				battery_CanExpire = item[4]
				break
		
		print str(battery_CanExpire)				

		
elif item_type == 'sensor':

	#[1]	Host
	#[2]	State
	#[3]	ID
	#[4]	Slot
	
	sensor_state_n = 2
	sensor_id_n = 3
	sensor_slot_n = 4
	
	if args["item"] == "Discovery":
	
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		sensorArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name'], item['status']))
			
		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)

			sensor = req.json()['thermalSensors']
			for item in sensor:
				if sysName == str(host):
					sensorArray.append((sysID, sysName, item['status'], item['thermalSensorRef'], item['physicalLocation']['slot']))	
	
		#print sensorArray
		
		items = sensorArray
		items_count = len(items) # to remove last comma		
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Health"
		write_to_file(filename, items)


		# create json
		zabbix_inventory_json = '{"data":['
	
		for item in items:
			items_count -= 1 # to remove last comma
		
			sensor_slot = (item[(sensor_slot_n)])
			sensor_id = (item[(sensor_id_n)])
			
			zabbix_item_name = str (sensor_slot) + " (" + str(sensor_id) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + sensor_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + sensor_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json		
		
		
	# Item Status (Health)
	if args["item"] == "Status" and args["statusmode"] == "Health" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (state)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[3] == args["id"]:
				sensor_Health = item[2]
				break
		
		print str(sensor_Health)				
		
		
elif item_type == 'tray':

	#[1]	Host
	#[2]	Slot
	#[3]	ID
	
	tray_slot_n = 2
	tray_id_n = 3	

	if args["item"] == "Discovery":

		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()
		fcArray = list()
		trayArray = list()
		
		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			systemArray.append((item['id'], item['name'], item['status']))
		
		# Hardware
		for item in systemArray:
			sysID = item[0]
			sysName = item[1]
			hardID = "https://{0}:{1}/devmgr/v2/storage-systems/{2}/hardware-inventory/".format(hostIP, Port, item[0])
			req = requests.get(hardID, auth=HTTPBasicAuth(user, passwd), verify=False)

			tray = req.json()['trays']
			for item in tray:
				if sysName == str(host):
					trayArray.append((sysID, sysName, item['physicalLocation']['slot'], item['trayRef']))
				
		items = trayArray
		items_count = len(items) # to remove last comma		
		
		# list of data for item status (state) > /tmp/netapp
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Slot"	
		write_to_file(filename, items)

		# create json
		zabbix_inventory_json = '{"data":['
	
		for item in items:
			items_count -= 1 # to remove last comma
		
			tray_slot = (item[(tray_slot_n)])
			tray_id = (item[(tray_id_n)])
			
			zabbix_item_name = str (tray_slot) + " (" + str(tray_id) + ")"		
			
			if items_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + tray_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_item_name + '","{#ID}": "' + tray_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json		
		

	# Item Status (Slot)
	if args["item"] == "Status" and args["statusmode"] == "Slot" and args["id"] is not None:
		
		# /tmp/netapp > list of data for item status (slot)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[3] == args["id"]:
				tray_slot = item[2]
				break
		
		print int(tray_slot)		
			
		
elif item_type == 'system':
		
	if args["item"] == "Status" and args["statusmode"] == "Health":
	
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		systemArray = list()

		systemID = "https://{0}:{1}/devmgr/v2/storage-systems/".format(hostIP, Port)
		req = requests.get(systemID, auth=HTTPBasicAuth(user, passwd), verify=False)
		for item in req.json():
			sysName = item['name']
			if sysName == str(host):
				print (item['status'])
	
	
	# System Response time 		
	if args["item"] == "Status" and args["statusmode"] == "resTime":
		
		all_lun_restime = 0
		
		# /tmp/netapp > list of data for item metrics
		filename = str(args["host"]) + "_lun_resTime"
		items = read_from_file(filename)
		
		items_count = len(items)
		
		for item in items:
			all_lun_restime += float(item[3])
			
		sys_restime = all_lun_restime / items_count
		print float(sys_restime)


	#System Throughput
	if args["item"] == "Status" and args["statusmode"] == "Throughput":
		
		sys_throughput = 0 
	
		# /tmp/netapp > list of data for item metrics
		filename = str(args["host"]) + "_lun_Throughput"
		items = read_from_file(filename)
		
		for item in items:
			sys_throughput += item[4]
	
		print int (sys_throughput)
		
		
	#System I/O
	if args["item"] == "Status" and args["statusmode"] == "IO":
	
		sys_io = 0
		
		# /tmp/netapp > list of data for item metrics
		filename = str(args["host"]) + "_lun_IO"
		items = read_from_file(filename)
		
		for item in items:
			sys_io += item[5]		
		
		print float (sys_io)