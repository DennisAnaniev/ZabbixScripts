def beanNameAsDict( bean ) :
    result = {};
    for pair in bean.split( ':', 1 )[ 1 ].split( ',' ) :
        n, v = pair.split( '=', 1 );
        result[ n ] = v;
    return result;

for jvm in AdminControl.queryNames( 'name=%s,type=ThreadPool,*'% ('WebContainer') ).splitlines():
    jvmDict = beanNameAsDict( jvm );
    activetime = 0
    bean = AdminControl.getAttribute(jvm, 'stats')
    if bean.find("ActiveTime") >0:
        activetime = 1
    for line in AdminControl.getAttribute(jvm, 'stats').splitlines():
        if len(line.split(",")) > 1:
            #if line.split(',')[1].find('ID=3') > 0:
            result = {}
            for pair in line.split(','):
                k, v = pair.split('=')
                result[k.strip()] = v
            if len(result.keys()) > 2:
                if result['ID'] == '3':
                    print '%-20s %-20s' % (jvmDict['process'] ,jvmDict[ 'node' ]),
                    print result['current'], 
                if result['ID'] == '4':
                    if activetime:
                        print result['current'], result['highWaterMark'],
                    else:
                        print result['current'], result['highWaterMark'], 0
                if result['ID'] == '9':
                    print result['count']
