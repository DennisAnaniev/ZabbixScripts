#!/usr/bin/env python
import os, sys, subprocess, re, requests, argparse, ast
import json
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPDigestAuth

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers1 = {'Accept':'application/json',
           'Content-type':'application/json'}

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

tmp_dir = '/tmp/quantum/'

# Credentials
u_credentials  =  {
        "RSB-DSPMOS0TL1": {'User': 'monitoring',
                       'Password': 'P@ssw0rd',
                       'Host': '10.45.101.165',
                       },
        "RSB-DSPMOS1TL1": {'User': 'monitoring',
                       'Password': 'P@ssw0rd',
                       'Host': '10.45.109.165',
                       },
}

## state list > /tmp/quantum
def write_to_file(filename, data):
  with open(tmp_dir + filename + '.tmp', 'w+') as f1:
      f1.write(str(data))
      try:
	      os.remove(tmp_dir + filename)
      except OSError:
	      pass
      os.rename(tmp_dir + filename + '.tmp', tmp_dir + filename)
      f1.close()

## /tmp/quantum > state list
def read_from_file(filename):
  f1 = open(tmp_dir + filename, 'r')
  data1 = f1.read().replace("u'", "'")
  data2 = ast.literal_eval(data1)
  return data2

 # get credentials
credential = u_credentials.get(args["host"] )

if credential is not None:
	hostIP = credential.get("Host")
	user = credential.get("User")
	passwd = credential.get("Password")
else:
	print "No credential to host " + (args["host"])
	sys.exit()
	
