connect('weblogic','Weblogic19227','t3://10.45.35.250:7001') 

serverNames = cmo.getServers()
domainRuntime()
print "---Start---"
for name in serverNames:
    cd("/ServerLifeCycleRuntimes/" + name.getName())
    serverState = cmo.getState()
    print name.getName(), serverState
    
exit()
