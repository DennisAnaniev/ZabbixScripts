#!/usr/bin/expect -f 
set timeout 300 
spawn ssh Zabbix@10.44.48.7
expect "password:" 
send "O5Wvf|d%tE\r" 
expect "admin:" 
send "show network status nodns\r;" 
expect "admin:"
send "exit\r;"

interact
