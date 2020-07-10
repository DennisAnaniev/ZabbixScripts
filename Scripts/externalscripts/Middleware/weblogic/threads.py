connect('weblogic','Weblogic19227','t3://10.45.35.250:7001') 

serverRuntime()
ECODE='\n'

openSocks = cmo.getOpenSocketsCurrentCount();
print "---Start---"
print('OpenSockets ' + str(openSocks));
cd('serverRuntime:/ThreadPoolRuntime/ThreadPoolRuntime/')
compReq = cmo.getCompletedRequestCount()
status = cmo.getHealthState()
hoggingThreads = cmo.getHoggingThreadCount()
totalThreads = cmo.getExecuteThreadTotalCount()
idleThrds = cmo.getExecuteThreadIdleCount()
pending = cmo.getPendingUserRequestCount()
qLen = cmo.getQueueLength()
thruput = cmo.getThroughput()
print('ServerStatus ' + str(status).split(",")[1].split(":")[1]  +ECODE
+'NumOfCompletedRequests ' + str(compReq) +ECODE
+'ThreadsTotal ' + str(totalThreads)+ECODE
+'ThreadsIdle ' + str(idleThrds)+ECODE
+'ThreadsHogging ' + str(hoggingThreads)+ECODE
+'ThreadsPending ' + str(pending)+ECODE
+'ThreadPool_QueueLength ' + str(qLen)+ECODE
+'ServerThroughput ' +str(thruput)+ECODE)

exit()
