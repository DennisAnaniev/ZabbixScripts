def beanNameAsDict( bean ) :
    result = {};
    for pair in bean.split( ':', 1 )[ 1 ].split( ',' ) :
        n, v = pair.split( '=', 1 );
        result[ n ] = v;
    return result;

for jvm in AdminControl.queryNames( 'type=JVM,*' ).splitlines() :
    jvmDict = beanNameAsDict( jvm );
    heapSize = AdminControl.getAttribute( jvm, 'heapSize' )
    freeMemory = AdminControl.getAttribute( jvm, 'freeMemory' )
    percent =  float(freeMemory)/float(heapSize) * 100
    print '%-20s %-20s %10s %10s %10s' % (jvmDict['process'] ,jvmDict[ 'node' ], heapSize, freeMemory, percent)
