./db2 connect to dwh user RBS-LDAPZABBIX using uWR.vT2e5B6L1=k4 > /dev/null 2>&1
./db2 call MONREPORT.DBSUMMARY | grep LOCK_WAIT_TIME | awk '{ print $2;exit }'
