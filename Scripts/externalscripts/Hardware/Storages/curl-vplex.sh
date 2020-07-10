#!/bin/bash
#/etc/zabbix/externalscripts/host-dns.sh

case ${1} in
"curl_consistency-group_SM22-3")curl -k  -H 'Username:zabbix' -H 'Password:4M0nit0r' https://10.45.101.150/vplex/clusters/cluster-1/consistency-groups/SM22-3?detach-rule 2>/dev/null | awk -F': ' '/value/ {gsub("\"",""); print $2}';;
"curl_consistency-group_SM22-2")curl -k  -H 'Username:zabbix' -H 'Password:4M0nit0r' https://10.45.101.150/vplex/clusters/cluster-1/consistency-groups/SM22-2?detach-rule 2>/dev/null | awk -F': ' '/value/ {gsub("\"",""); print $2}' ;;
"curl_consistency-group_SM22")curl -k  -H 'Username:zabbix' -H 'Password:4M0nit0r' https://10.45.101.150/vplex/clusters/cluster-1/consistency-groups/SM22?detach-rule 2>/dev/null | awk -F': ' '/value/ {gsub("\"",""); print $2}' ;;
"curl_consistency-group_BR7")curl -k  -H 'Username:zabbix' -H 'Password:4M0nit0r' https://10.45.101.150/vplex/clusters/cluster-1/consistency-groups/BR7?detach-rule 2>/dev/null | awk -F': ' '/value/ {gsub("\"",""); print $2}' ;;
*) echo "ERROR" ;;
esac
