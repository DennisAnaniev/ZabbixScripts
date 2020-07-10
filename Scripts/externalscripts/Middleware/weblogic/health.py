connect('weblogic','Weblogic19227','t3://10.45.35.250:7001') 

serverRuntime()

servers_runtime = domainRuntimeService.getServerRuntimes()
print "---Start---"
for server in servers_runtime:
    components = server.getSubsystemHealthStates()
    for component in components:
        print str(component).split(",")[0].split(":")[1],
        print str(component).split(",")[1].split(":")[1]