### get all data
if args["item"] == "Discovery":

	community = '4Monitor'
	mcbmib = ('enterprises.3764.1.1.30.10.1.7.8.0.0.0.0.0.1.0.59', 'enterprises.3764.1.1.30.10.1.8.8.0.0.0.0.0.1.0.59', 'MCB')
	rcumib = ('enterprises.3764.1.1.30.10.1.7.8.0.0.0.0.0.5.0.49', 'enterprises.3764.1.1.30.10.1.8.8.0.0.0.0.0.5.0.49', 'RCU')
	cmb1mib = ('enterprises.3764.1.1.30.10.1.7.8.0.0.0.0.0.2.48.28', 'enterprises.3764.1.1.30.10.1.8.8.0.0.0.0.0.2.48.28', 'CMB')
	cmb2mib = ('enterprises.3764.1.1.30.10.1.7.8.0.0.0.0.0.2.56.28', 'enterprises.3764.1.1.30.10.1.8.8.0.0.0.0.0.2.56.28', 'CMB')
	cmb3mib = ('enterprises.3764.1.1.30.10.1.7.8.0.0.0.0.0.2.0.28', 'enterprises.3764.1.1.30.10.1.8.8.0.0.0.0.0.2.0.28', 'CMB')
	respcook = list()
	quantumdriveArray = list()
	quantumportArray = list()
	quantumrobotArray = list()
	quantumtowerArray = list()
	compArray = list()
	mibsArray = list((mcbmib, rcumib, cmb1mib, cmb2mib, cmb3mib))

	body = {'name': user, 
			'password': passwd, 
			'ldap': 'false'}
	drivemode = {'0': 'Unknown', 
				 '1': 'Online', 
				 '2': 'Offline'}
	drivestate = {'0': 'Unknown', 
				  '1': 'Varied On', 
				  '2': 'Varied Off', 
				  '3': 'Pending'}
	drivestatus = {'0': 'Unknown', 
				   '1': 'Good', 
				   '2': 'Failed', 
				   '3': 'Degraded', 
				   '4': 'Not Installed', 
				   '5': 'Initializing'}
	driveporttype = {'0': 'Unknown', 
					 '1': 'SCSI', 
					 '2': 'Fibre', 
					 '3': 'SAS'}
	driveportstatus = {'1': 'Down', 
					   '2': 'Active', 
					   '4': 'Passive'}
	librarymode = {'1': 'Online', 
				   '2': 'Offline'}
	robotstate = {'0': 'Unknown', 
				  '1': 'Varied On', 
				  '2': 'Varied Off'}
	robotstatus = {'0': 'Unknown', 
				   '1': 'Good', 
				   '2': 'Not Installed', 
				   '3': 'Initializing', 
				   '4': 'Failed', 
				   '5': 'N/A'}
	towerstatus = {'0': 'Unknown', 
				   '1': 'Not Present', 
				   '2': 'Failed', 
				   '3': 'Not Ready', 
				   '4': 'Initializing', 
				   '5': 'Ready'}
	towerstate = {'1': 'Varied On', 
				  '2': 'Varied Off'}
	towermode = {'0': 'Unknown', 
				 '1': 'Online', 
				 '2': 'Offline'}
	componentstatus = {'1': 'Unknown',
					   '2': 'Unused',
					   '3': 'OK',
					   '4': 'Warning',
					   '5': 'Failed'}

	login = "http://{0}/aml/users/login/".format(hostIP)
	drives = "http://{0}/aml/drives/".format(hostIP)
	ports = "http://{0}/aml/drives/ports".format(hostIP)
	library = "http://{0}/aml/physicalLibrary/mode".format(hostIP)
	robots = "http://{0}/aml/devices/robots".format(hostIP)
	towers = "http://{0}/aml/devices/towers".format(hostIP)

	reqpost = requests.post(login, headers = headers1, json = body, verify=False)

	respcook = reqpost.headers['set-cookie'].split(';')
	respcook1 = respcook[0]

	headers2= {'Accept': 'application/json',
			   'Content-type': 'application/json', 
			   'Cookie': respcook1, 
			   'Connection': 'keep-alive'}

	# Drives
	reqdrive = requests.get(drives, headers = headers2)

	freedrive = 0
	dr = reqdrive.json()['drive']
	for item in dr:
		drmode = drivemode[str(item['mode'])]
		drstate = drivestate[str(item['state'])]
		drstatus = drivestatus[str(item['status'])]
		if 'barcode' in item:
			freedrive += 1
		quantumdriveArray.append((item['logicalSerialNumber'], item['sledSerialNumber'], drmode, drstate, drstatus))

	freedrive = len(quantumdriveArray) - freedrive

	# Ports
	reqport = requests.get(ports, headers = headers2)
	prt = reqport.json()['drivePorts']
	for item in prt:
		sn = item['serialNumber']
		for item in item['ports']['port']:
			portstat = driveportstatus[str(item['status'])]
			porttype = driveporttype[str(item['type'])]
			quantumportArray.append((sn, item['id'], item['address'], portstat, porttype))

	reqlibmode = requests.get(library, headers = headers2)

	# Robots
	reqrobot = requests.get(robots, headers = headers2)
	rob = reqrobot.json()['robot']
	for item in rob:
		robstate = robotstate[str(item['state'])]
		robstatus = robotstatus[str(item['status'])]
		quantumrobotArray.append((item['name'], item['serialNumber'], robstate, robstatus))

	# Towers
	reqtowers = requests.get(towers, headers = headers2)
	tow = reqtowers.json()['tower']
	for item in tow:
		twstate = towerstate[str(item['state'])]
		twstat = towerstatus[str(item['status'])]
		twmode = towermode[str(item['mode'])]
		quantumtowerArray.append((item['serialNumber'], twstat, twmode, twstate))

	# Logout
	reqdel = requests.delete(login, headers = headers2)
	
	# Components
	i = 0
	for item in mibsArray:
		getsn = "snmpget -v 2c -c {0} {1} {2}".format(community, hostIP, mibsArray[i][0])
		p = subprocess.Popen(getsn, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ,shell=True)
		p.wait()
		string = p.stdout.read()
		if 'STRING' in string:
			line = string.replace('"', "").split()
			compsn = line[3]
			getstat = "snmpget -v 2c -c {0} {1} {2}".format(community, hostIP, mibsArray[i][1])
			p1 = subprocess.Popen(getstat, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ,shell=True)
			p1.wait()
			line1 = p1.stdout.read().split()
			compstat = componentstatus[str(line1[3])]
			compArray.append((mibsArray[i][2], compsn, compstat))
		i += 1
	
### end get all data

