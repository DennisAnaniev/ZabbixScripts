for i in AdminConfig.list('Server').split():
    try: 
        name = i.split('(')[0]
        node = i.split('/')[3]
        status = AdminControl.getAttribute(AdminControl.completeObjectName('name=' + name + ',node=' + node + ',type=Server,*'),'state')
        print name, node, status
    except:
        pass
