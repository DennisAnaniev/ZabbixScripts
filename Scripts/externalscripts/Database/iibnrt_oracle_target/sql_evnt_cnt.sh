#!/usr/bin/env bash
OUTTTEMP=/tmp/$(basename $0).$$.out
OUTJSON=/tmp/sql_evnt_cnt.json
TSTFILE=/tmp/$(basename $0).$$.timestamp
SQLSCRIPT=/usr/local/share/zabbix/externalscripts/iibnrt_oracle_target/sql_evnt_cnt.sql
ATTRNAME='#TARGETSYSTEM_STAGE'
DESCNAME="targetsystem.discovery"
OBJNAME="targetsystem.stage"
#HOST=$(hostname -s)
HOST="iibnrt"

if [ ! -s $SQLSCRIPT ]; then
      echo "Error: SQLPlus script ${SQLSCRIPT} not found" >&2;
            exit 1;
            fi;
            date '+%s' > $TSTFILE;
            sqlplus zabbix/PEWPEWPEWhandsup1@IIBNRT @${SQLSCRIPT} | awk '/^[A-Z]{2,6}_/' | sed -re 's/[^[:alnum:],_]//g' > $OUTTTEMP;
            echo "${HOST} ${DESCNAME} "$(<$TSTFILE)" {"$(awk -F, -v OBJNAME=${ATTRNAME} 'BEGIN {ORS=""; print "\"data\":["; sep=""; } {print sep"{\"{"OBJNAME"}\":\""$1"\"}"; sep=","} END { print "]"}' $OUTTTEMP)"}" > $OUTJSON;
            awk -F, -v TST=$(<$TSTFILE) -v HOST=${HOST} -v OBJNAME=${OBJNAME} '{ print HOST" "OBJNAME"["$1",State] "TST" "$2 }' $OUTTTEMP >> $OUTJSON;
            # cat $OUTJSON;
            rm -f $TSTFILE $OUTTTEMP;
            exit 0;
                        