if item_type == 'drive':
#[0]	Logical Serial Number 
#[1]	S/N 
#[2]	Mode (drivemode)
#[3]	State (drivestate)
#[4]	Status (drivestatus)
	
	# Data for Discovery Items
	if args["item"] == "Discovery":
	
		# list of data for item status (Mode) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Mode"
		write_to_file(filename, quantumdriveArray)
		
		# list of data for item status (State) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "State"
		write_to_file(filename, quantumdriveArray)		
		
		# list of data for item status (Status) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, quantumdriveArray)				
		
		# create json
		drive_count = len(quantumdriveArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for drive in quantumdriveArray:
			drive_count -= 1 # to remove last comma
		
			drive_id = drive[0]
			drive_sn = drive[1]	
			zabbix_drive_name = str(drive_sn) + " (" + str(drive_id) + ")"
			
			if drive_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_drive_name + '","{#ID}": "' + drive_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_drive_name + '","{#ID}": "' + drive_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json

		
	# drive Mode
	if args["item"] == "Status" and args["statusmode"] == "Mode" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Mode)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				drive_mode = item[2]
				break
		
		print (drive_mode)
		
	# drive State
	if args["item"] == "Status" and args["statusmode"] == "State" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (State)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				drive_state = item[3]
				break
		
		print (drive_state)

	# drive Status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				drive_status = item[4]
				break
		
		print (drive_status)
		
	
