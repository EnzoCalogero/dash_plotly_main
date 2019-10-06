
cd /usr/share/logstash/bin/


sudo cp server_syslog.conf template.conf

# sudo ./logstash -r -f template.conf &
echo 1
sleep 100

sudo cp  server_tasks.conf template.conf
echo 2
sleep 100
sudo cp  server_task_sy.conf template.conf 
echo 3
sleep 100
sudo cp server_auth.conf template.conf
echo 4
sleep 100
sudo cp  server_celery.conf  template.conf
echo 5
sleep 100
sudo cp server_task_sy.conf template.conf 
echo 6
sleep 100
sudo cp server_static.conf template.conf 
echo 7
sleep 100
sudo cp server_stat_err.conf template.conf
echo 8
sleep 100
sudo cp server_xrdp.conf template.conf 
echo 9
sleep 100
sudo cp server_rails.conf template.conf
echo 10
sleep 100
sudo cp server_ben_INFO.conf template.conf 
echo 11
sleep 100
sudo cp server_ben_WARN.conf template.conf
echo 12
sleep 100
sudo cp server_ben_ERROR.conf template.conf
echo 13
sleep 100
sudo cp server_ben_task.conf template.conf
echo 14
sleep 100
sudo cp server_ben_task_s.conf template.conf
echo 15
