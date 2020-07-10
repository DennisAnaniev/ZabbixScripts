#!/usr/bin/env python

import os
import sys
import subprocess
import re
import requests
import ast
import json
import argparse
import datetime
import time

from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from shutil import copytree

headers1 = {'Accept':'application/json',
           'Content-type':'application/json'}

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Credentials

port = '8443'
u_credentials  =  {
        "RSB-DSPMOS0-1981": {'User': 'zabbix',
						'Password': 'Nzrbmh72Wk',
						'Host': '10.45.101.238',
						'symID': '000297801981',
						},
        "RSB-DSPMOS1-1979": {'User': 'zabbix',
						'Password': 'Nzrbmh72Wk',
						'Host': '10.45.109.238',
						'symID': '000297801979',
						},
}

###########
tmp_dir = '/usr/lib/zabbix/externalscripts/vmax/'

# Arguments
ap = argparse.ArgumentParser()
ap.add_argument("--host", required=True)
ap.add_argument("--type", required=True)
ap.add_argument("--item", required=True)
ap.add_argument("--statusmode", required=False)
ap.add_argument("--id", required=False)
ap.add_argument("--port", required=False)
ap.add_argument("--test", required=False)
args = vars(ap.parse_args())

credential = u_credentials.get(args["host"]) # Getting credentials for specified host

if credential is not None:
	host = credential.get("Host")
	user = credential.get("User")
	password = credential.get("Password")
	symID = credential.get("symID")
else:
	print "No credential to host " + (args["host"])
	sys.exit()

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

if args["type"] == "sg" and args["item"] == "Discovery": # Storage group discovery. Returns JSON

	#
	# List of Storage Groups
	list_of_SGs = "https://{0}:{1}/univmax/restapi/performance/StorageGroup/keys".format(host, port)
	payload = {"symmetrixId": symID }
			
	req = requests.post(list_of_SGs, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)

	sg_list = list()

	items_count = len(req.json()['storageGroupInfo'])
	
	zabbix_inventory_json = '{"data":['
	
	for item in req.json()['storageGroupInfo']:
		items_count -= 1
		sg_name = item['storageGroupId']
		sg_id = item['storageGroupId']
		
		if items_count <> 0:
			zabbix_inventory_json += '{"{#NAME}": "' + sg_name + '","{#ID}": "' + sg_id + '"}, '
		else:
			zabbix_inventory_json += '{"{#NAME}": "' + sg_name + '","{#ID}": "' + sg_id + '"}]}'
			
	print zabbix_inventory_json

