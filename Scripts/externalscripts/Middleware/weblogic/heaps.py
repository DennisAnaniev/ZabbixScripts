#!/usr/bin/env python

connect('weblogic','Weblogic19227','t3://10.45.35.250:7001') 

domainRuntime()
cd('ServerRuntimes')
dirs = ls(returnMap=true)
cd(dirs.split()[1])
cd('JVMRuntime')
cd(dirs.split()[1])
print "---Start---"
print "AllProcLoad", cmo.getAllProcessorsAverageLoad()
print "FreeHeap", cmo.getFreeHeap()
print "FreePhysMemory", cmo.getFreePhysicalMemory()
print "FreeHeapPrcnt", cmo.getHeapFreePercent()
print "CurrHeapSize", cmo.getHeapSizeCurrent()
print "TotalPhysMemory", cmo.getTotalPhysicalMemory()
print "Uptime", cmo.getUptime()
print "UsedHeapSize", cmo.getUsedHeap()
print "UsedPhysMemory", cmo.getUsedPhysicalMemory()
cd('/ServerRuntimes')


exit()
