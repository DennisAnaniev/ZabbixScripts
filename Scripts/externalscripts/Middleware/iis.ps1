ImportSystemModules

Import-Module WebAdministration



$ZABBIX = "10.45.129.32"            #задаём адрес сервера Zabbix

$PROGRAM = "C:\Program Files\Zabbix_Agent\zabbix_sender.exe" #задаём путь к приложению zabbix_sender
$DATAPATH = "C:\Program Files\Zabbix_Agent\Scripts\"        #задаём путь к рабочей папке
$FILENAME = "export.iis.pools.txt"        #задаём имя файла выгрузки 
$HOSTNAME = hostname
Remove-Item $DATAPATH$FILENAME #удаляем существующий файл выгрузки
New-Item -Path $DATAPATH -Name $FILENAME -ItemType File             #создаём новый пустой файл выгрузки
                
$UNIXTIME = [int][double]::Parse($(Get-Date -date (Get-Date).ToUniversalTime()-uformat %s))
$APPPOOLS = Get-ChildItem -Path IIS:\Apppools -Name

$LINEPOOLS = $HOSTNAME + ' ' + "mscs.pools.discovery"+ ' '+ $UNIXTIME +' {"data":[' 

foreach ($APPPOOL in $APPPOOLS) 
{

		$POOLSTATE = (Get-WebAppPoolState -name $APPPOOL | select -ExpandProperty value)
	$UNIXTIME = [int][double]::Parse($(Get-Date -date (Get-Date).ToUniversalTime()-uformat %s))
	$LINEPOOLS = $LINEPOOLS+'{"{#APPPOOL}":"'+$APPPOOL.Replace(" ","")+ '"},'
            
            $LINEPOOLSTATE = $HOSTNAME + ' ' + 'mscs.poolstate['+$APPPOOL.Replace(" ","")+ ',State]' + ' ' + $UNIXTIME + ' '+ $POOLSTATE

		[array]$DISCOVEREDPOOLS+=$LINEPOOLSTATE
          	    
}

$LINEPOOLS = $LINEPOOLS.TrimEnd(",")
$LINEPOOLS = $LINEPOOLS +']}'


Out-File -FilePath $DATAPATH$FILENAME -inputobject $LINEPOOLS -Encoding ASCII -Append
Out-File -FilePath $DATAPATH$FILENAME -inputobject $DISCOVEREDPOOLS -Encoding ASCII -Append

cd $DATAPATH		

$Argument1 = '-z'	#задаём параметры для запуска приложения zabbix_sender
$Argument2 = $ZABBIX	#задаём параметры для запуска приложения zabbix_sender
$Argument6 = '-T'	#задаём параметры для запуска приложения zabbix_sender
$Argument3 = '-i'	#задаём параметры для запуска приложения zabbix_sender
$Argument4 = $FILENAME	#задаём параметры для запуска приложения zabbix_sender
$Argument5 = '-vv'	#задаём параметры для запуска приложения zabbix_sender

& $PROGRAM $Argument1 $Argument2 $Argument6 $Argument3 $Argument4 $Argument5