if item_type == 'port':	
#[0]	Logical Serial Number (drive)
#[1]	ID
#[2]	MAC
#[3]	Status (driveportstatus)
#[4]	Port type (driveporttype)

	# Data for Discovery Items
	if args["item"] == "Discovery":
	
		# list of data for item status (Status) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, quantumportArray)
		
		# list of data for item status (Position) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Position"
		write_to_file(filename, quantumportArray)
		
		# create json
		port_count = len(quantumportArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for port in quantumportArray:
			port_count -= 1 # to remove last comma
		
			port_mac = port[2]
			port_position = port[1]	
			zabbix_port_name = str(port_position) + " (" + str(port_mac) + ")"
			
			if port_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_port_name + '","{#ID}": "' + port_mac + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_port_name + '","{#ID}": "' + port_mac + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json


	# port Status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[2] == args["id"]:
				port_status = item[3]
				break
		
		print (port_status)
		
	# port ID
	if args["item"] == "Status" and args["statusmode"] == "Position" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (ID)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[2] == args["id"]:
				port_position = item[1]
				break
		
		print (port_position)
		
		
if item_type == 'robot':	
#[0]	Name
#[1]	S/N
#[2]	State (robotstate)
#[3]	Status (robotstatus)

	# Data for Discovery Items
	if args["item"] == "Discovery":

		# list of data for item status (State) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "State"
		write_to_file(filename, quantumrobotArray)
		
		# list of data for item status (Status) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, quantumrobotArray)
		
		# create json
		robot_count = len(quantumrobotArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for port in quantumrobotArray:
			robot_count -= 1 # to remove last comma
		
			robot_id = port[1]
			robot_name = port[0]	
			zabbix_robot_name = str(robot_name) + " (" + str(robot_id) + ")"
			
			if robot_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_robot_name + '","{#ID}": "' + robot_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_robot_name + '","{#ID}": "' + robot_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
	

	# robot Status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[1] == args["id"]:
				robot_status = item[3]
				break
		
		print (robot_status)
		

	# robot State
	if args["item"] == "Status" and args["statusmode"] == "State" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (State)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[1] == args["id"]:
				robot_state = item[2]
				break
		
		print (robot_state)
		
		
if item_type == 'tower':	
#[0]	S/N
#[1]	Status (towerstatus)
#[2]	Mode (towermode)
#[3]	State (towerstate)

	# Data for Discovery Items
	if args["item"] == "Discovery":
	
		# list of data for item status (State) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "State"
		write_to_file(filename, quantumtowerArray)
		
		# list of data for item status (Status) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, quantumtowerArray)
		
		# list of data for item status (Mode) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Mode"
		write_to_file(filename, quantumtowerArray)
		
		# create json
		tower_count = len(quantumtowerArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for port in quantumtowerArray:
			tower_count -= 1 # to remove last comma
		
			tower_sn = port[0]
			zabbix_robot_name = str(tower_sn)
			
			if tower_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_robot_name + '","{#ID}": "' + tower_sn + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_robot_name + '","{#ID}": "' + tower_sn + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json
		
		
	# tower Status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				tower_status = item[1]
				break
		
		print (tower_status)
		
	# tower State
	if args["item"] == "Status" and args["statusmode"] == "State" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (State)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				tower_state = item[3]
				break
		
		print (tower_state)
		
	# tower Mode
	if args["item"] == "Status" and args["statusmode"] == "Mode" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Mode)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[0] == args["id"]:
				tower_mode = item[2]
				break
		
		print (tower_mode)
		

# System Library State		
if item_type == 'library' and args["item"] == "Status" and args["statusmode"] == "State":	

	body = {'name': user, 
			'password': passwd, 
			'ldap': 'false'}
	respcook = list()
	librarymode = {'1': 'Online', 
				   '2': 'Offline'}

	login = "http://{0}/aml/users/login/".format(hostIP)
	library = "http://{0}/aml/physicalLibrary/mode".format(hostIP)
	reqpost = requests.post(login, headers = headers1, json = body, verify=False)

	respcook = reqpost.headers['set-cookie'].split(';')
	respcook1 = respcook[0]

	headers2= {'Accept': 'application/json',
			   'Content-type': 'application/json', 
			   'Cookie': respcook1, 
			   'Connection': 'keep-alive'}

	reqlibmode = requests.get(library, headers = headers2)
	print librarymode[str(reqlibmode.text)]
	reqdel = requests.delete(login, headers = headers2)
	
	
# Number of free drives		
if item_type == 'drive' and args["item"] == "Status" and args["statusmode"] == "Free":	

	body = {'name': user, 
			'password': passwd, 
			'ldap': 'false'}
	respcook = list()

	login = "http://{0}/aml/users/login/".format(hostIP)
	drives = "http://{0}/aml/drives/".format(hostIP)
	reqpost = requests.post(login, headers = headers1, json = body, verify=False)

	respcook = reqpost.headers['set-cookie'].split(';')
	respcook1 = respcook[0]

	headers2= {'Accept': 'application/json',
			   'Content-type': 'application/json', 
			   'Cookie': respcook1, 
			   'Connection': 'keep-alive'}


	reqdrive = requests.get(drives, headers = headers2)

	freedrive = 0
	dr = reqdrive.json()['drive']
	for item in dr:
		if 'barcode' in item:
			freedrive += 1

	freedrive = len(dr) - freedrive
	print freedrive

	reqdel = requests.delete(login, headers = headers2)
	
	
if item_type == 'component':
#[0]	Name
#[1]	ID
#[2]	Status

	# Data for Discovery Items
	if args["item"] == "Discovery":

		# list of data for item status (Status) > /tmp/quantum/
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + "Status"
		write_to_file(filename, compArray)				
		
		# create json
		drive_count = len(compArray) # to remove last comma
		zabbix_inventory_json = '{"data":['
		
		for component in compArray:
			drive_count -= 1 # to remove last comma
		
			component_id = component[1]
			component_name = component[0]	
			zabbix_component_name = str(component_name) + " (" + str(component_id) + ")"
			
			if drive_count <> 0: 
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + component_id + '"}, '
			else: # to remove last comma
				zabbix_inventory_json += '{"{#NAME}": "' + zabbix_component_name + '","{#ID}": "' + component_id + '"}'

		zabbix_inventory_json += ']}'
		print zabbix_inventory_json


	# component Status
	if args["item"] == "Status" and args["statusmode"] == "Status" and args["id"] is not None:
		
		# /tmp/quantum > list of data for item status (Status)
		filename = str(args["host"]) + "_" +  str(args["type"])  + "_" + str(args["statusmode"])
		items = read_from_file(filename)
		
		for item in items:
			if item[1] == args["id"]:
				component_status = item[2]
				break
		
		print (component_status)