def beanNameAsDict( bean ) :
    result = {};
    for pair in bean.split( ':', 1 )[ 1 ].split( ',' ) :
        n, v = pair.split( '=', 1 );
        result[ n ] = v;
    return result;

total = 0
for jvm in AdminControl.queryNames( '*,type=SessionManager' ).splitlines():
    jvmDict = beanNameAsDict( jvm );
    jvmDict['name'] = jvmDict['name'].replace(" ", "_") #bcs retards r retards.
    for line in AdminControl.getAttribute(jvm, 'stats').splitlines():
        if len(line.split(",")) > 1:
            #if line.split(',')[1].find('ID=3') > 0:
            result = {}
            try:
                for pair in line.split(','):
#                print pair.split('=', 1)
                    k, v = pair.split('=', 1)
                    result[k.strip()] = v
            except ValueError:
                continue
            if len(result.keys()) > 2:
                if result['ID'] == '7':
                    print '%-40s %-20s %-20s' % (jvmDict['name'] ,jvmDict['process'] ,jvmDict[ 'node' ]),
                    total += int(result['current'])
                    print result['current'] 

print 'TOTAL ALL ALL ' + str(total)
