def beanNameAsDict( bean ) :
    result = {};
    for pair in bean.split( ':', 1 )[ 1 ].split( ',' ) :
        n, v = pair.split( '=', 1 );
        result[ n ] = v;
    return result;


for jvm in AdminControl.queryNames( 'type=JVM,*' ).splitlines():
    jvmDict = beanNameAsDict( jvm );
   # heapSize = AdminControl.getAttribute( jvm, 'heapSize' )
   # freeMemory = AdminControl.getAttribute( jvm, 'freeMemory' )
    for line in AdminControl.getAttribute(jvm, 'stats').splitlines():
        #if 'dmgr' or 'nodeagent' in jvm:
        #    continue
        if len(line.split(",")) > 1 and line.split(',')[1].find('ID=5') > 0:
            print '%-20s %-20s' % (jvmDict['process'] ,jvmDict[ 'node' ]),
            print line.split(',')[-1].split('=')[1]
#    print '%-20s %-20s %10s %10s' % (jvmDict['process'] ,jvmDict[ 'node' ], heapSize, freeMemory )

