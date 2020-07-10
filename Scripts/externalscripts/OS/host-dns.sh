#!/bin/bash
#/etc/zabbix/externalscripts/host-dns.sh

HOST=$1
DNS_SERVER=$2

if [ `host $HOST $DNS_SERVER | grep "has address" | wc -l` -eq 0 ]; then
    #FAIL
echo "FAIL"
else
#DONE
echo "OK"
fi
