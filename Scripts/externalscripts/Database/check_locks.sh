#!/usr/bin/bash
/opt/ibm/db2/V10.5/bin/db2 connect to DATAHUB user rbs-ldapzabbix using uWR.vT2e5B6L1=k4  2>/dev/null
/opt/ibm/db2/V10.5/bin/db2 -x call MON.DBSUM > 123.txt
/opt/ibm/db2/V10.5/bin/db2 "values current timestamp"
/opt/ibm/db2/V10.5/bin/db2 connect reset