if args["type"] == "sg" and args["item"] == "Status" and args['statusmode'] is not None and args['id'] is not None: # Getting Storage Group average response time for past 10 minutes

	end_date = int(round(time.time()) * 1000) # VMAX uses milliseconds
	start_date = (end_date - 600000)
	
		
	payload = {
				"symmetrixId": symID,
				"endDate": end_date,
				"dataFormat": "Average",
				"storageGroupId": args["id"],
				"metrics": [args['statusmode']],
				"startDate": start_date
				}
	
	sg_perf = "https://{0}:{1}/univmax/restapi/performance/StorageGroup/metrics".format(host, port)
	req = requests.post(sg_perf, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	items_count = req.json()['count']
		
	sum_perf = 0.0
	for item in req.json()['resultList']['result']:
		sum_perf += item[args['statusmode']]		
	
	print sum_perf / items_count
	
	
if args["type"] == "array" and args["item"] == "Discovery": # Array discovery. Returns JSON

	#
	# List of Arrays
	list_of_arrays = "https://{0}:{1}/univmax/restapi/performance/Array/keys".format(host, port)
				
	req = requests.get(list_of_arrays, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	items_count = len(req.json()['arrayInfo'])
		
	zabbix_inventory_json = '{"data":['
	
	for item in req.json()['arrayInfo']:
		items_count -= 1
		array_name = "VMAX_" + item['symmetrixId']
		array_id = item['symmetrixId']
		
		if items_count <> 0:
			zabbix_inventory_json += '{"{#NAME}": "' + array_name + '","{#ID}": "' + array_id + '"}, '
		else:
			zabbix_inventory_json += '{"{#NAME}": "' + array_name + '","{#ID}": "' + array_id + '"}]}'
			
	print zabbix_inventory_json

	
if args["type"] == "array" and args["item"] == "Status" and args['statusmode'] is not None and args['id'] is not None: # Getting array health score 

	end_date = int(round(time.time()) * 1000) # VMAX uses milliseconds
	start_date = (end_date - 600000)
	
	payload = {
				"symmetrixId": symID,
				"endDate": end_date,
				"dataFormat": "Maximum",
				"metrics": [args['statusmode']],
				"startDate": start_date
				}
	
	array_perf = "https://{0}:{1}/univmax/restapi/performance/Array/metrics".format(host, port)
	req = requests.post(array_perf, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
		
	array_health = list()
	
	for item in req.json()['resultList']['result']:
		array_health.append(item[args['statusmode']])

	print min(array_health)

if args["type"] == "FE" and args["item"] == "Discovery": # FE Director discovery. Returns JSON

	#
	# List of FE directors
	list_of_FEs = "https://{0}:{1}/univmax/restapi/performance/FEDirector/keys".format(host, port)
	payload = {"symmetrixId": symID }
			
	req = requests.post(list_of_FEs, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	fe_list = list()

	items_count = len(req.json()['feDirectorInfo'])
	
	zabbix_inventory_json = '{"data":['
	
	for item in req.json()['feDirectorInfo']:
		items_count -= 1
		fe_name = "Director_" + item['directorId']
		fe_id = item['directorId']
		
		if items_count <> 0:
			zabbix_inventory_json += '{"{#NAME}": "' + fe_name + '","{#ID}": "' + fe_id + '"}, '
		else:
			zabbix_inventory_json += '{"{#NAME}": "' + fe_name + '","{#ID}": "' + fe_id + '"}]}'
			
	print zabbix_inventory_json

if args["type"] == "FE" and args["item"] == "Status" and args['statusmode'] is not None and args['id'] is not None: # Getting FE metrics

	end_date = int(round(time.time()) * 1000) # VMAX uses milliseconds
	start_date = (end_date - 600000)
	
	payload = {
				"symmetrixId": symID,
				"endDate": end_date,
				"dataFormat": "Average",
				"directorId": args['id'],
				"metrics": [args['statusmode']],
				"startDate": start_date
				}
	
	fe_perf = "https://{0}:{1}/univmax/restapi/performance/FEDirector/metrics".format(host, port)
	req = requests.post(fe_perf, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	items_count = req.json()['count']
		
	sum_perf = 0.0
	
	for item in req.json()['resultList']['result']:
		sum_perf += item[args['statusmode']]		
	
	print sum_perf / items_count
	
if args["type"] == "FE_ports" and args["item"] == "Discovery": # FE ports discovery. Returns JSON

	#
	# List of FE directors
	list_of_FEs = "https://{0}:{1}/univmax/restapi/performance/FEDirector/keys".format(host, port)
	payload = {"symmetrixId": symID }
		
	zabbix_inventory_json = '{"data":['	
	
	req = requests.post(list_of_FEs, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	for item in req.json()['feDirectorInfo']:
		#print item['directorId']
		#
		# List of FE ports per Director
		list_of_SG_ports = "https://{0}:{1}/univmax/restapi/performance/FEPort/keys".format(host, port)
		payload = {"symmetrixId": symID ,
				"directorId": item['directorId']
		}
			
		req2 = requests.post(list_of_SG_ports, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)

		for item2 in req2.json()['fePortInfo']:
			fe_port_name = item['directorId'] + "_" + item2['portId']
			fe_port_id = item2['portId']
		
			zabbix_inventory_json += '{"{#NAME}": "' + fe_port_name + '","{#ID}": "' + fe_port_id + '"}, '
			
	zabbix_inventory_json = zabbix_inventory_json[:-4]
	zabbix_inventory_json += '"}]}'		
	
	print zabbix_inventory_json

if args["type"] == "FE_ports" and args["item"] == "Status" and args['statusmode'] is not None and args['id'] is not None: # Getting FE port metrics

	end_date = int(round(time.time()) * 1000) # VMAX uses milliseconds
	start_date = (end_date - 600000)
	
	director_name = args['id'].split('_')[0] # Strip directorID from --port 
	port_id = args['id'].split('_')[1]
	
	payload = {
				"symmetrixId": symID,
				"endDate": end_date,
				"dataFormat": "Average",
				"directorId": director_name,
				"portId": port_id,
				"metrics": [args['statusmode']],
				"startDate": start_date
				}
	
	fe_port_perf = "https://{0}:{1}/univmax/restapi/performance/FEPort/metrics".format(host, port)
	req = requests.post(fe_port_perf, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	items_count = req.json()['count']
		
	sum_perf = 0.0
	
	for item in req.json()['resultList']['result']:
		sum_perf += item[args['statusmode']]		
	
	print sum_perf / items_count	

if args["type"] == "RDF_ports" and args["item"] == "Discovery": # RDF ports discovery. Returns JSON

	#
	# List of RDF directors
	list_of_RDFs = "https://{0}:{1}/univmax/restapi/performance/RDFDirector/keys".format(host, port)
	payload = {"symmetrixId": symID }
		
	zabbix_inventory_json = '{"data":['	
	
	req = requests.post(list_of_RDFs, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	for item in req.json()['rdfDirectorInfo']:
		
		#
		# List of RDF ports per Director
		list_of_RDF_ports = "https://{0}:{1}/univmax/restapi/performance/RDFPort/keys".format(host, port)
		payload = {"symmetrixId": symID ,
				"directorId": item['directorId']
		}
			
		req2 = requests.post(list_of_RDF_ports, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)

		for item2 in req2.json()['rdfPortInfo']:
			rdf_port_name = item['directorId'] + "_" + item2['portId']
			rdf_port_id = item2['portId']
		
			zabbix_inventory_json += '{"{#NAME}": "' + rdf_port_name + '","{#ID}": "' + rdf_port_id + '"}, '
			
	zabbix_inventory_json = zabbix_inventory_json[:-4]
	zabbix_inventory_json += '"}]}'		
	
	print zabbix_inventory_json

if args["type"] == "RDF_ports" and args["item"] == "Status" and args['statusmode'] is not None and args['id'] is not None: # Getting RDF port metrics

	end_date = int(round(time.time()) * 1000) # VMAX uses milliseconds
	start_date = (end_date - 600000)
	
	director_name = args['id'].split('_')[0] # Strip directorID from --port 
	port_id = args['id'].split('_')[1]
	
	payload = {
				"symmetrixId": symID,
				"endDate": end_date,
				"dataFormat": "Average",
				"directorId": director_name,
				"portId": port_id,
				"metrics": [args['statusmode']],
				"startDate": start_date
				}
	
	rdf_port_perf = "https://{0}:{1}/univmax/restapi/performance/RDFPort/metrics".format(host, port)
	req = requests.post(rdf_port_perf, json = payload, auth = HTTPBasicAuth(user, password), verify = False, headers = headers1)
	
	items_count = req.json()['count']
		
	sum_perf = 0.0
	
	for item in req.json()['resultList']['result']:
		sum_perf += item[args['statusmode']]		
	
	print sum_perf / items_count	