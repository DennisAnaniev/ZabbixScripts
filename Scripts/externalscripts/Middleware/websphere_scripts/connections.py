from com.ibm.websphere.management.exception import AdminException

for item in AdminConfig.list('DataSource').splitlines():
        name = item.split('(')[0]
        if name.find('Default') >= 0:
           continue
        try:
            status = AdminControl.testConnection(AdminConfig.getid('/DataSource:'+name+'/'))
        except AdminException, msg:
            status = 'Failed'
            name = name.replace(" ", "_")
            name = name.replace('"', "")
            print name, status
            continue
        else:
            if status.find('WASX7217I')>0:
                continue
            else:
                name = name.replace(" ", "_")
                name = name.replace('"', "")
                print name, 'Successful'
