connect('weblogic','Weblogic19227','t3://10.45.35.250:7001') 

domainRuntime()
cd('/ServerRuntimes/')
cd('AdminServer')
apps=cmo.getApplicationRuntimes()
print "---Start---"
Total = 0
for app in apps:
	#print 'Application Name: ',  app.getName()
    	comps=app.getComponentRuntimes()
        for comp in comps:
            try:
                sessions=comp.getServletSessions()
                #print 'Total no. of sessions - ', len(sessions)
		print app.getName() ,len(sessions)
		Total += int(len(sessions))
            except AttributeError:
		#print app.getName(), ": 0"
                continue
print "Total", Total
exit()
