#网点服务器编号(2位省代码+4位0+3位序号)，省内唯一
export SERVER_ID=610000001

#网点流水号起号
export START_SEQNO="000001"

#网点流水号止号
export END_SEQNO="050000"

#代理保险全国中心WSNADDR
export WSNADDR=//10.229.70.71:4901,//22.230.40.11:4901
export CPAIWSN=//10.229.70.71:4901,//22.230.40.11:4901

#基金全国中心WSNADDR
export JJWSN=//10.229.15.72:40000     

#第三方存管全国中心WSNADDR
export CGWSN=//10.229.21.250:40008 

#后台接入服务名
export DEFAULTSVC=COM_SVC

#模拟服务运行目录
export TUXCONFIG=$HOME/SimServer/tuxedo/server/tuxconfig

#MYSQL参数配置区
export DBSOCK=$HOME/etc/mysql_cpai.sock
export DBPORT=3333
export DBADDRESS=127.0.0.1
export DBNAME=cpai
export DBPASS=cpai
export DBUSER=cpai

runspy >/dev/null 2>&1;
export CGWSN=//22.230.9.6:52024,//22.246.2.167:52024  #ptds三方存管服务器
export MSTWSN=//22.230.44.76:8670,//22.230.44.12:8670
