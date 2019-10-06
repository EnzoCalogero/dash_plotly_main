#!/bin/bash
#List tech_views on artifactory

curl http://artifactory.enzo.net/list/tech_views/ >list
cat list|grep .tgz >list2
sed -i  '/<pre>/d' list2
cat list2 | tr " " "," >list
cat list | tr ">" "," >list2
cat list2 | tr "<" "," >list

cut -d, -f 4 list
