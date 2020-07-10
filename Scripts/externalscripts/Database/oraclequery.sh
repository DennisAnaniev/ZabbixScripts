#!/bin/bash
## Для корректной работы нужно задать переменные окружения ниже
export ORACLE_HOME=/usr/lib/oracle/11.2/client64
export PATH=$PATH:$ORACLE_HOME/bin
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib64:/usr/lib:$ORACLE_HOME/bin
export TNS_ADMIN=$ORACLE_HOME/network/admin
## Директория для хранения sql – файлов. Созданная предварительно.
## Обязательно убедиться, что пользователю zabbix выданы права доступа на запись и чтение
scriptLocation=/usr/local/share/zabbix/externalscripts/oraclesqlscripts
## Тут задается абсолютный путь и название создаваемого файла с выполняемым запросом
## в качестве первого параметра скрипта предполагается передавать какую-то уникальную ## строку, для идентификации файла с запросом
sqlFile=$scriptLocation/sqlScript_"$1".sql
## Записываем выполняемый запрос в файл
echo "$2" > /usr/local/share/zabbix/externalscripts/sqlFile;
## Собственно, ниже подключаемся к БД и выполняем запрос из ранее сохраненного файла.
## Логин и пароль открытые, не хорошо. 
username="$3"
password="$4"
tnsname="$5"
var=$($ORACLE_HOME/bin/sqlplus -s $username/$password@$tnsname < $sqlFile)
## Получаем результат запроса из полученной выше строки и возвращаем результат.
echo $var | cut -f3 -d " "