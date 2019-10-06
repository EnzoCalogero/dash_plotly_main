#!/bin/bash

name_tag=$2
file=$1
echo $name_tag >/home/enzo/test1.txt
echo $file >/home/enzo/test2.txt

rm -rf /home/enzo/delete_me
mkdir /home/enzo/delete_me
cd /home/enzo/delete_me
curl --user enzo.calogero:xxxxxxxxx  -o tech_view.tgz http://artifactory.enzo.net/tech_views/$file
tar -xzf tech_view.tgz
cp database.sql /home/enzo/main/testing/database/tech_view/database.sql
cd ..
 rm -rf /home/enzo/delete_me
/home/enzo/dashboard-analytics/TechoutDockerBuilder/do_it.sh $name_tag
echo "" >/home/enzo/finito.txt




