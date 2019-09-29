#!/bin/bash

rm -f /home/cpai/old_org.txt


mysql << EOF
use cpai;
select * from smctl_term_mng   where length(unit_code)=9 into outfile '/home/cpai/old_org.txt';
EOF
echo " import completed !"
echo "-----------------------------------------"

n=`awk 'END{print NR}' /home/cpai/old_new.txt`

for ((i=1;i<=n;i++));
  do  
  old=`awk 'NR=='$i'{print $1}' /home/cpai/old_new.txt`
  new=`awk 'NR=='$i'{print $2}' /home/cpai/old_new.txt`
  #echo "old_org:$old"
  #echo "new_org:$new"
  sed -i 's/'$old'/'$new'/g' /home/cpai/old_org.txt
  echo "$old update $new completed !"
done
echo "--------------------------------------------"
sleep 3

m=`awk 'END{print NR}' /home/cpai/old_org.txt`
for ((i=1;i<=m;i++));
   do
   old_org=`awk 'NR=='$i'{print $2}' /home/cpai/old_org.txt`
   old_org_len=`echo $old_org |wc -L`
   if [ $old_org_len -eq 9 ];
     then
     sed -i '/'$old_org'/d' /home/cpai/old_org.txt
     echo "$old_org deleted"
   fi
done
echo "-------------------------------------------"
sleep 3

x=`awk 'END{print NR}' /home/cpai/old_org.txt`
for ((i=1;i<=x;i++));
  do
  ttyp_no=`awk 'NR=='$i'{print $1}' /home/cpai/old_org.txt`
  orgcode=`awk 'NR=='$i'{print $2}' /home/cpai/old_org.txt`
  gongzuozhan=`awk 'NR=='$i'{print $3}' /home/cpai/old_org.txt`
  sh TermUpdate.sh $ttyp_no $orgcode $gongzuozhan 2
done
echo "ALL COMPLETED !!"
echo "-------------------------------------------"
  






