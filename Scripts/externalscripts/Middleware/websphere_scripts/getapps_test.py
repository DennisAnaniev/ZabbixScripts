try:
    name = AdminControl.completeObjectName('type=Cluster,*').split(',')[0].split('=')[1]
except:
    applist = AdminApp.list().split('\n')
    for app in applist:
        app = app.replace(" ","_")
        serverName = AdminConfig.list('Server').split('(')[0]
        appStatus = AdminControl.queryNames('WebSphere:type=Application,name='+app+',*')
        name = serverName
        if appStatus != "":
            print app, name, serverName, "running"
        else:
            print app, name, serverName, "stopped"
else:
    for item in AdminConfig.list('ServerCluster').splitlines():
        name = item.split('(')[0]
        clusterID=AdminConfig.getid('/ServerCluster:'+ name + '/')
        clusterList = AdminConfig.list('ClusterMember', clusterID)
        servers=clusterList.split('\n')
        applist = AdminApp.list().split('\n')
        for app in applist:
            app = app.replace(" ","_")
            for serverID in servers:
                serverName=AdminConfig.showAttribute(serverID, 'memberName')
                appStatus = AdminControl.queryNames('WebSphere:type=Application,name='+app+',process='+serverName+',*')
                if appStatus != "":
                    print app, name, serverName, "running"
                else:
                    print app, name, serverName, "stopped"
