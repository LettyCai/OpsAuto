#������������(2λʡ����+4λ0+3λ���)��ʡ��Ψһ
export SERVER_ID=610000001

#������ˮ�����
export START_SEQNO="000001"

#������ˮ��ֹ��
export END_SEQNO="050000"

#������ȫ������WSNADDR
export WSNADDR=//10.229.70.71:4901,//22.230.40.11:4901
export CPAIWSN=//10.229.70.71:4901,//22.230.40.11:4901

#����ȫ������WSNADDR
export JJWSN=//10.229.15.72:40000     

#���������ȫ������WSNADDR
export CGWSN=//10.229.21.250:40008 

#��̨���������
export DEFAULTSVC=COM_SVC

#ģ���������Ŀ¼
export TUXCONFIG=$HOME/SimServer/tuxedo/server/tuxconfig

#MYSQL����������
export DBSOCK=$HOME/etc/mysql_cpai.sock
export DBPORT=3333
export DBADDRESS=127.0.0.1
export DBNAME=cpai
export DBPASS=cpai
export DBUSER=cpai

runspy >/dev/null 2>&1;
export CGWSN=//22.230.9.6:52024,//22.246.2.167:52024  #ptds������ܷ�����
export MSTWSN=//22.230.44.76:8670,//22.230.44.12:8670
