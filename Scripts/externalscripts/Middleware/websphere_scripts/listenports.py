def beanNameAsDict( bean ) :
    result = {};
    for pair in bean.split( ':', 1 )[ 1 ].split( ',' ) :
        n, v = pair.split( '=', 1 );
        result[ n ] = v;
    return result;

for jvm in AdminControl.queryNames('type=ListenerPort,*').splitlines():
    jvmDict = beanNameAsDict( jvm );
    for line in AdminControl.getAttribute(jvm, 'started').splitlines():
        print '%-40s' % (jvmDict['name']),
        print line

