#!/bin/bash

if [ -f /usr/lib/oracle/11.2/client64/network/admin/oracle.env ]; then
        . /usr/lib/oracle/11.2/client64/network/admin/oracle.env
fi

/bin/date
/usr/local/share/zabbix/externalscripts/iibnrt_oracle_target/sql_evnt_cnt.sh
/usr/bin/zabbix_sender -z 10.45.129.43 -T -s iibnrt -i /tmp/sql_evnt_cnt.json -vv
