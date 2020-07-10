#!/usr/bin/ksh
DB2CLI=/opt/ibm/db2/V10.5/bin/db2;
if $DB2CLI 'connect to DATAHUB user rbs-ldapzabbix using uWR.vT2e5B6L1=k4' >/dev/null 2>&1; then
$DB2CLI -x call MONREPORT.DBSUMMARY | awk '/LOCK_WAIT_TIME/ {printf("%d\n", $2); exit;}'
$DB2CLI connect reset >/dev/null 2>&1;
else
       echo "Could not connect to DATAHUB" >&2;
              exit 1;
              fi;
              
