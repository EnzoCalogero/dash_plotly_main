name_tag=$1

cd /home/enzo/main/testing/database/tech_view
#make testing/database/tech_view
docker build -t artifactory.enzp.net:8000/tech_view:$name_tag .
docker push  artifactory.enzp.net:8000/tech_view:$name_tag
# docker tag amd64/testing/database/tech_view:latest artifactory.enzp.net:8000/tech_view:$name_tag
# docker push artifactory.enzp.net:8000/tech_view:$name_tag
rm -f /home/enzo/enzp-main/testing/database/tech_view/database.sql

exit

